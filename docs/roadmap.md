# 🌳 Learn A.I Workflow for Data Science — Roadmap v2

> **Target utama:** menjadi **Data Scientist / Data Analyst yang AI-native** — kuat di Data Science/Data Analytics dan sangat familiar dengan AI sebagai force multiplier untuk pekerjaan nyata.

---

# 🎯 TARGET PROFESIONAL

```text
             🎯 DATA PROFESSIONAL
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
   📊 Data Science       📈 Data Analytics
          │                   │
          └─────────┬─────────┘
                    ↓
             🤖 AI POWER USER
                    │
          ┌─────────┼─────────┐
          ↓         ↓         ↓
       GenAI      AI Tools   Automation
          │         │         │
          └─────────┴─────────┘
                    ↓
        🚀 AI-ENHANCED DATA PROFESSIONAL
```

### Prinsip utama

> **AI sebagai force multiplier, bukan pengganti fondasi Data.**

Prioritas:

1. 📊 Data Science
2. 📈 Data Analytics
3. 🤖 AI Literacy
4. ⚙️ Practical AI Automation
5. 💻 Software Engineering secukupnya
6. 🧠 AI Engineering hanya pada level foundation/application

---

# 🌍 FASE 1 — PYTHON FOUNDATION

## 🎯 Tujuan

Memiliki fondasi Python yang cukup kuat untuk bekerja dengan data, membuat program, dan memahami code yang dihasilkan AI.

### Materi inti

- Python syntax & fundamentals
- Variables & data types
- Operators
- Conditional
- Loop
- Function
- Data structures
  - List
  - Tuple
  - Dictionary
  - Set
- String manipulation
- Comprehension
- Function arguments
- Module & import
- Error handling
- File I/O
- Virtual environment & pip
- OOP dasar

### 💻 Software Engineering — exposure ringan

- Clean code dasar
- Modular code
- Struktur file sederhana
- Git & GitHub
- `.gitignore`
- README dasar

> Tidak perlu mempelajari software architecture secara mendalam pada fase ini.

### 🏗️ Project

**Python Mini Project**

Contoh:
- CLI data tracker
- Expense/income tracker
- Simple data management tool

---

# 🌍 FASE 2 — DATA SCIENCE & DATA ANALYTICS

## 🎯 Tujuan

Mampu mengambil, membersihkan, mengeksplorasi, menganalisis, dan memvisualisasikan data.

---

## 📦 NumPy

- Array
- Shape & dimension
- Indexing & slicing
- Reshape
- Broadcasting
- Vectorization
- Universal functions
- Statistical operations
- Searching
- Sorting
- Array manipulation
- Aggregation
- Linear algebra dasar
- Random
- File I/O
- Performance dasar
- NumPy Capstone

**Status:** mengikuti validasi progres aktual, bukan asumsi.

---

## 🐼 Pandas

### Fundamentals
- Series
- DataFrame
- Creating Data
- Index
- Columns
- Shape
- head()
- tail()
- info()
- describe()

### Data Selection
- Single column
- Multiple column
- iloc()
- loc()

### Filtering
- Comparison operators
- Single condition
- Multiple conditions
- isin()
- between()
- query()

### Manipulasi Data
- Column manipulation
- Row manipulation
- Missing values
- Sorting

### Statistics
- mean()
- sum()
- count()
- min()
- max()
- median()
- mode()
- std()
- value_counts()

### Grouping & Combining
- groupby()
- agg()
- Multiple aggregation
- merge()
- concat()
- join()

### Import / Export
- CSV
- Excel
- JSON

### 👑 Pandas Capstone

Analisis dataset publik secara end-to-end.

---

## 📊 Visualization

### Matplotlib

- Line plot
- Bar plot
- Histogram
- Scatter plot
- Subplots
- Styling & labels
- Figure & Axes
- Boxplot
- Errorbar
- Axis limits & scale
- Legend & tick formatting
- savefig()

### Seaborn

- Statistical visualization
- Distribution plots
- Categorical plots
- Relationship plots
- Heatmap
- Pairplot

### Jupyter / Google Colab

- Notebook workflow
- Markdown
- Reproducibility
- Kernel/runtime basics

### 🌐 Web Scraping

**Optional**

- requests
- BeautifulSoup
- Mengambil dataset sederhana dari web

---

## 🗄️ SQL & Database Fundamentals

**Ditambahkan karena relevan langsung dengan Data Analyst/Data Scientist.**

- SELECT
- WHERE
- ORDER BY
- GROUP BY
- Aggregation
- JOIN
- Subquery dasar
- Relational database concepts
- SQLite
- PostgreSQL fundamentals

