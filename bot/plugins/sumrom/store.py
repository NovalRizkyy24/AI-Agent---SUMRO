"""Penyimpanan SQLite SUMROM: grup, pesan, ringkasan, tugas.

Waktu disimpan sebagai detik epoch (UTC) supaya perbandingan rentang
sederhana; konversi ke WIB dilakukan saat ditampilkan.
"""

from __future__ import annotations

import sqlite3
import threading
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .formatting import SearchHit, Task
from .timeparse import WIB

RETENTION_DAYS = 7

SCHEMA = """
CREATE TABLE IF NOT EXISTS groups (
    wa_group_id     TEXT PRIMARY KEY,
    nama            TEXT,
    aktif           INTEGER NOT NULL DEFAULT 0,
    jadwal_ringkas  TEXT,
    gaya_ringkasan  TEXT NOT NULL DEFAULT 'singkat',
    jadwal_terakhir TEXT,
    dibuat_pada     INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id        TEXT NOT NULL REFERENCES groups(wa_group_id),
    wa_message_id   TEXT,
    pengirim        TEXT NOT NULL,
    pengirim_id     TEXT,
    isi             TEXT NOT NULL,
    tipe            TEXT NOT NULL DEFAULT 'teks',
    waktu           INTEGER NOT NULL,
    sudah_diringkas INTEGER NOT NULL DEFAULT 0,
    UNIQUE (group_id, wa_message_id)
);
CREATE INDEX IF NOT EXISTS idx_messages_group_time ON messages(group_id, waktu);
CREATE INDEX IF NOT EXISTS idx_messages_group_flag ON messages(group_id, sudah_diringkas);

CREATE TABLE IF NOT EXISTS summaries (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id      TEXT NOT NULL REFERENCES groups(wa_group_id),
    dari_waktu    INTEGER NOT NULL,
    sampai_waktu  INTEGER NOT NULL,
    isi_ringkasan TEXT NOT NULL,
    jumlah_pesan  INTEGER NOT NULL,
    dibuat_pada   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id          TEXT NOT NULL REFERENCES groups(wa_group_id),
    summary_id        INTEGER REFERENCES summaries(id),
    deskripsi         TEXT NOT NULL,
    penanggung_jawab  TEXT,
    tenggat           TEXT,
    status            TEXT NOT NULL DEFAULT 'terbuka',
    dibuat_pada       INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tasks_group ON tasks(group_id, dibuat_pada);
"""


@dataclass
class Group:
    wa_group_id: str
    nama: str
    aktif: bool
    jadwal: str | None
    gaya: str
    jadwal_terakhir: str | None


@dataclass
class StoredMessage:
    id: int
    sender: str
    text: str
    kind: str
    sent_at: datetime


def _ts(dt: datetime) -> int:
    return int(dt.timestamp())


def _dt(ts: int) -> datetime:
    return datetime.fromtimestamp(ts, WIB)


