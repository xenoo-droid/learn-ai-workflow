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

Opsi global: --root <folder repo>  --today YYYY-MM-DD
Kebutuhan: Python 3.9+ dan PyYAML (pip install pyyaml).
"""
from __future__ import annotations

import argparse
import datetime as dt
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
        return 0
    except StateError as x:
        print(f"❌ {x}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
