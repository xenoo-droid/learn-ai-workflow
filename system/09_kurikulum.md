---
dokumen: kurikulum
versi: 1.1
tanggal: 2026-10-30
peran: Rincian setiap modul roadmap menjadi quest beserta fungsi/konsep wajib. Dipakai mentor untuk menyajikan materi, menyusun ujian, dan retrieval review.
otoritas: Di bawah roadmap (system/02_roadmap.md). Roadmap menentukan modul dan urutannya; kurikulum ini merinci isi setiap modul.
---

# Kurikulum Learn A.I Workflow for Data Science

## Cara memakai

- Setiap quest punya **id** yang sama persis dengan id di `state/state.yaml`. Kolom `modul` di Evidence Entry diisi id ini.
- **Wajib** adalah daftar fungsi/konsep yang harus diajarkan (`lanjut`) dan **semuanya** diujikan saat validasi quest itu. Ujian yang hanya mencakup sebagian daftar tidak boleh memvalidasi quest; mentor menunda validasi sampai sisanya diajarkan dan diuji.
- Satu item = satu bagian yang dipisah koma (koma di dalam kurung tidak memisah). Pada daftar bertingkat, satu sub-butir = satu item dengan kunci label sebelum titik dua. Kolom `cakupan` di Evidence Entry diisi item-item ini dan diperiksa `tools/progress.py`; daftar siap salin: `python tools/progress.py cakupan <id>`. Karena itu, ubah pemisahan item dengan hati-hati dan catat di changelog.
- **Fokus ujian** memberi arah soal dan challenge sesuai `system/03_rubrik_validasi.md`.
- Modul yang sudah selesai (status legacy/validated) tidak diubah statusnya. Rinciannya di sini menjadi **cakupan retrieval review**: soal review diambil dari daftar wajibnya.
- Modul **review** (misalnya Seaborn Review) menguji gabungan semua quest di modulnya pada dataset baru (challenge L3), termasuk item yang belum sempat diujikan.
- Kurikulum hanya berubah dengan persetujuan Rafa, dicatat di `docs/changelog.md`. Celah yang ditemukan saat riset dilaporkan di bagian akhir dokumen, bukan langsung ditambahkan.

---

# 🌍 WORLD 1 — PYTHON FOUNDATION *(selesai — cakupan retrieval)*

#### `python_fundamentals` — Python Fundamentals
- **Wajib:** variabel dan tipe data (`int`, `float`, `str`, `bool`, `None`), `type()`, konversi (`int()`, `float()`, `str()`), operator aritmatika (`+ - * / // % **`), perbandingan, logika (`and or not`), `input()`, `print()`, f-string, `if/elif/else`, `for` + `range()`, `while`, `break`/`continue`, method string (`upper`, `lower`, `strip`, `split`, `join`, `replace`, `find`), slicing string
- **Fokus ujian:** menulis program kecil berlogika bercabang dan berulang; memilih tipe data yang tepat

#### `data_structures` — Data Structures
- **Wajib:** list (`append`, `extend`, `insert`, `remove`, `pop`, `sort`/`sorted`, slicing), tuple (immutability, unpacking), dict (`keys`, `values`, `items`, `get`, `update`, iterasi), set (`add`, union, intersection, difference), list/dict/set comprehension, struktur bersarang (list of dict)
- **Fokus ujian:** memilih struktur data yang tepat untuk masalah; mengolah list of dict

#### `functions_modules` — Functions & Modules
- **Wajib:** `def`, `return`, parameter default, keyword argument, `*args`, `**kwargs`, scope lokal/global, `lambda`, docstring, `import`, `from ... import`, `as`, modul buatan sendiri, `if __name__ == "__main__":`, standard library (`math`, `random`, `datetime`)
- **Fokus ujian:** memecah program jadi fungsi yang bisa dipakai ulang

#### `error_handling` — Error Handling
- **Wajib:** `try/except/else/finally`, beberapa `except`, `raise`, custom exception, exception umum (`ValueError`, `TypeError`, `KeyError`, `IndexError`, `ZeroDivisionError`, `FileNotFoundError`), membaca traceback
- **Fokus ujian:** menangani input tidak valid tanpa program berhenti

#### `file_io` — File I/O
- **Wajib:** `open()` dengan mode `r/w/a`, `with`, `read`/`readline`/`readlines`, `write`, `encoding="utf-8"`, `pathlib.Path`, modul `csv`, modul `json` (`load`, `dump`)
- **Fokus ujian:** menyimpan dan membaca data program ke/dari file

