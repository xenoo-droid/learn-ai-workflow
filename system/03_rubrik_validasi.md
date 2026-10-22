---
dokumen: rubrik_validasi
versi: 1.0
tanggal: 2026-10-22
peran: Menjawab "kapan sebuah modul boleh naik status?" Dibaca oleh mentor AI dan oleh tools/progress.py.
otoritas: Di bawah constitution.md, di atas protokol_mentor.md
---

# Rubrik Validasi

Rubrik ini menentukan kapan sebuah modul boleh naik status. Aturannya bersifat **constraint**, bukan saran. Perubahan rubrik hanya sah dengan persetujuan eksplisit Rafa.

## 1. Lima status

| Status | Arti | Syarat naik |
|---|---|---|
| **Learned** | Materi dan latihan terpandu selesai, belum diuji | Materi selesai dipelajari |
| **Validated** | Lulus ujian validasi | Lihat bagian 3 |
| **Retained** | Masih bisa setelah jeda, di konteks baru | Lihat bagian 5 |
| **Mastered** | Terbukti dipakai mandiri di situasi baru | Lihat bagian 6 |
| **Validated (legacy)** | Dinyatakan selesai sebelum rubrik ini ada; bukti belum terdokumentasi | Lihat bagian 7 |

Istilah `COMPLETED` tidak dipakai lagi. Skor tinggi atau challenge yang sukses tidak otomatis berarti Retained atau Mastered.

## 2. Bentuk ujian per tipe modul

| Tipe modul | Contoh | Bentuk ujian validasi |
|---|---|---|
| Quest materi | Scatter Plot, groupby() | 3–5 soal + 1 challenge (sesuai aturan sesi "latihan") |
| Review modul | Matplotlib Review | 1 challenge transfer Level 3 pada dataset baru yang memakai ≥2 skill sebelumnya + 3 soal retrieval |
| Portfolio | Data Analysis Report | Proyek lengkap + README + refleksi (apa masalahnya, keputusan, keterbatasan) |

Level soal: **L1** terpandu, **L2** terapan (memilih konsep sendiri), **L3** transfer (masalah baru, pendekatan dipilih sendiri). Setiap ujian memuat minimal satu soal L2, dan semakin tinggi World, semakin banyak L3.

## 3. Syarat Validated

Semua syarat harus terpenuhi:

1. **Akurasi ≥ 80%** pada skor gabungan (soal 50%, challenge 50%). Challenge tidak punya gerbang terpisah: bila challenge kurang berhasil, dampaknya cukup tercermin di skor gabungan.
2. **Pemahaman:** Rafa menjelaskan alasan dari **dua keputusan** yang ia ambil (bukan hanya sintaks).
3. **Bukti tersimpan:** notebook atau file yang bisa dibuka kembali, dirujuk di Evidence Entry.

Jika tidak lulus: status tetap Learned. Mentor memberi umpan balik, dan Rafa boleh mengulang kapan saja dengan soal berbeda, tanpa batas jumlah percobaan. Rubrik ini dibuat untuk belajar otodidak: tujuannya mendiagnosis, bukan menghukum.

## 4. Mode bantuan AI

Tiga mode, selalu **dicatat** di Evidence Entry:

- **Independent**: Rafa mencoba sendiri sepenuhnya.
- **Assisted**: AI memberi hint, debugging, atau umpan balik terarah.
- **Review**: AI mengkritik solusi yang sudah selesai.

Aturan:
- Untuk **Validated**, bantuan AI fleksibel (tidak dibatasi), tetapi modenya wajib dicatat dan keluaran AI tidak dianggap benar otomatis.
- Untuk **Retained** dan **Mastered**, mode wajib **Independent**. Mengingat dengan bantuan AI tidak membuktikan retensi.

## 5. Syarat Retained (retrieval review)

- Dilakukan **minimal 7 hari** setelah tanggal Validated.
- 2–3 soal **retrieval** tanpa membuka catatan, pada **konteks baru** (bukan contoh yang sama dengan saat belajar).
- Akurasi **≥ 80%**, mode **Independent**.
- Jadwal otomatis: review pertama H+7 setelah tanggal Validated. Setelah lulus, konfirmasi dijadwalkan pada H+30 dari tanggal Validated (paling cepat 7 hari setelah retrieval). Untuk modul legacy yang tidak punya tanggal Validated, konfirmasi jatuh 30 hari setelah retrieval pertama.
- Setelah konfirmasi lulus, tidak ada review terjadwal lagi; jalur berikutnya adalah Mastered.

Jika retrieval gagal: status **tidak turun** dan pencapaian tidak dihapus. Modul diberi tanda `perlu_review`, lalu dijadwalkan ulang H+3.

## 6. Syarat Mastered

- Skill terbukti dipakai **mandiri (Independent)** di **≥ 2 konteks berbeda** (dataset atau masalah berbeda), misalnya challenge L3 atau proyek portofolio.
- Bukti dirujuk dari kedua konteks.
- Hanya modul berstatus Retained yang boleh naik ke Mastered.

## 7. Aturan Validated (legacy)

- Tetap **dihitung sebagai progres selesai**. Tidak ada pencapaian yang hilang.
- Ada dua jalan keluar:
  - Bukti lama ditemukan dan ditambahkan → naik menjadi **Validated**.
  - Lulus retrieval review (bagian 5) → naik langsung menjadi **Retained**, karena retrieval itu sendiri adalah bukti baru.
- Modul legacy otomatis masuk antrean review.

## 8. Evidence Entry (bukti wajib)

Setiap perubahan status harus disertai satu entri dengan kolom berikut:

| Kolom | Isi |
|---|---|
| id | Pengenal unik, contoh `2026-10-22-matplotlib-review` |
| modul | `id` modul/quest di `state/state.yaml` (contoh `savefig`) |
| tanggal | YYYY-MM-DD |
| jenis | `validasi`, `retrieval`, atau `mastery` |
| skor_persen | Angka 0–100 |
| mode_ai | `independent`, `assisted`, atau `review` |
| level_soal | Ringkasan L1/L2/L3 yang diuji |
| bukti | Path file atau tautan commit |
| pemahaman | Dua keputusan beserta alasannya |
| konteks | Khusus `mastery`: minimal dua konteks berbeda beserta bukti masing-masing |
| keputusan | Status baru yang diusulkan; tulis `tetap` bila ujian tidak lulus |

`tools/progress.py` menghitung sendiri hasil akhirnya. Bila `keputusan` tidak sama dengan hasil perhitungan, entri ditolak.

## 9. Siapa yang boleh mengubah state?

- **Mentor AI** hanya **mengusulkan** Evidence Entry. Mentor tidak pernah mengubah `state.yaml` dan tidak boleh mengklaim progres dari ingatannya sendiri.
- **tools/progress.py** memeriksa aturan di atas lalu menulis `state.yaml`.
- **Rafa** menyetujui dan melakukan commit.
- Jika ingatan mentor bertentangan dengan `state.yaml`, yang berlaku adalah `state.yaml`.

## 10. Yang dilarang

- Menaikkan status karena topik "pernah dibahas".
- Melompati modul atau World yang masih terkunci.
- Menghapus atau menurunkan status yang sudah tervalidasi.
- Mengubah format dashboard di luar spesifikasi yang disetujui.