> Tidak diarahkan menjadi Database Engineer.

---

## 🤖 AI untuk Pekerjaan Data — Level Familiar

Mulai mengenal AI sebagai alat kerja:

- AI-assisted Python
- AI-assisted SQL
- Debugging dengan AI
- Membantu EDA
- Membantu data cleaning
- Membantu visualisasi
- Membantu dokumentasi
- Membantu draft insight

**Human validation tetap wajib.**

### 🏗️ Portfolio Project #1

**Data Analysis Report**

```text
Dataset
 ↓
Cleaning
 ↓
EDA
 ↓
Visualization
 ↓
Insight
 ↓
Report / Dashboard
```

**Deliverable:**
- Notebook
- README
- Laporan/dashboard sederhana
- Insight utama

---

# 🌍 FASE 3 — MATHEMATICS & STATISTICS FOR DATA/AI

## 🎯 Tujuan

Memahami logika statistik dan matematika yang benar-benar diperlukan untuk Data Science dan AI tanpa berubah menjadi spesialis matematika.

### Linear Algebra

- Vector
- Matrix
- Dot product
- Matrix operations
- Transpose
- Intuisi eigenvalue/eigenvector

### Calculus

- Derivative
- Gradient
- Intuisi optimization

### Statistics

- Mean
- Variance
- Standard deviation
- Distribution
- Sampling
- Correlation
- Covariance

### Probability

- Probability basics
- Conditional probability
- Bayes theorem

### Optimization

- Gradient descent
- Loss minimization

### 🧠 AI Literacy

Mulai memahami:

- Bagaimana model belajar
- Data → model → prediction
- Training vs inference
- Mengapa evaluation penting

### 🏗️ Portfolio

Tidak perlu project besar.

**Notebook eksplorasi matematika/statistika** cukup.

Contoh:
- Gradient descent sederhana
- Visualisasi distribusi
- Bayes theorem
- Simulasi statistik

---

# 🌍 FASE 4 — MACHINE LEARNING FUNDAMENTAL

## 🎯 Tujuan

Mampu membangun, mengevaluasi, dan menjelaskan model ML klasik untuk masalah Data Science.

### Machine Learning Fundamentals

- Supervised vs unsupervised learning
- Train/validation/test
- Overfitting & underfitting
- Bias/variance intuition
- Feature engineering
- Data preprocessing

### Supervised Learning

- Linear Regression
- Logistic Regression
- Decision Tree
- Random Forest
- KNN
- SVM

### Unsupervised Learning

- K-Means
- PCA

### Evaluation

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- Cross-validation
- Regression metrics

### Scikit-learn

- Pipeline dasar
- Model selection
- Preprocessing
- Training
- Evaluation

---

## 💻 Software Engineering — Formal Introduction

Mulai lebih serius, tetapi tetap sesuai kebutuhan Data:

- Project structure
- Modular Python
- Reusable functions
- Basic testing
- Configuration
- Requirements/dependencies
- Environment variables dasar
- Logging dasar
- Git workflow
- Reproducibility

Contoh:

```text
ml-project/
├── data/
├── notebooks/
├── src/
├── tests/
├── models/
├── README.md
├── requirements.txt
└── .gitignore
```

> Fase 4 adalah titik formal Software Engineering, tetapi bukan jalur Software Engineer penuh.

### 🏗️ Portfolio Project #2

**Prediction / Classification Model**

```text
Problem
 ↓
Data
 ↓
Preprocessing
 ↓
Feature Engineering
 ↓
Training
 ↓
Evaluation
 ↓
Interpretation
```

Deliverable:
- Notebook
- Source code yang rapi
- Model
- Evaluation
- README

---

# 🌍 FASE 5 — DEEP LEARNING & NEURAL NETWORK

## 🎯 Tujuan

Memahami neural network dan konsep modern AI secukupnya untuk menjadi Data Professional yang memahami teknologi di balik GenAI.

### Neural Network

- Perceptron
- MLP
- Forward propagation
- Backpropagation
- Loss function
- Activation function

### Deep Learning

- CNN
- RNN/LSTM secara konseptual
- Transformer & Attention
- Transfer learning

### Framework

Pilih salah satu sebagai utama:

- PyTorch
- TensorFlow/Keras

> Tidak perlu mendalami training foundation model dari nol.

### 🧠 Kedalaman yang DIKURANGI

Tidak menjadi fokus:

- Distributed training
- CUDA optimization tingkat lanjut
- Training LLM from scratch
- Advanced research architecture

### 🏗️ Portfolio Project #3

