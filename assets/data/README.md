# 🗃️ Bank Dataset Latihan

Kumpulan dataset untuk **challenge L3 (transfer)**, **retrieval di konteks baru**, dan **bukti Mastered** (≥ 2 konteks berbeda), sesuai `system/03_rubrik_validasi.md`. Tujuannya supaya ujian tidak memakai dataset yang itu-itu saja.

> ⚠️ **Semua dataset di sini sintetis.** Angkanya dibuat oleh `tools/buat_dataset.py` dengan seed tetap. Datanya bukan data nyata, tidak berisi orang sungguhan, dan tidak boleh dikutip sebagai fakta. Pola di dalamnya (musim, korelasi, perbedaan grup) sengaja ditanam supaya ada insight yang bisa ditemukan. Untuk **Portfolio**, tetap pakai dataset publik sungguhan (lihat `system/09_kurikulum.md`, `portfolio_1`).

## Cara memakai

1. Mentor memilih dataset yang **belum pernah** dipakai untuk quest itu (cek `bukti:` dan `konteks:` di `state/evidence/`).
2. **Salin** file datasetnya ke folder notebook yang memakainya, misalnya ke `notebooks/2_data_science/seaborn/`. Aturannya (`notebooks/README.md`): file data disimpan di samping notebook, supaya notebook bisa dijalankan ulang oleh `tools/cek_notebook.py`.
3. Untuk entri `mastery`, tulis nama dataset di `konteks:` supaya jelas bahwa konteksnya berbeda.

Membuat ulang semua file (hasilnya selalu sama): `python tools\buat_dataset.py`.

## Katalog

| File | Domain | Ukuran | Cocok untuk |
|---|---|---|---|
| `retail_penjualan.csv` | Transaksi toko ritel 5 kota, 2025 | 2.015 × 11 | Pandas (cleaning, `groupby`, `merge`), Matplotlib/Seaborn (tren bulanan, categorical), statistika deskriptif, Portfolio latihan |
| `ojol_perjalanan.csv` | Perjalanan ojek online, Jun–Jul 2025 | 1.500 × 10 | Relational plots, regression plots, korelasi, outlier |
| `klinik_kunjungan.csv` | Kunjungan pasien klinik, 2025 | 1.200 × 9 | Distribution & categorical plots, perbandingan kelompok, data skewed (mean vs median) |
| `hr_karyawan.csv` | Data karyawan dan resign | 900 × 10 | Categorical plots, heatmap korelasi, tabulasi silang, uji chi-square, nanti klasifikasi (World 4) |
| `mahasiswa_akademik.csv` | Kebiasaan belajar dan IPK | 700 × 10 | Regression plots, pairplot, korelasi ≠ kausalitas, regresi linear (World 4) |
| `ab_test_checkout.csv` | A/B test tombol checkout, Sep 2025 | 6.000 × 8 | Statistika terapan (proporsi, confidence interval, uji hipotesis), segmentasi |
| `kualitas_udara_harian.csv` | PM2.5 harian 5 kota, 2024–2025 | 3.655 × 6 | Time series (`lineplot`, `resample`, `rolling`), heatmap bulan × kota, missing values berurutan |
| `toko.db` | Basis data SQLite toko (4 tabel) | 300 pelanggan, 40 produk, 1.500 transaksi | Semua quest SQL, `pd.read_sql_query`, `JOIN` (termasuk baris tanpa pasangan) |

## Kolom

**retail_penjualan.csv**: `id_transaksi`, `tanggal`, `cabang`, `kategori`, `produk`, `jumlah`, `harga_satuan`, `diskon_persen`, `metode_bayar`, `id_pelanggan`, `rating` (1–5)

**ojol_perjalanan.csv**: `id_perjalanan`, `waktu_pesan`, `kota`, `layanan` (Motor/Mobil/Kirim Barang), `jarak_km`, `durasi_menit`, `cuaca`, `pakai_promo`, `tarif_rp`, `rating_driver`

**klinik_kunjungan.csv**: `id_kunjungan`, `tanggal`, `poli`, `usia`, `jenis_kelamin`, `metode_bayar` (BPJS/Umum/Asuransi Swasta), `waktu_tunggu_menit`, `biaya_rp` (0 untuk BPJS), `kunjungan_ulang`

