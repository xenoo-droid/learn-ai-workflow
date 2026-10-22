---
dokumen: spesifikasi_dashboard
versi: 2.0
peran: Aturan tampilan dashboard. Isi dashboard sendiri ada di state/dashboard.md.
---

# Spesifikasi Dashboard

## Prinsip

Gamifikasi adalah lapisan motivasi dan komunikasi. Ia tidak boleh menggantikan pelacakan berbasis bukti.

```text
state/state.yaml  (sumber kebenaran)
        ↓ dibaca oleh tools/progress.py
state/dashboard.md  (tampilan)
```

Dashboard tidak boleh mengarang, menyimpulkan, atau menimpa progres.

## Siapa yang membuat dashboard

- **Hanya `tools/progress.py`** yang membuat `state/dashboard.md`. Perintahnya: `python tools/progress.py dashboard --tulis`. Perintah `apply` juga membuatnya ulang otomatis.
- **Mentor AI menampilkan isi `state/dashboard.md` apa adanya** dalam blok kode saat Rafa mengetik `cek progres`. Mentor tidak membuat dashboard sendiri dan tidak merapikan atau mengubah isinya.
- File itu ditandai "dihasilkan otomatis". Jangan diedit manual; `python tools/progress.py check` memberi peringatan bila isinya tidak sinkron dengan state.

## Pola tampilan (gaya skill tree / world map)

- **World** mewakili fase besar roadmap.
- World yang **selesai** menampilkan semua modulnya dan penutup `CLEARED`.
- World yang **sedang berjalan** meringkas modul yang selesai, memperluas modul aktif, lalu menampilkan modul berikutnya sebagai rantai terkunci.
- World yang **terkunci** hanya satu baris ringkasan.
- **Quest aktif** ditandai jelas. **Quest berikutnya** dan **kemenangan terbaru** ditampilkan terpisah di bagian bawah.
- Konten terkunci tetap terlihat terkunci.

## Label status

| Status di `state.yaml` | Label di dashboard |
|---|---|
| `belum` | 🔒 LOCKED |
| `aktif` | ⚔️ CURRENT QUEST ◀ |
| `learned` | 📘 LEARNED ◀ |
| `validated_legacy` | ✅ LEGACY |
| `validated` | ✅ VALIDATED |
| `retained` | 🧠 RETAINED |
| `mastered` | 👑 MASTERED |

Istilah `COMPLETED` tidak dipakai lagi untuk status modul.

## Aturan konsistensi

Setelah format disetujui, struktur dan istilahnya tidak boleh diubah tanpa persetujuan eksplisit Rafa. Jika format lain terlihat berguna, usulkan dulu, jangan menggantinya diam-diam. Perubahan format dilakukan dengan mengubah `tools/progress.py`, spesifikasi ini, dan tes di `tests/` secara bersamaan.

## Belum termasuk

Level, XP, dan daftar achievements belum dimasukkan. Sistem itu akan dirancang ulang dengan aturan hitung yang jelas dan otomatis dari state, setelah inti sistem stabil. Catatan lamanya ada di `archive/progres-lama/`.
