#!/usr/bin/env python3
"""simpan.py - satu perintah untuk menyimpan progres belajar.

Alur lama: push bukti, buat file entri, push lagi, tunggu bot, git pull,
ganti file di Project. Alur baru: salin entri dari mentor, jalankan satu perintah.

    python tools\\simpan.py                  baca entri dari clipboard
    python tools\\simpan.py --berkas e.yaml  baca entri dari berkas
    python tools\\simpan.py --dry            hanya periksa dan simulasi, tidak mengubah apa pun

Yang dikerjakan, berurutan:
    1. Mengambil entri (clipboard atau berkas), membuang pagar ```yaml bila ada
    2. git pull --rebase --autostash, supaya state lokal terbaru (dilewati bila --tanpa-push)
    3. Simulasi aturan rubrik (progress.py apply --dry); ditolak berarti berhenti, tidak ada yang berubah
    4. Menerapkan entri ke state/state.yaml, dashboard, dan state/evidence/
    5. Memeriksa konsistensi; bila gagal, semua perubahan dikembalikan
    6. Satu commit berisi file bukti + state, lalu push
    7. Membangun ulang paket ChatGPT Project dan membuka folder unggahan

Satu-satunya langkah manual yang tersisa: mengganti state.yaml dan dashboard.md
di ChatGPT Project (tidak ada cara otomatis untuk itu).

Workflow GitHub tetap berjalan sebagai pengaman (tes + check), tetapi bot tidak
perlu meng-commit apa pun, jadi tidak perlu git pull setelahnya.

Kebutuhan: Python 3.9+, PyYAML, dan git.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import progress as P  # noqa: E402

import yaml  # noqa: E402

PAGAR = re.compile(r"```[ \t]*(?:ya?ml)?[ \t]*\r?\n(.*?)```", re.S | re.I)


# --------------------------------------------------------------------------
# Mengambil dan membersihkan teks entri
# --------------------------------------------------------------------------
def bersihkan_teks(teks: str) -> str:
    """Hasil salinan dari chat sering terbungkus pagar ```yaml ... ```; ambil isinya saja."""
    teks = teks.lstrip("﻿").replace("\r\n", "\n")
    m = PAGAR.search(teks)
    if m:
        teks = m.group(1)
    return textwrap.dedent(teks).strip() + "\n"


def baca_clipboard() -> str:
    if sys.platform.startswith("win"):
        cmd = ["powershell", "-NoProfile", "-Command",
               "[Console]::OutputEncoding=[Text.Encoding]::UTF8; Get-Clipboard -Raw"]
    elif sys.platform == "darwin":
        cmd = ["pbpaste"]
    else:
        cmd = ["xclip", "-selection", "clipboard", "-o"]
    try:
        r = subprocess.run(cmd, capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError) as x:
        raise P.StateError(f"Tidak bisa membaca clipboard ({type(x).__name__}). Pakai: --berkas <file.yaml>")
    teks = r.stdout.decode("utf-8-sig", errors="replace")
    if not teks.strip():
        raise P.StateError("Clipboard kosong. Salin dulu Evidence Entry dari mentor, atau pakai --berkas <file.yaml>")
    return teks


def baca_berkas(path: str) -> str:
    p = Path(path)
    if not p.is_file():
        raise P.StateError(f"Berkas tidak ditemukan: {path}")
    return p.read_text(encoding="utf-8-sig")


# --------------------------------------------------------------------------
# git
# --------------------------------------------------------------------------
def git(root: Path, *args, runner=subprocess.run) -> str:
    try:
        r = runner(["git", *args], cwd=str(root), capture_output=True, text=True, encoding="utf-8")
    except OSError:
        raise P.StateError("git tidak ditemukan. Pasang git atau pakai --tanpa-git")
    if r.returncode != 0:
        raise P.StateError(f"git {' '.join(args)} gagal:\n{(r.stderr or r.stdout).strip()}")
    return r.stdout


def jalur_bukti(root: Path, bukti: list) -> list:
    """Item bukti yang berupa file lokal di repo (URL dilewati)."""
    out = []
    for b in bukti:
        if isinstance(b, str) and not b.startswith(("http://", "https://")):
            p = Path(b.replace("\\", "/"))
            if (root / p).is_file():
                out.append(p.as_posix())
    return out


# --------------------------------------------------------------------------
# Inti
# --------------------------------------------------------------------------
def snapshot(repo: P.Repo) -> dict:
    snap = {}
    for p in (repo.state_path, repo.dashboard_path):
        snap[p] = p.read_bytes() if p.exists() else None
    return snap


def pulihkan(snap: dict, evidence: Path) -> None:
    for p, isi in snap.items():
        if isi is None:
            p.unlink(missing_ok=True)
        else:
            p.write_bytes(isi)
    evidence.unlink(missing_ok=True)


def proses(root: Path, teks: str, today: dt.date, *, dry=False, pakai_git=True, push=True,
           bangun=True, buka=False, varian="gratis", runner=subprocess.run) -> int:
    root = Path(root)
    repo = P.Repo(root)

    # 1. entri
    try:
        e = yaml.safe_load(bersihkan_teks(teks))
    except yaml.YAMLError as x:
        raise P.StateError(f"Teks entri bukan YAML yang valid ({type(x).__name__}). Pastikan seluruh blok entri tersalin.")
    if not isinstance(e, dict) or not e.get("id"):
        raise P.StateError("Teks entri tidak dikenali sebagai Evidence Entry (kolom id tidak ada).")
    print(f"1/6 Entri: {e.get('id')}  modul={e.get('modul')}  jenis={e.get('jenis')}  skor={e.get('skor_persen')}")

    # 2. tarik versi terbaru
    if pakai_git and push and not dry:
        try:
            git(root, "pull", "--rebase", "--autostash", runner=runner)
        except P.StateError as x:
            raise P.StateError(f"{x}\nNiat menyimpan dibatalkan; belum ada yang berubah. "
                               "Tanpa internet? Pakai --tanpa-push (commit lokal), lalu git pull --rebase dan git push saat online.")
        print("2/6 git pull selesai (state lokal terbaru)")
    else:
        print("2/6 git pull dilewati")

    # 3. simulasi
    with tempfile.TemporaryDirectory() as tmp:
        nama = e["id"] if isinstance(e["id"], str) and P.ID_ENTRI.match(e["id"]) else "entri"
        berkas = Path(tmp) / f"{nama}.yaml"
        berkas.write_text(bersihkan_teks(teks), encoding="utf-8")
        msgs, _ = P.apply_entry(repo, berkas, today, dry=True)
        print("3/6 Lolos pemeriksaan rubrik:")
        for m in msgs:
            print("    •", m)
        if dry:
            print("\nDRY-RUN: tidak ada file yang diubah")
            return 0

        # 4. terapkan (dengan cadangan untuk pemulihan)
        snap = snapshot(repo)
        tujuan_evidence = repo.evidence_dir / f"{e['id']}.yaml"
        P.apply_entry(repo, berkas, today)
    print("4/6 state.yaml, dashboard.md, dan state/evidence/ diperbarui")

    # 5. periksa konsistensi
    errors, warnings = P.check(repo)
    if errors:
        pulihkan(snap, tujuan_evidence)
        raise P.StateError("State tidak konsisten setelah entri diterapkan; semua perubahan dikembalikan:\n  - "
                           + "\n  - ".join(errors))
    print(f"5/6 State konsisten ({len(warnings)} peringatan)")

    # 6. commit + push
    if pakai_git:
        paths = ["state/state.yaml", "state/dashboard.md", f"state/evidence/{e['id']}.yaml"]
        try:
            git(root, "add", "--", *paths, runner=runner)
            for b in jalur_bukti(root, e.get("bukti") or []):
                try:
                    git(root, "add", "--", b, runner=runner)
                    paths.append(b)
                except P.StateError as x:
                    print(f"    ⚠️  bukti tidak ikut di-commit (cek .gitignore?): {b}\n       {x}")
            pesan = f"progres: {e['modul']} {e['jenis']} ({e['skor_persen']}%)"
            # hanya path ini yang masuk commit, jadi file lain yang sedang kamu kerjakan tidak ikut terbawa
            git(root, "commit", "-m", pesan, "--", *paths, runner=runner)
            print(f"6/6 Commit: {pesan}")
            if push:
                git(root, "push", runner=runner)
                print("    Push berhasil")
            else:
                print("    Push dilewati (--tanpa-push); jalankan git push nanti")
        except P.StateError as x:
            print(f"❌ {x}")
            print("Progres SUDAH diterapkan di komputermu, tetapi belum tersimpan ke GitHub.")
            print("Perbaiki masalah git di atas, lalu jalankan: git add -A  &&  git commit  &&  git push")
            return 1
    else:
        print("6/6 Commit dilewati (--tanpa-git)")

    # paket Project (kegagalan di sini tidak membatalkan penyimpanan)
    folder = root / ("paket_project" if varian == "gratis" else "state")
    if bangun:
        try:
            spec = importlib.util.spec_from_file_location("bangun_paket", Path(__file__).resolve().parent / "bangun_paket.py")
            bp = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(bp)
            bp.main(["--root", str(root)])
        except Exception as x:  # noqa: BLE001
            print(f"⚠️  Paket Project gagal dibuat ({type(x).__name__}: {x}). Jalankan manual: python tools\\bangun_paket.py")
    print("\n✅ Progres tersimpan.")
    print(f"Langkah terakhir (manual): di ChatGPT Project, ganti state.yaml dan dashboard.md dengan yang ada di:\n  {folder}")
    if buka:
        buka_folder(folder)
    return 0


def buka_folder(folder: Path) -> None:
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(folder))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(folder)], check=False)
        else:
            subprocess.run(["xdg-open", str(folder)], check=False)
    except OSError:
        pass


def main(argv=None) -> int:
    P.pakai_utf8()
    ap = argparse.ArgumentParser(description="Simpan progres belajar dengan satu perintah")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--today", default=None)
    ap.add_argument("--berkas", default=None, help="baca entri dari berkas, bukan clipboard")
    ap.add_argument("--dry", action="store_true", help="hanya periksa dan simulasi")
    ap.add_argument("--tanpa-push", action="store_true", help="commit saja, jangan push")
    ap.add_argument("--tanpa-git", action="store_true", help="terapkan ke file saja, tanpa pull/commit/push")
    ap.add_argument("--varian", choices=["gratis", "plus"], default="gratis",
                    help="gratis: buka paket_project/ (5 file); plus: buka state/")
    ap.add_argument("--tidak-buka", action="store_true", help="jangan membuka folder unggahan")
    ap.add_argument("--tanpa-paket", action="store_true", help="jangan membangun ulang paket_project/")
    a = ap.parse_args(argv)

    today = P.to_date(a.today) if a.today else dt.date.today()
    try:
        teks = baca_berkas(a.berkas) if a.berkas else baca_clipboard()
        return proses(Path(a.root), teks, today, dry=a.dry, pakai_git=not a.tanpa_git,
                      push=not a.tanpa_push, bangun=a.varian == "gratis" and not a.tanpa_paket,
                      buka=not a.tidak_buka, varian=a.varian)
    except P.StateError as x:
        print(f"❌ {x}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
