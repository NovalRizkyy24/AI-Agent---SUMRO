# SUMROM (Sumbul Roamer)

**Asisten WhatsApp perangkum percakapan grup berbasis Hermes Agent**

| Item | Keterangan |
|---|---|
| Nama aplikasi | SUMROM (Sumbul Roamer) |
| Nomor bot | 0895-2161-4500 (format internasional: +62 895-2161-4500) |
| Platform | WhatsApp (nomor bot terpisah) |
| Mesin agen | Hermes Agent (Nous Research, open-source, lisensi MIT) |
| Deployment | Docker / Docker Compose |
| Status dokumen | Rancangan awal (versi 0.1) |

---

## 1. Deskripsi Aplikasi

SUMROM adalah asisten WhatsApp berbasis Hermes Agent yang membantu pengguna memahami percakapan grup yang ramai tanpa harus membaca ratusan pesan satu per satu. Bot bergabung ke grup menggunakan nomor terpisah, menyimpan pesan yang masuk, lalu merangkumnya sesuai perintah (misalnya `/ringkas`) atau secara otomatis pada jadwal tertentu. Hasilnya tidak hanya berupa rangkuman naratif, tetapi juga terstruktur menjadi keputusan yang diambil, tugas beserta penanggung jawab dan tenggat waktunya, serta pertanyaan yang belum terjawab. Berkat memori persisten Hermes, bot mengingat konteks diskusi sebelumnya dan gaya ringkasan yang disukai pengguna, sehingga hasilnya semakin relevan dari waktu ke waktu. Seluruh sistem dijalankan di lingkungan terisolasi (Docker) agar data tetap aman dan terkendali.

## 2. Latar Belakang dan Tujuan

**Masalah**
- Grup WhatsApp (kelas, kerja, komunitas, organisasi) menghasilkan ratusan pesan per hari.
- Informasi penting (keputusan, tugas, tenggat) tenggelam di antara obrolan.
- Anggota yang terlambat membaca sering ketinggalan atau bertanya ulang.

**Tujuan**
1. Menyediakan ringkasan cepat dan akurat atas percakapan grup.
2. Mengekstrak keputusan, tugas, dan pertanyaan terbuka secara terstruktur.
3. Menghemat waktu baca anggota grup.
4. Menjaga privasi melalui penyimpanan yang terkendali dan penghapusan otomatis.

**Target pengguna:** anggota dan admin grup WhatsApp (kelas, tim kerja, komunitas, organisasi).

## 3. Ruang Lingkup

**Termasuk (versi awal)**
- Menerima dan menyimpan pesan teks grup yang diaktifkan.
- Ringkasan sesuai perintah dan terjadwal.
- Ekstraksi keputusan, tugas, dan pertanyaan terbuka.
- Pencarian diskusi lama dan daftar tugas.
- Pengaturan per grup oleh admin.

**Belum termasuk (tahap lanjutan)**
- Transkripsi voice note, pengenalan isi gambar.
- Dashboard web, statistik grup, dukungan multi-bahasa.

## 4. Arsitektur Sistem

```
[Grup WhatsApp]
      │ pesan masuk / perintah
      ▼
┌──────────────────────┐
│ 1. WhatsApp Gateway  │  nomor bot 0895-2161-4500
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 2. Message Handler   │  filter, parsing perintah, cek grup aktif
└───────┬──────────┬───┘
        │ simpan   │ perintah (/ringkas, /cari, ...)
        ▼          ▼
┌────────────┐  ┌──────────────────────┐
│ 3. Database│◄─┤ 4. Summarizer        │
│  (SQLite)  │  │  (Hermes + model API)│
└────────────┘  └──────────┬───────────┘
        ▲                  │ ringkasan
        │                  ▼
┌────────────┐  ┌──────────────────────┐
│ 5. Scheduler│─►│ 6. Sender            │──► balas ke grup / chat pribadi
└────────────┘  └──────────────────────┘
        ▲
┌───────┴────────┐
│ 7. Pembersih & │  hapus pesan mentah lama, backup
│    Backup      │
└────────────────┘
```

### Komponen