class Store:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._lock = threading.Lock()
        with self._lock:
            self._conn.executescript(SCHEMA)

    # ---------- grup ----------

    def get_group(self, wa_group_id: str) -> Group | None:
        row = self._conn.execute("SELECT * FROM groups WHERE wa_group_id = ?", (wa_group_id,)).fetchone()
        if not row:
            return None
        return Group(row["wa_group_id"], row["nama"] or "grup", bool(row["aktif"]),
                     row["jadwal_ringkas"], row["gaya_ringkasan"], row["jadwal_terakhir"])

    def upsert_group(self, wa_group_id: str, nama: str | None, now: datetime) -> Group:
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT INTO groups (wa_group_id, nama, dibuat_pada) VALUES (?, ?, ?) "
                "ON CONFLICT(wa_group_id) DO UPDATE SET nama = COALESCE(excluded.nama, groups.nama)",
                (wa_group_id, nama, _ts(now)),
            )
        return self.get_group(wa_group_id)  # type: ignore[return-value]

    def set_active(self, wa_group_id: str, active: bool) -> None:
        with self._lock, self._conn:
            self._conn.execute("UPDATE groups SET aktif = ? WHERE wa_group_id = ?", (int(active), wa_group_id))

    def set_schedule(self, wa_group_id: str, hhmm: str | None) -> None:
        with self._lock, self._conn:
            self._conn.execute("UPDATE groups SET jadwal_ringkas = ? WHERE wa_group_id = ?", (hhmm, wa_group_id))

    def mark_schedule_ran(self, wa_group_id: str, day: str) -> None:
        with self._lock, self._conn:
            self._conn.execute("UPDATE groups SET jadwal_terakhir = ? WHERE wa_group_id = ?", (day, wa_group_id))

    def set_style(self, wa_group_id: str, style: str) -> None:
        with self._lock, self._conn:
            self._conn.execute("UPDATE groups SET gaya_ringkasan = ? WHERE wa_group_id = ?", (style, wa_group_id))

    def scheduled_groups(self) -> list[Group]:
        rows = self._conn.execute(
            "SELECT wa_group_id FROM groups WHERE aktif = 1 AND jadwal_ringkas IS NOT NULL"
        ).fetchall()
        return [g for g in (self.get_group(r["wa_group_id"]) for r in rows) if g]

    # ---------- pesan ----------

    def add_message(self, group_id: str, wa_message_id: str | None, sender: str, sender_id: str | None,
                    text: str, kind: str, sent_at: datetime) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT OR IGNORE INTO messages (group_id, wa_message_id, pengirim, pengirim_id, isi, tipe, waktu) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (group_id, wa_message_id, sender, sender_id, text, kind, _ts(sent_at)),
            )

    def _rows_to_messages(self, rows) -> list[StoredMessage]:
        return [StoredMessage(r["id"], r["pengirim"], r["isi"], r["tipe"], _dt(r["waktu"])) for r in rows]

    def unsummarized(self, group_id: str) -> list[StoredMessage]:
        rows = self._conn.execute(
            "SELECT * FROM messages WHERE group_id = ? AND sudah_diringkas = 0 ORDER BY waktu, id", (group_id,)
        ).fetchall()
        return self._rows_to_messages(rows)

    def since(self, group_id: str, start: datetime) -> list[StoredMessage]:
        rows = self._conn.execute(
            "SELECT * FROM messages WHERE group_id = ? AND waktu >= ? ORDER BY waktu, id", (group_id, _ts(start))
        ).fetchall()
        return self._rows_to_messages(rows)

    def mark_summarized(self, ids: list[int]) -> None:
        if not ids:
            return
        with self._lock, self._conn:
            self._conn.executemany("UPDATE messages SET sudah_diringkas = 1 WHERE id = ?", [(x,) for x in ids])

    def search(self, group_id: str, query: str) -> list[SearchHit]:
        escaped = query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        rows = self._conn.execute(
            "SELECT pengirim, isi, waktu FROM messages WHERE group_id = ? AND tipe = 'teks' "
            "AND isi LIKE ? ESCAPE '\\' ORDER BY waktu DESC",
            (group_id, f"%{escaped}%"),
        ).fetchall()
        return [SearchHit(r["pengirim"], _dt(r["waktu"]), r["isi"]) for r in rows]

    # ---------- ringkasan & tugas ----------

    def save_summary(self, group_id: str, start: datetime, end: datetime, text: str, count: int,
                     tasks: list[Task], now: datetime) -> int:
        with self._lock, self._conn:
            cur = self._conn.execute(
                "INSERT INTO summaries (group_id, dari_waktu, sampai_waktu, isi_ringkasan, jumlah_pesan, dibuat_pada) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (group_id, _ts(start), _ts(end), text, count, _ts(now)),
            )
            summary_id = cur.lastrowid
            self._conn.executemany(
                "INSERT INTO tasks (group_id, summary_id, deskripsi, penanggung_jawab, tenggat, dibuat_pada) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                [(group_id, summary_id, t.what, t.who, t.when, _ts(now)) for t in tasks],
            )
        return int(summary_id)

    def open_tasks(self, group_id: str, limit: int = 30) -> list[Task]:
        rows = self._conn.execute(
            "SELECT deskripsi, penanggung_jawab, tenggat FROM tasks WHERE group_id = ? AND status = 'terbuka' "
            "ORDER BY dibuat_pada DESC, id DESC LIMIT ?",
            (group_id, limit),
        ).fetchall()
        return [Task(r["penanggung_jawab"] or "", r["deskripsi"], r["tenggat"]) for r in rows]

    # ---------- pembersihan ----------

    def purge_older_than(self, cutoff: datetime) -> int:
        """Hapus pesan, ringkasan, dan tugas yang lebih tua dari batas retensi."""
        ts = _ts(cutoff)
        with self._lock, self._conn:
            n = self._conn.execute("DELETE FROM messages WHERE waktu < ?", (ts,)).rowcount
            self._conn.execute("DELETE FROM tasks WHERE dibuat_pada < ?", (ts,))
            self._conn.execute("DELETE FROM summaries WHERE dibuat_pada < ? "
                               "AND id NOT IN (SELECT summary_id FROM tasks WHERE summary_id IS NOT NULL)", (ts,))
        return n
