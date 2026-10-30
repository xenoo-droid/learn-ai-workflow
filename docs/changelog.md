# Changelog

## 2026-10-30 (Salin Dashboard)

- Menambahkan `Salin Dashboard.bat` dan `tools/salin_dashboard.py`. Bila mentor tidak bisa membuka state dari GitHub (gagal, terpotong, atau cache lama), satu klik menyalin isi `state/dashboard.md` dan konsep lemah (bila ada) dari repo lokal ke clipboard untuk ditempel ke mentor. Script hanya membaca dan memberi peringatan bila ada commit yang belum di-push
- `system/04` aturan awal sesi nomor 4 dan `system/07` (`cek progres`) kini meminta Rafa memakai Salin Dashboard; panduan save progres dan `tools/README.md` diperbarui; tes baru `tests/test_salin_dashboard.py`

## 2026-10-30 (penguatan validasi, notebook, dataset, dan roadmap World 2)

Disetujui Rafa pada 2026-10-30. Pengingat review otomatis diusulkan tetapi **tidak** dipakai, atas keputusan Rafa.

- **Evidence Entry lebih ketat** (`system/03_rubrik_validasi.md` v1.1, `system/04_protokol_mentor.md` v2.1, `system/07_alur_kerja_command.md` v2.1):
  - `cakupan` wajib untuk validasi quest aktif dan retrieval, lalu dicocokkan `progress.py` dengan item *Wajib* di kurikulum. Validasi quest materi harus mencakup semuanya. Modul review menyebut id quest yang dipakai (minimal "≥N" di kurikulum). Ini mencegah kejadian seperti koreksi cakupan Seaborn 2026-10-29
  - `ujian` merekam setiap soal (level, pertanyaan, skor) dan challenge. Jumlah soal dan level diperiksa, lalu skor gabungan dihitung ulang dan harus sama dengan `skor_persen` (toleransi 1 poin)
  - `kesalahan` / `teratasi` (opsional) mengisi `konsep_lemah` per modul di `state.yaml`, juga saat ujian tidak lulus. Retrieval review mengutamakan konsep ini
  - Entri lama di `state/evidence/` tidak diperiksa ulang. Modul legacy yang naik karena bukti lama dan Portfolio tidak wajib mengisi kolom baru
- **Notebook bukti harus bisa dijalankan ulang**: `tools/cek_notebook.py` menjalankan notebook di `bukti:` pada salinan sementara. `simpan.py` memakainya sebelum menyimpan (opsi `--tanpa-cek-notebook`; dilewati bila `nbclient` belum terpasang). Workflow baru `.github/workflows/notebook.yml` mewajibkan entri format baru lolos dan hanya melaporkan entri lama. Dependensinya di `requirements-notebook.txt`
  - Temuan saat pertama dijalankan: `notebooks/2_data_science/seaborn/latihan.ipynb` (bukti Seaborn Distribution) membaca `data_mahasiswa.csv` yang tidak ada di repo. Statusnya tidak berubah; file datanya perlu ditambahkan di samping notebook
- **Roadmap v2, World 2**: dua modul baru sebelum Portfolio #1. **Statistika Terapan untuk Analisis** (`stat_terapan_deskriptif`, `stat_terapan_inferensi`) ditempatkan setelah SQL. **Data Storytelling & Komunikasi Insight** (`story_struktur_insight`, `story_visual_penjelas`) ditempatkan setelah AI untuk Pekerjaan Data. Keempat quest ditambahkan ke `state.yaml` secara manual dengan status `belum`; progres yang ada tidak berubah, dan quest aktif tetap Categorical Plots. Bagian "Portfolio Lock" (sebelumnya menyebut "Portfolio World 1") dan "Review Queue" di roadmap diselaraskan dengan sistem sekarang
- Usulan BI tools, Excel lanjutan, Streamlit untuk analitik, dan Git kolaboratif **tidak** masuk Roadmap v2. Usulan ini dicatat di `docs/usulan_advanced_data_analyst.md` untuk sistem kedua
- **Kurikulum v1.1**: rincian keempat quest baru; uji hipotesis dihapus dari daftar celah karena sudah masuk. Redaksi tiga baris *Wajib* dirapikan supaya bisa dipecah script tanpa mengubah isinya (`gf_prompting_rag_ft`, `mcp`, dan `COUNT(DISTINCT ...)` di `sql_groupby_agg`). Ditambah penjelasan cara item dipecah
- **Penyajian materi v1.1**: checklist kualitas sesi berisi 5 butir yang bisa dipakai Rafa untuk meminta perbaikan materi
- **Dokumen**: `docs/portfolio.md` ditulis ulang mengikuti penomoran World Roadmap v2, tanpa angka progres manual (status dibaca dari state). `docs/sumber-belajar.md` disusun per World dan dirujukkan ke kebijakan referensi; tautan baru dicek 2026-10-30
- **Bank dataset sintetis** di `assets/data/`: 7 CSV dan 1 basis data SQLite, dibuat ulang dengan `tools/buat_dataset.py` (seed tetap). Katalognya di `assets/data/README.md`, untuk challenge L3, retrieval di konteks baru, dan bukti Mastered
- **`progress.py`**: perintah baru `cakupan <id>` (daftar item siap salin) dan `statistik` (tren skor, rata-rata per jenis/mode, percobaan per modul, konsep lemah)
- **Tes**: `tests/test_rekaman_ujian.py`, `tests/test_cek_notebook.py`, `tests/test_konsistensi.py` (kurikulum terbaca, paket Project sinkron, tautan dan path di dokumen ada, portfolio di World yang benar, katalog dataset lengkap); potongan kurikulum beku di `tests/fixtures/system/`
- Konstitusi dan format dashboard tidak diubah; dashboard hanya mendapat baris untuk modul baru

