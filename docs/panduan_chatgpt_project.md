# Panduan ChatGPT Project

Panduan menyiapkan ChatGPT Project sebagai ruang mentor, dengan repo ini sebagai sumber kebenaran.

## Fakta yang membentuk rancangan

- ChatGPT Project membaca file lewat **retrieval teks**: mengambil potongan yang relevan, bukan membaca semuanya. Banyak file yang mirip membuat potongan saling berebut masuk ke jawaban.
- Batas jumlah file per project: 5 (Free), 25 (Plus/Go), 40 (Pro/Business/Edu/Enterprise). Sumber: [OpenAI Help Center, Projects in ChatGPT](https://help.openai.com/en/articles/8555545-projects-in-chatgpt).
- Karena itu pack dibuat kecil, satu topik per file, tanpa duplikat, tanpa arsip. Ada dua varian sesuai paket langganan (lihat bawah).
- Percakapan lama di dalam Project bukan file dan tidak dihitung ke batas file. Per 2026-10-22 diuji: `cek progres` tetap membaca `state.yaml`, bukan percakapan lama. Teks instruksi sengaja menyatakan bahwa `state.yaml` menang atas percakapan lama.

## Pilih varian

| Varian | Kapan | Jumlah file |
|---|---|---|
| **A. Paket 5 file** | Paket Free | 5 |
| **B. Paket 9 file** | Plus/Go atau lebih | 9 |

Jangan unggah `archive/`, `notebooks/`, atau `docs/` di varian mana pun.

## Varian A: paket 5 file (Free)

Dari folder repo, jalankan:

```powershell
python tools\bangun_paket.py
```

Skrip membuat folder `paket_project/` (diabaikan git; hanya turunan) berisi:

| # | File | Isi |
|---|---|---|
| 1 | `aturan_mentor.md` | Gabungan otomatis: konstitusi, protokol mentor, alur command, spesifikasi dashboard, kebijakan referensi |
| 2 | `02_roadmap.md` | Materi dan urutan |
| 3 | `03_rubrik_validasi.md` | Syarat naik status |
| 4 | `state.yaml` | **Progres terkini** |
| 5 | `dashboard.md` | **Tampilan progres terkini** |

Unggah kelimanya dari `paket_project/`. Jangan menyimpan `aturan_mentor.md` di dalam folder `system/`, supaya tidak ada dua versi aturan di repo.

Teks instruksi Project (tempel di Tingkat lanjut / Instruksi):

```text
Kamu mentor belajar Rafa untuk "Learn A.I Workflow for Data Science" (target: Data Scientist/Data Analyst yang AI-native). Bahasa: Indonesia.

Sumber kebenaran adalah file di Project ini, bukan ingatanmu dan bukan percakapan lama di Project ini. Urutan otoritas: aturan_mentor.md (bagian Konstitusi) > 02_roadmap.md > state.yaml. Jika percakapan lama bertentangan dengan state.yaml, state.yaml yang benar.

Di awal setiap sesi baca state.yaml dan dashboard.md. Jangan pernah menyatakan progres dari ingatan percakapan. Jika file tidak ketemu atau terpotong, katakan dan minta Rafa menempelkan isinya. Jangan menebak.

Kamu hanya MENGUSULKAN perubahan progres lewat Evidence Entry (format di bagian Protokol Mentor, aturan_mentor.md; syarat naik status di 03_rubrik_validasi.md). Jangan menyatakan status naik; perubahan status hanya dilakukan tools/progress.py (otomatis lewat state/inbox/ atau dijalankan Rafa). Saat menyerahkan entri, sebut nama berkas state/inbox/<tanggal>-<modul>.yaml dan ingatkan bahwa file bukti harus sudah ada di repo.

Untuk "cek progres": tampilkan isi dashboard.md apa adanya dalam blok kode, jangan membuat atau mengubah format dashboard.

Command: cek progres, lanjut, review, latihan, save, prepare commit, commit progres (arti di bagian Alur Kerja dan Command, aturan_mentor.md). Sesi "latihan": 3–5 soal + 1 challenge, tanpa petunjuk sebelum Rafa mencoba. Sebelum materi baru: riset, bandingkan dengan roadmap, laporkan celah (Protokol Mentor).
```

## Varian B: paket 9 file (Plus/Go atau lebih)

| # | File | Fungsi |
|---|---|---|
| 1 | `system/01_constitution.md` | Aturan tertinggi |
| 2 | `system/02_roadmap.md` | Materi dan urutan |
| 3 | `system/03_rubrik_validasi.md` | Syarat naik status |
| 4 | `system/04_protokol_mentor.md` | Cara mentor bekerja |
| 5 | `system/05_spesifikasi_dashboard.md` | Aturan tampilan |
| 6 | `system/06_kebijakan_referensi.md` | Sumber belajar yang dipercaya |
| 7 | `system/07_alur_kerja_command.md` | Arti command dan alur commit |
| 8 | `state/state.yaml` | **Progres terkini** |
| 9 | `state/dashboard.md` | **Tampilan progres terkini** |

Teks instruksi Project:

```text
Kamu mentor belajar Rafa untuk "Learn A.I Workflow for Data Science" (target: Data Scientist/Data Analyst yang AI-native). Bahasa: Indonesia.

Sumber kebenaran adalah file di Project ini, bukan ingatanmu dan bukan percakapan lama di Project ini. Urutan otoritas: 01_constitution > 02_roadmap > state.yaml > evidence. Jika percakapan lama bertentangan dengan state.yaml, state.yaml yang benar.

Di awal setiap sesi baca state.yaml dan dashboard.md. Jangan pernah menyatakan progres dari ingatan percakapan. Jika file tidak ketemu atau terpotong, katakan dan minta Rafa menempelkan isinya. Jangan menebak.

Kamu hanya MENGUSULKAN perubahan progres lewat Evidence Entry (format di 04_protokol_mentor.md). Jangan menyatakan status naik; perubahan status hanya dilakukan tools/progress.py (otomatis lewat state/inbox/ atau dijalankan Rafa). Saat menyerahkan entri, sebut nama berkas state/inbox/<tanggal>-<modul>.yaml dan ingatkan bahwa file bukti harus sudah ada di repo.

Untuk "cek progres": tampilkan isi dashboard.md apa adanya dalam blok kode, jangan membuat atau mengubah format dashboard.

Command: cek progres, lanjut, review, latihan, save, prepare commit, commit progres (arti di 07_alur_kerja_command.md). Sesi "latihan": 3–5 soal + 1 challenge, tanpa petunjuk sebelum Rafa mencoba. Sebelum materi baru: riset, bandingkan dengan roadmap, laporkan celah (04).
```

## Mengirim Evidence Entry lewat ChatGPT Work

Work boleh menulis ke repo, tetapi hanya untuk menaruh satu file entri di `state/inbox/`. Workflow GitHub yang menerapkannya (lihat `state/inbox/README.md`). Prompt untuk Work, ganti bagian dalam kurung:

```text
Repo: xenoo-droid/learn-ai-workflow, branch main.
Buat satu file baru state/inbox/<tanggal>-<modul>.yaml berisi teks YAML di bawah ini persis apa adanya, lalu commit langsung ke main dengan pesan "inbox: <modul>".
Jangan membuat, mengubah, atau menghapus file lain. Terutama jangan menyentuh state/state.yaml, state/dashboard.md, dan state/evidence/.
Setelah commit, berhenti dan laporkan nama commit-nya.

<tempel Evidence Entry di sini>
```

Sebelumnya pastikan file bukti (notebook, gambar) sudah di-commit dan di-push, kalau tidak entri ditolak. Hasilnya bisa dilihat di tab Actions di GitHub: hijau berarti diterima, merah berarti ditolak (alasannya di `state/inbox/ditolak/`).

## Sinkronisasi setelah setiap milestone

File yang berubah tiap milestone hanya dua: `state.yaml` dan `dashboard.md`. Sisanya jarang berubah.

1. Terapkan entri lewat alur di `system/07_alur_kerja_command.md` (Jalur A otomatis, atau Jalur B manual), lalu `git pull` supaya komputermu memuat commit bot.
2. Varian A: jalankan `python tools\bangun_paket.py`, lalu ambil `state.yaml` dan `dashboard.md` dari `paket_project/`. Varian B: ambil keduanya dari folder `state/`.
3. Di Project, **hapus** `state.yaml` dan `dashboard.md` lama, lalu **unggah** versi baru.

Jika `system/` yang berubah (jarang), varian A perlu mengganti juga `aturan_mentor.md`, `02_roadmap.md`, dan `03_rubrik_validasi.md`; varian B mengganti file `system/` yang berubah.

Tanpa langkah 3, mentor masih membaca state lama. Aku belum bisa memastikan apakah ChatGPT bisa menyinkronkan Project langsung dari GitHub, jadi alur ini sengaja manual.

## Tips supaya RAG bekerja baik

- Sebut nama file saat bertanya, misalnya "baca `state.yaml` lalu tampilkan quest aktifku".
- Jika jawaban mentor tidak menyebut isi state, minta: "baca `state.yaml` dulu".
- Jangan mengunggah dua versi file yang sama; retrieval bisa mengambil yang lama.
- Jika menambah dokumen sistem baru, pastikan satu topik per file dan beri judul yang jelas. Di varian A, daftarkan dokumen baru ke `GABUNG` di `tools/bangun_paket.py`.
- Jika ragu mentor membaca file yang benar, tempel isi `state.yaml` langsung ke chat.
