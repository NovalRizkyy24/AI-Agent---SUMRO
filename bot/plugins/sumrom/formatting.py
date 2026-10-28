"""Format pesan WhatsApp SUMROM.

Semua teks yang dikirim bot ke grup disusun di sini, supaya nadanya
seragam: tegas, langsung ke pokok, tanpa basa-basi. Bagian yang kosong
dilewati, bukan diisi karangan. Angka masa simpan tidak pernah disebut.

Penanda tebal/miring memakai gaya WhatsApp (*tebal*, _miring_). Kalau
pengiriman lewat Hermes ternyata mengubah markdown, set
SUMROM_TEXT_STYLE=markdown supaya penanda ditulis **tebal** dan biarkan
Hermes yang mengonversi.
"""

from __future__ import annotations

import os
import random
from dataclasses import dataclass, field
from datetime import datetime

MAX_CHUNK = 3500  # WhatsApp sanggup ~4096; sisakan ruang aman.

WEEKDAYS = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]


def _style() -> str:
    return os.environ.get("SUMROM_TEXT_STYLE", "whatsapp").strip().lower()


def b(text: str) -> str:
    """Teks tebal."""
    return f"**{text}**" if _style() == "markdown" else f"*{text}*"


def i(text: str) -> str:
    """Teks miring."""
    return f"_{text}_"


def landing_url() -> str:
    return os.environ.get("SUMROM_LANDING_URL", "").strip()


@dataclass
class Task:
    who: str
    what: str
    when: str | None = None


@dataclass
class Summary:
    core: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    def is_empty(self) -> bool:
        return not (self.core or self.decisions or self.tasks or self.open_questions)


def fmt_time(dt: datetime) -> str:
    return dt.strftime("%H.%M")


def fmt_day_time(dt: datetime, now: datetime) -> str:
    if dt.date() == now.date():
        return f"hari ini {fmt_time(dt)}"
    return f"{WEEKDAYS[dt.weekday()]} {dt.day}/{dt.month} {fmt_time(dt)}"


def fmt_range(start: datetime, end: datetime, now: datetime) -> str:
    if start.date() == end.date():
        day = "Hari ini" if end.date() == now.date() else f"{WEEKDAYS[end.weekday()]} {end.day}/{end.month}"
        return f"{day}, {fmt_time(start)}–{fmt_time(end)}"
    return f"{fmt_day_time(start, now)} sampai {fmt_day_time(end, now)}"


def task_line(t: Task) -> str:
    when = t.when.strip() if t.when and t.when.strip() else i("tanpa tenggat")
    return f"- {b(t.who.strip() or 'Belum jelas siapa')} · {t.what.strip()} · {when}"


# ---------- Ringkasan ----------

def summary_message(group: str, summary: Summary, count: int, range_label: str) -> str:
    lines = [f"📌 {b('Ringkasan ' + group)}", f"{range_label} · {count} pesan"]

    def section(title: str, items: list[str]) -> None:
        if items:
            lines.append("")
            lines.append(title)
            lines.extend(f"- {x.strip()}" for x in items if x.strip())

    section(b("Inti"), summary.core)
    section(f"✅ {b('Keputusan')}", summary.decisions)
    if summary.tasks:
        lines.append("")
        lines.append(f"📝 {b('Tugas')}")
        lines.extend(task_line(t) for t in summary.tasks)
    section(f"❓ {b('Belum terjawab')}", summary.open_questions)

    if summary.is_empty():
        lines.append("")
        lines.append("Tidak ada keputusan, tugas, atau pertanyaan penting. Isinya obrolan biasa.")

    lines.append("")
    lines.append(i("Ringkasan bisa keliru. Untuk keputusan penting, cek pesan aslinya."))
    return "\n".join(lines)


def nothing_new() -> str:
    return "Belum ada pesan baru sejak ringkasan terakhir. Tidak ada yang perlu diringkas."


def nothing_in_range(range_label: str) -> str:
    return f"Tidak ada pesan tercatat untuk {range_label}."