**hr_karyawan.csv**: `id_karyawan`, `departemen`, `level`, `masa_kerja_tahun`, `gaji_juta`, `jam_lembur_bulanan`, `skor_kepuasan` (1–5), `kerja_remote`, `jarak_rumah_km`, `resign` (Ya/Tidak)

**mahasiswa_akademik.csv**: `id_mahasiswa`, `prodi`, `angkatan`, `jenis_kelamin`, `jam_belajar_mingguan`, `persen_kehadiran`, `jam_tidur`, `kerja_paruh_waktu`, `ipk`, `lulus_tepat_waktu` (Ya/Tidak/Belum lulus)

**ab_test_checkout.csv**: `id_pengguna`, `tanggal`, `grup` (A = lama, B = tombol baru), `perangkat`, `sumber_trafik`, `klik_checkout` (0/1), `konversi` (0/1), `nilai_order_rp`

**kualitas_udara_harian.csv**: `tanggal`, `kota`, `pm25` (µg/m³), `suhu_c`, `kelembapan_persen`, `curah_hujan_mm`

**toko.db**:
- `pelanggan` (`id_pelanggan` PK, `kode_pelanggan`, `kota`, `segmen`, `tanggal_daftar`)
- `produk` (`id_produk` PK, `nama_produk`, `kategori`, `harga`)
- `transaksi` (`id_transaksi` PK, `id_pelanggan`, `tanggal`, `cabang`, `metode_bayar`)
- `detail_transaksi` (`id_transaksi`, `id_produk`, `jumlah`, `diskon_persen`)

<details>
<summary><b>Untuk mentor: masalah kualitas data dan pola yang sengaja ditanam</b> (jangan dibuka Rafa sebelum ujian)</summary>

| File | Masalah kualitas data | Pola yang bisa ditemukan |
|---|---|---|
| `retail_penjualan.csv` | 15 baris ganda; `rating` kosong 140 baris; `diskon_persen` kosong 25 baris; 12 `jumlah` negatif (retur); 30 penulisan `cabang` tidak konsisten (`surabaya`, `SBY`, `Surabaya `) | Penjualan naik di Maret–April (Ramadan/Lebaran) dan Desember; Jakarta cabang terbesar |
| `ojol_perjalanan.csv` | 6 `durasi_menit` ekstrem (×8, GPS bermasalah); `rating_driver` kosong 60 baris | Tarif dan durasi naik bersama jarak; jam sibuk dan hujan memperlambat dan menaikkan tarif; rating turun bila perjalanan > 45 menit |
| `klinik_kunjungan.csv` | `usia` kosong 30 baris; 4 `usia` = 999 (salah input) | Waktu tunggu condong kanan (median lebih jujur dari mean); pasien BPJS dan hari Senin menunggu lebih lama |
| `hr_karyawan.csv` | (bersih) | Resign ±13%; lebih sering pada lembur tinggi, kepuasan rendah, masa kerja pendek; lembur Operasional paling tinggi |
| `mahasiswa_akademik.csv` | `jam_tidur` kosong 20 baris | IPK berkorelasi dengan jam belajar (r ≈ 0,55) dan kehadiran; kerja paruh waktu menurunkan IPK sedikit; status lulus hanya bermakna untuk angkatan 2021 |
| `ab_test_checkout.csv` | (bersih) | Konversi B sedikit lebih tinggi secara keseluruhan (≈ 10,9% vs 9,7%) tetapi **tidak signifikan** di α = 0,05; selisihnya muncul di Mobile, tidak di Desktop. Bagus untuk latihan "jujur tentang ketidakpastian" dan bahaya mencari-cari segmen |
| `kualitas_udara_harian.csv` | Setiap kota punya 10 hari berurutan tanpa data (sensor mati) | PM2.5 naik di Juni–September (kemarau), lebih rendah di akhir pekan dan saat hujan; Jakarta tertinggi, Denpasar terendah |
| `toko.db` | 20 transaksi dengan `id_pelanggan` yang tidak ada di tabel `pelanggan`; 3 produk tidak pernah terjual | Latihan `INNER` vs `LEFT JOIN` dan mendeteksi baris yang hilang |

</details>
