# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

(Permukaan web: landing page, halaman panduan, dashboard admin. Produk intinya hidup di dalam WhatsApp; lihat Operating Context.)

## Stack

Delegated: diserahkan ke rekomendasi Claude.
- Hosting web: **Vercel** (dipilih pemilik 2026-10-18), Root Directory `landing`.
- Landing page dan halaman panduan: **Astro** (output statis). Kontennya kebanyakan teks dan jarang berubah, bisa di-host gratis, dan halaman docs bisa ditulis dalam Markdown.
- Dashboard admin: **belum diputuskan**. Dashboard butuh backend yang membaca database bot (SQLite di server yang sama dengan Hermes), jadi stack-nya dipilih saat dashboard mulai dibangun. Kandidatnya Astro mode SSR atau backend Python yang sebahasa dengan skrip/skill penghubung.

## Users

**Pengguna utama:** anggota grup WhatsApp (kelas, tim kerja, komunitas, organisasi) yang terlambat membaca. Mereka membuka grup yang sudah berisi ratusan pesan dan ingin langsung tahu apa yang diputuskan, tugas apa yang jatuh ke siapa dan kapan tenggatnya, serta apa yang masih belum terjawab, tanpa scroll dan tanpa bertanya ulang.

**Pengguna kedua:** admin grup yang mengaktifkan bot, mengatur jadwal dan gaya ringkasan, dan bertanggung jawab memberi tahu anggota soal privasi.

## Product Purpose

SUMROM (Sumbul Roamer) adalah bot WhatsApp berbasis Hermes Agent. Bot ini bergabung ke grup dengan nomor terpisah, menyimpan pesan, lalu merangkumnya saat diminta (`/ringkas`) atau sesuai jadwal. Hasilnya berupa ringkasan terstruktur: inti pembahasan, keputusan, tugas (siapa–apa–kapan), dan pertanyaan yang belum terjawab.

SUMROM berhasil kalau anggota yang ketinggalan bisa menyusul dalam satu kali baca, tanpa ada keputusan atau tenggat yang terlewat.

## Positioning

SUMROM tidak sekadar menyingkat obrolan. Isi grup dipilah menjadi keputusan, tugas, dan pertanyaan terbuka, dan bagian yang kosong dilewati, bukan dikarang. Bot bekerja langsung di dalam grup WhatsApp yang sudah dipakai, tanpa aplikasi tambahan, dan memori persisten Hermes membuatnya mengingat konteks diskusi serta gaya ringkasan per grup.

## Operating Context

- Interaksi utama terjadi **di dalam chat WhatsApp**: perintah teks (`/ringkas`, `/ringkas 3 jam`, `/tugas`, `/cari`, `/gaya`, `/jadwal`, `/aktifkan`, `/nonaktifkan`, `/bantuan`) dan balasan teks dari bot. Format pesan WhatsApp hanya mendukung teks, emoji, dan format bawaan WhatsApp (*tebal*, _miring_, ~coret~, ```monospace```), dibaca di layar HP.
- Format ringkasan saat ini ada di `SUMROM-rancangan-aplikasi.md` §10 (📌 judul, Inti pembahasan, ✅ Keputusan, 📝 Tugas, ❓ Belum terjawab).
- Nomor bot: 0895-2161-4500 (+62 895-2161-4500), nama profil disarankan "SUMROM Bot".
- Deployment: Docker Compose (`nousresearch/hermes-agent`), awalnya di laptop lalu pindah ke VPS.
- Permukaan web yang direncanakan: landing page, halaman panduan/docs (perintah, privasi, pemberitahuan untuk anggota), dan dashboard admin web (dalam rancangan awal dashboard ada di tahap 5, sekarang ingin dimajukan).

## Capabilities and Constraints

- Lingkup MVP: menyimpan pesan teks grup yang diaktifkan, ringkasan sesuai perintah dan terjadwal, ekstraksi keputusan/tugas/pertanyaan, `/cari`, `/tugas`, pengaturan per grup oleh admin.
- Belum termasuk: transkripsi voice note, pengenalan gambar (media ditandai `[media]`), statistik grup, multi-bahasa.
- Retensi: pesan mentah, ringkasan, dan tugas terdeteksi semuanya dihapus otomatis setelah **7 hari** (dikonfirmasi pemilik 2026-10-18). Keputusan pemilik (2026-10-18): masa simpan **tidak ditampilkan** di permukaan publik (landing page, panduan); jangan sebut angka retensi di sana.
- Bahasa produk: Bahasa Indonesia.
- Integrasi WhatsApp lewat bridge non-resmi (Baileys) punya risiko nomor dibatasi; WhatsApp Business Cloud API jadi alternatif resmi.
- Pesan yang masuk saat bot mati tidak bisa diambil kembali.
- Isi pesan dikirim ke penyedia model AI untuk diringkas; hal ini wajib diinformasikan ke anggota grup.
- Belum diverifikasi (rancangan §15): apakah bot menerima semua pesan grup, nama pengaturan allowlist, path volume data di container, dan cara skill menyimpan pesan ke database.

## Brand Commitments

- Nama: **SUMROM** (Sumbul Roamer).
- Suara: **tegas dan sedikit frontal**. Langsung ke pokok, tanpa basa-basi, berani menyebut siapa yang punya tugas dan apa yang belum beres. Dipakai di balasan bot dan di halaman web.
- Bot harus jelas terlihat sebagai bot, bukan menyamar sebagai anggota.
- Belum ada logo atau aset visual.

## Evidence on Hand

- Dokumen rancangan: `SUMROM-rancangan-aplikasi.md` (v0.1).
- **Belum ada** pengguna, uji coba di grup nyata, contoh ringkasan asli, testimoni, angka penghematan waktu, atau logo. Pekerjaan berikutnya tidak boleh mengarang satu pun dari itu. Contoh ringkasan di halaman web harus diberi label contoh/ilustrasi.
- Skala saat ini: dipakai di grup sendiri dulu, bukan layanan publik. Jangan ada klaim "siapa saja bisa menambahkan bot" atau harga.

## Product Principles

1. **Yang penting dulu.** Keputusan, tugas, dan tenggat lebih penting daripada narasi. Anggota yang ketinggalan harus menemukannya dalam hitungan detik.
2. **Jangan mengarang.** Bagian kosong dilewati, tugas tanpa tenggat ditulis tanpa tenggat. Akurasi lebih penting daripada kelengkapan.
3. **Terang-terangan soal privasi.** Bot hanya aktif kalau diaktifkan, anggota diberi tahu, isi pesan dikirim ke model AI, dan siapa pun boleh menolak. Hal-hal ini tidak boleh disembunyikan di halaman mana pun. Angka masa simpan tidak ditampilkan di permukaan publik (keputusan pemilik 2026-10-18).
4. **Tegas, bukan kasar.** Suaranya langsung dan frontal tentang apa yang belum beres, tanpa merendahkan orang.
5. **WhatsApp tetap rumahnya.** Permukaan web melayani bot (memperkenalkan, menjelaskan, mengatur), bukan menggantikan kebiasaan membaca di grup.