def summary_failed() -> str:
    return (
        "Ringkasan gagal dibuat. Pesannya belum ditandai, jadi tidak ada yang hilang.\n"
        "Coba /ringkas lagi sebentar lagi."
    )


def summarizing_notice(count: int) -> str:
    return f"Merangkum {count} pesan. Tunggu sebentar."


# ---------- /tugas ----------

def tasks_message(tasks: list[Task]) -> str:
    if not tasks:
        return "Tidak ada tugas tercatat. Tugas muncul di sini setelah ada /ringkas yang menemukannya."
    lines = [f"📝 {b(f'Tugas tercatat ({len(tasks)})')}"]
    lines.extend(task_line(t) for t in tasks)
    lines.append("")
    lines.append(i("Diambil dari ringkasan grup ini. Tugas yang sudah beres tetap muncul sampai catatannya terhapus."))
    return "\n".join(lines)


# ---------- /cari ----------

@dataclass
class SearchHit:
    sender: str
    sent_at: datetime
    text: str


def search_message(query: str, hits: list[SearchHit], now: datetime, limit: int) -> str:
    if not hits:
        return f"Tidak ada pesan berisi \"{query}\" di catatan grup ini."
    lines = [f"{b(f'Hasil “{query}”')} · {len(hits)} pesan" + (f", {limit} terbaru" if len(hits) > limit else "")]
    for h in hits[:limit]:
        snippet = " ".join(h.text.split())
        if len(snippet) > 160:
            snippet = snippet[:157].rstrip() + "…"
        lines.append("")
        lines.append(f"{b(h.sender)} · {fmt_day_time(h.sent_at, now)}")
        lines.append(f"> {snippet}")
    return "\n".join(lines)


def search_usage() -> str:
    return "Tulis kata yang dicari. Contoh: /cari kunci ruangan"


# ---------- /bantuan ----------

def help_message() -> str:
    lines = [
        b("SUMROM · perintah"),
        "",
        "/ringkas — pesan sejak ringkasan terakhir",
        "/ringkas 3 jam — hanya rentang waktu itu",
        "/ringkas hari ini — semua pesan hari ini",
        "/tugas — tugas yang tercatat",
        "/cari kata — cari diskusi lama",
        "/bantuan — pesan ini",
        "",
        b("Khusus admin"),
        "/aktifkan · /nonaktifkan",
        "/jadwal 21:00 · /jadwal mati",
        "/gaya singkat · /gaya detail",
    ]
    if landing_url():
        lines += ["", f"Penjelasan lengkap: {landing_url()}"]
    return "\n".join(lines)


# ---------- Aktivasi ----------

def activated_message() -> str:
    lines = [
        b("SUMROM aktif di grup ini."),
        "",
        "Mulai sekarang pesan teks di grup ini dicatat, dan siapa pun bisa ketik /ringkas.",
        "",
        "- Isi pesan dikirim ke penyedia model AI untuk diringkas.",
        "- Gambar dan voice note tidak dibaca.",
        "- Jangan bahas data rahasia di sini selama bot aktif.",
        f"- {b('Keberatan? Bilang ke admin.')} Admin wajib ketik /nonaktifkan.",
    ]
    if landing_url():
        lines += ["", f"Baca selengkapnya: {landing_url()}"]
    return "\n".join(lines)


def already_active() -> str:
    return "SUMROM sudah aktif di grup ini."


def deactivated_message() -> str:
    return b("SUMROM berhenti mencatat grup ini.") + "\nPesan baru tidak dicatat lagi. Admin bisa ketik /aktifkan untuk menyalakan kembali."


def already_inactive() -> str:
    return "SUMROM memang sedang tidak aktif di grup ini."


def inactive_hint() -> str:
    return "SUMROM belum aktif di grup ini. Admin bisa ketik /aktifkan."


# ---------- Pengaturan ----------

def schedule_set(hhmm: str) -> str:
    return f"Ringkasan otomatis dikirim setiap hari pukul {hhmm} WIB, kalau ada pesan baru."


