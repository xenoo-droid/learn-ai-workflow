---
dokumen: alur_kerja_command
versi: 2.1
peran: Arti setiap command dan alur dari belajar sampai commit. Dibaca mentor dan Rafa.
---

# Alur Kerja dan Command

## Pembagian peran

| Pelaku | Tugas |
|---|---|
| **Mentor AI** (ChatGPT Project) | Mengajar, menguji, memberi umpan balik, mengusulkan Evidence Entry |
| **ChatGPT Work** (bila dipakai) | Hanya menaruh file Evidence Entry di `state/inbox/` pada repo. Tidak mengubah file lain |
| **`tools/progress.py`** | Memeriksa entri terhadap rubrik, mengubah `state.yaml`, membuat dashboard, menghitung review |
| **`tools/simpan.py`** | Satu perintah untuk Rafa: ambil entri dari clipboard, periksa, terapkan lewat `progress.py`, satu commit + push, bangun ulang paket Project |
| **Workflow GitHub** (`progres.yml`) | Pengaman di server: pada setiap push ke `main` menjalankan tes dan `check`, serta memproses `state/inbox/` bila ada entri (jalur ChatGPT Work). Bot hanya meng-commit bila ada entri di inbox |
| **Rafa** | Mengerjakan ujian, menyalin entri dari mentor, lalu menjalankan **Simpan Progres** (`Simpan Progres.bat`) |

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
| `commit progres` | Ingatkan langkah menyimpan: salin entri, jalankan Simpan Progres |

### `cek progres`

1. Mentor membuka `state/dashboard.md` dan `state/state.yaml` terbaru langsung dari GitHub (alamat di `system/04_protokol_mentor.md`). Jika gagal dibuka atau masih cache lama (misalnya tanggal "Diperbarui" belum berubah padahal Rafa baru menyimpan), mentor meminta Rafa menjalankan **Salin Dashboard** (`Salin Dashboard.bat`) dan menempelkan hasilnya, lalu menampilkan dashboard dari teks itu (langkah 2). Teks itu tidak memuat jadwal review, jadi langkah 3 dilewati.
2. Menampilkan isi `dashboard.md` **apa adanya** dalam blok kode.
3. Menyebut review yang jatuh tempo berdasarkan `review_berikutnya` dan `perlu_review` di `state.yaml`. Daftar resminya: `python tools/progress.py due`.
4. Jika Rafa melaporkan kemajuan baru, mentor meminta bukti lalu mengusulkan Evidence Entry. Mentor tidak mengubah status. Jika tidak ada kemajuan, jangan mengarang kemajuan.

### `lanjut`

Melanjutkan quest di `posisi_saat_ini`. Tidak boleh melompat ke materi mendatang atau mengubah dependensi roadmap. Materi baru mengikuti `system/08_penyajian_materi.md` (2–3 subtopik terkait per sesi, struktur tetap, contoh kode beserta output).

### `review`

Menjalankan retrieval review untuk modul yang jatuh tempo: 2–3 soal tanpa catatan, di konteks baru, mode `independent`. Soal diambil dari item *Wajib* modul itu di `system/09_kurikulum.md`, dengan prioritas pada `konsep_lemah` modul itu di `state.yaml`. Modul legacy masuk antrean maksimal 2 per sesi. Hasilnya menjadi Evidence Entry berjenis `retrieval` (dengan `cakupan`, `ujian`, dan bila ada `kesalahan`/`teratasi`).

### `latihan`

Sesi berisi 3–5 soal dan 1 challenge, hanya dari materi yang sudah diajarkan. Untuk ujian validasi, ikuti `system/03_rubrik_validasi.md`.

### `save` (penyesuaian, menunggu persetujuan Rafa)

Definisi lama: menyimpan historis percakapan yang relevan dan memperbarui memori proyek, tanpa commit dan push. Karena sumber kebenaran kini file di repo dan mentor tidak bisa menulis ke repo, `save` menjadi: mentor merangkum sesi dan, bila ada milestone, menyusun Evidence Entry untuk Rafa. Tetap tanpa commit dan push.

### `prepare commit`

Hanya persiapan, tidak mengubah apa pun. Mentor memeriksa Evidence Entry:

1. Kolom lengkap dan sesuai rubrik.
2. `cakupan` memuat semua item *Wajib* quest (validasi) dan cocok dengan soal yang benar-benar diberikan.
3. `ujian` mencatat setiap soal dan challenge; `skor_persen` sama dengan hitungannya (50% rata-rata soal + 50% challenge; retrieval: rata-rata soal).
4. `keputusan` konsisten dengan skor.
5. Notebook di `bukti:` sudah disimpan di folder repo beserta file datanya, dan sudah dicoba *Restart & Run All*.

Lalu menyusun pesan commit dan menyatakan **SIAP** atau **BELUM SIAP**. Rafa bisa memeriksa sendiri tanpa mengubah apa pun dengan `python tools\simpan.py --dry`.

### `commit progres`

Mentor menyerahkan Evidence Entry sebagai satu blok kode YAML dan mengingatkan Rafa menyalinnya lalu menjalankan **Simpan Progres** (`Simpan Progres.bat`, atau `python tools\simpan.py`; jalur utama di bawah). Nama berkas `state/inbox/<tanggal>-<modul>.yaml` hanya disebut bila Rafa memakai jalur inbox (ChatGPT Work). Mentor sendiri tidak melakukan commit.

