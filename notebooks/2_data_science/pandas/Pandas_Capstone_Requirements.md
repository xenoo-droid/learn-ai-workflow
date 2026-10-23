# 👑 PANDAS CAPSTONE — FINAL QUEST

**Objective:** membangun satu analisis data end-to-end menggunakan Pandas.

## 🎯 CAPSTONE BRIEF

Kamu akan bekerja dengan dataset penjualan berikut:

```python
import pandas as pd

data = {
    "Tanggal": [
        "2026-01-03", "2026-01-05", "2026-01-08",
        "2026-01-12", "2026-01-15", "2026-01-18",
        "2026-01-22", "2026-01-25", "2026-01-28",
        "2026-01-30"
    ],
    "Produk": [
        "Laptop", "Mouse", "Keyboard",
        "Laptop", "Monitor", "Mouse",
        "Keyboard", "Laptop", "Monitor", "Mouse"
    ],
    "Kategori": [
        "Elektronik", "Aksesoris", "Aksesoris",
        "Elektronik", "Elektronik", "Aksesoris",
        "Aksesoris", "Elektronik", "Elektronik", "Aksesoris"
    ],
    "Kota": [
        "Surabaya", "Malang", "Surabaya",
        "Jakarta", "Malang", "Jakarta",
        "Surabaya", "Jakarta", "Surabaya", "Malang"
    ],
    "Jumlah": [2, 10, 5, 1, 3, 8, 7, 2, 4, 12],
    "Harga": [
        8000000, 150000, 300000, 8000000, 2500000,
        150000, 300000, 8000000, 2500000, 150000
    ]
}

df = pd.DataFrame(data)
```

---

# 🗺️ QUEST 1 — DATA INSPECTION

Selesaikan:

1. Tampilkan `head()` dan `tail()`.
2. Periksa `info()`.
3. Periksa `describe()`.
4. Periksa `shape`.
5. Pastikan apakah ada missing value.

### 🎯 Target

Kamu harus bisa menjelaskan:

- berapa baris dan kolom;
- kolom apa saja yang tersedia;
- tipe data masing-masing kolom;
- apakah ada missing value;
- gambaran statistik dasar dataset.

---

# 🧹 QUEST 2 — DATA PREPARATION

Lakukan:

1. Ubah `Tanggal` menjadi datetime.
2. Buat kolom baru:

```text
Total = Jumlah × Harga
```

3. Periksa kembali DataFrame.
4. Pastikan tidak ada kesalahan tipe data.

---

# 🎯 QUEST 3 — DATA ANALYSIS

Jawab pertanyaan berikut menggunakan Pandas:

### A. Produk

- Produk apa yang menghasilkan **total penjualan terbesar**?
- Produk mana yang memiliki **jumlah unit terjual terbanyak**?

### B. Kota

- Kota mana yang menghasilkan **revenue terbesar**?
- Berapa total revenue setiap kota?

### C. Kategori

- Kategori mana yang menghasilkan revenue terbesar?
- Berapa rata-rata `Harga` setiap kategori?

### D. Statistik

Hitung:

```text
mean Total
sum Total
min Total
max Total
median Total
```

---

# 📊 QUEST 4 — GROUPBY

Gunakan `groupby()` untuk menghasilkan tabel:

```text
Produk | Total Unit | Total Revenue | Rata-rata Harga
```

Kemudian urutkan berdasarkan:

```text
Total Revenue → terbesar ke terkecil
```

---

# 🔗 QUEST 5 — MERGE / JOIN

Buat DataFrame kedua:

```python
target = pd.DataFrame({
    "Kota": ["Surabaya", "Malang", "Jakarta"],
    "Target": [10000000, 8000000, 15000000]
})
```

Gabungkan dengan hasil analisis kota menggunakan `merge()`.

Hasil akhirnya harus memungkinkan kamu membandingkan:

```text
Kota | Revenue | Target
```

Lalu tambahkan kolom:

```text
Status
```

dengan nilai:

- `"Tercapai"` jika Revenue >= Target
- `"Belum Tercapai"` jika Revenue < Target

---

# 💾 QUEST 6 — IMPORT / EXPORT

Export hasil final ke:

```text
pandas_capstone_result.csv
```

Kemudian baca kembali file tersebut menggunakan Pandas dan pastikan datanya sama.

---

# 👑 FINAL BOSS — BUSINESS INSIGHT

Berdasarkan analisis yang kamu lakukan, tuliskan **minimal 5 insight**.

Contoh bentuknya:

```text
1. Produk X menghasilkan revenue terbesar karena ...
2. Kota X memiliki performa terbaik karena ...
3. Kategori X memiliki rata-rata harga ...
4. ...
5. ...
```

**Jangan cuma menyebut angka. Jelaskan maknanya.**

---

# 🏆 CAPSTONE VALIDATION

| Area | Target |
|---|---:|
| Inspection | 20 |
| Data Preparation | 20 |
| Selection & Filtering | 20 |
| Statistics | 20 |
| GroupBy | 30 |
| Sorting | 20 |
| Merge | 30 |
| Import / Export | 20 |
| Business Insight | 40 |
| **TOTAL** | **220** |

### 🎯 Passing rule

**≥ 200/220** dan seluruh konsep utama benar.

Kalau ada kesalahan, kita **debug → revisi → validasi ulang**. Tidak langsung dianggap selesai.

---

# 🚀 CURRENT QUEST

```text
👑 PANDAS CAPSTONE

🟨 QUEST 1
└── Data Inspection
    ├── head()
    ├── tail()
    ├── info()
    ├── describe()
    ├── shape
    └── missing values
```

**Kerjakan Quest 1 dulu. Kirim kode + output-nya ke chat untuk direview sebelum Quest 2 dibuka.**
