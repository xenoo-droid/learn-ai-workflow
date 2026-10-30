# 🏗️ Portfolio Roadmap

> Setiap proyek portofolio menutup satu World di Roadmap v2 (`system/02_roadmap.md`) dan menjadi bukti kemampuan yang bisa dilihat orang lain.

Dokumen ini hanya menjelaskan **isi** setiap proyek. **Status** proyek (terkunci, aktif, validated) tidak ditulis di sini, karena sumber kebenarannya `state/state.yaml` dan tampilannya `state/dashboard.md`. Sebuah portfolio terbuka otomatis setelah semua modul non-opsional di World-nya selesai, dan divalidasi dengan rubrik portfolio di `system/03_rubrik_validasi.md` bagian 2. Rincian wajibnya ada di `system/09_kurikulum.md`.

Proyek final disimpan di `projects/<nama-proyek>/` (lihat `projects/README.md`).

---

# 🌍 WORLD 2 — DATA SCIENCE & DATA ANALYTICS

## 📊 Portfolio #1: Data Analysis Report (`portfolio_1`)

Prasyarat: semua modul non-opsional World 2, termasuk Statistika Terapan dan Data Storytelling.

- [ ] Pilih dataset publik dan rumuskan pertanyaan bisnis
- [ ] Data cleaning (keputusan cleaning dicatat)
- [ ] Exploratory Data Analysis
- [ ] Ringkasan statistik dan, bila relevan, uji perbedaan kelompok
- [ ] Visualisasi (Matplotlib/Seaborn) dengan judul berbentuk insight
- [ ] Insight dan rekomendasi
- [ ] Notebook rapi yang bisa dijalankan ulang
- [ ] README: masalah, keputusan, keterbatasan
- [ ] Publikasi di GitHub

---

# 🌍 WORLD 3 — MATHEMATICS & STATISTICS FOR DATA/AI

## 📈 Portfolio: Notebook Eksplorasi Matematika/Statistika (`portfolio_math`)

Cukup satu notebook dengan penjelasan dan visualisasi, misalnya:

- [ ] Gradient descent dari nol dengan NumPy, atau
- [ ] Simulasi distribusi dan Central Limit Theorem, atau
- [ ] Demonstrasi teorema Bayes

---

# 🌍 WORLD 4 — MACHINE LEARNING FUNDAMENTAL

## 🤖 Portfolio #2: Prediction / Classification Model (`portfolio_2`)

- [ ] Problem dan dataset
- [ ] Preprocessing dan feature engineering
- [ ] Training beberapa model dengan `Pipeline`
- [ ] Evaluasi dengan metrik yang tepat dan cross-validation
- [ ] Interpretasi hasil
- [ ] Notebook, source code rapi di `src/`, model tersimpan
- [ ] README dan publikasi di GitHub

---

# 🌍 WORLD 5 — DEEP LEARNING & NEURAL NETWORK

## 🧠 Portfolio #3: Image / Text Classifier (`portfolio_3`)

- [ ] Dataset
- [ ] Model pretrained / transfer learning
- [ ] Training dan evaluasi
- [ ] README dan publikasi di GitHub

---

# 🌍 WORLD 6 — GENERATIVE AI & AI-ENHANCED DATA WORKFLOW

## 💬 Proyek RAG: RAG-based Q&A System (bagian dari quest `rag_pipeline`)

Bukan portfolio terpisah di `state.yaml`; proyek ini adalah bukti quest `rag_pipeline` dan bisa ditampilkan sebagai portofolio.

- [ ] Document loader dan chunking
- [ ] Embedding dan vector database (FAISS atau Chroma)
- [ ] Retrieval pipeline
- [ ] Integrasi LLM
- [ ] Antarmuka sederhana (misalnya Streamlit)
- [ ] README dan publikasi di GitHub

## 👑 Capstone: AI-Enhanced Data Workflow (`capstone`)

- [ ] Aplikasi/workflow yang berjalan
- [ ] README profesional dan diagram arsitektur
- [ ] Contoh evaluasi dan failure cases
- [ ] Demo
- [ ] Repo GitHub

---

# 🚀 Urutan

```text
📊 Portfolio #1: Data Analysis Report          (World 2)
        │
        ▼
📈 Notebook Eksplorasi Matematika/Statistika    (World 3)
        │
        ▼
🤖 Portfolio #2: Prediction / Classification    (World 4)
        │
        ▼
🧠 Portfolio #3: Image / Text Classifier        (World 5)
        │
        ▼
💬 RAG Q&A System → 👑 Capstone                 (World 6)
```

---

# 📝 Standar semua proyek

- README yang jelas: masalah, data, keputusan, hasil, keterbatasan
- Source code yang rapi
- Dokumentasi proses
- Hasil evaluasi
- Lesson learned

XP, rank, dan achievements belum dipakai; sistem itu akan dirancang ulang dari state (lihat `system/05_spesifikasi_dashboard.md`, bagian "Belum termasuk").
