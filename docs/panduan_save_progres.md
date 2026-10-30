# 💾 Panduan Save Progres

Panduan singkat menyimpan progres belajar setelah lulus ujian. Semua langkah teknis dikerjakan oleh **Simpan Progres** (`Simpan Progres.bat`), dan mentor membaca hasilnya langsung dari GitHub.

---

## ⚡ Ringkasan (2 langkah)

```text
1. Salin        → blok YAML Evidence Entry dari mentor
2. Klik dua kali → Simpan Progres.bat
```

Selesai. Progresmu tersimpan di GitHub, dan mentor membaca versi terbaru dari sana. Tidak ada file yang perlu diunggah ke ChatGPT Project.

---

## 🔧 Persiapan sekali saja: shortcut di Desktop

1. Buka folder repo: `C:\Workspace\02_Projects_&_Coding\Porto Github\learn-ai-workflow`
2. Klik kanan `Simpan Progres.bat` → **Show more options** → **Send to** → **Desktop (create shortcut)**.
3. Opsional: klik kanan shortcut → **Pin to taskbar** atau ganti namanya, misalnya "💾 Simpan Progres".

Shortcut tetap menjalankan script dari folder repo, jadi aman dipindah ke mana saja.

---

## 📋 Sebelum menyimpan

| Cek | Keterangan |
|---|---|
| ✅ Ujian sudah selesai | Skor gabungan minimal **80%** untuk naik status |
| ✅ File bukti tersimpan di folder repo | Misalnya `notebooks/2_data_science/seaborn/latihan.ipynb`. **Tidak perlu** di-commit atau di-push dulu |
| ✅ Notebook bisa dijalankan ulang | Di Jupyter: *Kernel → Restart & Run All* tanpa error. File data (CSV dan sebagainya) disimpan **di samping notebook** |

---

## 🪜 Langkah lengkap

### Langkah 1: Minta Evidence Entry dari mentor

Setelah ujian, ketik `save` di ChatGPT Project. Mentor akan memberi satu blok YAML seperti ini:

```yaml
id: 2026-11-02-seaborn-categorical
modul: seaborn_categorical
tanggal: 2026-11-02
jenis: validasi
skor_persen: 86
mode_ai: assisted
level_soal: "2 soal L1, 2 soal L2, challenge L2"
bukti:
  - notebooks/2_data_science/seaborn/latihan_categorical.ipynb
cakupan: [stripplot, swarmplot, boxplot, violinplot, boxenplot, pointplot, barplot, countplot, catplot]
ujian:
  soal:
    - {level: L1, pertanyaan: "Beda stripplot dan swarmplot?", skor: 100}
    - {level: L1, pertanyaan: "Kapan countplot dipakai, bukan barplot?", skor: 100}
    - {level: L2, pertanyaan: "Pilih box/violin/boxen untuk data tips per hari", skor: 75}
    - {level: L2, pertanyaan: "Arti errorbar='sd' vs ('ci', 95)", skor: 69}
  challenge: {level: L2, deskripsi: "catplot durasi per kelas dan shift", skor: 86}
kesalahan:
  - "barplot errorbar: tertukar arti sd dan ci"
pemahaman: >
  Keputusan 1: ... alasannya ...
  Keputusan 2: ... alasannya ...
keputusan: validated
```

Periksa sebentar:

- `bukti:` menunjuk file yang benar-benar ada di folder repo (huruf besar-kecil dan spasi harus sama).
- `mode_ai:` sesuai kenyataan: `independent` (sendiri), `assisted` (dibantu hint/debug), atau `review` (AI hanya mengkritik hasil akhir).
- `keputusan:` berisi `tetap` bila skor di bawah 80.
- `cakupan:` memuat semua item *Wajib* quest itu. Daftarnya bisa kamu lihat sendiri: `python tools\progress.py cakupan seaborn_categorical`.
- `ujian:` berisi soal yang benar-benar kamu kerjakan. `skor_persen` = 50% rata-rata soal + 50% challenge; script menghitung ulang.

