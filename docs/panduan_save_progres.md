# 💾 Panduan Save Progres

Panduan singkat menyimpan progres belajar setelah lulus ujian. Semua langkah teknis dikerjakan oleh satu perintah: `python tools\simpan.py`.

---

## ⚡ Ringkasan (3 langkah)

```text
1. Salin  → blok YAML Evidence Entry dari mentor
2. Jalankan → python tools\simpan.py
3. Ganti  → state.yaml + dashboard.md di ChatGPT Project
```

Kalau ketiganya selesai, progresmu sudah tersimpan di GitHub dan mentor membaca progres terbaru.

---

## 📋 Sebelum mulai

Pastikan dua hal ini:

| Cek | Keterangan |
|---|---|
| ✅ Ujian sudah selesai | Skor gabungan minimal **80%** untuk naik status |
| ✅ File bukti tersimpan di folder repo | Misalnya `notebooks/05_seaborn.ipynb`. **Tidak perlu** di-commit atau di-push dulu |

---

## 🪜 Langkah lengkap

### Langkah 1: Minta Evidence Entry dari mentor

Setelah ujian, ketik `save` di ChatGPT Project. Mentor akan memberi satu blok YAML seperti ini:

```yaml
id: 2026-10-30-seaborn
modul: seaborn
tanggal: 2026-10-30
jenis: validasi
skor_persen: 88
mode_ai: assisted
level_soal: "2 soal L1, 2 soal L2, challenge L2"
bukti:
  - notebooks/05_seaborn.ipynb
pemahaman: >
  Keputusan 1: ... alasannya ...
  Keputusan 2: ... alasannya ...
keputusan: validated
```

Periksa sebentar:

- `bukti:` menunjuk file yang benar-benar ada di folder repo (huruf besar-kecil dan spasi harus sama).
- `mode_ai:` sesuai kenyataan: `independent` (sendiri), `assisted` (dibantu hint/debug), atau `review` (AI hanya mengkritik hasil akhir).
- `keputusan:` berisi `tetap` bila skor di bawah 80.

Lalu **salin seluruh blok** (klik tombol *Copy* di blok kode). Teks penjelasan di luar blok tidak masalah ikut tersalin; script membuangnya otomatis.

### Langkah 2: Buka PowerShell di folder repo

```powershell
cd "C:\Workspace\02_Projects_&_Coding\Porto Github\learn-ai-workflow"
```

> Tanda kutip **wajib**, karena path-nya mengandung spasi dan `&`.
> Pastikan awal baris berubah menjadi `PS C:\Workspace\...\learn-ai-workflow>`.

### Langkah 3: Jalankan simpan

```powershell
python tools\simpan.py
```

Ragu entrinya benar? Coba dulu tanpa mengubah apa pun:

```powershell
python tools\simpan.py --dry
```

Contoh hasil bila berhasil:

```text
1/6 Entri: 2026-10-30-seaborn  modul=seaborn  jenis=validasi  skor=88
2/6 git pull selesai (state lokal terbaru)
3/6 Lolos pemeriksaan rubrik:
    • Seaborn: aktif → validated; review H+7 pada 2026-11-06
    • Quest aktif berikutnya: Jupyter / Google Colab
4/6 state.yaml, dashboard.md, dan state/evidence/ diperbarui
5/6 State konsisten (2 peringatan)
6/6 Commit: progres: seaborn validasi (88%)
    Push berhasil
✅ Paket dibuat di: ...\paket_project

✅ Progres tersimpan.
```

Di akhir, folder `paket_project/` terbuka otomatis.

### Langkah 4: Ganti dua file di ChatGPT Project

1. Buka Project **Learn AI Workflow** → bagian **Files**.
2. **Hapus** `state.yaml` dan `dashboard.md` yang lama.
3. **Unggah** `state.yaml` dan `dashboard.md` dari folder `paket_project/` yang terbuka.

> Hapus dulu, baru unggah. Dua versi file yang sama membuat mentor bisa membaca yang lama.

Selesai. Ketik `cek progres` di Project untuk memastikan mentor sudah membaca progres baru.

---

## 🧭 Jenis entri

