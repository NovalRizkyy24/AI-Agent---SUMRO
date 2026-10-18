"""Uji plugin SUMROM tanpa Hermes: gateway, adapter, dan model dipalsukan.

Jalankan dari folder bot/:  python -m unittest discover -s tests -v
"""

from __future__ import annotations

import asyncio
import os
import sys
import tempfile
import unittest
from datetime import timedelta
from enum import Enum
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "plugins"))

from sumrom import Sumrom  # noqa: E402
from sumrom import formatting as fmt  # noqa: E402
from sumrom.summarize import build_chunks, parse_summary  # noqa: E402
from sumrom.store import StoredMessage  # noqa: E402
from sumrom.timeparse import now_wib, parse_hhmm, parse_range  # noqa: E402

GROUP = "120363000000000000@g.us"
ADMIN = "6281200000000@s.whatsapp.net"
MEMBER = "6281299999999@s.whatsapp.net"


class Platform(str, Enum):
    WHATSAPP = "whatsapp"


class FakeAdapter:
    def __init__(self):
        self.sent: list[tuple[str, str]] = []

    async def send(self, chat_id, content, **kwargs):
        self.sent.append((chat_id, content))
        return SimpleNamespace(success=True)


class FakeLLM:
    def __init__(self, parsed=None, fail=False):
        self.parsed = parsed
        self.fail = fail
        self.calls = []

    async def acomplete_structured(self, **kwargs):
        self.calls.append(kwargs)
        if self.fail:
            raise RuntimeError("provider down")
        return SimpleNamespace(parsed=self.parsed, text="")


SAMPLE = {
    "inti": ["Rapat dipindah karena ruang dipakai."],
    "keputusan": ["Rapat pindah ke Kamis, 19.00."],
    "tugas": [
        {"siapa": "Rina", "apa": "Slide bab 2", "kapan": "Kamis"},
        {"siapa": "Bayu", "apa": "Rekap absen", "kapan": None},
    ],
    "belum_terjawab": ["Siapa yang pegang kunci ruangan?"],
}


def event(text, user=MEMBER, name="Rina", chat_type="group", message_id=None):
    source = SimpleNamespace(
        platform=Platform.WHATSAPP, chat_id=GROUP if chat_type == "group" else user,
        chat_name="Kelas 3B", chat_type=chat_type, user_id=user, user_id_alt=None,
        user_name=name, is_bot=False, message_id=message_id,
    )
    return SimpleNamespace(text=text, source=source, message_id=message_id, internal=False,
                           message_type=SimpleNamespace(name="TEXT"))


class PluginTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["SUMROM_DB"] = str(Path(self.tmp.name) / "t.db")
        os.environ["SUMROM_ADMINS"] = "6281200000000"
        os.environ["SUMROM_LANDING_URL"] = "https://sumrom.vercel.app"
        os.environ.pop("SUMROM_TEXT_STYLE", None)
        self.llm = FakeLLM(SAMPLE)
        self.plugin = Sumrom(SimpleNamespace(llm=self.llm))
        self.adapter = FakeAdapter()
        self.gateway = SimpleNamespace(adapters={Platform.WHATSAPP: self.adapter})

    async def asyncTearDown(self):
        if self.plugin.scheduler:
            self.plugin.scheduler.cancel()
        self.plugin.store._conn.close()
        self.tmp.cleanup()

    async def say(self, text, **kw):
        return await self.plugin.on_dispatch(event(text, **kw), gateway=self.gateway)

    def last(self):
        return self.adapter.sent[-1][1]

    async def test_inactive_group_is_not_recorded(self):
        result = await self.say("halo semua")
        self.assertEqual(result["action"], "skip")
        self.assertEqual(self.plugin.store.unsummarized(GROUP), [])
        await self.say("/ringkas")
        self.assertIn("belum aktif", self.last())

    async def test_only_admin_can_activate(self):
        await self.say("/aktifkan")
        self.assertEqual(self.last(), fmt.admin_only())
        await self.say("/aktifkan", user=ADMIN, name="Admin")
        self.assertIn("SUMROM aktif di grup ini", self.last())
        self.assertIn("/nonaktifkan", self.last())
        self.assertNotIn("7 hari", self.last())

    async def test_full_summary_flow(self):
        await self.say("/aktifkan", user=ADMIN)
        for i, t in enumerate(["Rapat pindah Kamis ya", "Oke, aku bikin slide bab 2", "Kunci ruangan siapa?"]):
            result = await self.say(t, message_id=f"m{i}")
            self.assertEqual(result, {"action": "skip", "reason": "sumrom-dicatat"})
        self.assertEqual(len(self.plugin.store.unsummarized(GROUP)), 3)

        await self.say("/ringkas")
        text = self.last()
        self.assertIn("*Ringkasan Kelas 3B*", text)
        self.assertIn("3 pesan", text)
        self.assertIn("✅ *Keputusan*", text)
        self.assertIn("- *Rina* · Slide bab 2 · Kamis", text)
        self.assertIn("- *Bayu* · Rekap absen · _tanpa tenggat_", text)
        self.assertIn("❓ *Belum terjawab*", text)
        self.assertEqual(self.plugin.store.unsummarized(GROUP), [])
        self.assertIn("[", self.llm.calls[0]["input"][0]["text"])  # transkrip terkirim ke model

        await self.say("/ringkas")
        self.assertEqual(self.last(), fmt.nothing_new())

        await self.say("/tugas")
        self.assertIn("Tugas tercatat (2)", self.last())

    async def test_failed_model_keeps_messages_unsummarized(self):
        await self.say("/aktifkan", user=ADMIN)
        await self.say("pesan penting", message_id="x1")
        self.plugin.ctx.llm.fail = True
        await self.say("/ringkas")
        self.assertEqual(self.last(), fmt.summary_failed())
        self.assertEqual(len(self.plugin.store.unsummarized(GROUP)), 1)

    async def test_empty_sections_are_skipped(self):
        self.llm.parsed = {"inti": ["Ngobrol soal makan siang."], "keputusan": [], "tugas": [], "belum_terjawab": []}
        await self.say("/aktifkan", user=ADMIN)
        await self.say("makan di mana", message_id="a")
        await self.say("/ringkas")
        self.assertNotIn("Keputusan", self.last())
        self.assertNotIn("Tugas", self.last())
        self.assertNotIn("Belum terjawab", self.last())

    async def test_search_and_settings(self):
        await self.say("/aktifkan", user=ADMIN)
        await self.say("kunci ruangan dipegang Ayu", message_id="k")
        await self.say("/cari kunci")
        self.assertIn("kunci ruangan dipegang Ayu", self.last())
        await self.say("/cari xyz")
        self.assertIn("Tidak ada pesan", self.last())
        await self.say("/jadwal 21:00")
        self.assertEqual(self.last(), fmt.admin_only())
        await self.say("/jadwal 21.00", user=ADMIN)
        self.assertIn("21:00 WIB", self.last())
        await self.say("/gaya detail", user=ADMIN)
        self.assertIn("detail", self.last())
        self.assertEqual(self.plugin.store.get_group(GROUP).gaya, "detail")

    async def test_unknown_slash_is_normal_message(self):
        await self.say("/aktifkan", user=ADMIN)
        await self.say("/shrug wkwk", message_id="s")
        self.assertEqual(len(self.plugin.store.unsummarized(GROUP)), 1)

    async def test_dm_is_ignored_except_help(self):
        result = await self.say("halo bot", chat_type="dm")
        self.assertEqual(result["action"], "skip")
        self.assertEqual(self.adapter.sent, [])
        await self.say("/bantuan", chat_type="dm")
        self.assertIn("/ringkas", self.last())
        self.assertIn("https://sumrom.vercel.app", self.last())

    async def test_purge_removes_old_data(self):
        await self.say("/aktifkan", user=ADMIN)
        old = now_wib() - timedelta(days=8)
        self.plugin.store.add_message(GROUP, "old", "Rina", None, "lama", "teks", old)
        await self.say("baru", message_id="new")
        removed = self.plugin.store.purge_older_than(now_wib() - timedelta(days=7))
        self.assertEqual(removed, 1)
        self.assertEqual([m.text for m in self.plugin.store.unsummarized(GROUP)], ["baru"])

    async def test_scheduled_summary_sends_once(self):
        await self.say("/aktifkan", user=ADMIN)
        await self.say("ada rapat", message_id="r")
        now = now_wib()
        self.plugin.store.set_schedule(GROUP, now.strftime("%H:%M"))
        task = asyncio.get_running_loop().create_task(self.plugin._schedule_loop())
        await asyncio.sleep(0.3)
        task.cancel()
        summaries = [s for _, s in self.adapter.sent if s.startswith("📌")]
        self.assertEqual(len(summaries), 1)


class PureTest(unittest.TestCase):
    def test_parse_range(self):
        now = now_wib()
        self.assertEqual(parse_range("3 jam", now)[1], "3 jam terakhir")
        self.assertEqual(parse_range("30 menit", now)[1], "30 menit terakhir")
        self.assertEqual(parse_range("hari ini", now)[0].hour, 0)
        self.assertIsNone(parse_range("banyak", now))
        self.assertEqual(parse_range("30 hari", now)[0].date(), (now - timedelta(days=7)).date())

    def test_parse_hhmm(self):
        self.assertEqual(parse_hhmm("7:05"), "07:05")
        self.assertEqual(parse_hhmm("21.00"), "21:00")
        self.assertIsNone(parse_hhmm("25:00"))

    def test_split_message_keeps_lines(self):
        text = "\n".join(f"- baris {i} " + "x" * 50 for i in range(200))
        parts = fmt.split_message(text, 1000)
        self.assertTrue(all(len(p) <= 1000 for p in parts))
        self.assertEqual("\n".join(parts), text)

    def test_chunks_and_parse(self):
        now = now_wib()
        msgs = [StoredMessage(i, "A", "y" * 100, "teks", now) for i in range(50)]
        self.assertGreater(len(build_chunks(msgs, 1000)), 1)
        s = parse_summary({"inti": [" a ", ""], "keputusan": [], "tugas": [{"siapa": "", "apa": "x", "kapan": "null"}],
                           "belum_terjawab": []})
        self.assertEqual(s.core, ["a"])
        self.assertIsNone(s.tasks[0].when)
        self.assertIn("Belum jelas siapa", fmt.task_line(s.tasks[0]))

    def test_markdown_style(self):
        os.environ["SUMROM_TEXT_STYLE"] = "markdown"
        try:
            self.assertEqual(fmt.b("x"), "**x**")
        finally:
            os.environ.pop("SUMROM_TEXT_STYLE")


if __name__ == "__main__":
    unittest.main()