Lalu **salin seluruh blok** (klik tombol *Copy* di blok kode). Teks penjelasan di luar blok tidak masalah ikut tersalin; script membuangnya otomatis.

### Langkah 2: Klik dua kali Simpan Progres

Klik dua kali shortcut **Simpan Progres** di Desktop (atau `Simpan Progres.bat` di folder repo). Jendela hitam terbuka dan menampilkan prosesnya:

```text
1/6 Entri: 2026-11-02-seaborn-categorical  modul=seaborn_categorical  jenis=validasi  skor=86
2/6 git pull selesai (state lokal terbaru)
3/6 Lolos pemeriksaan rubrik:
    • Categorical Plots: aktif → validated; review H+7 pada 2026-11-09
    • Quest aktif berikutnya: Relational Plots
    • konsep lemah dicatat: barplot errorbar: tertukar arti sd dan ci
    ✅ notebook notebooks/2_data_science/seaborn/latihan_categorical.ipynb: lolos
4/6 state.yaml, dashboard.md, dan state/evidence/ diperbarui
5/6 State konsisten (2 peringatan)
6/6 Commit: progres: seaborn_categorical validasi (86%)
    Push berhasil

✅ Progres tersimpan.
Mentor membaca progres terbaru langsung dari GitHub; tidak ada file yang perlu diunggah.
Press any key to continue . . .
```

Tekan tombol apa saja untuk menutup jendela.

> Lebih suka terminal? Dari folder repo jalankan `python tools\simpan.py`. Hasilnya sama.
> Ingin mencoba tanpa mengubah apa pun? `python tools\simpan.py --dry`.

### Langkah 3 (opsional): Cek di mentor

Tunggu ±5 menit (GitHub menyimpan cache sebentar), lalu ketik `cek progres` di ChatGPT Project. Tanggal "Diperbarui" dan quest aktif di dashboard seharusnya sudah berubah.

---

## 🧭 Jenis entri

| Jenis | Kapan | Syarat utama | Hasil bila lulus |
|---|---|---|---|
| `validasi` | Selesai quest aktif, atau membuktikan modul legacy | Skor ≥ 80%, dua keputusan dijelaskan di `pemahaman`, bukti ada; untuk quest aktif juga `cakupan` lengkap dan rekaman `ujian` | **Validated**, quest berikutnya terbuka |
| `retrieval` | Review setelah jeda (lihat `cek progres`) | Minimal **7 hari** setelah validasi, mode wajib `independent`, 2–3 soal di `ujian`, skor ≥ 80% | **Retained** |
| `mastery` | Skill dipakai mandiri di ≥ 2 konteks berbeda | Status sudah Retained, mode `independent`, isi `konteks:` minimal dua | **Mastered** |

Skor di bawah 80% tetap bisa disimpan dengan `keputusan: tetap`. Status tidak turun, dan kamu boleh mengulang kapan saja dengan `id` baru.

---

## ⚙️ Opsi lewat terminal

| Perintah | Kegunaan |
|---|---|
| `python tools\simpan.py` | Sama dengan klik dua kali Simpan Progres |
| `python tools\simpan.py --dry` | Hanya memeriksa dan simulasi, tidak ada yang berubah |
| `python tools\simpan.py --berkas entri.yaml` | Baca entri dari file, bukan clipboard |
| `python tools\simpan.py --tanpa-push` | Saat tanpa internet: simpan dan commit di komputer saja |
| `python tools\simpan.py --buka` | Buka folder `paket_project/` setelah selesai (bila aturan di `system/` berubah) |
| `python tools\simpan.py --tanpa-cek-notebook` | Lewati cek notebook (GitHub tetap mengeceknya setelah push) |
| `python tools\progress.py statistik` | Lihat tren skor, percobaan per modul, dan konsep lemah |

---

## 🛠️ Kalau muncul masalah

Script **tidak mengubah apa pun** bila entri ditolak. Baca pesannya, perbaiki, lalu jalankan lagi.

