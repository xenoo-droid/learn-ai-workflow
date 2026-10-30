# 📓 Notebooks

Notebook belajar dan latihan selama perjalanan Learn AI Workflow, disusun per World lalu per modul sesuai Roadmap v2 (`system/02_roadmap.md`).

## Struktur

```text
notebooks/
├── 1_python_foundation/        World 1: Python Foundation
│   ├── 00_Review Queue.ipynb     Review Queue (Error Handling, File I/O, venv & pip)
│   └── 01–06_Python_Dasar_Part_*.ipynb
├── 2_data_science/             World 2: Data Science & Data Analytics
│   ├── numpy/                    materi, latihan, review, NumPy Capstone + file data (.npy, .txt)
│   ├── pandas/                   materi 1–6, latihan, 👑 Pandas Capstone + file data (.csv, .json, .xlsx)
│   ├── matplotlib/               materi, latihan, Answer.md + gambar hasil
│   └── seaborn/                  materi dan latihan (quest aktif)
└── matplotlib_review/          Bukti validasi Matplotlib Review (dirujuk oleh state/evidence/, jangan dipindah)
```

## Aturan

- File data disimpan **di samping notebook yang memakainya**, supaya notebook bisa dijalankan ulang tanpa mengubah path.
- Notebook bukti harus lolos *Restart & Run All*: `tools/cek_notebook.py` menjalankannya ulang saat Simpan Progres dan di GitHub. Sel yang sengaja error diberi tag `raises-exception`.
- Butuh dataset baru untuk challenge atau review? Salin dari bank dataset di `assets/data/` (katalog di `assets/data/README.md`).
- Notebook baru masuk ke folder World dan modulnya, misalnya `2_data_science/seaborn/`.
- Jangan memindahkan atau mengganti nama notebook yang sudah dirujuk di `bukti:` sebuah Evidence Entry (lihat `state/evidence/`), karena path-nya harus tetap ada.
- Jika notebook sudah menjadi project final, pindahkan ke folder `projects/`.
- `.ipynb_checkpoints/` tidak di-commit (diabaikan `.gitignore`).

## Catatan

Notebook di `1_python_foundation/` dan `2_data_science/` (kecuali `seaborn/`) berasal dari masa sebelum rubrik validasi ada. Modulnya berstatus Validated (legacy) di `state/state.yaml`. Notebook ini bisa dijadikan bukti untuk menaikkan modul legacy menjadi Validated (lihat `system/03_rubrik_validasi.md` bagian 7).
