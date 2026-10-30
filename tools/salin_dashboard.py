#!/usr/bin/env python3
"""salin_dashboard.py - salin progres terbaru ke clipboard untuk ditempel ke mentor.

Dipakai saat mentor tidak bisa membuka state dari GitHub (alamat gagal, terpotong, atau
masih cache lama setelah Simpan Progres). Isinya diambil dari repo lokal, yang sudah
paling baru karena simpan.py menerapkan entri di komputer sebelum push.

    Salin Dashboard.bat                   klik dua kali (sama dengan perintah di bawah)
    python tools\\salin_dashboard.py       salin ke clipboard dan tampilkan di layar
    python tools\\salin_dashboard.py --tanpa-clipboard   hanya tampilkan

Yang disalin: isi state/dashboard.md apa adanya dan konsep lemah per modul (bila ada).
Script ini hanya membaca; tidak ada file yang diubah.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import progress as P  # noqa: E402


def susun_teks(repo: P.Repo, today: dt.date) -> str:
    if not repo.dashboard_path.is_file():
        raise P.StateError("state/dashboard.md belum ada. Jalankan: python tools\\progress.py dashboard --tulis")
    data, _ = repo.load()
    dashboard = repo.dashboard_path.read_text(encoding="utf-8").strip()
    if dashboard != P.dashboard_file(data).strip():
        raise P.StateError("state/dashboard.md tidak sinkron dengan state.yaml. "
                           "Jalankan dulu: python tools\\progress.py dashboard --tulis")
    # baris komentar HTML hanya penanda untuk file; tidak perlu ikut ditempel
    dashboard = "\n".join(b for b in dashboard.splitlines() if not b.startswith("<!--")).strip()
    L = [
        "Mentor, state di GitHub belum bisa kamu buka atau masih cache lama. Ini salinan dari repo lokal Rafa,",
        f"dibuat otomatis oleh tools/salin_dashboard.py pada {today}. Isi dashboard dihasilkan tools/progress.py",
        "dari state/state.yaml; tampilkan apa adanya (aturan cek progres) dan pakai sebagai state terbaru.",
        "",
        dashboard,
        "",
    ]
    lemah = [(r["item"], k) for r in P.leaves(data) for k in r["item"].get("konsep_lemah") or []]
    if lemah:
        L.append("Konsep lemah (prioritas soal retrieval):")
        L += [f"- {it['nama']} [{it['id']}]: {k}" for it, k in lemah]
    return "\n".join(L).rstrip() + "\n"


def belum_di_push(root: Path, runner=subprocess.run):
    """Jumlah commit lokal yang belum di-push, atau None bila tidak bisa dicek."""
    try:
        r = runner(["git", "rev-list", "--count", "@{u}..HEAD"], cwd=str(root),
                   capture_output=True, text=True, encoding="utf-8")
    except OSError:
        return None
    if r.returncode != 0:
        return None
    try:
        return int(r.stdout.strip())
    except ValueError:
        return None


def ke_clipboard(teks: str) -> None:
    if sys.platform.startswith("win"):
        # lewat berkas UTF-8 supaya emoji dashboard tidak rusak (clip.exe tidak aman untuk emoji)
        fd, path = tempfile.mkstemp(suffix=".txt")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(teks)
            perintah = ["powershell", "-NoProfile", "-Command",
                        f"Get-Content -Raw -Encoding UTF8 -LiteralPath '{path}' | Set-Clipboard"]
            subprocess.run(perintah, check=True, capture_output=True)
        finally:
            os.unlink(path)
    elif sys.platform == "darwin":
        subprocess.run(["pbcopy"], input=teks.encode("utf-8"), check=True)
    else:
        subprocess.run(["xclip", "-selection", "clipboard"], input=teks.encode("utf-8"), check=True)


def main(argv=None, clipboard=ke_clipboard) -> int:
    P.pakai_utf8()
    ap = argparse.ArgumentParser(description="Salin dashboard ke clipboard untuk mentor")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--today", default=None)
    ap.add_argument("--tanpa-clipboard", action="store_true", help="hanya tampilkan, jangan salin")
    a = ap.parse_args(argv)
    root = Path(a.root)
    today = P.to_date(a.today) if a.today else dt.date.today()
    try:
        teks = susun_teks(P.Repo(root), today)
    except P.StateError as x:
        print(f"❌ {x}")
        return 1

    print(teks)
    n = belum_di_push(root)
    if n:
        print(f"⚠️  Ada {n} commit yang belum di-push, jadi GitHub memang belum punya progres ini.")
        print("   Jalankan git push dari folder repo supaya mentor bisa membacanya sendiri lain kali.\n")
    if a.tanpa_clipboard:
        return 0
    try:
        clipboard(teks)
    except (OSError, subprocess.CalledProcessError) as x:
        print(f"⚠️  Tidak bisa menyalin ke clipboard ({type(x).__name__}). Blok teks di atas bisa disalin manual.")
        return 1
    print("✅ Tersalin ke clipboard. Tempel (Ctrl+V) di chat mentor, lalu ketik: cek progres")
    return 0


if __name__ == "__main__":
    sys.exit(main())