#### `venv_pip` — Virtual Environment & pip
- **Wajib:** `python -m venv`, aktivasi di Windows, `pip install/uninstall/list/freeze`, `requirements.txt`, `pip install -r`
- **Fokus ujian:** menyiapkan environment proyek yang bisa diulang di komputer lain

#### `oop_dasar` — OOP Dasar
- **Wajib:** `class`, `__init__`, `self`, atribut dan method, atribut kelas vs instance, `__str__`/`__repr__`, inheritance, `super()`, konvensi enkapsulasi (`_atribut`)
- **Fokus ujian:** memodelkan objek sederhana (misalnya rekening, produk) dengan class

#### `python_mini_project` — Python Mini Project
- **Wajib:** program CLI modular, penyimpanan data ke file, error handling, Git & GitHub (`init`, `add`, `commit`, `push`), `.gitignore`, README dasar
- **Fokus ujian:** proyek berjalan, README menjelaskan cara pakai dan keputusan desain

---

# 🌍 WORLD 2 — DATA SCIENCE & DATA ANALYTICS

## 📦 NumPy *(selesai — cakupan retrieval)*

#### `numpy` — NumPy
- **Wajib:**
  - Membuat array: `np.array`, `arange`, `linspace`, `zeros`, `ones`, `empty`, `eye`, `full`
  - Atribut: `ndim`, `shape`, `size`, `dtype`, `itemsize`, `nbytes`, `T`
  - Indexing & slicing 1D/2D, fancy indexing, boolean indexing
  - Manipulasi: `reshape`, `flatten`/`ravel`, `concatenate`, `vstack`/`hstack`, `split`
  - Broadcasting, vectorization, ufunc (`sqrt`, `exp`, `log`, `abs`)
  - Agregasi dengan `axis`: `sum`, `mean`, `median`, `std`, `var`, `min`, `max`; `argmax`/`argmin`; `any`/`all`
  - Sorting & searching: `sort`, `argsort`, `where`, `unique`
  - Linear algebra dasar: `dot`, `@`, `linalg.inv`, `linalg.det`
  - Random: `np.random.default_rng`, `integers`, `random`, `normal`, `choice`, seed
  - File I/O: `save`/`load`, `savetxt`/`loadtxt`
  - Performa: loop vs vectorization (`%timeit`)
  - NumPy Capstone
- **Fokus retrieval:** operasi berbasis `axis`, boolean indexing, broadcasting

## 🐼 Pandas *(selesai — cakupan retrieval)*

#### `pandas` — Pandas
- **Wajib:**
  - Fundamentals: `Series`, `DataFrame`, membuat data dari dict/list, `index`, `columns`, `shape`, `head`, `tail`, `info`, `describe`, `dtypes`
  - Seleksi: `df["kol"]`, `df[["a","b"]]`, `loc`, `iloc`
  - Filtering: perbandingan, kondisi ganda `&`/`|`, `isin`, `between`, `query`
  - Manipulasi: kolom baru, `rename`, `drop`, `astype`, `apply`/`map`, tambah/hapus baris
  - Missing values: `isna`, `fillna`, `dropna`
  - Sorting: `sort_values`, `sort_index`
  - Statistik: `mean`, `sum`, `count`, `min`, `max`, `median`, `mode`, `std`, `value_counts`
  - Grouping & combining: `groupby`, `agg`, agregasi ganda, `merge`, `concat`, `join`
  - Import/Export: CSV, Excel, JSON
  - Pandas Capstone
- **Fokus retrieval:** `groupby` + `agg`, `merge`, filtering bersyarat ganda

## 📈 Matplotlib *(selesai — cakupan retrieval)*

