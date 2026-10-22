# Panduan ChatGPT Project

Panduan menyiapkan ChatGPT Project sebagai ruang mentor, dengan repo ini sebagai sumber kebenaran.

## Fakta yang membentuk rancangan

- ChatGPT Project membaca file lewat **retrieval teks**: mengambil potongan yang relevan, bukan membaca semuanya. Banyak file yang mirip membuat potongan saling berebut masuk ke jawaban.
- Batas jumlah file per project: 5 (Free), 25 (Plus/Go), 40 (Pro/Business/Edu/Enterprise). Sumber: [OpenAI Help Center, Projects in ChatGPT](https://help.openai.com/en/articles/8555545-projects-in-chatgpt).
- Karena itu pack dibuat kecil: **9 file**, satu topik per file, tanpa duplikat, tanpa arsip.

## 1. File yang diunggah ke Project

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

Jangan unggah `archive/`, `notebooks/`, atau `docs/`. File nomor 8 dan 9 **berubah setiap milestone**; sisanya jarang berubah.

## 2. Teks instruksi Project

Tempel ke kolom instruksi Project:

```text
Kamu mentor belajar Rafa untuk "Learn A.I Workflow for Data Science" (target: Data Scientist/Data Analyst yang AI-native). Bahasa: Indonesia.

Sumber kebenaran adalah file di Project ini, bukan ingatanmu. Urutan otoritas: 01_constitution > 02_roadmap > state.yaml > evidence.

Di awal setiap sesi baca state.yaml dan dashboard.md. Jangan pernah menyatakan progres dari ingatan percakapan. Jika file tidak ketemu atau terpotong, katakan dan minta Rafa menempelkan isinya. Jangan menebak.

Kamu hanya MENGUSULKAN perubahan progres lewat Evidence Entry (format di 04_protokol_mentor.md). Jangan menyatakan status naik; Rafa menjalankan tools/progress.py.

Untuk "cek progres": tampilkan isi dashboard.md apa adanya dalam blok kode, jangan membuat atau mengubah format dashboard.

Command: cek progres, lanjut, review, latihan, save, prepare commit, commit progres (arti di 07_alur_kerja_command.md). Sesi "latihan": 3–5 soal + 1 challenge, tanpa petunjuk sebelum Rafa mencoba. Sebelum materi baru: riset, bandingkan dengan roadmap, laporkan celah (04).
```

## 3. Sinkronisasi setelah setiap milestone

1. Jalankan alur di `system/07_alur_kerja_command.md` (apply → check → commit → push).
2. Di Project, **hapus** `state.yaml` dan `dashboard.md` lama.
3. **Unggah** versi baru dari folder `state/` di komputermu.

Tanpa langkah 2–3, mentor masih membaca state lama. Aku belum bisa memastikan apakah ChatGPT bisa menyinkronkan Project langsung dari GitHub, jadi alur ini sengaja manual.

## 4. Tips supaya RAG bekerja baik

- Sebut nama file saat bertanya, misalnya "baca `state.yaml` lalu tampilkan quest aktifku".
- Jika jawaban mentor tidak menyebut isi state, minta: "baca `state.yaml` dulu".
- Jangan mengunggah dua versi file yang sama; retrieval bisa mengambil yang lama.
- Jika menambah dokumen sistem baru, pastikan satu topik per file dan beri judul yang jelas.
- Jika ragu mentor membaca file yang benar, tempel isi `state.yaml` langsung ke chat.