def schedule_off() -> str:
    return "Ringkasan otomatis dimatikan. /ringkas tetap bisa dipakai kapan saja."


def schedule_usage() -> str:
    return "Format jam tidak dikenali. Contoh: /jadwal 21:00 atau /jadwal mati"


def style_set(style: str) -> str:
    detail = "pendek, hanya yang penting" if style == "singkat" else "lebih lengkap, inti pembahasan dijabarkan"
    return f"Gaya ringkasan: {b(style)} ({detail})."


def style_usage() -> str:
    return "Pilih salah satu: /gaya singkat atau /gaya detail"


def range_usage() -> str:
    return "Rentang waktu tidak dikenali. Contoh: /ringkas 3 jam, /ringkas 30 menit, /ringkas hari ini"


def admin_only() -> str:
    return "Perintah ini khusus admin."


def whoami(user_id: str) -> str:
    return f"ID WhatsApp kamu di grup ini: {user_id}\nAdmin bot perlu memasukkan ID ini ke SUMROM_ADMINS."


# ---------- /jam benguk (tersembunyi, sengaja tidak ada di /bantuan) ----------

JAM_BENGUK = {
    "hina": [
        "Jam segitu kamu bengong lagi. Konsisten sih, sayang konsistennya di hal nggak guna.",
        "Itu jam produktifmu. Satu-satunya, jangan sampai kelewat.",
        "Jam segitu otakmu biasanya loading. Sabar ya, sinyalnya memang lemah dari lahir.",
        "Tugas numpuk, kamu malah nanya jam benguk. Prioritasmu perlu diservis.",
        "Jadwal rebahan resmi. Bedanya sama jam lain cuma ada di kertas.",
        "Jam segitu kamu baru sadar deadline. Telat, seperti biasa.",
    ],
    "puji": [
        "Jam segitu kamu lagi cakep-cakepnya. Sayang nggak ada yang lihat.",
        "Itu jam kamu paling encer. Pakai buat kerja, jangan buat scroll.",
        "Jam segitu ide brilianmu muncul. Catat, jangan cuma dipikirin.",
        "Jam segitu kamu jadi orang paling waras di grup ini. Bukan prestasi besar, tapi tetap selamat.",
        "Jam segitu aura kamu keluar. Jangan disia-siain buat ngelamun.",
    ],
    "motivasi": [
        "Bangun. Mimpi doang nggak bayar cicilan.",
        "Jam segitu waktunya mulai. Bukan besok, bukan habis makan. Jam segitu.",
        "Kamu nggak capek, kamu cuma belum mulai. Gas.",
        "Satu langkah kecil di jam segitu lebih berguna dari seribu rencana di kepala.",
        "Benguk boleh, menyerah jangan. Habis itu kerjain.",
        "Orang lain lagi ngejar target. Kamu lagi ngejar apa? Mulai jam segitu.",
    ],
}


def jam_benguk(rng: random.Random | None = None) -> str:
    rng = rng or random
    jam = f"{rng.randrange(24):02d}.{rng.randrange(60):02d}"
    kalimat = rng.choice(JAM_BENGUK[rng.choice(list(JAM_BENGUK))])
    return f"{b(f'Jam benguk kamu: {jam} WIB')}\n{kalimat}"


# ---------- Pemecah pesan panjang ----------

def split_message(text: str, limit: int = MAX_CHUNK) -> list[str]:
    """Pecah di batas paragraf/baris supaya format tidak terpotong di tengah."""
    if len(text) <= limit:
        return [text]
    chunks: list[str] = []
    current = ""
    for line in text.split("\n"):
        candidate = f"{current}\n{line}" if current else line
        if len(candidate) <= limit:
            current = candidate
            continue
        if current:
            chunks.append(current)
        while len(line) > limit:
            chunks.append(line[:limit])
            line = line[limit:]
        current = line
    if current:
        chunks.append(current)
    return chunks
