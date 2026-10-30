# tools/

`progress.py` adalah penjaga aturan progres. Ia satu-satunya yang mengubah `state/state.yaml` (selain Rafa secara sadar).

| Perintah | Fungsi |
|---|---|
| `python tools\progress.py check` | Periksa konsistensi state (satu quest aktif, tanpa lompatan, bukti ada, dashboard sinkron) |
| `python tools\progress.py dashboard [--tulis]` | Tampilkan dashboard; `--tulis` menyimpannya ke `state/dashboard.md` |
| `python tools\progress.py due` | Daftar review yang jatuh tempo dan antrean legacy |
| `python tools\progress.py learned <id>` | Tandai quest aktif sudah dipelajari, belum diuji |
| `python tools\progress.py apply <entri.yaml> [--dry]` | Terapkan Evidence Entry; `--dry` hanya simulasi |
| `python tools\progress.py inbox [--dry]` | Terapkan semua entri di `state/inbox/`; yang ditolak dipindah ke `state/inbox/ditolak/` beserta alasannya. Dijalankan otomatis oleh workflow GitHub |
| `python tools\progress.py cakupan <id>` | Daftar item *Wajib* quest dari `system/09_kurikulum.md`, siap disalin ke kolom `cakupan:` (untuk modul review: daftar id quest yang bisa dipakai) |
| `python tools\progress.py statistik` | Tren skor per tanggal, rata-rata per jenis dan mode AI, modul dengan beberapa percobaan, dan konsep lemah yang masih tercatat. Hanya membaca |

Opsi global: `--root <folder repo>` dan `--today YYYY-MM-DD`.

Aturan yang dijalankan ada di `system/03_rubrik_validasi.md`. Selain rubrik, setiap entri diperiksa: `id` aman dan belum pernah dipakai, file di `bukti` benar-benar ada di repo, ukuran berkas wajar.

Untuk validasi quest aktif dan retrieval, entri juga wajib membawa:

- `cakupan`: dicocokkan dengan item *Wajib* di kurikulum. Validasi quest materi harus mencakup semuanya; modul review menyebut id quest yang dipakai (minimal angka "≥N" di kurikulum); retrieval cukup sebagian. Item boleh disalin apa adanya dari kurikulum: backtick dan isi kurung diabaikan saat dicocokkan.
- `ujian`: rekaman soal (`level`, `pertanyaan`, `skor`) dan challenge. Jumlah soal dan level diperiksa, lalu skor gabungan dihitung ulang (50% rata-rata soal + 50% challenge; retrieval: rata-rata soal) dan harus sama dengan `skor_persen` (toleransi 1 poin).
- `kesalahan` / `teratasi` (opsional): memperbarui daftar `konsep_lemah` modul itu di `state.yaml`, juga saat ujian tidak lulus.

Tes: `python -m unittest discover -s tests -v`. Tes memakai state dan potongan kurikulum yang dibekukan di `tests/fixtures/`, jadi tidak berubah saat `state.yaml` asli maju; tes lain memeriksa bahwa `state.yaml` asli tetap konsisten dan bahwa dokumen saling sinkron (`tests/test_konsistensi.py`).

Di GitHub, `.github/workflows/progres.yml` menjalankan tes, `inbox`, dan `check` pada setiap push ke `main`. Bila entri sudah diterapkan lewat `simpan.py`, inbox kosong dan bot tidak perlu meng-commit apa pun. Workflow kedua, `.github/workflows/notebook.yml`, menjalankan ulang notebook bukti (lihat `cek_notebook.py` di bawah).

## simpan.py

Satu perintah untuk menyimpan progres belajar. Salin Evidence Entry dari mentor, lalu **klik dua kali `Simpan Progres.bat`** di akar repo, atau jalankan:

```powershell
python tools\simpan.py
```

Setelah push, mentor membaca state terbaru langsung dari GitHub, jadi tidak ada file yang perlu diunggah ke ChatGPT Project.

| Perintah | Fungsi |
|---|---|
| `python tools\simpan.py` | Baca entri dari clipboard (pagar ```yaml dibuang otomatis), `git pull --rebase --autostash`, simulasi rubrik, jalankan ulang notebook bukti, terapkan, `check`, satu commit (bukti + state), push, bangun ulang `paket_project/` |
| `... --dry` | Hanya periksa dan simulasi; tidak ada yang berubah |
| `... --berkas <file.yaml>` | Baca entri dari berkas, bukan clipboard |
| `... --tanpa-push` | Commit lokal saja (tanpa pull dan push); untuk saat tanpa internet |
| `... --tanpa-git` | Terapkan ke file saja (tanpa pull, commit, push) |
| `... --buka` | Buka folder `paket_project/` setelah selesai (berguna bila `system/` berubah) |
| `... --tanpa-paket` | Jangan membangun ulang `paket_project/` |
| `... --tanpa-cek-notebook` | Jangan menjalankan ulang notebook bukti |

Aturan keselamatan: entri ditolak atau notebook bukti gagal dijalankan ulang berarti tidak ada file yang berubah; bila `check` gagal setelah diterapkan, `state.yaml`, `dashboard.md`, dan salinan evidence dikembalikan; hanya file state dan file di `bukti:` yang masuk ke commit. Tes: `tests/test_simpan.py` (memakai repo git sementara dengan remote bare).

## cek_notebook.py

Menjalankan ulang notebook `.ipynb` yang dirujuk di `bukti:` dari awal sampai akhir, di salinan sementara (notebook asli tidak diubah). Folder kerjanya folder notebook itu, jadi file data harus ada di sampingnya. Sel yang sengaja error diberi tag `raises-exception`.

Butuh paket tambahan: `pip install -r requirements-notebook.txt`. Tanpa paket itu, `simpan.py` melewati cek ini dengan pemberitahuan dan GitHub tetap mengeceknya.

| Perintah | Fungsi |
|---|---|
| `python tools\cek_notebook.py` | Cek notebook dari entri format baru (yang punya `ujian:`); dipakai workflow `notebook` dan wajib lolos |
| `... --semua` | Termasuk entri format lama; di GitHub hanya dilaporkan, tidak membuat run merah |
| `... --entri <file.yaml>` | Cek notebook dari satu entri |
| `... <path.ipynb> ...` | Cek notebook tertentu |

## buat_dataset.py

Membuat ulang bank dataset sintetis di `assets/data/` (seed tetap, jadi hasilnya selalu sama). Katalognya: `assets/data/README.md`.

| Perintah | Fungsi |
|---|---|
| `python tools\buat_dataset.py` | Tulis ulang semua dataset (butuh NumPy dan pandas) |

## bangun_paket.py

Untuk ChatGPT Project paket Free (batas 5 file). Paketnya hanya berisi aturan; progres dibaca mentor dari GitHub.

| Perintah | Fungsi |
|---|---|
| `python tools\bangun_paket.py` | Buat folder `paket_project/` berisi 4 file aturan siap unggah (`aturan_mentor.md`, `02_roadmap.md`, `03_rubrik_validasi.md`, `09_kurikulum.md`) |

`aturan_mentor.md` di dalamnya adalah gabungan otomatis dari lima dokumen `system/`. Folder `paket_project/` diabaikan git karena hanya turunan; sumbernya tetap `system/` dan `state/`. Detail: `docs/panduan_chatgpt_project.md`.