| Pesan | Artinya | Solusi |
|---|---|---|
| `Clipboard kosong` | Entri belum tersalin | Salin ulang blok YAML dari mentor |
| `bukan YAML yang valid` / `tidak dikenali sebagai Evidence Entry` | Blok tersalin sebagian atau rusak | Salin ulang seluruh blok dengan tombol *Copy* |
| `bukti tidak ditemukan di repo` | Path di `bukti:` salah atau file belum disimpan | Cek nama file dan foldernya, samakan dengan `bukti:` |
| `keputusan usulan ... hasil perhitungan ...` | `keputusan:` tidak cocok dengan skor | Skor ≥ 80 → `validated`/`retained`/`mastered`; di bawah 80 → `tetap` |
| `ujian validasi belum mencakup semua item Wajib` | Ada item kurikulum yang belum diuji | Minta mentor menguji item yang disebut, atau tunda validasi |
| `skor_persen ... tidak sama dengan hitungan dari ujian` | Skor ringkas tidak cocok dengan skor per soal | Hitung ulang bersama mentor: 50% rata-rata soal + 50% challenge |
| `jumlah soal ...` / `challenge wajib diisi` | Bentuk ujian tidak sesuai rubrik | Materi 3–5 soal + challenge; review 3 soal + challenge L3; retrieval 2–3 soal |
| `Notebook bukti tidak bisa dijalankan ulang` | Notebook error saat dijalankan dari awal, biasanya file data tidak ada | Salin file data ke samping notebook, *Restart & Run All*, lalu simpan lagi |
| `id ... sudah pernah dipakai` | Entri yang sama pernah disimpan | Ganti `id`, misalnya tambah `-2` di belakang |
| `tanggal ... berada di masa depan` | Tanggal entri salah | Pakai tanggal hari ini atau sebelumnya |
| `validasi hanya untuk quest aktif/learned atau modul legacy` | Mencoba memvalidasi modul yang belum terbuka | Kerjakan quest aktif dulu (lihat `cek progres`) |
| `jeda baru ... hari, minimal 7 hari` | Retrieval terlalu cepat | Tunggu sampai jadwal review |
| `retrieval wajib mode independent` | Retrieval dikerjakan dengan bantuan AI | Ulangi review tanpa catatan dan tanpa AI |
| `git pull ... gagal` | Tidak ada internet atau masalah GitHub | Pakai `python tools\simpan.py --tanpa-push`, lalu saat online: `git pull --rebase` dan `git push` |
| `Progres SUDAH diterapkan ... belum tersimpan ke GitHub` | Push gagal setelah commit | Saat online jalankan `git push` dari folder repo |
| `'python' is not recognized` / `'py' is not recognized` | Python tidak ada di PATH | Pasang Python dari python.org dengan opsi *Add to PATH*, atau jalankan lewat terminal yang biasa kamu pakai |
| Mentor masih menampilkan progres lama | Cache GitHub | Tunggu beberapa menit lalu `cek progres` lagi, atau minta mentor membuka alamat `github.com/.../blob/main/state/dashboard.md` |

Masih buntu? Salin seluruh pesan error ke mentor atau ke Claude.

---

## 🚫 Jangan lakukan

- Mengedit `state/state.yaml` atau `state/dashboard.md` secara manual. Workflow GitHub akan menandainya merah.
- Menaikkan status tanpa ujian, atau karena topik "pernah dibahas".
- Menulis `mode_ai` yang tidak sesuai kenyataan.
- Mengunggah `state.yaml` atau `dashboard.md` ke ChatGPT Project. Salinan itu akan basi dan bisa terbaca sebagai progres lama.

---

## ✅ Checklist cepat

```text
[ ] Ujian selesai, skor sudah diketahui
[ ] File bukti tersimpan di folder repo (notebook lolos Restart & Run All)
[ ] Blok YAML dari mentor sudah disalin
[ ] Klik dua kali Simpan Progres → muncul "✅ Progres tersimpan."
[ ] (Opsional) ±5 menit kemudian: cek progres di Project
```

---

Rujukan lengkap: `system/07_alur_kerja_command.md` (alur dan command), `system/03_rubrik_validasi.md` (syarat naik status), `docs/panduan_chatgpt_project.md` (pengaturan Project), `tools/README.md` (detail perintah).
