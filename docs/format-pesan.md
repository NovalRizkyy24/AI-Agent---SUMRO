# Format pesan WhatsApp SUMROM

Dokumen ini mencatat bentuk setiap pesan yang dikirim bot ke grup. Sumber kebenarannya adalah kode di [`bot/plugins/sumrom/formatting.py`](../bot/plugins/sumrom/formatting.py). Contoh di bawah dihasilkan langsung dari kode itu. Kalau formatnya diubah, ubah kodenya dulu, lalu perbarui dokumen ini.

## Prinsip

1. **Yang penting dulu.** Keputusan, tugas, dan pertanyaan terbuka harus terbaca dalam satu kali scroll di HP.
2. **Jangan mengarang.** Bagian yang kosong tidak ditampilkan. Tugas tanpa tenggat ditulis _tanpa tenggat_, dan tugas tanpa nama ditulis *Belum jelas siapa*.
3. **Tegas, bukan kasar.** Kalimatnya pendek dan langsung, tanpa sapaan atau "semoga membantu".
4. **Empat penanda saja:** 📌 judul, ✅ keputusan, 📝 tugas, ❓ belum terjawab. Emoji lain tidak dipakai.
5. **Format bawaan WhatsApp:** `*tebal*` untuk judul bagian dan nama orang, `_miring_` untuk catatan, dan `>` untuk kutipan di hasil `/cari`.
6. **Tidak ada angka masa simpan.** Keputusan pemilik: angka retensi tidak ditampilkan di permukaan publik, termasuk di chat.
7. **Pesan panjang dipecah** di batas baris (maksimal sekitar 3.500 karakter per pesan), supaya format tidak terpotong di tengah.

## Ringkasan (`/ringkas` dan ringkasan terjadwal)

```
📌 *Ringkasan Kelas 3B*
Hari ini, 07.12–20.48 · 214 pesan

*Inti*
- Rapat minggu ini dipindah karena ruang dipakai kelas lain.
- Kas bulan ini kurang untuk sewa proyektor.

✅ *Keputusan*
- Rapat pindah ke Kamis, 19.00.
- Iuran kas naik jadi Rp20.000.

📝 *Tugas*
- *Rina* · Slide bab 2 · Kamis
- *Dimas* · Bayar kas · Senin
- *Bayu* · Rekap absen · _tanpa tenggat_

❓ *Belum terjawab*
- Siapa yang pegang kunci ruangan?

_Ringkasan bisa keliru. Untuk keputusan penting, cek pesan aslinya._
```

- **Urutan bagian:** Inti, Keputusan, Tugas, Belum terjawab. Bagian kosong dilewati.
- **Kalau semuanya kosong:** setelah baris judul muncul "Tidak ada keputusan, tugas, atau pertanyaan penting. Isinya obrolan biasa."
- **`/gaya singkat`:** Inti maksimal 3 butir. **`/gaya detail`:** Inti maksimal 6 butir.
- **Baris rentang waktu:** "Hari ini, 07.12–20.48" untuk satu hari, atau "Sen 12/10 21.05 sampai hari ini 08.30" untuk lintas hari.
- **Pesan dari model hanya berupa data JSON** (inti, keputusan, tugas, belum terjawab). Susunan teks selalu dibuat oleh kode, jadi bentuknya tidak bisa melenceng.

## `/tugas`

```
📝 *Tugas tercatat (3)*
- *Rina* · Slide bab 2 · Kamis
- *Dimas* · Bayar kas · Senin
- *Bayu* · Rekap absen · _tanpa tenggat_

_Diambil dari ringkasan grup ini. Tugas yang sudah beres tetap muncul sampai catatannya terhapus._
```

Kalau belum ada tugas: "Tidak ada tugas tercatat. Tugas muncul di sini setelah ada /ringkas yang menemukannya."

## `/cari kata`

```
*Hasil “kunci”* · 1 pesan

*Ayu* · Sab 17/10 19.00
> Kunci ruangan aku titip ke pak satpam ya, ambil di pos depan
```

