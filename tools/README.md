# tools/

`progress.py` adalah penjaga aturan progres. Ia satu-satunya yang mengubah `state/state.yaml` (selain Rafa secara sadar).

| Perintah | Fungsi |
|---|---|
| `python tools\progress.py check` | Periksa konsistensi state (satu quest aktif, tanpa lompatan, bukti ada, dashboard sinkron) |
| `python tools\progress.py dashboard [--tulis]` | Tampilkan dashboard; `--tulis` menyimpannya ke `state/dashboard.md` |
| `python tools\progress.py due` | Daftar review yang jatuh tempo dan antrean legacy |
| `python tools\progress.py learned <id>` | Tandai quest aktif sudah dipelajari, belum diuji |
| `python tools\progress.py apply <entri.yaml> [--dry]` | Terapkan Evidence Entry; `--dry` hanya simulasi |

Opsi global: `--root <folder repo>` dan `--today YYYY-MM-DD`.

Aturan yang dijalankan ada di `system/03_rubrik_validasi.md`. Tes: `python -m unittest discover -s tests -v`.

## bangun_paket.py

Untuk ChatGPT Project paket Free (batas 5 file).

| Perintah | Fungsi |
|---|---|
| `python tools\bangun_paket.py` | Buat folder `paket_project/` berisi 5 file siap unggah |

`aturan_mentor.md` di dalamnya adalah gabungan otomatis dari lima dokumen `system/`. Folder `paket_project/` diabaikan git karena hanya turunan; sumbernya tetap `system/` dan `state/`. Detail: `docs/panduan_chatgpt_project.md`.