**Image/Text Classifier**

Tujuan utama:

- memahami workflow deep learning,
- training,
- evaluation,
- dan penggunaan model pretrained/transfer learning.

---

# 🌍 FASE 6 — GENERATIVE AI & AI-ENHANCED DATA WORKFLOW

## 🎯 Tujuan

Menjadi sangat familiar dengan AI generatif dan mampu memanfaatkannya untuk pekerjaan Data Science/Data Analytics.

> Ini bukan fase untuk menjadi AI Infrastructure Engineer.

---

## 6A — Generative AI Fundamentals

- Apa itu LLM
- Tokenization
- Embedding
- Context window
- Attention
- Autoregressive generation
- Training vs inference
- Prompting vs RAG vs fine-tuning
- Multimodal AI secara konsep

---

## 6B — Prompt & Context Engineering

### Prompting

- Zero-shot
- Few-shot
- System/user instructions
- Structured output
- JSON output
- Prompt iteration

### Context

- Context selection
- Context quality
- Conversation state
- Memory secara konsep
- Retrieval context
- Tool results

> Fokusnya bukan membuat prompt yang “keren”, tetapi menghasilkan output yang berguna dan dapat divalidasi.

---

## 6C — LLM API

- API request/response
- Authentication
- Error handling
- Streaming secara konsep
- Token usage
- Cost awareness
- Structured responses

### AI Coding Workflow

- AI-assisted Python
- AI-assisted SQL
- Debugging
- Refactoring
- Documentation
- Research assistance

---

## 6D — RAG

### Konsep

- Embedding
- Chunking
- Retrieval
- Vector search
- Context injection
- RAG pipeline

### Tools

Pilih seperlunya:

- FAISS / Chroma
- Satu framework orchestration yang relevan

Tidak perlu mengejar banyak framework sekaligus.

### Project

**RAG-based Q&A System**

Contoh:
> Chatbot untuk dokumen kuliah/data/report.

---

## 6E — AI Workflow vs AI Agent

### Workflow

Pahami kapan workflow deterministik lebih tepat:

```text
Input
 ↓
LLM
 ↓
Tool
 ↓
LLM
 ↓
Output
```

### Agent

Pahami:

```text
Goal
 ↓
LLM
 ↓
Decide
 ↓
Tool
 ↓
Observe
 ↓
Decide
 ↓
Finish
```

### Agent Skills — Foundation

- Tool calling
- Function calling
- Tool selection
- Multi-step task
- Basic agent state

**Target:** mampu membuat agent sederhana, bukan production-grade agent infrastructure.

---

## 6F — AI Automation

Ini salah satu skill bernilai tinggi untuk target karier.

- Workflow automation
- Trigger → AI → Action
- n8n / Make
- API integration
- Data processing workflow
- Human approval sederhana

Contoh:

```text
Data masuk
 ↓
Python / SQL
 ↓
AI analysis
 ↓
Human validation
 ↓
Report
```

atau:

```text
File masuk
 ↓
Automation
 ↓
AI membaca
 ↓
Insight
 ↓
Report / Notification
```

---

## 6G — AI Evaluation

Wajib memahami konsep:

- Test cases
- Golden examples
- Expected output
- Accuracy/relevance
- Failure analysis
- Regression testing sederhana

Prinsip:

> **AI output tidak dianggap benar hanya karena terlihat meyakinkan.**

---

## 6H — Guardrails & Human-in-the-loop

Level praktis:

- Permission awareness
- Data boundaries
- Tool restrictions
- Human approval
- Fallback
- Prompt injection awareness
- Validation sebelum action

Tidak perlu mendalami AI safety engineering secara akademis.

---

## 6I — Observability

Cukup memahami dan menerapkan dasar:

- Logging
- Errors
- Latency
- Token/cost awareness
- Tool calls
- Basic tracing concept

Tujuannya agar dapat menjawab:

> “Kalau workflow AI gagal, gagal di mana?”

---

## 6J — MCP

**Familiarity + prototype level.**

- Apa itu MCP
- Server/client concept
- Tools/resources concept
- Menghubungkan AI dengan external tools/data
- Prototype sederhana

Tidak perlu mendalami implementasi protocol tingkat rendah.

---

## 6K — Deployment

Level practical:

- Streamlit
- API dasar
- Environment variables
- Basic hosting/deployment

Tidak mengejar:

- Kubernetes
- Distributed infrastructure
- Advanced DevOps

---

# 👑 FASE 6 CAPSTONE

## AI-Enhanced Data Workflow

Capstone tidak lagi sekadar:

> “Aku membuat AI Agent.”