- Yang ditampilkan maksimal 5 pesan terbaru. Kalau lebih, judulnya menjadi "· 12 pesan, 5 terbaru".
- Potongan pesan maksimal 160 karakter.
- Kalau tidak ada hasil: `Tidak ada pesan berisi "xyz" di catatan grup ini.`

## `/bantuan`

```
*SUMROM · perintah*

/ringkas — pesan sejak ringkasan terakhir
/ringkas 3 jam — hanya rentang waktu itu
/ringkas hari ini — semua pesan hari ini
/tugas — tugas yang tercatat
/cari kata — cari diskusi lama
/bantuan — pesan ini

*Khusus admin*
/aktifkan · /nonaktifkan
/jadwal 21:00 · /jadwal mati
/gaya singkat · /gaya detail

Penjelasan lengkap: https://<alamat-landing-page>
```

## Saat bot diaktifkan (`/aktifkan`)

Pesan ini adalah pemberitahuan resmi ke anggota bahwa grup mulai dicatat.

```
*SUMROM aktif di grup ini.*

Mulai sekarang pesan teks di grup ini dicatat, dan siapa pun bisa ketik /ringkas.

- Isi pesan dikirim ke penyedia model AI untuk diringkas.
- Gambar dan voice note tidak dibaca.
- Jangan bahas data rahasia di sini selama bot aktif.
- *Keberatan? Bilang ke admin.* Admin wajib ketik /nonaktifkan.

Baca selengkapnya: https://<alamat-landing-page>
```

## Pesan pendek lainnya

| Situasi | Pesan |
|---|---|
| `/nonaktifkan` | *SUMROM berhenti mencatat grup ini.* Pesan baru tidak dicatat lagi. Admin bisa ketik /aktifkan untuk menyalakan kembali. |
| Perintah dipakai saat bot belum aktif | SUMROM belum aktif di grup ini. Admin bisa ketik /aktifkan. |
| Perintah admin oleh bukan admin | Perintah ini khusus admin. |
| `/ringkas`, tidak ada pesan baru | Belum ada pesan baru sejak ringkasan terakhir. Tidak ada yang perlu diringkas. |
| `/ringkas 3 jam`, kosong | Tidak ada pesan tercatat untuk 3 jam terakhir. |
| Rentang tidak dikenali | Rentang waktu tidak dikenali. Contoh: /ringkas 3 jam, /ringkas 30 menit, /ringkas hari ini |
| Lebih dari 150 pesan | Merangkum 214 pesan. Tunggu sebentar. |
| `/ringkas` saat ringkasan lain sedang jalan | Ringkasan sedang dibuat. Tunggu hasilnya dulu. |
| Model AI gagal | Ringkasan gagal dibuat. Pesannya belum ditandai, jadi tidak ada yang hilang. Coba /ringkas lagi sebentar lagi. |
| `/jadwal 21:00` | Ringkasan otomatis dikirim setiap hari pukul 21:00 WIB, kalau ada pesan baru. |
| `/jadwal mati` | Ringkasan otomatis dimatikan. /ringkas tetap bisa dipakai kapan saja. |
| `/gaya detail` | Gaya ringkasan: *detail* (lebih lengkap, inti pembahasan dijabarkan). |
| `/idsaya` | ID WhatsApp kamu di grup ini: … Admin bot perlu memasukkan ID ini ke SUMROM_ADMINS. |

## Kapan bot diam

- **Obrolan biasa di grup:** selalu dicatat (kalau grup aktif) dan tidak pernah dibalas.
- **Teks diawali `/` yang bukan perintah SUMROM** (misalnya `/shrug`): dianggap pesan biasa.
- **Chat pribadi ke nomor bot:** diabaikan, kecuali `/bantuan` dan `/idsaya`.
- **Ringkasan terjadwal tanpa pesan baru:** tidak mengirim apa pun.
