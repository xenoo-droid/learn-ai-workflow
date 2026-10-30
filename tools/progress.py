#!/usr/bin/env python3
"""progress.py - penjaga aturan progres Learn A.I Workflow for Data Science.

Sumber kebenaran progres adalah state/state.yaml. Script ini satu-satunya
yang boleh mengubahnya (selain Rafa secara sadar). Mentor AI hanya
mengusulkan Evidence Entry; script memeriksanya terhadap
system/03_rubrik_validasi.md lalu memperbarui state.

Perintah:
    python tools/progress.py check              periksa konsistensi state
    python tools/progress.py dashboard [--tulis]  tampilkan dashboard (--tulis: simpan ke state/dashboard.md)
    python tools/progress.py due                daftar review yang jatuh tempo
    python tools/progress.py learned <id>       tandai quest aktif sudah dipelajari (belum diuji)
    python tools/progress.py apply <entri.yaml> [--dry]   terapkan Evidence Entry
    python tools/progress.py inbox [--dry]      terapkan semua entri di state/inbox/ (dipakai workflow GitHub)
    python tools/progress.py cakupan <id>       daftar item Wajib quest dari kurikulum (untuk kolom cakupan:)
    python tools/progress.py statistik          tren skor, percobaan per modul, dan konsep lemah

Opsi global: --root <folder repo>  --today YYYY-MM-DD
Kebutuhan: Python 3.9+ dan PyYAML (pip install pyyaml).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

import yaml

# --------------------------------------------------------------------------
# Aturan (selaras dengan system/03_rubrik_validasi.md)
# --------------------------------------------------------------------------
STATUS = ["belum", "aktif", "learned", "validated_legacy", "validated", "retained", "mastered"]
SELESAI = {"validated_legacy", "validated", "retained", "mastered"}
SEDANG = {"aktif", "learned"}  # status quest yang sedang dikerjakan
TIPE = {"materi", "review", "portfolio", "capstone"}
JENIS = {"validasi", "retrieval", "mastery"}
MODE_AI = {"independent", "assisted", "review"}
AMBANG = 80
JEDA_RETRIEVAL = 7
KONFIRMASI = 30
ULANG_GAGAL = 3
LEGACY_PER_SESI = 2
ID_ENTRI = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{2,79}$")  # dipakai sebagai nama file; tanpa titik/garis miring
BATAS_ENTRI_BYTE = 64 * 1024
LEVEL = ("L1", "L2", "L3")
# jumlah soal yang sah per (jenis ujian, tipe modul); lihat system/03_rubrik_validasi.md bagian 2 dan 5
JUMLAH_SOAL = {("validasi", "materi"): (3, 5), ("validasi", "review"): (3, 3), ("retrieval", None): (2, 3)}
TOLERANSI_SKOR = 1   # selisih pembulatan yang diizinkan antara skor_persen dan hitungan dari ujian
MIN_REVIEW = 2       # jumlah quest minimal di cakupan modul review bila kurikulum tidak menyebut "≥N"
BATAS_KONSEP_LEMAH = 15

# --------------------------------------------------------------------------
# Presentasi dashboard (bukan data progres, jadi tidak disimpan di state)
# --------------------------------------------------------------------------
IKON = {
    "python_fundamentals": "🐍", "data_structures": "🧩", "functions_modules": "⚙️",
    "error_handling": "🛡️", "file_io": "📂", "venv_pip": "🔧",
    "numpy": "📦", "pandas": "🐼", "matplotlib": "📈",
    "line_plot": "📉", "bar_plot": "📊", "histogram": "📊", "scatter_plot": "🔵",
    "subplots": "🧩", "styling_labels": "🎨", "figure_axes": "🖼️", "boxplot": "📦",
    "errorbar": "📏", "axis_limits_scale": "📐", "legend_tick_formatting": "🏷️",
    "savefig": "💾", "matplotlib_review": "🏆", "seaborn": "🎨", "sql_database": "🗄️",
    "portfolio_1": "📊",
    "seaborn_distribusi": "📊", "seaborn_categorical": "📦", "seaborn_relational": "🔵",
    "seaborn_regression": "📈", "seaborn_matrix": "🟥", "seaborn_grids": "🔗",
    "seaborn_aesthetics": "🎨", "seaborn_review": "🏆",
    "jupyter_colab": "📓", "ai_untuk_data": "🤖",
    "statistika_terapan": "📐", "data_storytelling": "🗣️",
}
IKON_TIPE = {"review": "🏆", "portfolio": "📊", "capstone": "👑"}
IKON_DEFAULT = "🔹"
RINGKASAN_WORLD = {
    3: "🧮 Math • Statistics • Probability • Optimization",
    4: "🤖 ML Models • Evaluation • Scikit-learn",
    5: "🧠 Neural Network • CNN • Transformer",
    6: "🚀 LLM • RAG • Agents • Automation • Capstone",
}
LABEL = {
    "validated_legacy": "✅ LEGACY",
    "validated": "✅ VALIDATED",
    "retained": "🧠 RETAINED",
    "mastered": "👑 MASTERED",
    "learned": "📘 LEARNED ◀",
    "aktif": "⚔️ CURRENT QUEST ◀",
    "belum": "🔒 LOCKED",
}
SEP = "═" * 51
KOL_ITEM = 50
KOL_WORLD = 55


class StateError(Exception):
    pass


# --------------------------------------------------------------------------
# Utilitas
# --------------------------------------------------------------------------
def dwidth(s: str) -> int:
    """Perkiraan lebar tampilan (emoji = 2 kolom)."""
    w, chars = 0, list(s)
    for i, ch in enumerate(chars):
        if ch in ("️", "‍"):
            continue
        nxt = chars[i + 1] if i + 1 < len(chars) else ""
        if unicodedata.east_asian_width(ch) in ("W", "F") or ord(ch) >= 0x1F000 or nxt == "️":
            w += 2
        else:
            w += 1
    return w


def pad(s: str, width: int) -> str:
    return s + " " * max(1, width - dwidth(s))


def to_date(v, nama="tanggal"):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    if isinstance(v, str):
        try:
            return dt.date.fromisoformat(v)
        except ValueError:
            pass
    raise StateError(f"{nama} harus berformat YYYY-MM-DD, ditemukan: {v!r}")


def tipe_of(item: dict) -> str:
    return item.get("tipe", "materi")


# --------------------------------------------------------------------------
# I/O state
# --------------------------------------------------------------------------
class Repo:
    def __init__(self, root: Path):
        self.root = root
        self.state_path = root / "state" / "state.yaml"
        self.evidence_dir = root / "state" / "evidence"
        self.dashboard_path = root / "state" / "dashboard.md"
        self.kurikulum_path = root / "system" / "09_kurikulum.md"

    def load(self):
        text = self.state_path.read_text(encoding="utf-8")
        header = []
        for line in text.splitlines():
            if line.startswith("#") or not line.strip():
                header.append(line)
            else:
                break
        data = yaml.safe_load(text)
        return data, "\n".join(header).rstrip() + "\n\n"

    def save(self, data, header):
        body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=10000,
                              default_flow_style=None)
        self.state_path.write_text(header + body, encoding="utf-8")


def leaves(data):
    out = []
    for w in data["worlds"]:
        for m in w["modul"]:
            if "quest" in m:
                for q in m["quest"]:
                    out.append({"item": q, "world": w, "parent": m})
            else:
                out.append({"item": m, "world": w, "parent": None})
    return out


def find(data, item_id):
    for i, rec in enumerate(leaves(data)):
        if rec["item"]["id"] == item_id:
            return i, rec
    return None, None


def non_opsional(data):
    return [r for r in leaves(data) if not r["item"].get("opsional")]


def current(data):
    for r in leaves(data):
        if r["item"]["status"] in SEDANG:
            return r
    return None


def next_after(data, item_id):
    order = non_opsional(data)
    ids = [r["item"]["id"] for r in order]
    if item_id in ids:
        k = ids.index(item_id)
        return order[k + 1] if k + 1 < len(order) else None
    # item opsional: cari item non-opsional berikutnya menurut urutan penuh
    full = leaves(data)
    pos, _ = find(data, item_id)
    for r in full[pos + 1:]:
        if not r["item"].get("opsional"):
            return r
    return None


def portfolio_ok(data, world) -> bool:
    for m in world["modul"]:
        for r in ([{"item": q} for q in m["quest"]] if "quest" in m else [{"item": m}]):
            it = r["item"]
            if it.get("opsional") or tipe_of(it) in ("portfolio", "capstone"):
                continue
            if it["status"] not in SELESAI:
                return False
    return True


def set_position(data, rec):
    if rec is None:
        data["posisi_saat_ini"] = None
        data["quest_berikutnya"] = None
        return
    item, parent, world = rec["item"], rec["parent"], rec["world"]
    data["posisi_saat_ini"] = {
        "world": world["id"],
        "modul": parent["id"] if parent else item["id"],
        "quest": item["id"] if parent else None,
    }
    nxt = next_after(data, item["id"])
    data["quest_berikutnya"] = nxt["item"]["id"] if nxt else None


# --------------------------------------------------------------------------
# check
# --------------------------------------------------------------------------
def load_evidence(repo: Repo, eid: str):
    p = repo.evidence_dir / f"{eid}.yaml"
    if not p.exists():
        return None
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def check(repo: Repo, data=None):
    if data is None:
        data, _ = repo.load()
    errors, warnings = [], []
    if data.get("versi_skema") != 1:
        errors.append("versi_skema harus 1")
    recs = leaves(data)
    ids = [r["item"]["id"] for r in recs] + [m["id"] for w in data["worlds"] for m in w["modul"] if "quest" in m]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        errors.append(f"id tidak unik: {sorted(dup)}")

    for r in recs:
        it = r["item"]
        if it["status"] not in STATUS:
            errors.append(f"{it['id']}: status tidak sah '{it['status']}'")
        if tipe_of(it) not in TIPE:
            errors.append(f"{it['id']}: tipe tidak sah '{tipe_of(it)}'")
        if it["status"] in ("validated", "retained", "mastered"):
            ev = it.get("evidence") or []
            if not ev:
                errors.append(f"{it['id']}: status {it['status']} wajib punya evidence")
            for eid in ev:
                e = load_evidence(repo, eid)
                if e is None:
                    errors.append(f"{it['id']}: file evidence '{eid}' tidak ditemukan")
                elif e.get("kelengkapan") == "sebagian":
                    warnings.append(f"{it['id']}: evidence '{eid}' masih sebagian (lengkapi tanggal/skor/mode_ai/bukti)")
            if it["status"] == "validated" and not it.get("tanggal_validasi"):
                warnings.append(f"{it['id']}: tanggal_validasi belum tercatat")
        if it["status"] == "validated_legacy" and it.get("evidence"):
            warnings.append(f"{it['id']}: punya evidence, pertimbangkan naik ke validated")
        kl = it.get("konsep_lemah")
        if kl is not None and (not isinstance(kl, list) or not all(isinstance(x, str) for x in kl)):
            errors.append(f"{it['id']}: konsep_lemah harus berupa daftar teks")

    # tepat satu quest sedang dikerjakan, tidak ada lompatan
    sedang = [r for r in recs if r["item"]["status"] in SEDANG]
    order = recs
    if len(sedang) > 1:
        errors.append(f"lebih dari satu quest aktif: {[r['item']['id'] for r in sedang]}")
    elif len(sedang) == 1:
        idx = order.index(sedang[0])
        for k, r in enumerate(order):
            it = r["item"]
            if k < idx and not it.get("opsional") and it["status"] not in SELESAI:
                errors.append(f"{it['id']} berada sebelum quest aktif tetapi belum selesai (status {it['status']})")
            if k > idx and it["status"] != "belum":
                errors.append(f"{it['id']} berstatus {it['status']} padahal berada setelah quest aktif (melompati roadmap)")
        pos = data.get("posisi_saat_ini") or {}
        it = sedang[0]["item"]
        exp_modul = sedang[0]["parent"]["id"] if sedang[0]["parent"] else it["id"]
        exp_quest = it["id"] if sedang[0]["parent"] else None
        if (pos.get("world"), pos.get("modul"), pos.get("quest")) != (sedang[0]["world"]["id"], exp_modul, exp_quest):
            errors.append(f"posisi_saat_ini tidak cocok dengan quest aktif '{it['id']}'")
        nxt = next_after(data, it["id"])
        if (nxt["item"]["id"] if nxt else None) != data.get("quest_berikutnya"):
            warnings.append("quest_berikutnya tidak cocok dengan urutan roadmap")
    else:
        if not all(r["item"]["status"] in SELESAI or r["item"].get("opsional") for r in recs):
            errors.append("tidak ada quest aktif, padahal roadmap belum selesai")

    # portfolio/capstone tidak boleh terbuka sebelum prasyaratnya selesai
    for r in recs:
        it = r["item"]
        if tipe_of(it) in ("portfolio", "capstone") and it["status"] != "belum":
            if not portfolio_ok(data, r["world"]):
                errors.append(f"{it['id']}: dibuka sebelum prasyarat World {r['world']['id']} selesai")

    # dashboard.md harus sinkron dengan state
    if repo.dashboard_path.exists():
        if repo.dashboard_path.read_text(encoding="utf-8") != dashboard_file(data):
            warnings.append("state/dashboard.md tidak sinkron dengan state.yaml (jalankan: dashboard --tulis)")
    else:
        warnings.append("state/dashboard.md belum ada (jalankan: dashboard --tulis)")
    return errors, warnings


# --------------------------------------------------------------------------
# dashboard
# --------------------------------------------------------------------------
def ikon(item):
    return IKON.get(item["id"], IKON_TIPE.get(tipe_of(item), IKON_DEFAULT))


def world_status(world):
    items = []
    for m in world["modul"]:
        items += m["quest"] if "quest" in m else [m]
    req = [i for i in items if not i.get("opsional")]
    if all(i["status"] in SELESAI for i in req):
        return "cleared"
    if any(i["status"] in SEDANG for i in req):
        return "progress"
    return "locked"


def module_state(m):
    if "quest" not in m:
        return m["status"]
    st = [q["status"] for q in m["quest"]]
    if all(s in SELESAI for s in st):
        return "selesai"
    if any(s in SEDANG for s in st):
        return "aktif"
    return "belum"


def render_dashboard(data) -> str:
    L = []
    L += ["🌳 LEARN A.I WORKFLOW FOR DATA SCIENCE", "🎯 TARGET: AI-ENHANCED DATA PROFESSIONAL", "", SEP, ""]
    for w in data["worlds"]:
        ws = world_status(w)
        head = f"🌍 WORLD {w['id']} — {w['nama']}"
        tag = {"cleared": "🏆 CLEARED", "progress": "⚔️ IN PROGRESS", "locked": "🔒 LOCKED"}[ws]
        L.append(pad(head, KOL_WORLD) + tag)
        L.append("│")
        if ws == "locked":
            L.append("└── " + RINGKASAN_WORLD.get(w["id"], ", ".join(m["nama"] for m in w["modul"])))
        elif ws == "cleared":
            for m in w["modul"]:
                lab = LABEL[m["status"]] if "quest" not in m else "✅ SELESAI"
                L.append(pad(f"├── {ikon(m)} {m['nama']}", KOL_ITEM) + lab)
            L.append(pad(f"└── 🏆 {w['nama']}", KOL_ITEM) + "✅ CLEARED")
        else:
            mods = w["modul"]
            k_aktif = next(i for i, m in enumerate(mods) if module_state(m) == "aktif")
            for i, m in enumerate(mods[:k_aktif]):
                lab = "🏆 " + LABEL[m["status"]][2:] if "quest" not in m else "🏆 SELESAI"
                L.append(pad(f"├── {ikon(m)} {m['nama'].upper()}", KOL_ITEM) + lab)
                L.append("│")
            ma = mods[k_aktif]
            if "quest" in ma:
                L.append(pad(f"└── {ikon(ma)} {ma['nama'].upper()}", KOL_ITEM) + "⚔️ BOSS BATTLE")
                L.append("    │")
                qs = ma["quest"]
                for j, q in enumerate(qs):
                    last = j == len(qs) - 1
                    if last:
                        L.append("    │")
                    prefix = "    └── " if last else "    ├── "
                    nama = q["nama"].upper() if tipe_of(q) == "review" else q["nama"]
                    L.append(pad(f"{prefix}{ikon(q)} {nama}", KOL_ITEM) + LABEL[q["status"]])
            else:
                L.append(pad(f"└── {ikon(ma)} {ma['nama'].upper()}", KOL_ITEM) + LABEL[ma["status"]])
            for m in mods[k_aktif + 1:]:
                L.append("         │")
                L.append("         ▼")
                st = module_state(m)
                tail = LABEL["belum"] if st == "belum" else ("✅ SELESAI" if st == "selesai" else LABEL[st])
                extra = " (opsional)" if m.get("opsional") else ""
                nama = m["nama"].upper() if tipe_of(m) in ("portfolio", "capstone") or m["id"] in ("seaborn", "sql_database") else m["nama"]
                L.append(pad(f"    {ikon(m)} {nama}{extra}", KOL_ITEM) + tail)
        L += ["", SEP, ""]

    recs = leaves(data)
    cur = current(data)
    byid = {r["item"]["id"]: r["item"] for r in recs}
    if cur:
        it = cur["item"]
        L.append(f"🎯 CURRENT QUEST : {ikon(it)} {it['nama']}")
        nid = data.get("quest_berikutnya")
        if nid:
            L.append(f"➡️ NEXT QUEST    : {ikon(byid[nid])} {byid[nid]['nama']}")
    win = data.get("kemenangan_terbaru")
    if win and win in byid:
        st = byid[win]["status"].upper().replace("_", " ")
        L.append(f"🏆 LATEST WIN    : {ikon(byid[win])} {byid[win]['nama']} — {st}")
    if cur:
        L += ["", "📍 CURRENT POSITION"]
        parts = [f"WORLD {cur['world']['id']}"]
        if cur["parent"]:
            parts.append(cur["parent"]["nama"])
        parts.append(f"{ikon(cur['item'])} {cur['item']['nama']}")
        L.append(" → ".join(parts))
    L.append(SEP)
    return "\n".join(L) + "\n"


def dashboard_file(data) -> str:
    return (
        "<!-- DIHASILKAN OTOMATIS oleh tools/progress.py dari state/state.yaml. JANGAN DIEDIT MANUAL. -->\n"
        f"Diperbarui: {data.get('diperbarui')}\n\n"
        "```text\n" + render_dashboard(data) + "```\n"
    )


# --------------------------------------------------------------------------
# due (review jatuh tempo)
# --------------------------------------------------------------------------
def due(data, today: dt.date):
    jatuh, legacy = [], []
    for r in leaves(data):
        it = r["item"]
        st = it["status"]
        rb = it.get("review_berikutnya")
        if st in ("validated", "retained"):
            if rb:
                if to_date(rb) <= today:
                    alasan = "perlu_review (retrieval gagal sebelumnya)" if it.get("perlu_review") else "jadwal review tiba"
                    jatuh.append((it, f"{alasan}, jatuh tempo {to_date(rb)}"))
            elif st == "validated":
                tv = it.get("tanggal_validasi")
                if not tv:
                    jatuh.append((it, "tanggal validasi tidak tercatat; ambil retrieval review sekarang"))
                elif to_date(tv) + dt.timedelta(days=JEDA_RETRIEVAL) <= today:
                    jatuh.append((it, f"retrieval H+{JEDA_RETRIEVAL} sudah bisa dilakukan sejak {to_date(tv) + dt.timedelta(days=JEDA_RETRIEVAL)}"))
        elif st == "validated_legacy":
            if rb and to_date(rb) > today:
                continue
            legacy.append(it)
    return jatuh, legacy


# --------------------------------------------------------------------------
# kurikulum: daftar Wajib per quest (system/09_kurikulum.md)
# --------------------------------------------------------------------------
JUDUL_QUEST = re.compile(r"^#### `([a-z0-9_]+)`")
BARIS_WAJIB = re.compile(r"^- \*\*Wajib:\*\*\s*(.*)$")


def norm_item(teks) -> str:
    """Kunci pembanding item: tanpa backtick, tanpa isi kurung, huruf kecil, spasi dirapikan.

    Contoh: "`barplot` (`estimator`, `errorbar`)" -> "barplot". Jadi mentor boleh menyalin
    item dari kurikulum apa adanya, atau hanya menulis kuncinya.
    """
    s = str(teks).replace("`", "")
    out, dalam = [], 0
    for ch in s:
        if ch == "(":
            dalam += 1
        elif ch == ")":
            dalam = max(0, dalam - 1)
        elif dalam == 0:
            out.append(ch)
    return re.sub(r"\s+", " ", "".join(out)).strip(" .,;").lower()


def pecah_koma(teks: str) -> list:
    """Pecah daftar berkoma, kecuali koma di dalam kurung atau backtick."""
    bagian, buf, kurung, tick = [], [], 0, False
    for ch in teks:
        if ch == "`":
            tick = not tick
        elif not tick and ch == "(":
            kurung += 1
        elif not tick and ch == ")":
            kurung = max(0, kurung - 1)
        if ch == "," and kurung == 0 and not tick:
            bagian.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    bagian.append("".join(buf).strip())
    return [b for b in bagian if b]


def parse_kurikulum(teks: str) -> dict:
    """{id: {"wajib": [teks item], "kunci": [kunci item]}} untuk setiap `#### `id``."""
    hasil, cur, baris = {}, None, teks.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(baris):
        b = baris[i]
        m = JUDUL_QUEST.match(b)
        if m:
            cur = m.group(1)
            hasil[cur] = {"wajib": [], "kunci": []}
        elif cur and BARIS_WAJIB.match(b):
            sisa = BARIS_WAJIB.match(b).group(1).strip()
            if sisa:
                for it in pecah_koma(sisa):
                    hasil[cur]["wajib"].append(it)
                    hasil[cur]["kunci"].append(norm_item(it))
            else:  # daftar bertingkat: satu sub-butir = satu item, kuncinya label sebelum ':'
                while i + 1 < len(baris) and re.match(r"^\s+- ", baris[i + 1]):
                    i += 1
                    it = re.sub(r"^\s+- ", "", baris[i]).strip()
                    hasil[cur]["wajib"].append(it)
                    hasil[cur]["kunci"].append(norm_item(it.split(":", 1)[0]) if ":" in it else norm_item(it))
        elif b.startswith("#") and not b.startswith("####"):
            cur = None
        i += 1
    return hasil


def baca_kurikulum(repo: Repo) -> dict:
    if not repo.kurikulum_path.is_file():
        raise StateError(f"kurikulum tidak ditemukan: {repo.kurikulum_path}")
    return parse_kurikulum(repo.kurikulum_path.read_text(encoding="utf-8"))


def cocokkan_cakupan(cakupan: list, kunci: list):
    """Kembalikan (kunci yang tercakup, item cakupan yang tidak dikenal)."""
    tercakup, asing = set(), []
    for c in cakupan:
        n = norm_item(c)
        if n in kunci:
            tercakup.add(n)
        elif ":" in str(c) and norm_item(str(c).split(":", 1)[0]) in kunci:
            tercakup.add(norm_item(str(c).split(":", 1)[0]))
        else:
            asing.append(str(c))
    return tercakup, asing


def periksa_cakupan(repo: Repo, data, rec, e) -> tuple:
    """Periksa kolom cakupan terhadap item Wajib di kurikulum. Kembalikan (error, peringatan)."""
    it, parent = rec["item"], rec["parent"]
    kur = baca_kurikulum(repo)
    if it["id"] not in kur or not kur[it["id"]]["kunci"]:
        return [f"quest '{it['id']}' belum punya daftar Wajib di system/09_kurikulum.md"], []
    cakupan = e.get("cakupan") or []
    if not cakupan:
        return ["kolom cakupan wajib diisi: item Wajib yang diuji (lihat: python tools/progress.py cakupan "
                f"{it['id']})"], []
    err, warn = [], []
    if tipe_of(it) == "review":
        saudara = [q for q in (parent["quest"] if parent else []) if tipe_of(q) != "review"]
        ids = {q["id"] for q in saudara}
        kunci_saudara = {k for q in saudara for k in kur.get(q["id"], {}).get("kunci", [])}
        dipakai = sorted({str(c).strip() for c in cakupan if str(c).strip() in ids})
        asing = [str(c) for c in cakupan if str(c).strip() not in ids and norm_item(c) not in kunci_saudara]
        m = re.search(r"≥\s*(\d+)", " ".join(kur[it["id"]]["wajib"]))
        minimal = 1 if e["jenis"] == "retrieval" else (int(m.group(1)) if m else MIN_REVIEW)
        if len(dipakai) < minimal:
            err.append(f"cakupan modul review wajib menyebut minimal {minimal} id quest yang dipakai "
                       f"(pilihan: {', '.join(sorted(ids))}); tertulis: {dipakai or 'tidak ada'}")
    else:
        kunci = kur[it["id"]]["kunci"]
        tercakup, asing = cocokkan_cakupan(cakupan, kunci)
        if e["jenis"] == "validasi":
            kurang = [w for w, k in zip(kur[it["id"]]["wajib"], kunci) if k not in tercakup]
            if kurang:
                err.append("ujian validasi belum mencakup semua item Wajib quest ini. Yang belum: "
                           + "; ".join(kurang) + ". Tunda validasi sampai semuanya diajarkan dan diuji")
        elif not tercakup:
            err.append("cakupan retrieval harus memuat minimal satu item Wajib quest ini")
    if asing:
        warn.append("item cakupan tidak dikenal di kurikulum (diabaikan): " + "; ".join(asing))
    return err, warn


# --------------------------------------------------------------------------
# ujian: rekaman soal dan challenge, skor dihitung ulang
# --------------------------------------------------------------------------
def _skor_sah(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and 0 <= v <= 100


def periksa_ujian(e, tipe: str) -> tuple:
    """Periksa kolom ujian dan hitung skor gabungan. Kembalikan (error, skor_hitung)."""
    u = e.get("ujian")
    if not isinstance(u, dict) or not isinstance(u.get("soal"), list) or not u["soal"]:
        return ["kolom ujian wajib diisi: ujian.soal (daftar soal dengan level, pertanyaan, skor)"
                + (" dan ujian.challenge" if e["jenis"] == "validasi" else "")], None
    err = []
    for k, s in enumerate(u["soal"], 1):
        if not isinstance(s, dict):
            err.append(f"ujian.soal ke-{k} harus berupa pemetaan (level, pertanyaan, skor)")
            continue
        if s.get("level") not in LEVEL:
            err.append(f"ujian.soal ke-{k}: level harus salah satu dari {', '.join(LEVEL)}")
        if not isinstance(s.get("pertanyaan"), str) or not s["pertanyaan"].strip():
            err.append(f"ujian.soal ke-{k}: pertanyaan wajib diisi")
        if not _skor_sah(s.get("skor")):
            err.append(f"ujian.soal ke-{k}: skor harus angka 0-100")
    kunci = (e["jenis"], tipe if e["jenis"] == "validasi" else None)
    lo, hi = JUMLAH_SOAL.get(kunci, (1, 99))
    if not lo <= len(u["soal"]) <= hi:
        err.append(f"jumlah soal {len(u['soal'])}, seharusnya {lo}" + (f"-{hi}" if hi != lo else "")
                   + f" untuk {e['jenis']}" + (f" modul {tipe}" if e["jenis"] == "validasi" else ""))
    ch = u.get("challenge")
    if e["jenis"] == "validasi":
        if not isinstance(ch, dict):
            err.append("ujian.challenge wajib diisi untuk validasi (level, deskripsi, skor)")
        else:
            if ch.get("level") not in LEVEL:
                err.append(f"ujian.challenge: level harus salah satu dari {', '.join(LEVEL)}")
            elif tipe == "review" and ch["level"] != "L3":
                err.append("challenge modul review wajib level L3 (transfer)")
            if not isinstance(ch.get("deskripsi"), str) or not ch["deskripsi"].strip():
                err.append("ujian.challenge: deskripsi wajib diisi")
            if not _skor_sah(ch.get("skor")):
                err.append("ujian.challenge: skor harus angka 0-100")
    elif ch is not None:
        err.append("retrieval hanya berisi soal (tanpa challenge)")
    if err:
        return err, None
    level = [s["level"] for s in u["soal"]] + ([ch["level"]] if isinstance(ch, dict) else [])
    if not any(lv in ("L2", "L3") for lv in level):
        err.append("setiap ujian memuat minimal satu soal level L2 atau L3")
    rata = sum(s["skor"] for s in u["soal"]) / len(u["soal"])
    hitung = 0.5 * rata + 0.5 * ch["skor"] if e["jenis"] == "validasi" else rata
    hitung = round(hitung, 1)
    if abs(e["skor_persen"] - hitung) > TOLERANSI_SKOR:
        err.append(f"skor_persen {e['skor_persen']} tidak sama dengan hitungan dari ujian ({hitung}; "
                   + ("rata-rata soal 50% + challenge 50%" if e["jenis"] == "validasi" else "rata-rata soal") + ")")
    return err, hitung


def kunci_konsep(teks) -> str:
    return norm_item(str(teks).split(":", 1)[0])


def perbarui_konsep_lemah(it: dict, e) -> list:
    """kesalahan: menambah/menimpa konsep lemah; teratasi: menghapusnya. Kembalikan pesan."""
    msgs, lemah = [], list(it.get("konsep_lemah") or [])
    for t in e.get("teratasi") or []:
        k = kunci_konsep(t)
        sisa = [x for x in lemah if kunci_konsep(x) != k]
        if len(sisa) != len(lemah):
            msgs.append(f"konsep lemah teratasi: {str(t).split(':', 1)[0].strip()}")
        lemah = sisa
    for t in e.get("kesalahan") or []:
        k = kunci_konsep(t)
        lemah = [x for x in lemah if kunci_konsep(x) != k] + [str(t).strip()]
        msgs.append(f"konsep lemah dicatat: {str(t).strip()}")
    lemah = lemah[-BATAS_KONSEP_LEMAH:]
    if lemah:
        it["konsep_lemah"] = lemah
    else:
        it.pop("konsep_lemah", None)
    return msgs


# --------------------------------------------------------------------------
# apply (Evidence Entry)
# --------------------------------------------------------------------------
def periksa_bukti(root: Path, bukti: list) -> list:
    """Setiap bukti: URL http(s), atau path relatif yang benar-benar ada di dalam repo."""
    err = []
    base = root.resolve()
    for b in bukti:
        if not isinstance(b, str) or not b.strip():
            err.append("bukti berisi item kosong atau bukan teks")
            continue
        if b.startswith(("http://", "https://")):
            continue
        p = Path(b.replace("\\", "/"))
        if p.is_absolute() or ".." in p.parts:
            err.append(f"bukti harus path relatif di dalam repo: {b}")
            continue
        if not (base / p).resolve().is_file():
            err.append(f"bukti tidak ditemukan di repo: {b} (commit dan push file buktinya dulu)")
    return err


def validate_entry(e, root: Path | None = None) -> list:
    if not isinstance(e, dict):
        return ["isi entri harus berupa pemetaan YAML (kunci: nilai)"]
    err = []
    for k in ("id", "modul", "tanggal", "jenis", "skor_persen", "mode_ai", "bukti", "keputusan"):
        if e.get(k) in (None, "", []):
            err.append(f"kolom wajib kosong: {k}")
    if err:
        return err
    if not isinstance(e["id"], str) or not ID_ENTRI.match(e["id"]):
        err.append("id hanya boleh huruf, angka, '-' dan '_' (3-80 karakter), tanpa titik atau garis miring")
        return err
    if not isinstance(e["modul"], str):
        err.append("modul harus berupa teks (id quest di state.yaml)")
        return err
    try:
        to_date(e["tanggal"])
    except StateError as x:
        err.append(str(x))
    if e["jenis"] not in JENIS:
        err.append(f"jenis harus salah satu dari {sorted(JENIS)}")
    if e["mode_ai"] not in MODE_AI:
        err.append(f"mode_ai harus salah satu dari {sorted(MODE_AI)}")
    if not isinstance(e["skor_persen"], (int, float)) or not 0 <= e["skor_persen"] <= 100:
        err.append("skor_persen harus angka 0-100")
    if not isinstance(e["bukti"], list):
        err.append("bukti harus berupa daftar")
    elif root is not None:
        err.extend(periksa_bukti(root, e["bukti"]))
    if e.get("jenis") == "validasi" and not e.get("pemahaman"):
        err.append("jenis validasi wajib mengisi pemahaman (dua keputusan beserta alasannya)")
    if e.get("jenis") == "mastery" and len(e.get("konteks") or []) < 2:
        err.append("jenis mastery wajib mengisi konteks minimal dua")
    for k in ("cakupan", "kesalahan", "teratasi"):
        v = e.get(k)
        if v is not None and (not isinstance(v, list) or not all(isinstance(x, (str, int, float)) for x in v)):
            err.append(f"{k} harus berupa daftar teks")
    if e.get("ujian") is not None and not isinstance(e["ujian"], dict):
        err.append("ujian harus berupa pemetaan berisi soal (dan challenge untuk validasi)")
    return err


def apply_entry(repo: Repo, entry_path: Path, today: dt.date, dry=False):
    data, header = repo.load()
    if entry_path.stat().st_size > BATAS_ENTRI_BYTE:
        raise StateError(f"Entri ditolak: ukuran berkas melebihi {BATAS_ENTRI_BYTE // 1024} KB")
    try:
        e = yaml.safe_load(entry_path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, UnicodeDecodeError) as x:
        raise StateError(f"Entri ditolak: berkas bukan YAML yang valid ({type(x).__name__})")
    errs = validate_entry(e, repo.root)
    if errs:
        raise StateError("Entri ditolak:\n  - " + "\n  - ".join(errs))
    if (repo.evidence_dir / f"{e['id']}.yaml").exists() and \
            entry_path.resolve() != (repo.evidence_dir / f"{e['id']}.yaml").resolve():
        raise StateError(f"Entri ditolak: id '{e['id']}' sudah pernah dipakai (state/evidence/{e['id']}.yaml sudah ada)")
    pos, rec = find(data, e["modul"])
    if rec is None:
        induk = next((m for w in data["worlds"] for m in w["modul"] if m["id"] == e["modul"] and "quest" in m), None)
        if induk is not None:
            ids = ", ".join(q["id"] for q in induk["quest"])
            raise StateError(f"Entri ditolak: '{e['modul']}' adalah modul yang terdiri dari beberapa quest. "
                             f"Isi kolom modul dengan id quest yang benar-benar diuji: {ids}")
        raise StateError(f"Entri ditolak: modul '{e['modul']}' tidak ada di state.yaml")
    it = rec["item"]
    tgl = to_date(e["tanggal"])
    if tgl > today:
        raise StateError(f"Entri ditolak: tanggal {tgl} berada di masa depan")
    lulus = e["skor_persen"] >= AMBANG
    st = it["status"]
    msgs = []
    baru = None  # status baru bila lulus

    if e["jenis"] == "validasi":
        if st not in SEDANG and st != "validated_legacy":
            raise StateError(f"Entri ditolak: validasi hanya untuk quest aktif/learned atau modul legacy (status sekarang: {st})")
        if st == "validated_legacy" and not e["bukti"]:
            raise StateError("Entri ditolak: naik dari legacy butuh bukti")
        baru = "validated"
    elif e["jenis"] == "retrieval":
        if st not in ("validated", "validated_legacy", "retained"):
            raise StateError(f"Entri ditolak: retrieval hanya untuk modul yang sudah Validated/Retained (status sekarang: {st})")
        if e["mode_ai"] != "independent":
            raise StateError("Entri ditolak: retrieval wajib mode independent")
        tv = it.get("tanggal_validasi")
        if st == "validated" and tv and (tgl - to_date(tv)).days < JEDA_RETRIEVAL:
            raise StateError(f"Entri ditolak: jeda baru {(tgl - to_date(tv)).days} hari, minimal {JEDA_RETRIEVAL} hari sejak validasi")
        baru = "retained"
    else:  # mastery
        if st != "retained":
            raise StateError(f"Entri ditolak: mastery hanya untuk modul berstatus retained (status sekarang: {st})")
        if e["mode_ai"] != "independent":
            raise StateError("Entri ditolak: mastery wajib mode independent")
        baru = "mastered"

    # rekaman ujian: cakupan (terhadap kurikulum) dan soal/challenge (skor dihitung ulang)
    tipe = tipe_of(it)
    wajib_rekam = e["jenis"] == "retrieval" or (e["jenis"] == "validasi" and st in SEDANG
                                                and tipe in ("materi", "review"))
    errs = []
    if wajib_rekam:
        ce, cw = periksa_cakupan(repo, data, rec, e)
        errs += ce
        msgs += [f"⚠️ {w}" for w in cw]
    if wajib_rekam or (e["jenis"] == "validasi" and e.get("ujian") is not None):
        errs += periksa_ujian(e, tipe)[0]
    if errs:
        raise StateError("Entri ditolak:\n  - " + "\n  - ".join(errs))

    hasil = baru if lulus else "tetap"
    if e["keputusan"] != hasil:
        raise StateError(f"Entri ditolak: keputusan usulan '{e['keputusan']}', hasil perhitungan '{hasil}' (skor {e['skor_persen']}, ambang {AMBANG})")

    # --- terapkan ---
    if lulus:
        if e["jenis"] == "validasi":
            was_current = st in SEDANG
            it["status"] = "validated"
            it["tanggal_validasi"] = tgl
            it["review_berikutnya"] = tgl + dt.timedelta(days=JEDA_RETRIEVAL)
            it.pop("perlu_review", None)
            data["kemenangan_terbaru"] = it["id"]
            msgs.append(f"{it['nama']}: {st} → validated; review H+{JEDA_RETRIEVAL} pada {it['review_berikutnya']}")
            if was_current:
                nxt = next_after(data, it["id"])
                if nxt is None:
                    set_position(data, None)
                    msgs.append("Roadmap selesai.")
                else:
                    ni = nxt["item"]
                    if tipe_of(ni) in ("portfolio", "capstone") and not portfolio_ok(data, nxt["world"]):
                        raise StateError(f"{ni['id']} belum bisa dibuka: prasyarat World {nxt['world']['id']} belum selesai")
                    ni["status"] = "aktif"
                    set_position(data, nxt)
                    msgs.append(f"Quest aktif berikutnya: {ni['nama']}")
        elif e["jenis"] == "retrieval":
            tv = it.get("tanggal_validasi")
            if st == "retained":
                it["review_berikutnya"] = None
                msgs.append(f"{it['nama']}: konfirmasi retensi lulus; tidak ada review terjadwal lagi")
            else:
                it["status"] = "retained"
                if tv:
                    it["review_berikutnya"] = max(to_date(tv) + dt.timedelta(days=KONFIRMASI), tgl + dt.timedelta(days=JEDA_RETRIEVAL))
                else:
                    it["review_berikutnya"] = tgl + dt.timedelta(days=KONFIRMASI)
                msgs.append(f"{it['nama']}: {st} → retained; konfirmasi pada {it['review_berikutnya']}")
            it.pop("perlu_review", None)
        else:
            it["status"] = "mastered"
            it["review_berikutnya"] = None
            msgs.append(f"{it['nama']}: retained → mastered")
        ev = it.setdefault("evidence", [])
        if e["id"] not in ev:
            ev.append(e["id"])
    else:
        msgs.append(f"{it['nama']}: skor {e['skor_persen']}% < {AMBANG}%, status TIDAK berubah (tetap {st}); boleh mengulang kapan saja")
        if e["jenis"] == "retrieval":
            it["perlu_review"] = True
            it["review_berikutnya"] = tgl + dt.timedelta(days=ULANG_GAGAL)
            msgs.append(f"Ditandai perlu_review; jadwal ulang {it['review_berikutnya']}")
    msgs += perbarui_konsep_lemah(it, e)

    data["diperbarui"] = today
    if not dry:
        repo.evidence_dir.mkdir(parents=True, exist_ok=True)
        dest = repo.evidence_dir / f"{e['id']}.yaml"
        if entry_path.resolve() != dest.resolve():
            shutil.copyfile(entry_path, dest)
        repo.save(data, header)
        repo.dashboard_path.write_text(dashboard_file(data), encoding="utf-8")
    return msgs, ("DRY-RUN: tidak ada file yang diubah" if dry else None)


def mark_learned(repo: Repo, item_id: str, today: dt.date):
    data, header = repo.load()
    _, rec = find(data, item_id)
    if rec is None:
        raise StateError(f"id '{item_id}' tidak ada")
    if rec["item"]["status"] != "aktif":
        raise StateError(f"hanya quest aktif yang bisa ditandai learned (status sekarang: {rec['item']['status']})")
    rec["item"]["status"] = "learned"
    data["diperbarui"] = today
    repo.save(data, header)
    repo.dashboard_path.write_text(dashboard_file(data), encoding="utf-8")
    return f"{rec['item']['nama']}: aktif → learned (menunggu ujian validasi)"


def proses_inbox(repo: Repo, today: dt.date, dry: bool = False):
    """Terapkan semua entri di state/inbox/ (urut nama berkas).

    Entri yang diterima dihapus dari inbox (salinannya sudah ada di state/evidence/).
    Entri yang ditolak dipindah ke state/inbox/ditolak/ bersama berkas alasan,
    supaya tidak mengganjal proses berikutnya dan alasannya bisa dibaca.
    """
    inbox = repo.root / "state" / "inbox"
    if not inbox.is_dir():
        return [], []
    berkas = sorted(p for p in inbox.iterdir() if p.is_file() and p.suffix.lower() in (".yaml", ".yml"))
    diterima, ditolak = [], []
    for p in berkas:
        try:
            msgs, _ = apply_entry(repo, p, today, dry=dry)
        except Exception as x:  # satu entri bermasalah tidak boleh menghentikan yang lain
            alasan = str(x) if isinstance(x, StateError) else f"Kesalahan tak terduga: {type(x).__name__}: {x}"
            ditolak.append((p.name, alasan))
            if not dry:
                tujuan_dir = inbox / "ditolak"
                tujuan_dir.mkdir(parents=True, exist_ok=True)
                tujuan, n = tujuan_dir / p.name, 2
                while tujuan.exists():
                    tujuan = tujuan_dir / f"{p.stem}-{n}{p.suffix}"
                    n += 1
                shutil.move(str(p), str(tujuan))
                (tujuan_dir / f"{tujuan.name}.alasan.txt").write_text(
                    f"Ditolak pada {today}\n\n{alasan}\n", encoding="utf-8")
        else:
            diterima.append((p.name, msgs))
            if not dry:
                p.unlink()
    return diterima, ditolak


# --------------------------------------------------------------------------
# statistik (dibaca dari state/evidence/; tidak mengubah apa pun)
# --------------------------------------------------------------------------
def muat_semua_evidence(repo: Repo) -> list:
    out = []
    if repo.evidence_dir.is_dir():
        for p in sorted(repo.evidence_dir.glob("*.yaml")):
            try:
                e = yaml.safe_load(p.read_text(encoding="utf-8-sig"))
            except (yaml.YAMLError, UnicodeDecodeError):
                continue
            if isinstance(e, dict):
                out.append(e)
    return out


def _tanggal_atau_none(v):
    try:
        return to_date(v)
    except StateError:
        return None


def statistik(repo: Repo, data) -> str:
    entri = muat_semua_evidence(repo)
    nama = {m["id"]: m["nama"] for w in data["worlds"] for m in w["modul"]}
    nama.update({r["item"]["id"]: r["item"]["nama"] for r in leaves(data)})
    berskor = [e for e in entri if _skor_sah(e.get("skor_persen")) and _tanggal_atau_none(e.get("tanggal"))]
    berskor.sort(key=lambda e: (_tanggal_atau_none(e["tanggal"]), str(e.get("id"))))
    L = [f"📈 STATISTIK BELAJAR ({len(entri)} Evidence Entry; {len(berskor)} bertanggal dan berskor)", ""]

    L.append("Tren skor (urut tanggal):")
    if not berskor:
        L.append("  (belum ada)")
    for e in berskor:
        s = e["skor_persen"]
        bar = "█" * int(round(s / 10))
        tanda = "✅" if s >= AMBANG else "❌"
        L.append(f"  {_tanggal_atau_none(e['tanggal'])}  {s:>5}% {tanda} {bar:<10}  {str(e.get('jenis')):<9} "
                 f"{str(e.get('mode_ai')):<11} {nama.get(e.get('modul'), e.get('modul'))}")

    def rata(kelompok):
        return f"{sum(x['skor_persen'] for x in kelompok) / len(kelompok):.1f}% ({len(kelompok)} entri)"

    if berskor:
        L += ["", "Rata-rata skor:"]
        L.append(f"  {'semua':<20}: {rata(berskor)}; lulus {sum(e['skor_persen'] >= AMBANG for e in berskor)}/{len(berskor)}")
        for kol, nilai in (("jenis", sorted(JENIS)), ("mode_ai", sorted(MODE_AI))):
            for v in nilai:
                kel = [e for e in berskor if e.get(kol) == v]
                if kel:
                    L.append(f"  {kol + '=' + v:<20}: {rata(kel)}")
        if len(berskor) >= 4:
            h = len(berskor) // 2
            awal, akhir = berskor[:h], berskor[h:]
            selisih = sum(x["skor_persen"] for x in akhir) / len(akhir) - sum(x["skor_persen"] for x in awal) / len(awal)
            arah = "naik" if selisih > 0 else ("turun" if selisih < 0 else "datar")
            L.append(f"  {'tren':<20}: paruh kedua {arah} {abs(selisih):.1f} poin dibanding paruh pertama")

    level = {lv: 0 for lv in LEVEL}
    for e in entri:
        u = e.get("ujian") if isinstance(e.get("ujian"), dict) else {}
        for s in (u.get("soal") or []) + ([u["challenge"]] if isinstance(u.get("challenge"), dict) else []):
            if isinstance(s, dict) and s.get("level") in level:
                level[s["level"]] += 1
    if any(level.values()):
        L += ["", "Level soal yang sudah dikerjakan: " + ", ".join(f"{k} {v}" for k, v in level.items())]

    per_modul = {}
    for e in entri:
        per_modul.setdefault(e.get("modul"), []).append(e)
    ulang = {m: es for m, es in per_modul.items() if len(es) > 1 or any(
        _skor_sah(x.get("skor_persen")) and x["skor_persen"] < AMBANG for x in es)}
    L += ["", "Modul dengan lebih dari satu percobaan atau pernah gagal:"]
    if not ulang:
        L.append("  (tidak ada)")
    for m, es in ulang.items():
        skor = ", ".join(str(x.get("skor_persen")) for x in es)
        L.append(f"  - {nama.get(m, m)} [{m}]: {len(es)} percobaan (skor: {skor})")

    L += ["", "Konsep lemah yang masih tercatat (bahan retrieval review):"]
    ada = False
    for r in leaves(data):
        for k in r["item"].get("konsep_lemah") or []:
            L.append(f"  - {r['item']['nama']}: {k}")
            ada = True
    if not ada:
        L.append("  (tidak ada)")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def pakai_utf8():
    """Paksa keluaran UTF-8 agar emoji aman di Windows (cp1252) dan saat output dialihkan."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main(argv=None) -> int:
    pakai_utf8()
    ap = argparse.ArgumentParser(description="Penjaga aturan progres Learn A.I Workflow")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--today", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    d = sub.add_parser("dashboard")
    d.add_argument("--tulis", action="store_true")
    sub.add_parser("due")
    lr = sub.add_parser("learned")
    lr.add_argument("id")
    a = sub.add_parser("apply")
    a.add_argument("entri")
    a.add_argument("--dry", action="store_true")
    ib = sub.add_parser("inbox")
    ib.add_argument("--dry", action="store_true")
    ck = sub.add_parser("cakupan")
    ck.add_argument("id")
    sub.add_parser("statistik")
    args = ap.parse_args(argv)

    repo = Repo(Path(args.root))
    today = to_date(args.today) if args.today else dt.date.today()
    try:
        if args.cmd == "check":
            errors, warnings = check(repo)
            for w in warnings:
                print("⚠️ ", w)
            for x in errors:
                print("❌", x)
            if errors:
                print(f"\nGAGAL: {len(errors)} error, {len(warnings)} peringatan")
                return 1
            print(f"✅ State konsisten ({len(warnings)} peringatan)")
            return 0
        data, _ = repo.load()
        if args.cmd == "dashboard":
            if args.tulis:
                repo.dashboard_path.write_text(dashboard_file(data), encoding="utf-8")
                print(f"Ditulis: {repo.dashboard_path}")
            else:
                print(render_dashboard(data))
        elif args.cmd == "due":
            jatuh, legacy = due(data, today)
            print(f"📚 ANTREAN REVIEW (per {today})\n")
            print("Jatuh tempo:" if jatuh else "Jatuh tempo: (tidak ada)")
            for it, why in jatuh:
                print(f"  - {it['nama']} [{it['id']}]: {why}")
            print(f"\nAntrean legacy (maksimal {LEGACY_PER_SESI} per sesi, urutan roadmap):")
            for it in legacy[:LEGACY_PER_SESI]:
                print(f"  - {it['nama']} [{it['id']}]")
            if len(legacy) > LEGACY_PER_SESI:
                print(f"  ... dan {len(legacy) - LEGACY_PER_SESI} lainnya menunggu")
        elif args.cmd == "learned":
            print(mark_learned(repo, args.id, today))
        elif args.cmd == "apply":
            msgs, note = apply_entry(repo, Path(args.entri), today, dry=args.dry)
            for m in msgs:
                print("•", m)
            if note:
                print(note)
        elif args.cmd == "inbox":
            diterima, ditolak = proses_inbox(repo, today, dry=args.dry)
            if not diterima and not ditolak:
                print("Inbox kosong.")
            for nama, msgs in diterima:
                print(f"✅ diterapkan: {nama}")
                for m in msgs:
                    print("   •", m)
            for nama, alasan in ditolak:
                print(f"❌ ditolak: {nama}")
                for baris in alasan.splitlines():
                    print("   ", baris)
            if args.dry:
                print("DRY-RUN: tidak ada file yang diubah")
            return 1 if ditolak else 0
        elif args.cmd == "cakupan":
            _, rec = find(data, args.id)
            if rec is None:
                raise StateError(f"id '{args.id}' tidak ada di state.yaml")
            kur = baca_kurikulum(repo)
            if tipe_of(rec["item"]) == "review":
                qs = [q["id"] for q in (rec["parent"]["quest"] if rec["parent"] else []) if tipe_of(q) != "review"]
                print(f"{rec['item']['nama']} adalah modul review: isi cakupan dengan id quest yang dipakai, pilih dari:")
                for q in qs:
                    print(f"  - {q}")
            else:
                print(f"cakupan:   # {rec['item']['nama']} — validasi wajib mencakup semua item ini")
                for w, k in zip(kur.get(args.id, {}).get("wajib", []), kur.get(args.id, {}).get("kunci", [])):
                    print(f"  - {json.dumps(k, ensure_ascii=False)}" + (f"   # {w}" if norm_item(w) != k else ""))
        elif args.cmd == "statistik":
            print(statistik(repo, data))
        return 0
    except StateError as x:
        print(f"❌ {x}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