| Jenis | Kapan | Syarat utama | Hasil bila lulus |
|---|---|---|---|
| `validasi` | Selesai quest aktif, atau membuktikan modul legacy | Skor ≥ 80%, dua keputusan dijelaskan di `pemahaman`, bukti ada | **Validated**, quest berikutnya terbuka |
| `retrieval` | Review setelah jeda (lihat `cek progres`) | Minimal **7 hari** setelah validasi, mode wajib `independent`, skor ≥ 80% | **Retained** |
| `mastery` | Skill dipakai mandiri di ≥ 2 konteks berbeda | Status sudah Retained, mode `independent`, isi `konteks:` minimal dua | **Mastered** |

Skor di bawah 80% tetap bisa disimpan dengan `keputusan: tetap`. Status tidak turun, dan kamu boleh mengulang kapan saja dengan `id` baru.

---

## ⚙️ Opsi perintah

| Perintah | Kegunaan |
|---|---|
| `python tools\simpan.py` | Cara normal: entri dibaca dari clipboard |
| `python tools\simpan.py --dry` | Hanya memeriksa dan simulasi, tidak ada yang berubah |
| `python tools\simpan.py --berkas entri.yaml` | Baca entri dari file, bukan clipboard |
| `python tools\simpan.py --tanpa-push` | Saat tanpa internet: simpan dan commit di komputer saja |
| `python tools\simpan.py --varian plus` | Bila langganan Plus/Go (Project 9 file): buka folder `state/` |

---

## 🛠️ Kalau muncul masalah

Script **tidak mengubah apa pun** bila entri ditolak. Baca pesannya, perbaiki, lalu jalankan lagi.

| Pesan | Artinya | Solusi |
|---|---|---|
| `not a git repository` atau `Start directory is not importable` | PowerShell tidak berada di folder repo | Jalankan Langkah 2 (`cd "..."`) |
| `Clipboard kosong` | Entri belum tersalin | Salin ulang blok YAML dari mentor |
| `bukan YAML yang valid` / `tidak dikenali sebagai Evidence Entry` | Blok tersalin sebagian atau rusak | Salin ulang seluruh blok dengan tombol *Copy* |
| `bukti tidak ditemukan di repo` | Path di `bukti:` salah atau file belum disimpan | Cek nama file dan foldernya, samakan dengan `bukti:` |
| `keputusan usulan ... hasil perhitungan ...` | `keputusan:` tidak cocok dengan skor | Skor ≥ 80 → `validated`/`retained`/`mastered`; di bawah 80 → `tetap` |
| `id ... sudah pernah dipakai` | Entri yang sama pernah disimpan | Ganti `id`, misalnya tambah `-2` di belakang |
| `tanggal ... berada di masa depan` | Tanggal entri salah | Pakai tanggal hari ini atau sebelumnya |
| `validasi hanya untuk quest aktif/learned atau modul legacy` | Mencoba memvalidasi modul yang belum terbuka | Kerjakan quest aktif dulu (lihat `cek progres`) |
| `jeda baru ... hari, minimal 7 hari` | Retrieval terlalu cepat | Tunggu sampai jadwal review |
| `retrieval wajib mode independent` | Retrieval dikerjakan dengan bantuan AI | Ulangi review tanpa catatan dan tanpa AI |
| `git pull ... gagal` | Tidak ada internet atau masalah GitHub | Pakai `--tanpa-push`, lalu saat online: `git pull --rebase` dan `git push` |
| `Progres SUDAH diterapkan ... belum tersimpan ke GitHub` | Push gagal setelah commit | Saat online jalankan `git push` |

Masih buntu? Salin seluruh pesan error ke mentor atau ke Claude.

---

## 🚫 Jangan lakukan

- Mengedit `state/state.yaml` atau `state/dashboard.md` secara manual. Workflow GitHub akan menandainya merah.
- Menaikkan status tanpa ujian, atau karena topik "pernah dibahas".
- Menulis `mode_ai` yang tidak sesuai kenyataan.
- Lupa mengganti `state.yaml` dan `dashboard.md` di Project. Mentor akan membaca progres lama.

---

## ✅ Checklist cepat

```text
[ ] Ujian selesai, skor sudah diketahui
[ ] File bukti tersimpan di folder repo
[ ] Blok YAML dari mentor sudah disalin
[ ] cd ke folder repo
[ ] python tools\simpan.py  → muncul "✅ Progres tersimpan."
[ ] Ganti state.yaml + dashboard.md di ChatGPT Project
[ ] cek progres di Project
```

---

Rujukan lengkap: `system/07_alur_kerja_command.md` (alur dan command), `system/03_rubrik_validasi.md` (syarat naik status), `tools/README.md` (detail perintah).