#### `line_plot` — Pengenalan & Line Plot
- **Wajib:** `plt.plot`, `label`, `marker`, `linestyle`, `color`, `plt.show`
#### `bar_plot` — Bar Plot
- **Wajib:** `plt.bar`, `plt.barh`, bar berkelompok sederhana
#### `histogram` — Histogram
- **Wajib:** `plt.hist`, `bins`, `density`, `alpha`
#### `scatter_plot` — Scatter Plot
- **Wajib:** `plt.scatter`, `c`, `s`, `alpha`, `cmap`, colorbar
#### `subplots` — Subplots
- **Wajib:** `plt.subplots(nrows, ncols)`, indexing `ax[i, j]`, `sharex`/`sharey`, `tight_layout`
#### `styling_labels` — Styling & Labels
- **Wajib:** `title`, `xlabel`, `ylabel`, `grid`, `plt.style.use`, ukuran font
#### `figure_axes` — Figure & Axes
- **Wajib:** objek `fig` dan `ax`, gaya object-oriented (`ax.plot`, `ax.set_title`), `figsize`
#### `boxplot` — Boxplot
- **Wajib:** `ax.boxplot`, membaca median/IQR/outlier
#### `errorbar` — Errorbar
- **Wajib:** `ax.errorbar`, `yerr`/`xerr`, `fmt`, `capsize`
#### `axis_limits_scale` — Axis Limits & Scale
- **Wajib:** `set_xlim`/`set_ylim`, `set_xscale`/`set_yscale("log")`
#### `legend_tick_formatting` — Legend & Tick Formatting
- **Wajib:** `legend(loc=...)`, `set_xticks`, `set_xticklabels`, `tick_params`, rotasi label
#### `savefig` — savefig()
- **Wajib:** `savefig` vs `show`, format (`png`, `pdf`), `dpi`, `bbox_inches="tight"`
#### `matplotlib_review` — Matplotlib Review
- **Wajib:** challenge transfer L3 pada dataset baru yang memakai ≥2 skill Matplotlib + 3 soal retrieval

## 🎨 Seaborn

