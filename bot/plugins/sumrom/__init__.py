"""SUMROM — plugin Hermes untuk merangkum grup WhatsApp.

Cara kerja:
- Hook `pre_gateway_dispatch` melihat setiap pesan WhatsApp sebelum sampai
  ke agen. Pesan biasa di grup yang aktif disimpan ke SQLite lalu di-skip,
  jadi bot tidak ikut mengobrol.
- Perintah (/ringkas, /tugas, ...) ditangani di sini juga. Ringkasan dibuat
  lewat ctx.llm (model yang sedang dipakai Hermes) dan dikirim langsung ke
  grup. Pesan baru ditandai "sudah diringkas" setelah ringkasan terkirim.
- Penjadwal berjalan di event loop gateway untuk ringkasan otomatis dan
  penghapusan data yang lebih tua dari 7 hari.

Pengaturan lewat environment:
  SUMROM_ADMINS        nomor/ID admin, dipisah koma (wajib untuk /aktifkan)
  SUMROM_DB            lokasi database (default: $HERMES_HOME/sumrom/sumrom.db)
  SUMROM_LANDING_URL   link landing page, dipakai di /bantuan dan pesan aktivasi
  SUMROM_TEXT_STYLE    whatsapp (default) atau markdown
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
from datetime import timedelta
from pathlib import Path

from . import formatting as fmt
from .store import RETENTION_DAYS, Store
from .summarize import summarize
from .timeparse import now_wib, parse_hhmm, parse_range

log = logging.getLogger("sumrom")

ADMIN_COMMANDS = {"aktifkan", "nonaktifkan", "jadwal", "gaya"}
MEMBER_COMMANDS = {"ringkas", "tugas", "cari", "bantuan", "idsaya"}
SEARCH_LIMIT = 5
LONG_RUN_NOTICE = 150  # kirim "tunggu sebentar" kalau pesan sebanyak ini


def _db_path() -> Path:
    explicit = os.environ.get("SUMROM_DB")
    if explicit:
        return Path(explicit)
    home = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
    return home / "sumrom" / "sumrom.db"


def _digits(value: str | None) -> str:
    """Ambil bagian ID sebelum '@' dan buang selain angka (62895...@s.whatsapp.net -> 62895...)."""
    if not value:
        return ""
    return re.sub(r"\D", "", str(value).split("@", 1)[0].split(":", 1)[0])


def _admins() -> set[str]:
    raw = os.environ.get("SUMROM_ADMINS", "")
    return {d for d in (_digits(x) for x in raw.split(",")) if d}


def _platform_name(source) -> str:
    platform = getattr(source, "platform", "")
    return str(getattr(platform, "value", platform)).lower()


def _is_text(event) -> bool:
    kind = getattr(event, "message_type", None)
    name = str(getattr(kind, "name", kind) or "TEXT").upper()
    return name in ("TEXT", "COMMAND", "NONE")


class Sumrom:
    def __init__(self, ctx):
        self.ctx = ctx
        self.store = Store(_db_path())
        self.gateway = None
        self.scheduler: asyncio.Task | None = None
        self.locks: dict[str, asyncio.Lock] = {}
        log.info("SUMROM siap, database: %s", _db_path())
        if not _admins():
            log.warning("SUMROM_ADMINS kosong: tidak ada yang bisa /aktifkan. Pakai /idsaya untuk melihat ID.")

    # ---------- kirim ----------

    def _adapter(self, source):
        adapters = getattr(self.gateway, "adapters", {}) or {}
        platform = getattr(source, "platform", None)
        direct = adapters.get(platform)
        if direct is not None:
            return direct
        wanted = _platform_name(source)
        for key, adapter in adapters.items():
            if str(getattr(key, "value", key)).lower() == wanted:
                return adapter
        return None

    async def send(self, source, text: str) -> bool:
        adapter = self._adapter(source)
        if adapter is None:
            log.error("SUMROM: adapter WhatsApp tidak ditemukan")
            return False
        ok = True
        for chunk in fmt.split_message(text):
            try:
                result = await adapter.send(source.chat_id, chunk)
                if result is not None and getattr(result, "success", True) is False:
                    ok = False
                    log.error("SUMROM: kirim gagal: %s", getattr(result, "error", result))
            except Exception:  # noqa: BLE001 — jangan sampai gateway ikut jatuh
                ok = False
                log.exception("SUMROM: kirim gagal")
        return ok

    # ---------- hook ----------

    async def on_dispatch(self, event, gateway=None, session_store=None, **kwargs):
        if getattr(event, "internal", False):
            return None
        source = getattr(event, "source", None)
        if source is None or _platform_name(source) != "whatsapp":
            return None
        if gateway is not None:
            self.gateway = gateway
            self._ensure_scheduler()
        if getattr(source, "is_bot", False):
            return {"action": "skip", "reason": "sumrom-bot-sendiri"}

        text = (getattr(event, "text", None) or "").strip()
        command, arg = self._parse_command(text)

        if source.chat_type != "group":
            # Bot tidak melayani chat pribadi, kecuali dua perintah info.
            if command == "bantuan":
                await self.send(source, fmt.help_message())
            elif command == "idsaya":
                await self.send(source, fmt.whoami(source.user_id or "-"))
            return {"action": "skip", "reason": "sumrom-dm"}

        now = now_wib()
        group = self.store.upsert_group(source.chat_id, source.chat_name, now)

        if command:
            try:
                await self._handle_command(command, arg, source, group)
            except Exception:  # noqa: BLE001
                log.exception("SUMROM: perintah /%s gagal", command)
            return {"action": "skip", "reason": f"sumrom-{command}"}

        if group.aktif:
            is_text = _is_text(event)
            self.store.add_message(
                group_id=source.chat_id,
                wa_message_id=getattr(event, "message_id", None) or getattr(source, "message_id", None),
                sender=source.user_name or _digits(source.user_id) or "Tanpa nama",
                sender_id=source.user_id,
                text=text if is_text and text else (text or "[media]"),
                kind="teks" if is_text and text else "media",
                sent_at=now,
            )
        return {"action": "skip", "reason": "sumrom-dicatat" if group.aktif else "sumrom-nonaktif"}

    @staticmethod
    def _parse_command(text: str) -> tuple[str | None, str]:
        if not text.startswith("/"):
            return None, ""
        head, _, rest = text[1:].partition(" ")
        name = head.split("@", 1)[0].lower()
        if name in ADMIN_COMMANDS or name in MEMBER_COMMANDS:
            return name, rest.strip()
        return None, ""  # "/" lain diperlakukan sebagai pesan biasa

    def _is_admin(self, source) -> bool:
        admins = _admins()
        ids = {_digits(getattr(source, "user_id", None)), _digits(getattr(source, "user_id_alt", None))}
        return bool(admins & (ids - {""}))

    # ---------- perintah ----------

    async def _handle_command(self, command: str, arg: str, source, group) -> None:
        if command == "idsaya":
            await self.send(source, fmt.whoami(source.user_id or "-"))
            return
        if command == "bantuan":
            await self.send(source, fmt.help_message())
            return

        if command in ADMIN_COMMANDS and not self._is_admin(source):
            await self.send(source, fmt.admin_only())
            return

        if command == "aktifkan":
            if group.aktif:
                await self.send(source, fmt.already_active())
            else:
                self.store.set_active(group.wa_group_id, True)
                await self.send(source, fmt.activated_message())
            return

        if not group.aktif:
            if command == "nonaktifkan":
                await self.send(source, fmt.already_inactive())
            else:
                await self.send(source, fmt.inactive_hint())
            return

        if command == "nonaktifkan":
            self.store.set_active(group.wa_group_id, False)
            await self.send(source, fmt.deactivated_message())
        elif command == "jadwal":
            if arg.lower() in ("mati", "off", "stop"):
                self.store.set_schedule(group.wa_group_id, None)
                await self.send(source, fmt.schedule_off())
            elif (hhmm := parse_hhmm(arg)) is not None:
                self.store.set_schedule(group.wa_group_id, hhmm)
                await self.send(source, fmt.schedule_set(hhmm))
            else:
                await self.send(source, fmt.schedule_usage())
        elif command == "gaya":
            style = arg.lower()
            if style in ("singkat", "detail"):
                self.store.set_style(group.wa_group_id, style)
                await self.send(source, fmt.style_set(style))
            else:
                await self.send(source, fmt.style_usage())
        elif command == "tugas":
            await self.send(source, fmt.tasks_message(self.store.open_tasks(group.wa_group_id)))
        elif command == "cari":
            if not arg:
                await self.send(source, fmt.search_usage())
            else:
                hits = self.store.search(group.wa_group_id, arg)
                await self.send(source, fmt.search_message(arg, hits, now_wib(), SEARCH_LIMIT))
        elif command == "ringkas":
            await self.run_summary(source, group.wa_group_id, arg)

    # ---------- ringkasan ----------

    async def run_summary(self, source, group_id: str, arg: str = "", scheduled: bool = False) -> None:
        lock = self.locks.setdefault(group_id, asyncio.Lock())
        if lock.locked():
            if not scheduled:
                await self.send(source, "Ringkasan sedang dibuat. Tunggu hasilnya dulu.")
            return
        async with lock:
            now = now_wib()
            self.store.purge_older_than(now - timedelta(days=RETENTION_DAYS))
            group = self.store.get_group(group_id)
            if group is None:
                return

            if arg:
                parsed = parse_range(arg, now)
                if parsed is None:
                    await self.send(source, fmt.range_usage())
                    return
                start, label = parsed
                messages = self.store.since(group_id, start)
                if not messages:
                    await self.send(source, fmt.nothing_in_range(label))
                    return
            else:
                messages = self.store.unsummarized(group_id)
                if not messages:
                    if not scheduled:
                        await self.send(source, fmt.nothing_new())
                    return

            if len(messages) >= LONG_RUN_NOTICE and not scheduled:
                await self.send(source, fmt.summarizing_notice(len(messages)))

            try:
                summary = await summarize(self.ctx.llm.acomplete_structured, messages, group.gaya)
            except Exception:  # noqa: BLE001
                log.exception("SUMROM: ringkasan gagal untuk %s", group_id)
                await self.send(source, fmt.summary_failed())
                return

            start_at, end_at = messages[0].sent_at, messages[-1].sent_at
            text = fmt.summary_message(group.nama, summary, len(messages), fmt.fmt_range(start_at, end_at, now))
            if await self.send(source, text):
                self.store.save_summary(group_id, start_at, end_at, text, len(messages), summary.tasks, now)
                self.store.mark_summarized([m.id for m in messages])

    # ---------- penjadwal ----------

    def _ensure_scheduler(self) -> None:
        if self.scheduler is None or self.scheduler.done():
            self.scheduler = asyncio.get_running_loop().create_task(self._schedule_loop())

    async def _schedule_loop(self) -> None:
        last_purge = None
        while True:
            try:
                now = now_wib()
                if last_purge is None or now - last_purge >= timedelta(hours=1):
                    removed = self.store.purge_older_than(now - timedelta(days=RETENTION_DAYS))
                    if removed:
                        log.info("SUMROM: %d pesan lama dihapus", removed)
                    last_purge = now
                today, hhmm = now.strftime("%Y-%m-%d"), now.strftime("%H:%M")
                for group in self.store.scheduled_groups():
                    if group.jadwal == hhmm and group.jadwal_terakhir != today:
                        self.store.mark_schedule_ran(group.wa_group_id, today)
                        source = _ScheduledSource(group.wa_group_id, group.nama)
                        await self.run_summary(source, group.wa_group_id, scheduled=True)
            except Exception:  # noqa: BLE001
                log.exception("SUMROM: penjadwal error")
            await asyncio.sleep(20)


class _ScheduledSource:
    """Sumber tiruan untuk pengiriman terjadwal (tidak ada pesan pemicu)."""

    platform = "whatsapp"
    chat_type = "group"

    def __init__(self, chat_id: str, chat_name: str):
        self.chat_id = chat_id
        self.chat_name = chat_name


def register(ctx):
    plugin = Sumrom(ctx)
    ctx.register_hook("pre_gateway_dispatch", plugin.on_dispatch)