## Langkah milestone

### Jalur utama: satu perintah (`tools/simpan.py`)

1. Selesaikan ujian. Mentor menyerahkan Evidence Entry sebagai **satu blok kode YAML**.
2. Pastikan file bukti (notebook, gambar, dan sebagainya) **sudah tersimpan di folder repo** dan path-nya cocok dengan `bukti:`. Tidak perlu di-commit atau di-push lebih dulu; `simpan.py` memasukkannya ke commit yang sama.
3. Salin blok entri itu (ke clipboard), lalu **klik dua kali `Simpan Progres.bat`** (di akar repo, atau shortcut-nya di Desktop). Sama dengan menjalankan dari folder repo:

```powershell
python tools\simpan.py
```

   `simpan.py` mengerjakan, berurutan: `git pull --rebase --autostash`, simulasi rubrik, menjalankan ulang notebook di `bukti:` (bila `nbclient` terpasang; lihat `requirements-notebook.txt`), menerapkan entri, `check` (bila gagal semua perubahan dikembalikan), **satu commit** berisi file bukti dan state (file lain yang sedang kamu kerjakan tidak ikut), `git push`, lalu membangun ulang `paket_project/`.
4. Selesai. Tidak ada yang perlu diunggah ke ChatGPT Project: mentor membaca state langsung dari GitHub. Beri jeda ±5 menit sebelum `cek progres` karena cache GitHub.

Tidak perlu `git pull` sesudahnya dan tidak perlu menunggu bot: state sudah diterapkan di komputermu sebelum push. Workflow GitHub tetap berjalan sebagai pengaman (tes dan `check`).

Opsi (lewat terminal): `--dry` (periksa dan simulasi saja), `--berkas <file.yaml>` (baca dari berkas, bukan clipboard), `--tanpa-push`, `--tanpa-git`, `--tanpa-paket`, `--tanpa-cek-notebook` (lewati cek notebook; GitHub tetap mengeceknya), `--buka` (buka folder `paket_project/` setelah selesai).

**Jika notebook bukti gagal dijalankan ulang:** tidak ada file yang berubah. Biasanya file data belum disalin ke samping notebook, atau ada sel yang bergantung pada urutan eksekusi lama. Perbaiki, coba *Restart & Run All* di Jupyter, lalu jalankan lagi.

**Jika entri ditolak:** pesan menyebut aturan yang dilanggar dan tidak ada file yang berubah. Perbaiki entrinya bersama mentor lalu jalankan lagi dengan `id` baru. Jangan mengedit `state.yaml` manual untuk menyiasatinya.

**Jika push gagal, atau kamu sedang tanpa internet:** pakai `--tanpa-push` (atau biarkan gagal): progres sudah diterapkan dan di-commit di komputermu. Setelah online, jalankan `git pull --rebase` lalu `git push`; mentor baru melihat progres itu setelah push.

### Jalur inbox (ChatGPT Work, atau komputer tanpa Python)

1. File bukti harus sudah ada di repo: commit dan push dulu ke `main`. Setiap path di `bukti:` harus nyata, kalau tidak entri ditolak.
2. Evidence Entry ditaruh di `state/inbox/<tanggal>-<modul>.yaml` pada branch `main`, oleh Rafa sendiri atau ChatGPT Work (contoh perintah ada di `docs/panduan_chatgpt_project.md`). Hanya file entri itu yang boleh ditambahkan.
3. Push ke `main` memicu workflow `progres`: tes, `progress.py inbox`, dan `progress.py check`, lalu bot meng-commit `state.yaml`, `dashboard.md`, dan `state/evidence/`.
4. Di GitHub, run hijau berarti entri diterima. Run merah berarti ada yang ditolak: alasannya ada di `state/inbox/ditolak/<nama>.alasan.txt`.
5. Rafa menjalankan `git pull` supaya komputernya memuat commit bot. Mentor otomatis membaca state baru dari GitHub.

Selalu `git pull` sebelum bekerja di komputer lokal, karena bot menambahkan commit di `main` pada jalur ini.

### Jalur manual (cadangan)

Simpan Evidence Entry ke berkas di akar repo, misalnya `entri.yaml` (nama `entri*.yaml` di akar repo diabaikan git; salinan resminya otomatis dibuat di `state/evidence/`). Di PowerShell dari folder repo:

```powershell
git pull
python tools\progress.py apply entri.yaml --dry    # simulasi, tidak mengubah file
python tools\cek_notebook.py --entri entri.yaml    # jalankan ulang notebook bukti
python tools\progress.py apply entri.yaml          # terapkan
python tools\progress.py check                     # pastikan state konsisten
git add -A
git commit -m "docs: validasi <nama modul>"
git push
```

Mentor membaca state baru dari GitHub setelah push.

## Alur singkat

```text
Belajar → ujian → mentor menyerahkan Evidence Entry (satu blok YAML)
  → salin → klik dua kali Simpan Progres.bat   (periksa → terapkan → commit + push)
  → mentor membaca state terbaru dari GitHub → lanjut
```