Tetapi harus menunjukkan bagaimana AI **meningkatkan pekerjaan Data**.

Contoh:

```text
Raw Data
   ↓
Cleaning / SQL / Python
   ↓
EDA
   ↓
AI-assisted analysis
   ↓
Validation
   ↓
Insight
   ↓
Automated Report
```

Level lanjutan:

```text
Dataset / User Request
        ↓
AI Workflow
        ↓
Tool Calling
        ↓
Data Analysis
        ↓
AI Interpretation
        ↓
Evaluation
        ↓
Human Approval
        ↓
Report / Dashboard
```

### Deliverable

- Working application/workflow
- README profesional
- Architecture diagram
- Evaluation examples
- Failure cases
- Demo
- GitHub repository

---

# 🏗️ PORTFOLIO ROADMAP

```text
Fase 1–2
📊 Data Analysis Report
        ↓
Fase 3
📈 Mathematics / Statistics Notebook
        ↓
Fase 4
🤖 ML Prediction / Classification
        ↓
Fase 5
🧠 Deep Learning Classifier
        ↓
Fase 6
📚 RAG Application
        ↓
⚙️ AI-Enhanced Data Workflow
        ↓
👑 CAPSTONE
```

Portfolio harus semakin mendekati target karier:

```text
📊 Data Analysis
       ↓
🤖 ML
       ↓
🧠 Neural Network
       ↓
💬 LLM Application
       ↓
📚 RAG
       ↓
⚙️ AI Workflow
       ↓
👑 AI-Enhanced Data Professional
```

---

# 💻 SOFTWARE ENGINEERING LAYER

Software Engineering bukan fase tersendiri.

Ia menjadi skill transversal:

```text
Fase 1
🟢 Exposure
├── Git
├── GitHub
├── clean code
└── modular code

Fase 2
🟢 Practical
├── repository structure
├── environment
└── reproducibility

Fase 3
🟡 Basic
├── testing
└── clean/reproducible notebook

Fase 4
🟠 Formal
├── project structure
├── tests
├── configuration
├── logging
└── reusable modules

Fase 5
🟠 Applied
└── maintainable ML/DL project

Fase 6
🟠 Practical AI
├── API
├── services
├── environment variables
└── basic deployment
```

### Tidak menjadi target utama

```text
❌ Microservices
❌ Kubernetes
❌ Distributed systems
❌ Advanced CI/CD
❌ Complex design patterns
❌ Advanced DevOps
❌ High-scale backend architecture
```

---

# 📚 REVIEW QUEUE

Review Queue tetap terpisah dari roadmap utama.

Materi yang sudah tervalidasi:

- ✅ Error Handling
- ✅ File I/O
- ✅ Virtual Environment & pip

Jika queue selesai:

> 🏆 REVIEW QUEUE COMPLETED

Tidak aktif lagi sampai dibuat queue baru.

---

# 🏗️ PORTFOLIO LOCK

Portfolio World 1 tetap:

```text
📊 Data Analysis Report
└── 🔒 LOCKED
```

Unlock requirement:

```text
Fase 2 — Python untuk Data
        ↓
100% COMPLETED
        ↓
Portfolio World 1 UNLOCKED
```

---

# 🧭 ATURAN PRIORITAS ROADMAP

Setiap kali mentor mengevaluasi roadmap:

1. **Relevansi karier**
2. **Fondasi Data**
3. **AI literacy**
4. **Practical leverage**
5. **Automation**
6. **Software Engineering secukupnya**
7. **Gamifikasi**

Prinsip:

> **Pelajari sedalam yang memberikan leverage terhadap karier Data Science/Data Analyst — jangan belajar teknologi hanya karena terlihat keren.**

---

# 🔎 ATURAN AUDIT ROADMAP

Sebelum materi baru ditambahkan:

```text
Roadmap saat ini
      ↓
Riset kebutuhan skill/tools
      ↓
Bandingkan dengan roadmap
      ↓
Identifikasi gap
      ↓
Nilai relevansi
      ↓
Rekomendasi mentor
      ↓
Persetujuan pengguna
      ↓
Baru menjadi bagian roadmap
```

Roadmap tidak boleh diperbesar hanya karena teknologi baru sedang populer.

---

# 🧠 TARGET AKHIR

> **Become a strong Data Professional who uses AI as a force multiplier.**

Bukan:

> AI Engineer yang kebetulan bisa Data Science.

Tetapi:

> **Data Scientist / Data Analyst yang sangat familiar dengan AI, mampu menggunakannya secara kritis, dan dapat mengubah AI menjadi leverage nyata dalam pekerjaan Data.**