## 2026-10-29 (kurikulum semua World)

- Menambahkan `system/09_kurikulum.md`: setiap modul roadmap dirinci menjadi quest beserta fungsi/konsep wajib dan fokus ujian (102 quest/modul). Roadmap v2 tidak diubah; kurikulum merinci isinya
- Seaborn disusun ulang mengikuti API reference resmi: Distribution (lulus) → Categorical (aktif) → Relational → Regression → Matrix → Multi-plot Grids → Aesthetics & Palettes → Review. Quest yang belum dimulai diganti nama; status yang ada tidak berubah
- Modul World 3–6 dipecah menjadi quest di `state.yaml` sesuai kurikulum. Modul yang sudah selesai (World 1, NumPy, Pandas, Matplotlib) tidak diubah; rinciannya menjadi cakupan retrieval review
- Aturan: ujian validasi quest wajib mencakup semua item *Wajib*-nya (`system/04`, `system/08`); konstitusi mendapat rujukan ke kurikulum
- `bangun_paket.py` kini membuat 4 file (tambahan `09_kurikulum.md`); tes baru memastikan id di `state.yaml` dan kurikulum selalu sama
- Celah yang ditemukan (window functions/CTE SQL, time series Pandas, uji hipotesis) dicatat di akhir kurikulum, belum masuk wajib

## 2026-10-29 (koreksi cakupan Seaborn)

- Entri `2026-10-29-seaborn-distribution-plots` (skor 86) ditulis untuk modul `seaborn` utuh, padahal ujiannya hanya distribution plots; akibatnya seluruh Seaborn tercatat validated dan quest aktif melompat ke Jupyter/Colab
- Dengan persetujuan Rafa, Seaborn dipecah menjadi quest sesuai roadmap: Pengenalan & Distribution Plots (validated, skor 86 tetap tercatat), Categorical Plots (aktif), Relationship Plots, Heatmap, Pairplot, Seaborn Review. Pencapaian tidak dihapus, hanya dipindah ke cakupan yang benar
- Jupyter/Colab, SQL & Database Fundamentals, dan AI untuk Pekerjaan Data juga dipecah menjadi quest sesuai daftar materi di roadmap (isi roadmap tidak berubah)
- `progress.py` menolak entri yang memakai id modul induk ber-quest dengan pesan yang menyebut id quest yang sah; perbaikan tampilan dashboard untuk modul ber-quest yang belum dimulai; tes baru di `tests/test_progress.py`
- `system/04`: kolom `modul` wajib id quest yang benar-benar diuji

## 2026-10-27 (aturan penyajian materi)

- Menambahkan `system/08_penyajian_materi.md`: porsi 2–3 subtopik terkait per sesi, struktur tetap per subtopik (apa dan kenapa, sintaks, contoh dasar, parameter penting, contoh realistis, kesalahan umum, kapan dipakai), minimal dua contoh kode beserta output, penutup berisi ringkasan, hubungan dengan materi lama, cek pemahaman, dan sumber
- Aturan riset sebelum materi dipindah dari `system/04` ke `system/08`; laporan celah roadmap dibatasi maksimal 3 poin di akhir sesi
- `system/08` ikut digabung ke `aturan_mentor.md` oleh `bangun_paket.py`; konstitusi mendapat satu baris rujukan di tabel pemisahan tanggung jawab

## 2026-10-27 (save progres tanpa upload)

- Mentor kini membuka `state/dashboard.md` dan `state/state.yaml` langsung dari GitHub (diuji 2026-10-27), jadi tidak ada lagi file progres yang diunggah ulang ke ChatGPT Project setelah setiap milestone
- Menambahkan `Simpan Progres.bat` di akar repo: salin entri dari mentor, lalu klik dua kali; tidak perlu membuka terminal
- `simpan.py` tidak lagi membuka folder unggahan (opsi `--buka` bila perlu); opsi `--varian` dihapus
- `bangun_paket.py` kini membuat 3 file aturan saja (tanpa `state.yaml` dan `dashboard.md`)
- Memperbarui `system/04`, `system/05`, `system/07`, `docs/panduan_chatgpt_project.md`, `docs/panduan_save_progres.md`, `tools/README.md`, `README.md`; `.bat` dijaga berakhir CRLF lewat `.gitattributes`
- Rubrik, konstitusi, dan roadmap tidak diubah

