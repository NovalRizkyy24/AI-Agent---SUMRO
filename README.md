# SUMROM (Sumbul Roamer)

Bot WhatsApp yang merangkum percakapan grup. Bot ini berjalan di atas [Hermes Agent](https://hermes-agent.nousresearch.com).

Grup kelas, kerja, dan komunitas bisa menghasilkan ratusan pesan sehari. Keputusan, tugas, dan tenggat sering tenggelam di antaranya. SUMROM bergabung ke grup dengan nomor terpisah dan menyimpan pesan teks. Saat ada yang mengetik `/ringkas`, atau sesuai jadwal, bot mengirim ringkasan terstruktur berisi:

- **Inti pembahasan**
- **Keputusan** yang diambil
- **Tugas** dengan format siapa, apa, kapan
- **Pertanyaan yang belum terjawab**

Bagian yang tidak ada isinya dilewati, tidak dikarang.

## Status

Proyek ini masih tahap awal.

| Bagian | Status |
|---|---|
| Rancangan aplikasi | Versi 0.1, lihat [SUMROM-rancangan-aplikasi.md](SUMROM-rancangan-aplikasi.md) |
| Landing page | Selesai, di [landing/](landing/) |
| Bot (Hermes + WhatsApp) | Belum dibangun (tahap 1 MVP) |
| Halaman panduan, dashboard admin | Direncanakan |

## Isi repository

```
.
├── SUMROM-rancangan-aplikasi.md   rancangan lengkap: arsitektur, database, fitur, perintah, setup Docker
├── PRODUCT.md                     ringkasan produk: pengguna, tujuan, batasan, prinsip
├── DESIGN.md                      sistem desain visual (modern minimalis)
├── landing/                       landing page (Astro, statis)
└── .impeccable/                   konfigurasi dan catatan desain
```

## Landing page

Landing page menjelaskan kepada anggota grup apa yang dicatat bot, apa risikonya, dan cara menolaknya. Link halaman ini dibagikan oleh admin di grup WhatsApp.

Butuh Node.js 18.20 ke atas.

```bash
cd landing
npm install
npm run dev       # server pengembangan di http://localhost:4321
npm run build     # hasil statis ke landing/dist
npm run preview   # lihat hasil build
```

Isi folder `landing/dist` bisa di-host di layanan statis mana pun, misalnya Netlify, Vercel, Cloudflare Pages, atau GitHub Pages.

## Perintah bot (rencana)

| Perintah | Fungsi | Hak akses |
|---|---|---|
| `/ringkas` | Ringkas pesan sejak ringkasan terakhir | Semua anggota |
| `/ringkas 3 jam` | Ringkas rentang waktu tertentu | Semua anggota |
| `/tugas` | Daftar tugas yang terdeteksi | Semua anggota |
| `/cari kata` | Cari diskusi lama | Semua anggota |
| `/bantuan` | Daftar perintah | Semua anggota |
| `/gaya singkat` / `/gaya detail` | Atur panjang ringkasan | Admin |
| `/jadwal 21:00` | Atur ringkasan otomatis | Admin |
| `/aktifkan` / `/nonaktifkan` | Aktifkan atau matikan bot di grup | Admin |

## Privasi

- Bot hanya bekerja di grup yang diaktifkan secara eksplisit oleh admin, dan anggota grup diberi tahu.
- Pesan mentah dihapus otomatis setelah beberapa hari.
- Isi pesan dikirim ke penyedia model AI untuk diringkas.
- Jika ada anggota yang keberatan, admin wajib menonaktifkan bot dengan `/nonaktifkan`.
- API key disimpan di `.env`. File `.env` dan folder data Hermes (`~/.hermes`) **tidak boleh** di-commit ke repository ini.

## Teknologi

- **Agen:** Hermes Agent (Nous Research, MIT)
- **WhatsApp:** bridge bawaan Hermes (Baileys), dengan nomor bot terpisah
- **Database:** SQLite
- **Deployment:** Docker Compose
- **Landing page:** Astro, dengan huruf Schibsted Grotesk dan JetBrains Mono
