# Bot SUMROM

Bot WhatsApp SUMROM berjalan sebagai **plugin Hermes Agent** di dalam Docker. Format setiap pesan bot dijelaskan di [docs/format-pesan.md](../docs/format-pesan.md).

## Cara kerja

```
Pesan grup ──► bridge WhatsApp Hermes ──► plugin SUMROM (hook pre_gateway_dispatch)
                                            │
                    obrolan biasa ──────────┤──► disimpan ke SQLite, bot diam
                    /ringkas, /tugas, ... ──┘──► dijawab langsung oleh plugin
                                                 (ringkasan lewat model AI Hermes)
```

- Plugin melihat **setiap** pesan WhatsApp sebelum sampai ke agen Hermes. Semua pesan di-skip, jadi agen tidak pernah ikut mengobrol di grup.
- Ringkasan dibuat lewat `ctx.llm`, yaitu model dan API key yang disetel di Hermes. Model hanya mengembalikan data JSON (inti, keputusan, tugas, belum terjawab), dan teks pesannya disusun oleh kode.
- Pesan baru ditandai "sudah diringkas" **setelah** ringkasan terkirim. Kalau model gagal, tidak ada yang hilang.
- Pesan, ringkasan, dan tugas yang lebih tua dari 7 hari dihapus otomatis. Pembersihan berjalan setiap jam dan setiap kali ada `/ringkas`.
- Semua data Hermes (API key, sesi WhatsApp, `config.yaml`, database SUMROM di `/opt/data/sumrom/sumrom.db`) disimpan di Docker volume `sumrom-hermes-data`, bukan folder Windows. Di Docker Desktop, folder Windows terlalu lambat untuk bridge WhatsApp, sehingga bridge gagal start dalam 15 detik, dan tidak aman untuk SQLite.

```
bot/
├── docker-compose.yml
├── .env.example            salin jadi .env
├── plugins/sumrom/
│   ├── plugin.yaml
│   ├── __init__.py         hook, perintah, penjadwal
│   ├── formatting.py       semua teks pesan WhatsApp
│   ├── summarize.py        transkrip → model → JSON
│   ├── store.py            SQLite
│   └── timeparse.py        WIB, /ringkas 3 jam, /jadwal 21:00
└── tests/test_sumrom.py
```

## Persiapan

- **Docker Desktop** yang sedang berjalan.
- **Nomor bot 0895-2161-4500** aktif di WhatsApp, di HP yang bisa dipakai untuk scan QR. Beri nama profil yang jelas, misalnya "SUMROM Bot".
- **API key penyedia model AI** (misalnya OpenRouter, Anthropic, atau OpenAI).

## Setup (sekali saja)

Semua perintah dijalankan dari folder `bot/`.

```powershell
cd D:\Gabutz\hermes\bot
copy .env.example .env
```

Buka `.env`, lalu isi:
- `SUMROM_ADMINS` dengan nomor admin (format `62812...`),
- `SUMROM_LANDING_URL` dengan link Vercel.

**1. Setup Hermes:** pilih penyedia model dan masukkan API key.

```powershell
docker compose run --rm hermes setup
```

**2. Tautkan WhatsApp:**

```powershell
docker compose run --rm hermes whatsapp
```

Pilih mode **bot** (nomor terpisah). Saat ditanya siapa yang boleh mengirim pesan ke bot, **kosongkan**. Jangan isi nomor bot. Lalu di HP nomor bot, buka WhatsApp → Perangkat tertaut → Tautkan perangkat, dan scan QR yang muncul.

**3. Atur Hermes dan aktifkan plugin:**

```powershell
docker compose run --rm hermes config set whatsapp.reply_prefix ""
docker compose run --rm hermes config set whatsapp.unauthorized_dm_behavior ignore
docker compose run --rm hermes plugins enable sumrom
```

**4. Jalankan bot:**

```powershell
docker compose up -d
docker compose logs -f hermes
```

Di log harus muncul `SUMROM siap, database: ...`.

## Uji di grup kecil

1. Masukkan nomor bot ke grup uji yang berisi 2–3 orang.
2. Admin mengetik `/idsaya`. Pastikan ID yang muncul sudah tercantum di `SUMROM_ADMINS`. Kalau belum, tambahkan, lalu jalankan `docker compose restart hermes`.
3. Admin mengetik `/aktifkan`. Bot mengirim pesan pemberitahuan ke grup.
4. Kirim beberapa pesan biasa. Bot harus diam.
5. Ketik `/ringkas`. Ringkasan dengan format di [docs/format-pesan.md](../docs/format-pesan.md) harus muncul.

## Verifikasi saat uji coba pertama

Hal-hal ini belum bisa dipastikan dari dokumentasi Hermes saja.

| Cek | Kalau gagal |
|---|---|
| Pesan biasa di grup tercatat (`/ringkas` menyebut jumlah pesan yang benar) | Aktifkan `WHATSAPP_ALLOW_ALL_USERS=true` di `.env`, lalu restart. Agen tetap diam karena plugin men-skip semua pesan. |
| Bot tidak membalas obrolan biasa | Pastikan plugin aktif: `docker compose run --rm hermes plugins list`. |
| `*tebal*` tampil tebal di grup | Kalau tampil miring, set `SUMROM_TEXT_STYLE=markdown`. |
| `/idsaya` menampilkan nomor 62..., bukan ID samaran | Kalau yang muncul ID samaran (LID), masukkan ID itu apa adanya ke `SUMROM_ADMINS`. |
| Ringkasan terjadwal (`/jadwal`) terkirim | Penjadwal mulai setelah pesan pertama masuk sejak bot dinyalakan. Setelah restart, kirim satu pesan apa saja di grup. |

## Perintah operasional

| Keperluan | Perintah |
|---|---|
| Lihat log | `docker compose logs -f hermes` |
| Restart (misalnya setelah mengubah `.env` atau plugin) | `docker compose restart hermes` |
| Berhenti | `docker compose down` |
| Update Hermes | `docker compose pull` lalu `docker compose up -d` |
| Pairing ulang WhatsApp | `docker compose down`, ulangi langkah 2, lalu `docker compose up -d` |
| Ubah `.env` (misalnya `SUMROM_ADMINS`) | `docker compose up -d --force-recreate` (restart biasa tidak membaca ulang `.env`) |

Untuk operasi 24 jam, pindahkan ke VPS: salin folder `bot/` beserta `.env`, lalu pindahkan isi volume `sumrom-hermes-data` (misalnya ekspor dengan `docker run --rm -v sumrom-hermes-data:/d -v ${PWD}:/b alpine tar czf /b/hermes-data.tgz -C /d .`).

## Menjalankan tes

Tes tidak butuh Hermes, Docker, atau API key. Gateway dan model dipalsukan.

```powershell
cd D:\Gabutz\hermes\bot
python -m unittest discover -s tests -v
```

## Privasi

- `.env` dan volume `sumrom-hermes-data` berisi API key, sesi WhatsApp, dan isi pesan grup. **Jangan** di-commit atau dibagikan.
- Jangan menjalankan dua bridge WhatsApp dengan sesi yang sama sekaligus. WhatsApp akan memutus sesi, dan nomor bot harus ditautkan ulang.
- Tidak ada port yang dibuka ke internet.
- Jangan aktifkan bot di grup yang membahas data pribadi atau rahasia.
