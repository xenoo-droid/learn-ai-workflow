---
dokumen: alur_kerja_command
versi: 2.0
peran: Arti setiap command dan alur dari belajar sampai commit. Dibaca mentor dan Rafa.
---

# Alur Kerja dan Command

## Pembagian peran

| Pelaku | Tugas |
|---|---|
| **Mentor AI** (ChatGPT Project) | Mengajar, menguji, memberi umpan balik, mengusulkan Evidence Entry |
| **`tools/progress.py`** | Memeriksa entri terhadap rubrik, mengubah `state.yaml`, membuat dashboard, menghitung review |
| **Rafa** | Mengerjakan ujian, menyetujui, menjalankan script, commit, dan mengunggah ulang file state ke Project |

Mentor tidak mengubah state dan tidak melakukan commit.

## Command

| Command | Fungsi |
|---|---|
| `cek progres` | Tampilkan dashboard dan review yang jatuh tempo |
| `lanjut` | Lanjutkan quest aktif |
| `review` | Jalankan retrieval review |
| `latihan` | Sesi latihan: 3–5 soal + 1 challenge |
| `save` | Rangkum sesi dan usulkan Evidence Entry (penyesuaian, lihat catatan) |
| `prepare commit` | Periksa kesiapan sebelum commit |
| `commit progres` | Berikan langkah commit dan unggah ulang |

### `cek progres`

1. Mentor membaca `state/state.yaml` dan `state/dashboard.md`.
2. Menampilkan isi `dashboard.md` **apa adanya** dalam blok kode.
3. Menyebut review yang jatuh tempo berdasarkan `review_berikutnya` dan `perlu_review` di `state.yaml`. Daftar resminya: `python tools/progress.py due`.
4. Jika Rafa melaporkan kemajuan baru, mentor meminta bukti lalu mengusulkan Evidence Entry. Mentor tidak mengubah status. Jika tidak ada kemajuan, jangan mengarang kemajuan.

### `lanjut`

Melanjutkan quest di `posisi_saat_ini`. Tidak boleh melompat ke materi mendatang atau mengubah dependensi roadmap. Materi baru mengikuti aturan penyajian materi di `system/04_protokol_mentor.md`.

### `review`

Menjalankan retrieval review untuk modul yang jatuh tempo: 2–3 soal tanpa catatan, di konteks baru, mode `independent`. Modul legacy masuk antrean maksimal 2 per sesi. Hasilnya menjadi Evidence Entry berjenis `retrieval`.

### `latihan`

Sesi berisi 3–5 soal dan 1 challenge, hanya dari materi yang sudah diajarkan. Untuk ujian validasi, ikuti `system/03_rubrik_validasi.md`.

### `save` (penyesuaian, menunggu persetujuan Rafa)

Definisi lama: menyimpan historis percakapan yang relevan dan memperbarui memori proyek, tanpa commit dan push. Karena sumber kebenaran kini file di repo dan mentor tidak bisa menulis ke repo, `save` menjadi: mentor merangkum sesi dan, bila ada milestone, menyusun Evidence Entry untuk Rafa. Tetap tanpa commit dan push.

### `prepare commit`

Hanya persiapan, tidak mengubah apa pun. Mentor memeriksa Evidence Entry: kolom lengkap, sesuai rubrik, `keputusan` konsisten dengan skor. Lalu menyusun pesan commit dan menyatakan **SIAP** atau **BELUM SIAP**.

### `commit progres`

Mentor memberi langkah persis untuk dijalankan Rafa (di bawah). Mentor sendiri tidak melakukan commit.

## Langkah milestone untuk Rafa

Simpan Evidence Entry dari mentor ke sebuah file di akar repo, misalnya `entri.yaml` (nama `entri*.yaml` diabaikan git, jadi tidak ikut ter-commit; salinan resminya otomatis dibuat di `state/evidence/`). Lalu di PowerShell dari folder repo:

```powershell
python tools\progress.py apply entri.yaml --dry    # simulasi, tidak mengubah file
python tools\progress.py apply entri.yaml          # terapkan
python tools\progress.py check                     # pastikan state konsisten
git add -A
git commit -m "docs: validasi <nama modul>"
git push
```

Lalu **ganti dua file di ChatGPT Project**: hapus versi lama `state.yaml` dan `dashboard.md`, unggah versi baru. Tanpa langkah ini mentor masih membaca state lama.

Jika `apply` menolak entri, pesan galatnya menyebut aturan mana yang dilanggar. Perbaiki entrinya bersama mentor; jangan mengedit `state.yaml` manual untuk menyiasatinya.

## Alur singkat

```text
Belajar → ujian → mentor usul Evidence Entry → Rafa jalankan apply → check
       → commit + push → ganti state.yaml & dashboard.md di Project → lanjut
```