| # | Komponen | Tanggung jawab |
|---|---|---|
| 1 | WhatsApp Gateway | Menerima dan mengirim pesan memakai nomor bot (bridge bawaan Hermes berbasis Baileys / WhatsApp Web) |
| 2 | Message Handler | Mengabaikan pesan bot sendiri, mengenali perintah, hanya memproses grup yang diizinkan |
| 3 | Database | Menyimpan grup, pesan, ringkasan, tugas, dan pengaturan |
| 4 | Summarizer | Mengambil pesan yang belum diringkas, merangkum bertahap, menyusun format hasil |
| 5 | Scheduler | Memicu ringkasan otomatis (misalnya 07.00 dan 21.00) |
| 6 | Sender | Mengirim hasil, memecah pesan yang terlalu panjang |
| 7 | Pembersih & Backup | Menghapus pesan mentah setelah N hari, mencadangkan data |

## 5. Tech Stack

| Lapisan | Pilihan | Catatan |
|---|---|---|
| Agen | Hermes Agent | Memori persisten, skill, otomasi terjadwal, gateway pesan |
| Model AI | Model via API | Dipilih berdasarkan harga dan kualitas bahasa Indonesia |
| Kanal WhatsApp | Bridge bawaan Hermes (Baileys), mode *Separate bot number* | Alternatif resmi: WhatsApp Business Cloud API |
| Database | SQLite (awal), PostgreSQL (jika berkembang) | |
| Bahasa | Python (untuk skrip/skill penghubung) | |
| Penjadwal | Fitur jadwal Hermes atau cron | |
| Deployment | Docker + Docker Compose | Image: `nousresearch/hermes-agent` |
| Server | Laptop (uji coba), lalu VPS | Bot harus hidup terus agar pesan tercatat |

## 6. Rancangan Database

**groups**

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | integer (PK) | |
| wa_group_id | text | ID grup dari WhatsApp |
| nama | text | |
| aktif | boolean | Bot hanya bekerja bila true |
| jadwal_ringkas | text | Contoh: `21:00` |
| gaya_ringkasan | text | `singkat` / `detail` |
| dibuat_pada | datetime | |

**messages**

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | integer (PK) | |
| group_id | integer (FK) | |
| pengirim | text | |
| isi | text | |
| tipe | text | teks / media |
| waktu | datetime | |
| sudah_diringkas | boolean | |

**summaries**

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | integer (PK) | |
| group_id | integer (FK) | |
| dari_waktu | datetime | |
| sampai_waktu | datetime | |
| isi_ringkasan | text | |
| jumlah_pesan | integer | |
| dibuat_pada | datetime | |

**tasks** (opsional)

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | integer (PK) | |
| group_id | integer (FK) | |
| deskripsi | text | |
| penanggung_jawab | text | |
| tenggat | datetime | |
| status | text | terbuka / selesai |

Indeks penting: `messages(group_id, waktu)` dan `messages(group_id, sudah_diringkas)`.

## 7. Fitur

### Fitur inti (MVP)
- **Ringkas sesuai perintah:** `/ringkas` merangkum pesan sejak ringkasan terakhir.
- **Ringkas berdasarkan waktu:** `/ringkas 3 jam` atau `/ringkas hari ini`.
- **Penyimpanan pesan per grup:** pengirim dan waktu tercatat.
- **Penanda sudah diringkas:** pesan tidak diulang di ringkasan berikutnya.

### Ringkasan cerdas
- Format terstruktur: inti pembahasan, keputusan, tugas, pertanyaan terbuka.
- Ekstraksi tugas (siapa, apa, kapan).
- Ringkas bertahap untuk pesan sangat banyak.
- Pilihan gaya (singkat/detail, santai/formal) dan pengingat gaya per grup.

### Otomasi
- Ringkasan terjadwal (`/jadwal 21:00`).
- Pengingat tenggat yang disebut di grup.
- Kirim hasil ke chat pribadi pengguna.

### Pencarian dan pelacakan
- `/cari kata` untuk menemukan diskusi lama.
- `/tugas` untuk daftar tugas beserta statusnya.
- Riwayat ringkasan tersimpan.

### Pengelolaan
- Aktivasi per grup, hak admin untuk pengaturan, `/bantuan`.

### Privasi dan keamanan
- Penghapusan otomatis pesan mentah, pemberitahuan ke anggota grup, backup data.

## 8. Daftar Perintah