## 2026-10-23 (simpan progres satu perintah)

- Menambahkan `tools/simpan.py`: salin Evidence Entry dari mentor lalu jalankan satu perintah. Script melakukan pull, simulasi rubrik, penerapan, `check` (dipulihkan bila gagal), satu commit berisi bukti + state, push, dan membangun ulang `paket_project/`
- Tidak perlu lagi push bukti lebih dulu, membuat berkas di `state/inbox/`, menunggu bot, atau `git pull` setelahnya; satu-satunya langkah manual yang tersisa adalah mengganti `state.yaml` dan `dashboard.md` di ChatGPT Project
- Alur inbox dan workflow GitHub tetap ada: workflow menjadi pengaman (tes + `check`), dan inbox dipakai oleh ChatGPT Work
- Memperbarui `system/04`, `system/07`, `tools/README.md`, `README.md`, dan `docs/panduan_chatgpt_project.md`; menambahkan `tests/test_simpan.py`
- Rubrik, konstitusi, dan roadmap tidak diubah

## 2026-10-22 (otomatisasi progres)

- Menambahkan `state/inbox/` dan perintah `progress.py inbox`: entri bukti ditaruh di inbox, lalu diterapkan otomatis
- Menambahkan workflow `.github/workflows/progres.yml`: pada setiap push ke `main` menjalankan tes, memproses inbox, memeriksa konsistensi state, dan bot meng-commit hasilnya (zona waktu WIB)
- Memperketat pemeriksaan entri: `id` aman dan unik, file di `bukti` harus ada di repo, batas ukuran berkas, isi YAML wajib valid
- Memindahkan data tes ke `tests/fixtures/state/` agar tes tidak patah ketika `state.yaml` asli maju
- Memperbarui `system/04`, `system/07`, dan `docs/panduan_chatgpt_project.md` (Jalur A otomatis, Jalur B manual, prompt untuk ChatGPT Work)
- Matplotlib Review divalidasi (skor 88, mode review) sebagai milestone pertama dengan alur baru

## 2026-10-22 (reboot sistem)

- Membangun ulang sistem belajar: file di repo menjadi sumber kebenaran progres, ChatGPT Project menjadi ruang mentor
- Menambahkan `state/state.yaml` sebagai sumber kebenaran progres, dengan `state/evidence/` untuk bukti dan `state/dashboard.md` yang dihasilkan otomatis
- Menambahkan `tools/progress.py` (check, dashboard, due, learned, apply) beserta tes otomatis di `tests/`
- Menetapkan lima status progres (Learned, Validated, Retained, Mastered, Validated (legacy)) dan rubrik validasi dengan ambang 80%
- Semua progres sebelumnya dipertahankan; modul tanpa bukti terdokumentasi diberi status Validated (legacy), bukan dihapus
- Menyusun dokumen sistem berbahasa Indonesia di `system/` (konstitusi, rubrik, protokol mentor, spesifikasi dashboard, alur command) dan memindahkan roadmap v2 serta kebijakan referensi ke sana tanpa mengubah isinya
- Memindahkan dokumen progres tulisan tangan yang usang ke `archive/progres-lama/`
- Menambahkan `docs/panduan_chatgpt_project.md` dan menulis ulang `README.md`
- Menambahkan pola rahasia dan kode pemulihan ke `.gitignore`
- Tidak mengubah isi Roadmap v2

## 2026-10-22

- Added `docs/learning-references.md` to define source priorities for learning materials
- Clarified that official documentation is primary, quality tutorials are supplementary, and academic papers/journals are used when relevant rather than required for every lesson
- Required lesson records to distinguish sources actually consulted from recommended further reading
- Explicitly prohibited invented or unverified historical references
- Confirmed that this policy does not alter the Roadmap v2 or validated learning progress

## 2026-08-22

- Adopted Roadmap v2 as the project single source of truth
- Preserved all validated learning progress
- Advanced current learning state to Matplotlib → Figure & Axes (`fig`, `ax/axes`)
- Preserved Portfolio World 1 lock until Phase 2 reaches 100%

## 2026-08-20

- Completed Pandas → Import / Export with validated exercises and mini challenge
- Completed Pandas → Pandas Capstone with validated score 220/220
- Recorded Pandas Capstone as a completed milestone and achievement
- Advanced current state beyond Pandas Capstone; next quest not yet set

## 2026-08-18

- Completed Pandas → Statistics with 250/250
- Marked mean(), sum(), count(), min(), max(), median(), mode(), std(), and value_counts() as completed
- Recorded Pandas Statistics as a completed milestone and achievement
- Advanced current quest to Pandas → GroupBy
- Set next quest to Pandas → Merge & Join

## 2026-08-17

- Saved validated learning progress checkpoint
- Recorded current position at Pandas → Statistics → `mean()`
- Recorded completed Pandas submodules and completed Review Queue
- Preserved Portfolio World 1 lock until Phase 2 reaches 100%

## 2026-08-08

- Initialized the repository
- Added the main roadmap document
- Upgraded the README with project overview
- Added the AI workflow save file
