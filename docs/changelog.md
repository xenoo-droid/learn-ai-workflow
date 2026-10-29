# Changelog

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