| Perintah | Fungsi | Hak akses |
|---|---|---|
| `/ringkas` | Ringkas pesan sejak ringkasan terakhir | Semua anggota |
| `/ringkas 3 jam` | Ringkas rentang waktu tertentu | Semua anggota |
| `/tugas` | Tampilkan daftar tugas terdeteksi | Semua anggota |
| `/cari kata` | Cari diskusi lama | Semua anggota |
| `/gaya singkat` / `/gaya detail` | Atur panjang ringkasan | Admin |
| `/jadwal 21:00` | Atur ringkasan otomatis | Admin |
| `/aktifkan` / `/nonaktifkan` | Aktif/nonaktifkan bot di grup | Admin |
| `/bantuan` | Daftar perintah | Semua anggota |

## 9. Alur Kerja

### Perintah `/ringkas`
1. Handler menerima perintah dan memeriksa apakah grup aktif.
2. Ambil pesan dengan `sudah_diringkas = false` (atau sesuai rentang waktu).
3. Pesan sedikit: rangkum langsung. Pesan banyak: bagi per blok, rangkum tiap blok, lalu gabungkan.
4. Susun hasil dalam format tetap, simpan ke `summaries`, tandai pesan sudah diringkas.
5. Sender mengirim hasil ke grup.

### Ringkasan terjadwal
Sama seperti di atas, tetapi dipicu Scheduler untuk setiap grup aktif yang memiliki pesan baru.

## 10. Format Ringkasan

```
📌 Ringkasan [nama grup] ([rentang waktu], [N] pesan)

Inti pembahasan:
- ...

✅ Keputusan:
- ...

📝 Tugas:
- [siapa] – [apa] – [kapan]

❓ Belum terjawab:
- ...
```

Bagian yang tidak ada isinya dilewati, bukan diisi karangan.

## 11. Penyiapan Nomor Bot dan Hermes (Docker)

### Nomor bot
- Nomor bot: **0895-2161-4500** (+62 895-2161-4500).
- Nomor harus aktif, bisa menerima SMS/panggilan verifikasi, dan sudah terdaftar di WhatsApp pada HP yang memegang nomor tersebut.
- Beri nama profil yang jelas (misalnya "SUMROM Bot") agar anggota grup tahu itu bot.
- Jangan memakai nomor utama atau nomor yang berisi riwayat chat penting.

### Struktur proyek
```
sumrom/
├── docker-compose.yml
└── .env          # API key, jangan di-commit ke Git
```

### docker-compose.yml
```yaml
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: sumrom-hermes
    command: gateway run
    restart: unless-stopped
    env_file: .env
    volumes:
      - ~/.hermes:/opt/data
```
Catatan: path `/opt/data` diambil dari panduan pihak ketiga. Cocokkan dengan halaman Docker resmi Hermes sebelum dipakai.

### Langkah setup
1. **Setup awal (sekali):**
   ```
   docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent:latest setup
   ```
   Pilih penyedia model dan masukkan API key.
2. **Tautkan WhatsApp:**
   ```
   docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent:latest whatsapp
   ```
   Pilih mode *Separate bot number*, lalu scan QR dari HP nomor bot (WhatsApp → Pengaturan → Perangkat tertaut → Tautkan perangkat).
3. **Atur allowlist:** secara default gateway menolak semua pesan masuk. Daftarkan nomor/grup yang diizinkan.
4. **Jalankan bot:**
   ```
   docker compose up -d
   docker compose logs -f hermes
   ```
5. **Uji bertahap:** chat pribadi ke nomor bot, lalu grup uji kecil, lalu perintah `/ringkas`.

### Perintah operasional

| Keperluan | Perintah |
|---|---|
| Lihat log | `docker compose logs -f hermes` |
| Restart | `docker compose restart hermes` |
| Berhenti | `docker compose down` |
| Update | `docker compose pull && docker compose up -d` |
| Pairing ulang WhatsApp | ulangi langkah 2, lalu restart container |

### Catatan hosting
- Selama dijalankan di laptop, laptop harus tetap menyala dan terhubung internet. Matikan mode sleep.
- Untuk operasi 24 jam, pindahkan ke VPS. Cukup salin `docker-compose.yml`, `.env`, dan folder `~/.hermes`.

## 12. Keamanan dan Privasi

