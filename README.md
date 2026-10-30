# 🚀 Learn AI Workflow

> Sistem belajar mandiri untuk menjadi **Data Scientist / Data Analyst yang AI-native**: kuat di fondasi data, dengan AI sebagai pengganda kemampuan.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Roadmap](https://img.shields.io/badge/Roadmap-v2-purple.svg)](system/02_roadmap.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📍 Status saat ini

Lihat dashboard yang dihasilkan otomatis dari state: [`state/dashboard.md`](state/dashboard.md).

## 📖 Tentang

Repositori ini adalah **sumber kebenaran** sebuah sistem belajar yang dijalankan bersama mentor AI (ChatGPT Project). Mentor mengajar dan menguji. Progres dicatat di file, bukan di ingatan AI, dan hanya berubah lewat bukti yang lolos pemeriksaan script.

## ⚙️ Cara kerja

```text
Belajar & ujian bersama mentor AI
        ↓
Mentor mengusulkan Evidence Entry (bukti: cakupan, rekaman ujian, notebook)
        ↓
tools/progress.py memeriksa terhadap rubrik dan kurikulum; notebook dijalankan ulang
        ↓
state/state.yaml diperbarui + dashboard dibuat otomatis
        ↓
Commit + push ke GitHub → mentor membaca state terbaru langsung dari GitHub
```

Prinsipnya: **bukti → validasi → pembaruan progres → umpan balik → baru lanjut**.

## 🌳 Roadmap

Enam World, mengikuti Roadmap v2 di [`system/02_roadmap.md`](system/02_roadmap.md):

1. Python Foundation
2. Data Science & Data Analytics
3. Mathematics & Statistics for Data/AI
4. Machine Learning Fundamental
5. Deep Learning & Neural Network
6. Generative AI & AI-Enhanced Data Workflow

## 🏅 Lima status progres

Learned → Validated → Retained → Mastered, ditambah Validated (legacy) untuk modul yang selesai sebelum rubrik ada. Syaratnya ada di [`system/03_rubrik_validasi.md`](system/03_rubrik_validasi.md).

## 📂 Struktur repositori

```text
learn-ai-workflow/
├── README.md
├── system/        aturan sistem (dimuat ke ChatGPT Project)
├── state/         state.yaml · dashboard.md · evidence/
├── tools/         progress.py (penjaga aturan progres) · simpan.py · cek_notebook.py · buat_dataset.py
├── tests/         tes otomatis untuk tools/ dan konsistensi dokumen
├── notebooks/     notebook belajar
├── projects/      proyek portofolio
├── src/           kode pendukung proyek
├── assets/        bank dataset latihan (assets/data/), gambar, diagram
├── docs/          changelog, portofolio, sumber belajar, panduan ChatGPT Project
└── archive/       dokumen lama (hanya untuk riwayat)
```

## 🛠️ Cara memakai

Kebutuhan: Python 3.9+ dan PyYAML.

```powershell
pip install -r requirements.txt
python tools\simpan.py                # simpan progres (atau klik dua kali "Simpan Progres.bat")
python tools\salin_dashboard.py       # salin dashboard untuk mentor bila GitHub cache (atau "Salin Dashboard.bat")
python tools\progress.py check        # periksa konsistensi state
python tools\progress.py dashboard    # tampilkan dashboard
python tools\progress.py due          # review yang jatuh tempo
python tools\progress.py statistik    # tren skor dan konsep lemah
python tools\cek_notebook.py          # jalankan ulang notebook bukti (pip install -r requirements-notebook.txt)
python -m unittest discover -s tests  # jalankan tes
```

Alur lengkap dari ujian sampai commit ada di [`system/07_alur_kerja_command.md`](system/07_alur_kerja_command.md). Cara menyiapkan ChatGPT Project ada di [`docs/panduan_chatgpt_project.md`](docs/panduan_chatgpt_project.md).

## 🏗️ Portofolio

Proyek portofolio dibuka bertahap sesuai roadmap. Rinciannya di [`docs/portfolio.md`](docs/portfolio.md).

## 📜 Lisensi

MIT. Lihat [`LICENSE`](LICENSE).
