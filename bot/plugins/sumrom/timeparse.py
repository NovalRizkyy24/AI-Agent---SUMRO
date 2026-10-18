"""Waktu WIB dan pembacaan argumen rentang waktu (/ringkas 3 jam, /jadwal 21:00)."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

# WIB tidak punya musim panas, jadi offset tetap aman tanpa paket tzdata.
WIB = timezone(timedelta(hours=7), "WIB")


def now_wib() -> datetime:
    return datetime.now(WIB)


_UNIT = {
    "menit": "minutes", "mnt": "minutes", "m": "minutes",
    "jam": "hours", "j": "hours", "h": "hours",
    "hari": "days", "d": "days",
}


def parse_range(arg: str, now: datetime) -> tuple[datetime, str] | None:
    """Kembalikan (waktu mulai, label) atau None kalau tidak dikenali.

    Argumen kosong ditangani pemanggil (mode "sejak ringkasan terakhir").
    """
    text = " ".join(arg.lower().split())
    if text in ("hari ini", "hariini", "today"):
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return start, "hari ini"
    if text == "kemarin":
        start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        return start, "sejak kemarin"
    match = re.fullmatch(r"(\d{1,3})\s*([a-z]+)", text)
    if not match:
        return None
    amount, unit = int(match.group(1)), _UNIT.get(match.group(2))
    if not unit or amount <= 0:
        return None
    delta = timedelta(**{unit: amount})
    if delta > timedelta(days=7):
        delta = timedelta(days=7)
    label_unit = {"minutes": "menit", "hours": "jam", "days": "hari"}[unit]
    return now - delta, f"{amount} {label_unit} terakhir"


def parse_hhmm(arg: str) -> str | None:
    match = re.fullmatch(r"(\d{1,2})[:.](\d{2})", arg.strip())
    if not match:
        return None
    hour, minute = int(match.group(1)), int(match.group(2))
    if hour > 23 or minute > 59:
        return None
    return f"{hour:02d}:{minute:02d}"
