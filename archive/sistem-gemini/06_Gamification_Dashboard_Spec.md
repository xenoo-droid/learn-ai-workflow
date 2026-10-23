# Gamification & Dashboard Specification

## Purpose
Gamification is a motivation and communication layer. It must not replace evidence-based tracking.

## Architectural Rule
```text
Validated Progress State = Source of Truth
            ↓
Dashboard reads the state
            ↓
Dashboard displays progression
```

The dashboard must never invent, infer, or overwrite progress.

## Current Approved Style
Use the approved consolidated **skill-tree / world-map ASCII text dashboard** template below.

Core presentation pattern:
- Worlds represent major roadmap phases.
- Modules appear under their world.
- Current quest is clearly marked.
- Next quest is shown separately.
- Completed milestones use clear completion markers.
- Locked content remains visibly locked.

## Approved Dashboard Template
```text
🌳 LEARN A.I WORKFLOW FOR DATA SCIENCE
🎯 TARGET: AI-ENHANCED DATA PROFESSIONAL

═══════════════════════════════════════════════════

🌍 WORLD 1 — PYTHON FOUNDATION                         🏆 CLEARED
│
├── 🐍 Python Fundamentals                            ✅
├── 🧩 Data Structures                                ✅
├── ⚙️ Functions & Modules                            ✅
├── 🛡️ Error Handling                                 ✅
├── 📂 File I/O                                       ✅
├── 🔧 Virtual Environment & pip                      ✅
└── 🏆 PYTHON FOUNDATION                              ✅ COMPLETED

═══════════════════════════════════════════════════

🌍 WORLD 2 — DATA SCIENCE & DATA ANALYTICS            ⚔️ IN PROGRESS
│
├── 📦 NUMPY                                          🏆 COMPLETED
│
├── 🐼 PANDAS                                         🏆 COMPLETED
│
└── 📈 MATPLOTLIB                                     ⚔️ BOSS BATTLE
    │
    ├── 📉 Pengenalan & Line Plot                     ✅ COMPLETED
    ├── 📊 Bar Plot                                   ✅ COMPLETED
    ├── 📊 Histogram                                  ✅ COMPLETED
    ├── 🔵 Scatter Plot                               ✅ VALIDATED
    ├── 🧩 Subplots                                   ✅ VALIDATED
    ├── 🎨 Styling & Labels                           ✅ VALIDATED
    ├── 🖼️ Figure & Axes                              ✅ VALIDATED
    ├── 📦 Boxplot                                    ✅ VALIDATED
    ├── 📏 Errorbar                                   ✅ VALIDATED
    ├── 📐 Axis Limits & Scale                        ✅ VALIDATED
    ├── 🏷️ Legend & Tick Formatting                   ✅ VALIDATED
    ├── 💾 savefig()                                  ✅ VALIDATED
    │
    └── 🏆 MATPLOTLIB REVIEW                          ⚔️ CURRENT QUEST ◀
         │
         ▼
    🎨 SEABORN                                        🔒 LOCKED
         │
         ▼
    🗄️ SQL & DATABASE FUNDAMENTALS                    🔒 LOCKED
         │
         ▼
    📊 PORTFOLIO #1 — DATA ANALYSIS REPORT            🔒 LOCKED

═══════════════════════════════════════════════════

🌍 WORLD 3 — MATHEMATICS & STATISTICS FOR DATA/AI     🔒 LOCKED
│
└── 🧮 Math • Statistics • Probability • Optimization

═══════════════════════════════════════════════════

🌍 WORLD 4 — MACHINE LEARNING FUNDAMENTAL             🔒 LOCKED
│
└── 🤖 ML Models • Evaluation • Scikit-learn

═══════════════════════════════════════════════════

🌍 WORLD 5 — DEEP LEARNING & NEURAL NETWORK           🔒 LOCKED
│
└── 🧠 Neural Network • CNN • Transformer

═══════════════════════════════════════════════════

🌍 WORLD 6 — GENERATIVE AI & AI WORKFLOW              🔒 LOCKED
│
└── 🚀 LLM • RAG • Agents • Automation • Capstone

═══════════════════════════════════════════════════

🎯 CURRENT QUEST : 🏆 Matplotlib Review
➡️ NEXT QUEST    : 🎨 Seaborn
🏆 LATEST WIN    : 💾 savefig() — COMPLETED / VALIDATED

📍 CURRENT POSITION
WORLD 2 → Matplotlib → 🏆 Matplotlib Review
═══════════════════════════════════════════════════
```

## Consistency Rule
Once a dashboard format is approved, do not change its structure or terminology without explicit user approval. If a different format seems useful, propose it first rather than silently replacing the existing one.


