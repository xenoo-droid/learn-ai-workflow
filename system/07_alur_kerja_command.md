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
| **ChatGPT Work** (bila dipakai) | Hanya menaruh file Evidence Entry di `state/inbox/` pada repo. Tidak mengubah file lain |
| **`tools/progress.py`** | Memeriksa entri terhadap rubrik, mengubah `state.yaml`, membuat dashboard, menghitung review |
| **Workflow GitHub** (`progres.yml`) | Menjalankan `progress.py` di server pada setiap push ke `main`, lalu bot meng-commit hasilnya |
| **Rafa** | Mengerjakan ujian, menyetujui entri, memastikan file bukti sudah di-push, dan mengunggah ulang file state ke Project |

Mentor dan Work tidak mengubah `state.yaml`, `dashboard.md`, atau `state/evidence/`, dan tidak menyatakan status naik. Hanya `progress.py` yang mengubahnya.

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

Mentor memberi langkah persis untuk jalur yang sedang dipakai Rafa (Jalur A atau B di bawah), termasuk nama berkas entri `state/inbox/<tanggal>-<modul>.yaml`. Mentor sendiri tidak melakukan commit.

## Langkah milestone

Syarat untuk kedua jalur: **file bukti** (notebook, gambar, dan sebagainya) sudah ada di repo. Setiap path di `bukti:` harus nyata, kalau tidak entri ditolak.

### Jalur A: otomatis lewat inbox (default)

1. Rafa meng-commit dan push file bukti ke `main`.
2. Evidence Entry ditaruh di `state/inbox/<tanggal>-<modul>.yaml` pada branch `main`. Pelakunya Rafa sendiri atau ChatGPT Work (contoh perintah ada di `docs/panduan_chatgpt_project.md`). Hanya file entri itu yang boleh ditambahkan.
3. Push ke `main` memicu workflow `progres`. Ia menjalankan tes, `progress.py inbox`, dan `progress.py check`, lalu bot meng-commit `state.yaml`, `dashboard.md`, dan `state/evidence/`.
4. Di GitHub, run hijau berarti entri diterima. Run merah berarti ada yang ditolak: alasannya ada di `state/inbox/ditolak/<nama>.alasan.txt`. Perbaiki entrinya bersama mentor lalu kirim ulang dengan `id` baru.
5. Rafa menjalankan `git pull`, lalu **mengganti dua file di ChatGPT Project**: hapus versi lama `state.yaml` dan `dashboard.md`, unggah versi baru. Tanpa langkah ini mentor masih membaca state lama.

Selalu `git pull` sebelum bekerja di komputer lokal, karena bot menambahkan commit di `main`.

### Jalur B: manual di komputer (cadangan)

Simpan Evidence Entry ke berkas di akar repo, misalnya `entri.yaml` (nama `entri*.yaml` di akar repo diabaikan git; salinan resminya otomatis dibuat di `state/evidence/`). Di PowerShell dari folder repo:

```powershell
git pull
python tools\progress.py apply entri.yaml --dry    # simulasi, tidak mengubah file
python tools\progress.py apply entri.yaml          # terapkan
python tools\progress.py check                     # pastikan state konsisten
git add -A
git commit -m "docs: validasi <nama modul>"
git push
```

Lalu ganti dua file di ChatGPT Project seperti langkah 5 Jalur A.

### Jika entri ditolak

Pesan galat menyebut aturan mana yang dilanggar. Perbaiki entrinya bersama mentor; jangan mengedit `state.yaml` manual untuk menyiasatinya. Penyuntingan langsung `state.yaml` akan membuat run GitHub merah (tes dan `check` gagal).

## Alur singkat

```text
Belajar → ujian → mentor usul Evidence Entry
  Jalur A: push bukti → entri ke state/inbox/ → workflow GitHub menerapkan → git pull
  Jalur B: Rafa jalankan apply → check → commit + push
→ ganti state.yaml & dashboard.md di Project → lanjut
```