Rujukan: [seaborn API reference](https://seaborn.pydata.org/api) (dibaca 2026-10-29). Antarmuka objek (`seaborn.objects`) tidak termasuk cakupan; fokus pada function interface.

#### `seaborn_distribusi` — Pengenalan & Distribution Plots *(validated 2026-10-29)*
- **Wajib:** `sns.load_dataset`, figure-level vs axes-level, `histplot` (`bins`, `binwidth`, `hue`, `stat`, `kde`), `kdeplot` (`bw_adjust`, `fill`, `hue`), `ecdfplot`, `rugplot`, `displot` (`kind`, `col`/`row`)
- **Fokus ujian:** memilih plot distribusi yang tepat dan membaca bentuk distribusi
- **Catatan:** ujian 29 Okt belum mencakup `ecdfplot` dan `rugplot`; keduanya wajib muncul di Seaborn Review

#### `seaborn_categorical` — Categorical Plots
- **Wajib:** `stripplot`, `swarmplot`, `boxplot`, `violinplot`, `boxenplot`, `pointplot`, `barplot` (`estimator`, `errorbar`), `countplot`, `catplot` (`kind`, `col`)
- **Fokus ujian:** membandingkan kategori; kapan memakai box vs violin vs bar; arti error bar

#### `seaborn_relational` — Relational Plots
- **Wajib:** `scatterplot` (`hue`, `size`, `style`), `lineplot` (`estimator`, `errorbar`, data time series), `relplot` (`kind`, `col`/`row`)
- **Fokus ujian:** menampilkan hubungan dua variabel numerik dengan dimensi tambahan

#### `seaborn_regression` — Regression Plots
- **Wajib:** `regplot`, `lmplot` (`hue`, `col`), `residplot`, parameter `order` dan `ci`
- **Fokus ujian:** membaca garis tren dan residual; tidak menyamakan tren dengan kausalitas

#### `seaborn_matrix` — Matrix Plots
- **Wajib:** `heatmap` (`annot`, `fmt`, `cmap`, `center`, `vmin`/`vmax`) untuk `df.corr()` dan tabel pivot, `clustermap`
- **Fokus ujian:** heatmap korelasi yang bisa dibaca dan insight dari pola

#### `seaborn_grids` — Multi-plot Grids
- **Wajib:** `FacetGrid` (`map`, `map_dataframe`), `pairplot` (`hue`, `diag_kind`, `corner`), `PairGrid`, `jointplot` (`kind`), `JointGrid`
- **Fokus ujian:** eksplorasi banyak variabel sekaligus

#### `seaborn_aesthetics` — Figure Aesthetics & Color Palettes
- **Wajib:** `set_theme` (`style`, `context`, `palette`), `set_style`, `axes_style`, `set_context`, `color_palette`, palet kualitatif/sekuensial/divergen (`diverging_palette`), `despine`, `move_legend`, menggabungkan dengan Matplotlib (`ax=`, `fig`, `savefig`)
- **Fokus ujian:** membuat grafik siap laporan dan memilih palet sesuai jenis data

#### `seaborn_review` — Seaborn Review
- **Wajib:** challenge transfer L3 pada dataset baru yang memakai ≥3 keluarga plot di atas + Pandas untuk menyiapkan data, termasuk `ecdfplot`; 3 soal retrieval
- **Fokus ujian:** memilih visualisasi sendiri dan menulis insight

## 📓 Jupyter / Google Colab

#### `jupyter_notebook_markdown` — Notebook Workflow & Markdown
- **Wajib:** jenis sel (code/markdown), mode command vs edit, shortcut (`Shift+Enter`, `A`/`B`, `M`/`Y`, `DD`), Markdown (heading, list, tabel, blok kode, tautan, gambar, rumus `$...$`), Colab: upload file, mount Google Drive, berbagi notebook
- **Fokus ujian:** notebook yang terdokumentasi rapi seperti laporan

#### `jupyter_reproducibility` — Reproducibility & Kernel/Runtime
- **Wajib:** urutan eksekusi dan state tersembunyi, *Restart & Run All*, `%pip install` di notebook, `requirements.txt`, random seed, path relatif, runtime Colab (CPU/GPU, sesi yang hilang), magic command (`%timeit`, `%matplotlib inline`), export (`.ipynb`, `.py`, HTML/PDF)
- **Fokus ujian:** notebook yang berjalan dari awal sampai akhir di mesin lain tanpa error

## 🌐 Web Scraping *(opsional)*

#### `web_scraping` — Web Scraping
- **Wajib:** `requests.get` (`params`, `headers`, `timeout`), `status_code`, `response.text`/`.json()`, `BeautifulSoup(html, "html.parser")`, `find`/`find_all`/`select`, `get_text`, mengambil atribut, hasil ke `DataFrame`, etika (`robots.txt`, syarat layanan, jeda antar request)
- **Fokus ujian:** mengumpulkan dataset kecil dari halaman statis secara etis

## 🗄️ SQL & Database Fundamentals

#### `sql_select_where` — SELECT, WHERE, ORDER BY
- **Wajib:** `SELECT` kolom dan `*`, alias `AS`, `DISTINCT`, `WHERE` (`=`, `<>`, `<`, `>`, `AND`/`OR`/`NOT`, `IN`, `BETWEEN`, `LIKE`, `IS NULL`), `ORDER BY ASC/DESC`, `LIMIT`
- **Fokus ujian:** menerjemahkan pertanyaan bisnis menjadi query filter

#### `sql_groupby_agg` — GROUP BY & Aggregation
- **Wajib:** `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, hitung unik (`COUNT(DISTINCT kolom)`), `GROUP BY`, `HAVING` vs `WHERE`
- **Fokus ujian:** ringkasan per kelompok, setara dengan `groupby` + `agg` di Pandas

#### `sql_join_subquery` — JOIN & Subquery Dasar
- **Wajib:** `INNER JOIN`, `LEFT JOIN`, konsep `RIGHT`/`FULL JOIN`, alias tabel, kunci join, subquery di `WHERE` dan `FROM`
- **Fokus ujian:** menggabungkan tabel dengan benar dan mendeteksi baris yang hilang/duplikat

#### `sql_relational_sqlite` — Relational Database & SQLite
- **Wajib:** tabel, baris, kolom, primary key, foreign key, relasi one-to-many, intuisi normalisasi, `CREATE TABLE`, `INSERT`, `UPDATE`, `DELETE`, `sqlite3` di Python (`connect`, `execute`, parameter `?`), `pd.read_sql_query`, `DataFrame.to_sql`
- **Fokus ujian:** merancang skema kecil dan mengisinya dari Python

#### `sql_postgresql` — PostgreSQL Fundamentals
- **Wajib:** instalasi dan klien (`psql` atau pgAdmin), tipe data umum, perbedaan utama dengan SQLite, koneksi dari Python (psycopg atau SQLAlchemy), memuat CSV ke tabel
- **Fokus ujian:** menjalankan analisis yang sama di PostgreSQL

## 📐 Statistika Terapan untuk Analisis

Rujukan: [SciPy — Statistical functions (`scipy.stats`)](https://docs.scipy.org/doc/scipy/reference/stats.html) dan [pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html). Ditambahkan 2026-10-30. Teori dan rumus diperdalam di World 3 (Statistics, Probability); di sini fokusnya memakai statistik untuk menjawab pertanyaan data.

#### `stat_terapan_deskriptif` — Ringkasan & Perbandingan Kelompok
- **Wajib:** mean vs median pada data skewed, persentil dan IQR (`quantile`), deteksi outlier dengan aturan 1.5×IQR, proporsi dan persentase (`value_counts(normalize=True)`), rasio dan pertumbuhan (`pct_change`, MoM/YoY), segmentasi dengan `groupby` + `describe`, tabulasi silang (`pd.crosstab` dengan `normalize`), memilih ringkasan berdasarkan bentuk distribusi
- **Fokus ujian:** memilih ringkasan yang jujur untuk data nyata dan menjelaskan perbedaan antar kelompok

#### `stat_terapan_inferensi` — Sampel, Confidence Interval & Uji Hipotesis Dasar
- **Wajib:** populasi vs sampel dan sampling error, confidence interval untuk mean (rumus dan bootstrap dengan NumPy), hipotesis nol dan alternatif, p-value dan tingkat signifikansi (termasuk salah kaprah umumnya), uji t dua kelompok (`scipy.stats.ttest_ind` dengan `equal_var=False`), uji chi-square untuk tabel kontingensi (`scipy.stats.chi2_contingency`), A/B test sederhana (metrik, pembagian grup, membaca hasil), signifikan secara statistik vs penting secara praktis
- **Fokus ujian:** menyimpulkan perbedaan dua kelompok dengan benar dan jujur tentang ketidakpastian

## 🤖 AI untuk Pekerjaan Data

#### `ai_python_sql` — AI-assisted Python & SQL
- **Wajib:** memberi konteks yang cukup (skema tabel, contoh data, output yang diharapkan), meminta kode Python/SQL, membaca dan menjelaskan ulang kode hasil AI, menguji pada data kecil, membandingkan dengan solusi sendiri
- **Fokus ujian:** menemukan kesalahan pada kode hasil AI

#### `ai_debugging` — Debugging dengan AI
- **Wajib:** menyertakan traceback lengkap, membuat contoh minimal yang bisa diulang, meminta penjelasan penyebab (bukan hanya perbaikan), memverifikasi perbaikan
- **Fokus ujian:** memperbaiki bug sambil menjelaskan akar masalahnya

#### `ai_eda_cleaning` — AI untuk EDA & Data Cleaning
- **Wajib:** meminta rencana EDA dan checklist kualitas data, memvalidasi setiap klaim AI dengan Pandas sendiri, mengenali angka/kolom yang dikarang AI, mencatat keputusan cleaning
- **Fokus ujian:** EDA dibantu AI dengan semua klaim terverifikasi

#### `ai_viz_docs_insight` — AI untuk Visualisasi, Dokumentasi & Insight
- **Wajib:** meminta usulan jenis grafik lalu menilainya, membuat README/dokumentasi, draft insight dengan kerangka *Observation → Interpretation → Implication → Next Question*, human validation sebelum dipakai
- **Fokus ujian:** insight yang bisa dipertanggungjawabkan dari data

## 🗣️ Data Storytelling & Komunikasi Insight

Ditambahkan 2026-10-30. Rujukan utama: dokumentasi Matplotlib untuk anotasi ([Annotations](https://matplotlib.org/stable/users/explain/text/annotations.html)); bacaan pendukung yang disarankan ada di `docs/sumber-belajar.md`.

#### `story_struktur_insight` — Struktur Insight & Laporan
- **Wajib:** merumuskan pertanyaan bisnis dan audiens, struktur laporan (ringkasan eksekutif → temuan → rekomendasi → keterbatasan), judul berbentuk insight (bukan sekadar nama variabel), angka yang bermakna (pembanding, konteks, satuan), rekomendasi yang bisa ditindaklanjuti, menyebut keterbatasan data dan analisis
- **Fokus ujian:** mengubah hasil analisis menjadi ringkasan satu halaman yang bisa dipahami non-teknis

#### `story_visual_penjelas` — Grafik yang Menjelaskan
- **Wajib:** memilih grafik sesuai pesan (perbandingan, tren, komposisi, distribusi, hubungan), decluttering (grid, spines, legend seperlunya), warna untuk penekanan (satu warna aksen), anotasi (`ax.annotate`, `ax.axhline`, `ax.text`), urutan kategori yang bermakna, mengenali grafik menyesatkan (sumbu terpotong, dual axis, pie berlebihan), menyusun 3–5 grafik menjadi satu alur cerita
- **Fokus ujian:** merombak grafik eksplorasi menjadi grafik laporan yang langsung menyampaikan pesan

## 📊 Portfolio #1

#### `portfolio_1` — Portfolio #1: Data Analysis Report
- **Wajib:** dataset publik, cleaning, EDA, visualisasi (Matplotlib/Seaborn), insight, notebook rapi, README (masalah, keputusan, keterbatasan), publikasi di GitHub
- **Fokus penilaian:** rubrik portfolio di `system/03_rubrik_validasi.md`

---

# 🌍 WORLD 3 — MATHEMATICS & STATISTICS FOR DATA/AI

#### `la_vektor_matriks` — Vektor, Matriks & Operasinya
- **Wajib:** vektor dan matriks sebagai array NumPy, penjumlahan dan perkalian skalar, perkalian matriks, transpose, matriks identitas dan invers (intuisi)
#### `la_dot_product` — Dot Product
- **Wajib:** dot product, panjang vektor (norm), intuisi sudut dan kemiripan, perkalian matriks–vektor sebagai transformasi
#### `la_eigen` — Intuisi Eigenvalue & Eigenvector
- **Wajib:** arti eigenvector dan eigenvalue secara visual, `np.linalg.eig`, kaitannya dengan PCA

#### `calc_derivative` — Derivative
- **Wajib:** turunan sebagai kemiringan, aturan dasar (pangkat, konstanta, jumlah), turunan numerik dengan NumPy
#### `calc_gradient` — Gradient & Intuisi Optimization
- **Wajib:** turunan parsial, vektor gradien, arah penurunan tercepat, visualisasi permukaan fungsi

#### `stat_deskriptif` — Statistik Deskriptif
- **Wajib:** mean, median, modus, variance, standard deviation, kuartil/IQR, outlier
#### `stat_distribusi_sampling` — Distribusi & Sampling
- **Wajib:** distribusi normal, uniform, binomial, populasi vs sampel, sampling acak dengan NumPy, intuisi Central Limit Theorem lewat simulasi
#### `stat_korelasi_kovarians` — Korelasi & Kovarians
- **Wajib:** kovarians, korelasi Pearson, `df.corr()`, korelasi ≠ kausalitas, visualisasi dengan scatter/heatmap

#### `prob_dasar` — Probability Basics
- **Wajib:** ruang sampel, kejadian, aturan penjumlahan dan perkalian, kejadian saling lepas dan independen, simulasi peluang
#### `prob_bersyarat_bayes` — Conditional Probability & Bayes
- **Wajib:** peluang bersyarat, tabel kontingensi, teorema Bayes, contoh tes diagnostik/klasifikasi spam

#### `optimization` — Optimization (Gradient Descent)
- **Wajib:** fungsi loss, minimisasi loss, gradient descent dari nol dengan NumPy, learning rate dan konvergensi

#### `ai_literacy` — AI Literacy
- **Wajib:** bagaimana model belajar dari data, alur data → model → prediction, training vs inference, kenapa evaluasi penting

#### `portfolio_math` — Portfolio: Notebook Eksplorasi Matematika/Statistika
- **Wajib:** satu notebook (misalnya gradient descent sederhana, simulasi distribusi, atau Bayes) dengan penjelasan dan visualisasi

---

# 🌍 WORLD 4 — MACHINE LEARNING FUNDAMENTAL

Rujukan: [scikit-learn — Model selection and evaluation](https://scikit-learn.org/stable/model_selection.html) (dibaca 2026-10-29).

#### `mlf_konsep` — Konsep Machine Learning
- **Wajib:** supervised vs unsupervised, fitur dan target, train/validation/test, overfitting dan underfitting, intuisi bias–variance, data leakage
#### `mlf_preprocessing` — Data Preprocessing & Feature Engineering
- **Wajib:** menangani missing values, scaling (`StandardScaler`, `MinMaxScaler`), encoding (`OneHotEncoder`, `OrdinalEncoder`), membuat fitur baru, pemilihan fitur dasar

#### `sl_regresi_linear` — Linear Regression
- **Wajib:** `LinearRegression`, koefisien dan intercept, asumsi dasar, interpretasi
#### `sl_logistic` — Logistic Regression
- **Wajib:** `LogisticRegression`, probabilitas kelas, `predict_proba`, threshold keputusan
#### `sl_tree_forest` — Decision Tree & Random Forest
- **Wajib:** `DecisionTreeClassifier/Regressor`, `max_depth`, `RandomForestClassifier/Regressor`, `n_estimators`, feature importance
#### `sl_knn_svm` — KNN & SVM
- **Wajib:** `KNeighborsClassifier` (`n_neighbors`, pentingnya scaling), `SVC` (`kernel`, `C`) secara intuitif

#### `ul_kmeans` — K-Means
- **Wajib:** `KMeans`, memilih jumlah cluster (elbow, silhouette), interpretasi cluster
#### `ul_pca` — PCA
- **Wajib:** `PCA`, `explained_variance_ratio_`, reduksi dimensi untuk visualisasi

#### `ev_klasifikasi` — Evaluasi Klasifikasi
- **Wajib:** accuracy, precision, recall, F1-score, `confusion_matrix`, `classification_report`, kapan accuracy menyesatkan (data tidak seimbang)
#### `ev_regresi` — Evaluasi Regresi
- **Wajib:** MAE, MSE, RMSE, R²
#### `ev_cross_validation` — Cross-validation
- **Wajib:** `cross_val_score`, `KFold`, `StratifiedKFold`, membandingkan model secara adil

#### `sk_api_pipeline` — Scikit-learn API & Pipeline
- **Wajib:** pola `fit`/`predict`/`transform`, `Pipeline`, `ColumnTransformer`, mencegah leakage dengan pipeline
#### `sk_model_selection` — Model Selection
- **Wajib:** `train_test_split` (`stratify`, `random_state`), `GridSearchCV`, `RandomizedSearchCV`, memilih metrik `scoring`

#### `se_struktur_modular` — Struktur Proyek & Kode Modular
- **Wajib:** struktur folder proyek ML (`data/`, `notebooks/`, `src/`, `tests/`, `models/`), fungsi yang bisa dipakai ulang, file konfigurasi, `requirements.txt`
#### `se_testing_logging` — Testing, Logging & Reproducibility
- **Wajib:** tes dasar (`unittest`/`pytest`), `logging`, environment variables, alur Git (branch, commit kecil), reproducibility (seed, versi paket)

#### `portfolio_2` — Portfolio #2: Prediction / Classification Model
- **Wajib:** problem → data → preprocessing → feature engineering → training → evaluation → interpretasi; notebook, source code rapi, model, README

---

# 🌍 WORLD 5 — DEEP LEARNING & NEURAL NETWORK

Rujukan: [PyTorch — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html) (dibaca 2026-10-29). Kurikulum memakai **PyTorch** sebagai framework utama; bila Rafa memilih TensorFlow/Keras, quest `fw_*` disesuaikan dengan persetujuannya.

#### `nn_perceptron_mlp` — Perceptron & MLP
- **Wajib:** perceptron, layer, neuron, bobot dan bias, MLP, fungsi aktivasi (sigmoid, ReLU, softmax)
#### `nn_forward_backprop` — Forward Propagation, Loss & Backpropagation
- **Wajib:** forward pass, fungsi loss (MSE, cross-entropy), backpropagation secara intuitif, implementasi jaringan kecil dengan NumPy

#### `dl_cnn` — CNN
- **Wajib:** konvolusi, filter, pooling, arsitektur CNN sederhana untuk gambar
#### `dl_rnn_lstm` — RNN/LSTM (konseptual)
- **Wajib:** data berurutan, ide RNN, masalah vanishing gradient, LSTM secara konsep
#### `dl_transformer_attention` — Transformer & Attention
- **Wajib:** self-attention, query/key/value secara intuitif, arsitektur Transformer tingkat tinggi
#### `dl_transfer_learning` — Transfer Learning
- **Wajib:** model pretrained, feature extraction vs fine-tuning, kapan transfer learning tepat

#### `fw_tensor_autograd` — Tensor & Autograd
- **Wajib:** tensor PyTorch, operasi dan device (CPU/GPU), `requires_grad`, `backward()`, `torch.no_grad()`
#### `fw_training_loop` — Dataset, Model & Training Loop
- **Wajib:** `Dataset`, `DataLoader`, transforms, `nn.Module`, loss function, optimizer, training loop, evaluasi, `torch.save`/`load`

#### `portfolio_3` — Portfolio #3: Image / Text Classifier
- **Wajib:** workflow deep learning lengkap dengan model pretrained/transfer learning, evaluasi, README

---

# 🌍 WORLD 6 — GENERATIVE AI & AI-ENHANCED DATA WORKFLOW

#### `gf_llm_token_embedding` — LLM, Tokenization, Embedding & Context Window
- **Wajib:** apa itu LLM, token dan tokenisasi, embedding, context window dan batasnya
#### `gf_attention_generation` — Attention & Autoregressive Generation
- **Wajib:** attention secara intuitif, generasi token demi token, temperature, training vs inference
#### `gf_prompting_rag_ft` — Prompting vs RAG vs Fine-tuning
- **Wajib:** kapan memakai prompting vs RAG vs fine-tuning, multimodal AI secara konsep

#### `pc_prompting` — Prompting
- **Wajib:** zero-shot, few-shot, instruksi system vs user, structured output, output JSON, iterasi prompt
#### `pc_context` — Context Engineering
- **Wajib:** memilih konteks, kualitas konteks, conversation state, memory secara konsep, retrieval context, hasil tool sebagai konteks

#### `api_dasar` — LLM API Dasar
- **Wajib:** request/response, autentikasi dengan API key di environment variable, error handling dan retry, streaming secara konsep, token usage, kesadaran biaya
#### `api_structured_coding` — Structured Responses & AI Coding Workflow
- **Wajib:** respons terstruktur (JSON schema), validasi output, AI coding workflow: Python, SQL, debugging, refactoring, dokumentasi, bantuan riset

#### `rag_konsep` — Konsep RAG
- **Wajib:** embedding, chunking, retrieval, vector search, context injection
#### `rag_pipeline` — RAG Pipeline
- **Wajib:** pipeline RAG dengan FAISS atau Chroma + satu framework orkestrasi, RAG-based Q&A untuk dokumen kuliah/data/report

#### `wa_workflow` — AI Workflow Deterministik
- **Wajib:** pola Input → LLM → Tool → LLM → Output, kapan workflow lebih tepat daripada agent
#### `wa_agent` — AI Agent Dasar
- **Wajib:** tool/function calling, pemilihan tool, multi-step task, state agent dasar, membuat agent sederhana

#### `auto_konsep_n8n` — AI Automation dengan n8n/Make
- **Wajib:** workflow automation, pola Trigger → AI → Action, membuat workflow di n8n atau Make
#### `auto_integrasi` — Integrasi API & Human Approval
- **Wajib:** integrasi API, workflow pemrosesan data, langkah human approval sederhana

#### `ai_evaluation` — AI Evaluation
- **Wajib:** test cases, golden examples, expected output, accuracy/relevance, failure analysis, regression testing sederhana

#### `guardrails_hitl` — Guardrails & Human-in-the-loop
- **Wajib:** kesadaran izin, batas data, pembatasan tool, human approval, fallback, prompt injection, validasi sebelum aksi

#### `observability` — Observability
- **Wajib:** logging, error, latency, token/biaya, mencatat tool call, konsep tracing dasar

#### `mcp` — MCP
- **Wajib:** arsitektur host/client/server, primitive (tools, resources, prompts), transport (stdio, HTTP), prototype server sederhana
- Rujukan: [The Complete Guide to Model Context Protocol](https://machinelearningmastery.com/the-complete-guide-to-model-context-protocol/) (dibaca 2026-10-29); untuk implementasi gunakan dokumentasi resmi MCP

#### `dep_streamlit` — Deployment dengan Streamlit
- **Wajib:** aplikasi Streamlit (input, tabel, grafik), state sederhana, deploy ke Streamlit Community Cloud
#### `dep_api_hosting` — API Dasar & Hosting
- **Wajib:** API dasar (misalnya FastAPI), environment variables dan secrets, hosting/deployment dasar

#### `capstone` — Capstone: AI-Enhanced Data Workflow
- **Wajib:** aplikasi/workflow yang berjalan, README profesional, diagram arsitektur, contoh evaluasi, failure cases, demo, repo GitHub

---

## Celah yang ditemukan saat riset (belum masuk kurikulum)

Daftar ini **bukan** bagian kurikulum wajib. Masuk hanya bila Rafa menyetujui.

| Usulan | Posisi | Alasan |
|---|---|---|
| SQL window functions (`ROW_NUMBER`, `RANK`, `SUM() OVER`) dan CTE (`WITH`) | SQL, setelah `sql_join_subquery` | Sering muncul di pekerjaan dan tes teknis Data Analyst |
| Pandas time series (`to_datetime`, `resample`, `rolling`) | Retrieval Pandas atau sebelum Portfolio #1 | Banyak dataset bisnis berbasis waktu |

Uji hipotesis dasar (t-test, p-value, confidence interval) yang sebelumnya tercatat di sini sudah masuk sebagai `stat_terapan_inferensi` (2026-10-30).

## Sumber yang dibaca saat menyusun (2026-10-29)

- [seaborn API reference](https://seaborn.pydata.org/api)
- [scikit-learn — Model selection and evaluation](https://scikit-learn.org/stable/model_selection.html)
- [PyTorch — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)
- [pandas User Guide (daftar isi)](https://pandas.pydata.org/docs/_sources/user_guide/index.rst.txt)
- [The Complete Guide to Model Context Protocol](https://machinelearningmastery.com/the-complete-guide-to-model-context-protocol/)

Modul lain disusun dari isi Roadmap v2 dan rujukan yang direkomendasikan di `system/06_kebijakan_referensi.md`; sumbernya belum dibaca ulang untuk dokumen ini.