- Bot hanya aktif di grup yang diaktifkan secara eksplisit, dan anggota diberi tahu bahwa ada bot perangkum.
- Gunakan nomor terpisah; nomor pribadi tidak dipakai.
- Pesan mentah dihapus otomatis setelah beberapa hari; ringkasan disimpan lebih lama.
- API key di `.env`; folder `~/.hermes` dan `.env` tidak dibagikan atau diunggah ke Git.
- Port API gateway tidak diekspos ke publik.
- Hanya admin yang boleh mengubah pengaturan (jadwal, gaya, hapus data).
- Isi pesan dikirim ke penyedia model AI untuk diringkas; informasikan hal ini kepada anggota grup.
- Hindari mengaktifkan bot di grup yang membahas data pribadi atau rahasia.

## 13. Kasus Khusus dan Penanganannya

| Kasus | Penanganan |
|---|---|
| Pesan sangat banyak | Ringkas bertahap agar tidak melewati batas konteks model dan biaya terkendali |
| Gambar / voice note | Versi awal: diabaikan atau ditandai `[media]` |
| Bot mati/terputus | Restart otomatis lewat Docker; pesan yang terlewat saat mati tidak bisa diambil |
| Sesi WhatsApp kedaluwarsa | Simpan sesi di volume persisten; pairing ulang bila perlu |
| Gagal memanggil model | Coba ulang beberapa kali, beri tahu pengguna, jangan tandai pesan sebagai sudah diringkas |
| Nomor bot dibatasi WhatsApp | Integrasi non-resmi berisiko; pertimbangkan WhatsApp Business Cloud API untuk pemakaian serius |

## 14. Risiko dan Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Nomor bot dibatasi/diblokir WhatsApp (bridge non-resmi) | Bot berhenti bekerja | Pakai nomor terpisah; pertimbangkan jalur resmi (Cloud API) |
| Sesi terputus setelah pembaruan WhatsApp | Pesan tidak tercatat | Update Hermes, pairing ulang, pantau log |
| Privasi anggota grup | Konflik/etika | Pemberitahuan, aktivasi eksplisit, penghapusan otomatis |
| Biaya API model membengkak | Biaya tak terkendali | Ringkas bertahap, batasi frekuensi, pantau pemakaian |
| Ringkasan tidak akurat | Informasi keliru | Format terstruktur, tidak mengarang bagian kosong, uji pada grup kecil |
| Laptop mati | Pesan terlewat | Pindah ke VPS untuk operasi 24 jam |

## 15. Hal yang Perlu Diverifikasi Lewat Uji Coba

1. Apakah bot menerima **semua pesan grup** atau hanya pesan yang menyebut bot (menentukan cara menyimpan pesan untuk ringkasan).
2. Nama pengaturan allowlist untuk grup di konfigurasi Hermes.
3. Path volume data yang benar di dalam container (`/opt/data` atau lainnya).
4. Cara membuat skill/skrip untuk menyimpan pesan ke database dan menjalankan jadwal.

## 16. Tahap Pengembangan

| Tahap | Isi | Hasil |
|---|---|---|
| 1. MVP | Terima pesan, simpan ke SQLite, `/ringkas` | Bot merangkum pesan grup uji |
| 2. Fitur inti | Format keputusan dan tugas, ringkas bertahap | Ringkasan terstruktur |
| 3. Otomasi | Jadwal, `/cari`, `/tugas`, pengaturan gaya | Ringkasan otomatis harian |
| 4. Pengerasan | Penghapusan otomatis, backup, hak admin, monitoring, pindah ke VPS | Siap dipakai stabil |
| 5. Lanjutan | Voice note, gambar, statistik, dashboard | Fitur tambahan |

## 17. Estimasi Biaya (Komponen)

| Komponen | Keterangan |
|---|---|
| Nomor bot | Biaya kartu SIM/pulsa untuk menjaga nomor tetap aktif |
| Server | Laptop sendiri (tanpa biaya tambahan) atau VPS berbayar |
| API model | Bergantung pada volume pesan dan model yang dipilih |
| Domain/lain-lain | Tidak diperlukan pada versi awal |

Angka pasti perlu dicek ke penyedia masing-masing karena harga berubah-ubah.

## 18. Referensi

- Dokumentasi Hermes Agent: WhatsApp Setup (`hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp`)
- Dokumentasi Hermes Agent: WhatsApp Business Cloud API (`.../messaging/whatsapp-cloud`)
- Dokumentasi Hermes Agent: Docker (`hermes-agent.nousresearch.com/docs/user-guide/docker`)
