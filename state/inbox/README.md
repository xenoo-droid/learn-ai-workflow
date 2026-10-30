# state/inbox/

Kotak masuk Evidence Entry. Di sinilah mentor AI (atau Rafa) menaruh entri; **bukan** mengubah `state.yaml`.

## Cara kerja

1. Taruh satu file entri di folder ini, langsung di branch `main`.
2. Push ke `main` memicu workflow `.github/workflows/progres.yml`.
3. Workflow menjalankan `python tools/progress.py inbox`: tiap entri diperiksa terhadap rubrik (`system/03_rubrik_validasi.md`).
   - **Diterima**: `state/state.yaml` dan `state/dashboard.md` diperbarui, salinan entri disimpan di `state/evidence/`, file di inbox dihapus. Bot meng-commit hasilnya.
   - **Ditolak**: file dipindah ke `state/inbox/ditolak/` beserta `<nama>.alasan.txt`, state tidak berubah, dan run di GitHub bertanda merah.

## Aturan berkas

- Nama berkas: `<tanggal>-<modul>.yaml`, misalnya `2026-11-02-seaborn_categorical.yaml`. Entri diproses berurutan menurut nama.
- Format isi: lihat `system/04_protokol_mentor.md` (bagian Evidence Entry).
- `id` hanya huruf, angka, `-` dan `_`. Satu `id` hanya boleh dipakai sekali.
- Setiap path di `bukti` harus sudah ada di repo (commit dan push file buktinya **sebelum** entri masuk), atau berupa URL.
- Satu entri per berkas. Berkas lain selain `.yaml`/`.yml` diabaikan.

## Yang tidak boleh

Jangan mengedit `state/state.yaml` atau `state/dashboard.md` langsung. Perubahan manual akan terdeteksi sebagai kerusakan oleh workflow (run merah), karena state hanya sah jika hasil `progress.py`.
