# Changelog

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
