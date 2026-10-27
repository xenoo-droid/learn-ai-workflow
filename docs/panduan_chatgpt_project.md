# Panduan ChatGPT Project

Panduan menyiapkan ChatGPT Project sebagai ruang mentor, dengan repo ini sebagai sumber kebenaran.

## Fakta yang membentuk rancangan

- ChatGPT Project membaca file unggahan lewat **retrieval teks**: mengambil potongan yang relevan, bukan membaca semuanya. Banyak file yang mirip membuat potongan saling berebut masuk ke jawaban.
- Batas jumlah file per project: 5 (Free), 25 (Plus/Go), 40 (Pro/Business/Edu/Enterprise). Sumber: [OpenAI Help Center, Projects in ChatGPT](https://help.openai.com/en/articles/8555545-projects-in-chatgpt).
- Repo ini publik. Per 2026-10-27 diuji: mentor di Project berhasil membuka `state/dashboard.md` langsung dari GitHub dan menyebut quest aktif dengan benar. Karena itu **progres tidak lagi diunggah ke Project**; mentor membacanya dari GitHub di awal setiap sesi.
- GitHub bisa menyimpan cache file mentah (raw) selama beberapa menit. Setelah `simpan.py` push, beri jeda ±5 menit sebelum `cek progres`, atau minta mentor membuka alamat cadangan.
- Percakapan lama di dalam Project bukan file dan tidak dihitung ke batas file. Teks instruksi sengaja menyatakan bahwa state di GitHub menang atas percakapan lama.

## Alamat progres di GitHub

| File | Alamat utama (raw) | Alamat cadangan |
|---|---|---|
| Dashboard | https://raw.githubusercontent.com/xenoo-droid/learn-ai-workflow/main/state/dashboard.md | https://github.com/xenoo-droid/learn-ai-workflow/blob/main/state/dashboard.md |
| State | https://raw.githubusercontent.com/xenoo-droid/learn-ai-workflow/main/state/state.yaml | https://github.com/xenoo-droid/learn-ai-workflow/blob/main/state/state.yaml |

## Pilih varian

Yang diunggah ke Project hanya aturan, yang jarang berubah.

| Varian | Kapan | File yang diunggah |
|---|---|---|
| **A. Paket 3 file** | Paket Free | 3 |
| **B. Paket 8 file** | Plus/Go atau lebih | 8 |

Jangan unggah `state.yaml`, `dashboard.md`, `archive/`, `notebooks/`, atau `docs/` di varian mana pun. Salinan state di Project akan basi dan bisa terbaca sebagai progres lama.

## Varian A: paket 3 file (Free)

Dari folder repo, jalankan:

```powershell
python tools\bangun_paket.py
```

Skrip membuat folder `paket_project/` (diabaikan git; hanya turunan) berisi:

| # | File | Isi |
|---|---|---|
| 1 | `aturan_mentor.md` | Gabungan otomatis: konstitusi, protokol mentor, aturan penyajian materi, alur command, spesifikasi dashboard, kebijakan referensi |
| 2 | `02_roadmap.md` | Materi dan urutan |
| 3 | `03_rubrik_validasi.md` | Syarat naik status |

Unggah ketiganya dari `paket_project/`. Jangan menyimpan `aturan_mentor.md` di dalam folder `system/`, supaya tidak ada dua versi aturan di repo.

Teks instruksi Project (tempel di Tingkat lanjut / Instruksi):

```text
Kamu mentor belajar Rafa untuk "Learn A.I Workflow for Data Science" (target: Data Scientist/Data Analyst yang AI-native). Bahasa: Indonesia.

Sumber kebenaran aturan adalah file di Project ini. Sumber kebenaran PROGRES adalah file di GitHub, bukan ingatanmu, bukan percakapan lama, dan bukan file lain. Urutan otoritas: aturan_mentor.md (bagian Konstitusi) > 02_roadmap.md > state.yaml di GitHub.

Di awal setiap sesi, dan setiap kali Rafa mengetik "cek progres", buka versi terbaru:
- https://raw.githubusercontent.com/xenoo-droid/learn-ai-workflow/main/state/dashboard.md
- https://raw.githubusercontent.com/xenoo-droid/learn-ai-workflow/main/state/state.yaml
Jika gagal, pakai alamat github.com/xenoo-droid/learn-ai-workflow/blob/main/state/... untuk file yang sama. Jika keduanya gagal atau terpotong, katakan terus terang dan minta Rafa menempelkan isinya. Jangan menebak dan jangan menyatakan progres dari ingatan.

Kamu hanya MENGUSULKAN perubahan progres lewat Evidence Entry (format di bagian Protokol Mentor, aturan_mentor.md; syarat naik status di 03_rubrik_validasi.md). Jangan menyatakan status naik; perubahan status hanya dilakukan tools/progress.py. Serahkan entri sebagai satu blok kode YAML utuh, lalu ingatkan Rafa menyalinnya dan menjalankan "Simpan Progres" (atau python tools\simpan.py); file bukti harus sudah ada di folder repo.

Untuk "cek progres": tampilkan isi dashboard.md dari GitHub apa adanya dalam blok kode, jangan membuat atau mengubah format dashboard. Sebut tanggal "Diperbarui" di dashboard; jika Rafa baru saja menyimpan progres tetapi tanggal/isinya belum berubah, katakan bahwa GitHub mungkin masih menyimpan cache dan sarankan mencoba lagi beberapa menit kemudian.

Command: cek progres, lanjut, review, latihan, save, prepare commit, commit progres (arti di bagian Alur Kerja dan Command, aturan_mentor.md). Sesi "latihan": 3–5 soal + 1 challenge, tanpa petunjuk sebelum Rafa mencoba. Sebelum materi baru: riset, bandingkan dengan roadmap, laporkan celah (Protokol Mentor).
```

## Varian B: paket 8 file (Plus/Go atau lebih)

| # | File | Fungsi |
|---|---|---|
| 1 | `system/01_constitution.md` | Aturan tertinggi |
| 2 | `system/02_roadmap.md` | Materi dan urutan |
| 3 | `system/03_rubrik_validasi.md` | Syarat naik status |
| 4 | `system/04_protokol_mentor.md` | Cara mentor bekerja |
| 5 | `system/05_spesifikasi_dashboard.md` | Aturan tampilan |
| 6 | `system/06_kebijakan_referensi.md` | Sumber belajar yang dipercaya |
| 7 | `system/07_alur_kerja_command.md` | Arti command dan alur commit |
| 8 | `system/08_penyajian_materi.md` | Cara materi disajikan |

Teks instruksi Project: sama dengan Varian A, dengan dua perubahan. Urutan otoritas menjadi `01_constitution > 02_roadmap > state.yaml di GitHub > evidence`, dan rujukan "aturan_mentor.md" diganti nama file `system/` yang sesuai (format Evidence Entry di `04_protokol_mentor.md`, arti command di `07_alur_kerja_command.md`).

## Mengirim Evidence Entry lewat ChatGPT Work

Work boleh menulis ke repo, tetapi hanya untuk menaruh satu file entri di `state/inbox/`. Workflow GitHub yang menerapkannya (lihat `state/inbox/README.md`). Prompt untuk Work, ganti bagian dalam kurung:

```text
Repo: xenoo-droid/learn-ai-workflow, branch main.
Buat satu file baru state/inbox/<tanggal>-<modul>.yaml berisi teks YAML di bawah ini persis apa adanya, lalu commit langsung ke main dengan pesan "inbox: <modul>".
Jangan membuat, mengubah, atau menghapus file lain. Terutama jangan menyentuh state/state.yaml, state/dashboard.md, dan state/evidence/.
Setelah commit, berhenti dan laporkan nama commit-nya.

<tempel Evidence Entry di sini>
```

Sebelumnya pastikan file bukti (notebook, gambar) sudah di-commit dan di-push, kalau tidak entri ditolak. Hasilnya bisa dilihat di tab Actions di GitHub: hijau berarti diterima, merah berarti ditolak (alasannya di `state/inbox/ditolak/`).

## Sinkronisasi

- **Setiap milestone:** tidak ada yang perlu diunggah. `simpan.py` push ke GitHub, dan mentor membaca dari sana.
- **Bila `system/` berubah (jarang):** varian A menjalankan `python tools\bangun_paket.py` lalu mengganti file yang berubah di Project (hapus yang lama, unggah yang baru); varian B mengganti file `system/` yang berubah.
- **Pindah dari cara lama:** hapus `state.yaml` dan `dashboard.md` dari Project, ganti `aturan_mentor.md` dengan versi baru, dan tempel teks instruksi baru di atas.

## Tips supaya mentor membaca dengan benar

- Jika jawaban mentor tidak menyebut isi state, minta: "buka dashboard.md dari GitHub dulu".
- Jangan mengunggah dua versi file yang sama; retrieval bisa mengambil yang lama.
- Jika menambah dokumen sistem baru, pastikan satu topik per file dan beri judul yang jelas. Di varian A, daftarkan dokumen baru ke `GABUNG` di `tools/bangun_paket.py`.
- Jika mentor gagal membuka GitHub, tempel isi `state/dashboard.md` langsung ke chat.
