// Semua teks halaman ada di sini, supaya komponen hanya mengurus tampilan.

export const BOT_NUMBER = '0895-2161-4500';

export const nav = [
  { href: '#fitur', label: 'Fitur' },
  { href: '#contoh', label: 'Contoh' },
  { href: '#perintah', label: 'Perintah' },
  { href: '#privasi', label: 'Privasi' },
  { href: '#faq', label: 'FAQ' },
];

export const facts = [
  { label: 'Dicatat', text: 'Pesan teks yang dikirim di grup ini.' },
  { label: 'Dikirim ke model AI', text: 'Isi pesan, supaya bisa diringkas.' },
  { label: 'Keberatan?', text: 'Admin wajib mengetik /nonaktifkan.' },
];

// Log di layar terminal hero.
export const terminal = [
  { t: '> /ringkas', cmd: true },
  { t: '... Membaca 214 pesan baru' },
  { t: '... Memilah inti pembahasan' },
  { t: '... Mencatat 2 keputusan' },
  { t: '... Mencatat 4 tugas' },
  { t: '... Mencari pertanyaan terbuka' },
  { t: '... Ringkasan terkirim ke grup' },
];

export type IconName = 'summary' | 'tasks' | 'range' | 'search' | 'clock' | 'chat';

export const features: { icon: IconName; title: string; text: string }[] = [
  { icon: 'summary', title: 'Ringkasan terstruktur', text: 'Inti pembahasan, keputusan, tugas, dan pertanyaan terbuka. Bagian yang kosong dilewati, tidak dikarang.' },
  { icon: 'tasks', title: 'Tugas siapa, apa, kapan', text: '/tugas menampilkan tugas yang terdeteksi, lengkap dengan penanggung jawab, tenggat, dan statusnya.' },
  { icon: 'range', title: 'Rentang waktu bebas', text: '/ringkas 3 jam atau /ringkas hari ini, kalau kamu hanya butuh potongan tertentu.' },
  { icon: 'search', title: 'Cari diskusi lama', text: '/cari kata menemukan pembahasan yang sudah tenggelam di atas.' },
  { icon: 'clock', title: 'Ringkasan terjadwal', text: 'Admin bisa memasang /jadwal 21:00, dan ringkasan terkirim otomatis tiap hari.' },
  { icon: 'chat', title: 'Langsung di WhatsApp', text: 'Tanpa aplikasi tambahan. Bot ikut grup dengan nomornya sendiri dan diam sampai dipanggil.' },
];

export const sample = {
  decisions: ['Rapat pindah ke Kamis, 19.00.', 'Iuran kas naik jadi Rp20.000.'],
  tasks: [
    { what: 'Slide bab 2', who: 'Rina', when: 'Kamis', s: 'Buka' },
    { what: 'Bayar kas', who: 'Dimas', when: 'Senin', s: 'Lewat tenggat', tone: 'late' },
    { what: 'Booking ruang', who: 'Ayu', when: 'Jumat', s: 'Selesai', tone: 'done' },
    { what: 'Rekap absen', who: 'Bayu', when: null, s: 'Buka' },
  ],
  open: ['Siapa yang pegang kunci ruangan?'],
};

export const commands = [
  { c: '/ringkas', v: 'Semua pesan sejak ringkasan terakhir.' },
  { c: '/ringkas 3 jam', v: 'Hanya rentang waktu yang kamu sebut. Bisa juga "hari ini".' },
  { c: '/tugas', v: 'Daftar tugas yang terdeteksi, dengan status.' },
  { c: '/cari kata', v: 'Temukan diskusi lama.' },
  { c: '/bantuan', v: 'Semua perintah.' },
];

export const adminCommands = [
  { c: '/aktifkan', v: 'Bot mulai mencatat grup ini.' },
  { c: '/nonaktifkan', v: 'Bot berhenti mencatat. Wajib dipakai kalau ada yang keberatan.' },
  { c: '/jadwal 21:00', v: 'Ringkasan otomatis tiap hari di jam itu.' },
  { c: '/gaya singkat', v: 'Atur panjang ringkasan: singkat atau detail.' },
];

export const recorded = [
  { k: 'Nama atau nomor pengirim', v: 'Supaya ringkasan tahu siapa bilang apa.' },
  { k: 'Isi pesan teks', v: 'Bahan ringkasan.' },
  { k: 'Waktu kirim', v: 'Supaya /ringkas 3 jam tahu batasnya.' },
  { k: 'Ringkasan dan tugas', v: 'Hasil /ringkas, termasuk siapa, apa, kapan.' },
];

export const notRecorded = [
  { k: 'Gambar dan voice note', v: 'Tidak dibaca. Hanya ditandai [media].' },
  { k: 'Pesan saat bot mati', v: 'Tidak tercatat sama sekali.' },
];

export const risks = [
  { k: 'Isi pesan keluar dari WhatsApp.', v: 'Teksnya dikirim ke penyedia model AI. Itu satu-satunya cara bot bisa merangkum.' },
  { k: 'Jangan bahas data rahasia di sini.', v: 'Nomor rekening, data pribadi, hal sensitif: bahas di luar grup ini selama bot aktif.' },
  { k: 'Bot mati, pesan hilang.', v: 'Pesan yang masuk saat bot mati tidak tercatat. Ringkasan bisa bolong.' },
  { k: 'Ringkasan bisa keliru.', v: 'Untuk keputusan penting, cek pesan aslinya sebelum bertindak.' },
];

export const faq = [
  { q: 'Apa bedanya dengan membaca chat sendiri?', a: 'Ratusan pesan dipilah jadi keputusan, tugas, dan pertanyaan yang belum terjawab. Pesan aslinya tetap ada di grup kalau kamu mau mengecek.' },
  { q: 'Siapa yang bisa memakai /ringkas?', a: 'Semua anggota grup. Pengaturan seperti /jadwal, /gaya, /aktifkan, dan /nonaktifkan khusus admin.' },
  { q: 'Apakah gambar dan voice note ikut dibaca?', a: 'Tidak. Gambar, video, dan voice note hanya ditandai [media] di catatan.' },
  { q: 'Ke mana isi pesan dikirim?', a: 'Teks pesan dikirim ke penyedia model AI supaya bisa diringkas. Karena itu, jangan bahas data rahasia di grup selama bot aktif.' },
  { q: 'Bagaimana kalau saya keberatan?', a: 'Bilang ke admin. Satu orang keberatan sudah cukup: admin wajib mengetik /nonaktifkan, dan bot berhenti mencatat grup ini.' },
  { q: 'Apakah bot membalas chat pribadi?', a: 'Tidak. Di chat pribadi bot hanya menjawab /bantuan dan /idsaya.' },
  { q: 'Apakah ringkasannya selalu benar?', a: 'Tidak selalu. Ringkasan dibuat model AI dan bisa keliru. Untuk keputusan penting, cek pesan aslinya.' },
  { q: 'Kenapa ada ringkasan yang bolong?', a: 'Pesan yang masuk saat bot mati tidak tercatat, jadi tidak ikut diringkas.' },
];
