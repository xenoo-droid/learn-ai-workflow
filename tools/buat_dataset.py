#!/usr/bin/env python3
"""buat_dataset.py - bangun bank dataset latihan sintetis di assets/data/.

Semua data di sini DIBUAT dengan angka acak ber-seed tetap: bukan data nyata, tidak berisi
orang sungguhan, dan setiap kali dijalankan hasilnya sama persis. Pola di dalamnya
(musim, korelasi, perbedaan grup) sengaja ditanam supaya ada insight yang bisa ditemukan,
dan beberapa masalah kualitas data sengaja disisipkan untuk latihan cleaning.
Katalog lengkap: assets/data/README.md.

    python tools\\buat_dataset.py            tulis ulang semua dataset
    python tools\\buat_dataset.py --keluar X  tulis ke folder lain

Kebutuhan: NumPy dan pandas.
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261030
KOTA = ["Jakarta", "Surabaya", "Bandung", "Medan", "Makassar"]


def rng(offset: int) -> np.random.Generator:
    return np.random.default_rng(SEED + offset)


def tanggal_acak(r, mulai, akhir, n, bobot_bulan=None):
    hari = pd.date_range(mulai, akhir, freq="D")
    if bobot_bulan is None:
        p = None
    else:
        p = np.array([bobot_bulan[d.month - 1] for d in hari], dtype=float)
        p /= p.sum()
    return pd.Series(r.choice(hari, size=n, p=p)).sort_values(ignore_index=True)


# --------------------------------------------------------------------------
def retail(r) -> pd.DataFrame:
    n = 2000
    katalog = {
        "Elektronik": [("Earbuds Nirkabel", 350_000), ("Power Bank 10000mAh", 220_000), ("Smartwatch", 900_000),
                       ("Kabel USB-C", 45_000), ("Speaker Bluetooth", 410_000)],
        "Fashion": [("Kaos Polos", 75_000), ("Kemeja Batik", 260_000), ("Celana Chino", 210_000),
                    ("Jilbab Instan", 85_000), ("Sneakers", 480_000)],
        "Makanan": [("Kopi Bubuk 250g", 55_000), ("Kurma 500g", 70_000), ("Sambal Botol", 28_000),
                    ("Keripik Singkong", 18_000), ("Madu 350ml", 95_000)],
        "Rumah Tangga": [("Rice Cooker", 380_000), ("Set Panci", 450_000), ("Sapu Lantai", 35_000),
                         ("Rak Piring", 160_000), ("Dispenser Sabun", 60_000)],
        "Kecantikan": [("Sunscreen SPF50", 89_000), ("Serum Wajah", 145_000), ("Lip Tint", 59_000),
                       ("Sabun Cuci Muka", 42_000), ("Masker Wajah", 25_000)],
    }
    # Maret-April (Ramadan dan Lebaran) dan Desember lebih ramai
    tgl = tanggal_acak(r, "2025-01-01", "2025-12-31", n, [8, 8, 13, 12, 8, 8, 8, 8, 8, 9, 10, 13])
    kat = r.choice(list(katalog), size=n, p=[0.18, 0.24, 0.24, 0.16, 0.18])
    produk, harga = [], []
    for k in kat:
        nama, h = katalog[k][r.integers(len(katalog[k]))]
        produk.append(nama)
        harga.append(h)
    cabang = r.choice(KOTA, size=n, p=[0.32, 0.26, 0.18, 0.13, 0.11])
    jumlah = r.poisson(1.2, n) + 1
    diskon = r.choice([0, 0, 0, 5, 10, 15, 20, 30], size=n).astype(float)
    bayar = r.choice(["QRIS", "Tunai", "Kartu Debit", "Transfer", "Kartu Kredit"], size=n,
                     p=[0.36, 0.22, 0.18, 0.14, 0.10])
    rating = np.clip(np.round(r.normal(4.2, 0.7, n)), 1, 5)
    df = pd.DataFrame({
        "id_transaksi": [f"TRX{i:05d}" for i in range(1, n + 1)],
        "tanggal": tgl.dt.strftime("%Y-%m-%d"),
        "cabang": cabang,
        "kategori": kat,
        "produk": produk,
        "jumlah": jumlah,
        "harga_satuan": harga,
        "diskon_persen": diskon,
        "metode_bayar": bayar,
        "id_pelanggan": [f"PLG{v:04d}" for v in r.integers(1, 700, n)],
        "rating": rating,
    })
    # --- masalah kualitas data yang disengaja ---
    df.loc[r.choice(n, 140, replace=False), "rating"] = np.nan          # rating tidak diisi
    df.loc[r.choice(n, 25, replace=False), "diskon_persen"] = np.nan    # diskon kosong
    idx = r.choice(n, 12, replace=False)
    df.loc[idx, "jumlah"] = -df.loc[idx, "jumlah"]                      # retur tercatat negatif
    for i, v in zip(r.choice(n, 30, replace=False), ["surabaya", "SBY", "Surabaya "] * 10):
        df.loc[i, "cabang"] = v                                         # penulisan kota tidak konsisten
    dup = df.sample(15, random_state=SEED)                              # baris ganda
    return pd.concat([df, dup], ignore_index=True)


def ojol(r) -> pd.DataFrame:
    n = 1500
    waktu = pd.to_datetime("2025-06-01") + pd.to_timedelta(r.integers(0, 61 * 24 * 60, n), unit="min")
    waktu = waktu.sort_values()
    jam = waktu.hour
    sibuk = np.isin(jam, [7, 8, 17, 18, 19])
    layanan = r.choice(["Motor", "Mobil", "Kirim Barang"], size=n, p=[0.62, 0.25, 0.13])
    kota = r.choice(KOTA[:4], size=n, p=[0.4, 0.25, 0.2, 0.15])
    jarak = np.round(r.gamma(2.2, 2.6, n) + 0.5, 1)
    hujan = r.random(n) < np.where(np.isin(waktu.month, [11, 12, 1, 2]), 0.45, 0.2)
    kecepatan = np.where(layanan == "Mobil", 22, 28) * np.where(sibuk, 0.6, 1.0) * np.where(hujan, 0.75, 1.0)
    durasi = np.round(jarak / kecepatan * 60 + r.normal(4, 2, n), 0).clip(3)
    tarif_km = np.select([layanan == "Motor", layanan == "Mobil"], [2_500, 4_500], 3_000)
    tarif = np.round((np.maximum(jarak, 2) * tarif_km * np.where(sibuk | hujan, 1.25, 1.0)) / 500) * 500
    promo = r.random(n) < 0.3
    tarif_bayar = np.where(promo, np.round(tarif * 0.8 / 500) * 500, tarif)
    rating = np.clip(np.round(r.normal(4.75, 0.35, n) - (durasi > 45) * 0.6, 1), 1, 5)
    df = pd.DataFrame({
        "id_perjalanan": [f"OJ{i:05d}" for i in range(1, n + 1)],
        "waktu_pesan": waktu.strftime("%Y-%m-%d %H:%M"),
        "kota": kota,
        "layanan": layanan,
        "jarak_km": jarak,
        "durasi_menit": durasi.astype(int),
        "cuaca": np.where(hujan, "Hujan", "Cerah"),
        "pakai_promo": promo,
        "tarif_rp": tarif_bayar.astype(int),
        "rating_driver": rating,
    })
    idx = r.choice(n, 6, replace=False)
    df.loc[idx, "durasi_menit"] = df.loc[idx, "durasi_menit"] * 8       # outlier durasi (GPS bermasalah)
    df.loc[r.choice(n, 60, replace=False), "rating_driver"] = np.nan    # tidak memberi rating
    return df


def klinik(r) -> pd.DataFrame:
    n = 1200
    tgl = tanggal_acak(r, "2025-01-01", "2025-12-31", n)
    poli = r.choice(["Umum", "Gigi", "Anak", "Kandungan", "Penyakit Dalam"], size=n, p=[0.38, 0.14, 0.18, 0.12, 0.18])
    usia = np.where(poli == "Anak", r.integers(0, 15, n),
                    np.where(poli == "Penyakit Dalam", r.integers(35, 85, n), r.integers(15, 70, n))).astype(float)
    jk = np.where(poli == "Kandungan", "P", r.choice(["L", "P"], size=n))
    bayar = r.choice(["BPJS", "Umum", "Asuransi Swasta"], size=n, p=[0.6, 0.28, 0.12])
    hari_senin = tgl.dt.dayofweek == 0
    tunggu = np.round(r.lognormal(3.0, 0.5, n) * np.where(bayar == "BPJS", 1.4, 1.0) * np.where(hari_senin, 1.3, 1.0))
    dasar = {"Umum": 80_000, "Gigi": 250_000, "Anak": 120_000, "Kandungan": 200_000, "Penyakit Dalam": 180_000}
    biaya = np.array([dasar[p] for p in poli]) * r.lognormal(0, 0.35, n)
    biaya = np.where(bayar == "BPJS", 0, np.round(biaya / 1000) * 1000)
    df = pd.DataFrame({
        "id_kunjungan": [f"KJ{i:05d}" for i in range(1, n + 1)],
        "tanggal": tgl.dt.strftime("%Y-%m-%d"),
        "poli": poli,
        "usia": usia,
        "jenis_kelamin": jk,
        "metode_bayar": bayar,
        "waktu_tunggu_menit": tunggu.astype(int),
        "biaya_rp": biaya.astype(int),
        "kunjungan_ulang": r.random(n) < 0.35,
    })
    df.loc[r.choice(n, 30, replace=False), "usia"] = np.nan             # usia tidak tercatat
    df.loc[r.choice(n, 4, replace=False), "usia"] = 999                 # salah input
    return df


def hr(r) -> pd.DataFrame:
    n = 900
    dep = r.choice(["Penjualan", "Operasional", "IT", "Keuangan", "SDM", "Pemasaran"], size=n,
                   p=[0.25, 0.25, 0.15, 0.1, 0.08, 0.17])
    level = r.choice(["Staf", "Supervisor", "Manajer"], size=n, p=[0.68, 0.22, 0.10])
    masa = np.round(r.gamma(2.0, 2.2, n), 1)
    pengali = np.select([level == "Staf", level == "Supervisor"], [1.0, 1.6], 2.6)
    tambah = np.where(dep == "IT", 1.3, 1.0)
    gaji = np.round((5.5 + masa * 0.35) * pengali * tambah * r.lognormal(0, 0.12, n), 1)
    lembur = np.round(np.clip(r.normal(np.where(dep == "Operasional", 22, 12), 8, n), 0, 60))
    kepuasan = np.clip(np.round(r.normal(3.6 - lembur / 40, 0.8, n)), 1, 5)
    remote = r.random(n) < np.where(dep == "IT", 0.6, 0.2)
    jarak = np.round(r.gamma(2, 6, n), 1)
    logit = -2.2 + 0.05 * lembur - 0.55 * (kepuasan - 3) - 0.12 * masa + 0.02 * jarak - 0.4 * remote
    resign = r.random(n) < 1 / (1 + np.exp(-logit))
    return pd.DataFrame({
        "id_karyawan": [f"K{i:04d}" for i in range(1, n + 1)],
        "departemen": dep,
        "level": level,
        "masa_kerja_tahun": masa,
        "gaji_juta": gaji,
        "jam_lembur_bulanan": lembur.astype(int),
        "skor_kepuasan": kepuasan.astype(int),
        "kerja_remote": remote,
        "jarak_rumah_km": jarak,
        "resign": np.where(resign, "Ya", "Tidak"),
    })


def mahasiswa(r) -> pd.DataFrame:
    n = 700
    prodi = r.choice(["Sains Data", "Informatika", "Sistem Informasi", "Teknik Industri"], size=n)
    angkatan = r.choice([2021, 2022, 2023, 2024], size=n)
    belajar = np.round(np.clip(r.normal(14, 6, n), 1, 40), 1)
    hadir = np.round(np.clip(r.normal(85, 10, n), 40, 100), 0)
    tidur = np.round(np.clip(r.normal(6.6, 1.0, n), 3.5, 10), 1)
    kerja = r.random(n) < 0.28
    ipk = np.clip(1.9 + 0.035 * belajar + 0.012 * hadir + 0.06 * (tidur - 6.5) - 0.18 * kerja + r.normal(0, 0.28, n),
                  1.5, 4.0).round(2)
    tepat = r.random(n) < 1 / (1 + np.exp(-(-9 + 2.8 * ipk)))
    df = pd.DataFrame({
        "id_mahasiswa": [f"MHS{i:04d}" for i in range(1, n + 1)],
        "prodi": prodi,
        "angkatan": angkatan,
        "jenis_kelamin": r.choice(["L", "P"], size=n),
        "jam_belajar_mingguan": belajar,
        "persen_kehadiran": hadir,
        "jam_tidur": tidur,
        "kerja_paruh_waktu": kerja,
        "ipk": ipk,
        "lulus_tepat_waktu": np.where(angkatan <= 2021, np.where(tepat, "Ya", "Tidak"), "Belum lulus"),
    })
    df.loc[r.choice(n, 20, replace=False), "jam_tidur"] = np.nan
    return df


def ab_test(r) -> pd.DataFrame:
    n = 6000
    grup = r.choice(["A", "B"], size=n)
    perangkat = r.choice(["Mobile", "Desktop"], size=n, p=[0.7, 0.3])
    sumber = r.choice(["Organik", "Iklan Sosmed", "Email", "Langsung"], size=n, p=[0.4, 0.3, 0.1, 0.2])
    # B (tombol checkout baru) sedikit lebih baik, terutama di mobile
    p_klik = 0.32 + np.where(grup == "B", 0.03, 0) + np.where(perangkat == "Desktop", 0.04, 0)
    klik = r.random(n) < p_klik
    p_konv = np.where(klik, 0.30 + np.where((grup == "B") & (perangkat == "Mobile"), 0.04, 0), 0)
    konversi = r.random(n) < p_konv
    nilai = np.where(konversi, np.round(r.lognormal(12.1, 0.55, n) / 1000) * 1000, 0)
    return pd.DataFrame({
        "id_pengguna": [f"U{i:05d}" for i in range(1, n + 1)],
        "tanggal": tanggal_acak(r, "2025-09-01", "2025-09-28", n).dt.strftime("%Y-%m-%d"),
        "grup": grup,
        "perangkat": perangkat,
        "sumber_trafik": sumber,
        "klik_checkout": klik.astype(int),
        "konversi": konversi.astype(int),
        "nilai_order_rp": nilai.astype(int),
    })


def udara(r) -> pd.DataFrame:
    hari = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    basis = {"Jakarta": 42, "Surabaya": 30, "Bandung": 28, "Medan": 26, "Denpasar": 16}
    baris = []
    for kota, b in basis.items():
        kering = np.isin(hari.month, [6, 7, 8, 9])                    # musim kemarau lebih berpolusi
        hujan = np.clip(r.gamma(0.6, 12, len(hari)) * np.where(kering, 0.25, 1.4), 0, 150).round(1)
        pm = np.clip(b * np.where(kering, 1.35, 0.9) * np.where(hari.dayofweek >= 5, 0.88, 1.0)
                     - 0.15 * hujan + r.normal(0, b * 0.18, len(hari)), 3, None).round(1)
        suhu = (27.5 + np.where(kota == "Bandung", -4.5, 0) + 1.2 * np.sin((hari.dayofyear - 80) / 365 * 2 * np.pi)
                + r.normal(0, 0.8, len(hari))).round(1)
        lembap = np.clip(78 - np.where(kering, 8, 0) + r.normal(0, 5, len(hari)), 40, 99).round(0)
        d = pd.DataFrame({"tanggal": hari.strftime("%Y-%m-%d"), "kota": kota, "pm25": pm,
                          "suhu_c": suhu, "kelembapan_persen": lembap, "curah_hujan_mm": hujan})
        mulai = r.integers(0, len(hari) - 12)
        d.loc[mulai:mulai + 9, ["pm25", "suhu_c", "kelembapan_persen"]] = np.nan   # sensor mati 10 hari
        baris.append(d)
    return pd.concat(baris, ignore_index=True)


def toko_db(r, path: Path) -> None:
    """Basis data SQLite kecil (4 tabel) untuk quest SQL."""
    n_pel, n_prod, n_trx = 300, 40, 1500
    pelanggan = pd.DataFrame({
        "id_pelanggan": range(1, n_pel + 1),
        "kode_pelanggan": [f"PLG{i:04d}" for i in range(1, n_pel + 1)],
        "kota": r.choice(KOTA, size=n_pel, p=[0.32, 0.26, 0.18, 0.13, 0.11]),
        "segmen": r.choice(["Reguler", "Member", "Member Gold"], size=n_pel, p=[0.6, 0.3, 0.1]),
        "tanggal_daftar": tanggal_acak(r, "2023-01-01", "2025-06-30", n_pel).dt.strftime("%Y-%m-%d"),
    })
    kategori = ["Elektronik", "Fashion", "Makanan", "Rumah Tangga", "Kecantikan"]
    produk = pd.DataFrame({
        "id_produk": range(1, n_prod + 1),
        "nama_produk": [f"{kategori[i % 5]} {i // 5 + 1:02d}" for i in range(n_prod)],
        "kategori": [kategori[i % 5] for i in range(n_prod)],
        "harga": (np.round(r.lognormal(11.8, 0.7, n_prod) / 1000) * 1000).astype(int),
    })
    id_pel = r.integers(1, n_pel + 1, n_trx)
    id_pel[r.choice(n_trx, 20, replace=False)] = r.integers(n_pel + 1, n_pel + 30, 20)  # pelanggan sudah dihapus
    transaksi = pd.DataFrame({
        "id_transaksi": range(1, n_trx + 1),
        "id_pelanggan": id_pel,
        "tanggal": tanggal_acak(r, "2025-01-01", "2025-12-31", n_trx).dt.strftime("%Y-%m-%d"),
        "cabang": r.choice(KOTA, size=n_trx),
        "metode_bayar": r.choice(["QRIS", "Tunai", "Kartu Debit", "Transfer", "Kartu Kredit"], size=n_trx),
    })
    detail = []
    for t in transaksi["id_transaksi"]:
        for p in r.choice(n_prod, size=r.integers(1, 4), replace=False) + 1:
            detail.append((t, int(p), int(r.integers(1, 5)), int(r.choice([0, 0, 5, 10, 20]))))
    detail = pd.DataFrame(detail, columns=["id_transaksi", "id_produk", "jumlah", "diskon_persen"])
    # produk yang belum pernah terjual sengaja ada (untuk latihan LEFT JOIN)
    detail = detail[~detail["id_produk"].isin([38, 39, 40])]

    path.unlink(missing_ok=True)
    con = sqlite3.connect(path)
    try:
        con.executescript("""
            CREATE TABLE pelanggan (id_pelanggan INTEGER PRIMARY KEY, kode_pelanggan TEXT NOT NULL,
                                    kota TEXT, segmen TEXT, tanggal_daftar TEXT);
            CREATE TABLE produk (id_produk INTEGER PRIMARY KEY, nama_produk TEXT NOT NULL,
                                 kategori TEXT, harga INTEGER);
            CREATE TABLE transaksi (id_transaksi INTEGER PRIMARY KEY, id_pelanggan INTEGER,
                                    tanggal TEXT, cabang TEXT, metode_bayar TEXT);
            CREATE TABLE detail_transaksi (id_transaksi INTEGER REFERENCES transaksi(id_transaksi),
                                           id_produk INTEGER REFERENCES produk(id_produk),
                                           jumlah INTEGER, diskon_persen INTEGER);
        """)
        for nama, df in (("pelanggan", pelanggan), ("produk", produk), ("transaksi", transaksi),
                         ("detail_transaksi", detail)):
            df.to_sql(nama, con, if_exists="append", index=False)
        con.commit()
    finally:
        con.close()


DATASET = [
    ("retail_penjualan.csv", retail, 1),
    ("ojol_perjalanan.csv", ojol, 2),
    ("klinik_kunjungan.csv", klinik, 3),
    ("hr_karyawan.csv", hr, 4),
    ("mahasiswa_akademik.csv", mahasiswa, 5),
    ("ab_test_checkout.csv", ab_test, 6),
    ("kualitas_udara_harian.csv", udara, 7),
]


def main(argv=None) -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Bangun bank dataset latihan sintetis")
    ap.add_argument("--keluar", default=str(Path(__file__).resolve().parent.parent / "assets" / "data"))
    a = ap.parse_args(argv)
    keluar = Path(a.keluar)
    keluar.mkdir(parents=True, exist_ok=True)
    for nama, fungsi, off in DATASET:
        df = fungsi(rng(off))
        df.to_csv(keluar / nama, index=False, encoding="utf-8", lineterminator="\n")
        print(f"✅ {nama:<28} {len(df):>6} baris × {df.shape[1]} kolom  ({(keluar / nama).stat().st_size / 1024:.0f} KB)")
    toko_db(rng(8), keluar / "toko.db")
    print(f"✅ {'toko.db':<28} 4 tabel  ({(keluar / 'toko.db').stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
