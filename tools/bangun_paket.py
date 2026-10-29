#!/usr/bin/env python3
"""Bangun paket 4 file aturan untuk ChatGPT Project paket Free (batas 5 file).

Pemakaian (dari folder repo):
    python tools\\bangun_paket.py

Hasil: folder `paket_project/` berisi 4 file siap unggah. Progres (state.yaml, dashboard.md)
tidak ikut, karena mentor membacanya langsung dari GitHub. Folder itu turunan,
bukan sumber kebenaran, dan diabaikan git. Sumbernya tetap `system/` dan `state/`.
Jalankan ulang setiap kali `system/` berubah, lalu ganti file yang berubah di Project.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

# Dokumen yang digabung menjadi satu file `aturan_mentor.md`, berurutan.
GABUNG = [
    ("KONSTITUSI (aturan tertinggi)", "system/01_constitution.md"),
    ("PROTOKOL MENTOR", "system/04_protokol_mentor.md"),
    ("ATURAN PENYAJIAN MATERI", "system/08_penyajian_materi.md"),
    ("ALUR KERJA DAN COMMAND", "system/07_alur_kerja_command.md"),
    ("SPESIFIKASI DASHBOARD", "system/05_spesifikasi_dashboard.md"),
    ("KEBIJAKAN REFERENSI BELAJAR", "system/06_kebijakan_referensi.md"),
]

# File yang disalin apa adanya: (asal, nama di paket)
SALIN = [
    ("system/02_roadmap.md", "02_roadmap.md"),
    ("system/03_rubrik_validasi.md", "03_rubrik_validasi.md"),
    ("system/09_kurikulum.md", "09_kurikulum.md"),
]

KEPALA = """\
# Aturan Mentor: Learn A.I Workflow for Data Science

File ini adalah gabungan otomatis dari {n} dokumen sistem (dibuat oleh `tools/bangun_paket.py`).
Jangan diedit di sini; ubah sumbernya di folder `system/` lalu bangun ulang.

Isi, berurutan:
{daftar}

Petunjuk membaca: rujukan ke file seperti `system/04_protokol_mentor.md` berarti bagian
yang bersangkutan di file ini. Rujukan ke `system/03_rubrik_validasi.md` dan
`system/02_roadmap.md` berarti file `03_rubrik_validasi.md` dan `02_roadmap.md` di Project,
dan rujukan ke `system/09_kurikulum.md` berarti file `09_kurikulum.md` di Project.
"""

FRONT = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.S)


def baca(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def main(argv=None) -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Bangun paket 4 file aturan untuk ChatGPT Project (Free)")
    ap.add_argument("--root", default=".", help="folder repo (default: folder saat ini)")
    ap.add_argument("--keluar", default="paket_project", help="nama folder hasil")
    a = ap.parse_args(argv)

    root = Path(a.root).resolve()
    keluar = root / a.keluar
    perlu = [p for _, p in GABUNG] + [s for s, _ in SALIN]
    hilang = [p for p in perlu if not (root / p).is_file()]
    if hilang:
        print("❌ File sumber tidak ditemukan:\n  " + "\n  ".join(hilang))
        return 1

    if keluar.exists():
        shutil.rmtree(keluar)
    keluar.mkdir(parents=True)

    daftar = "\n".join(f"{i}. {judul} (asal: `{p}`)" for i, (judul, p) in enumerate(GABUNG, 1))
    bagian = [KEPALA.format(n=len(GABUNG), daftar=daftar)]
    for i, (judul, p) in enumerate(GABUNG, 1):
        isi = FRONT.sub("", baca(root / p), count=1).strip()
        bagian.append(f"\n\n---\n\n# [BAGIAN {i} dari {len(GABUNG)}] {judul}\n\n{isi}\n")
    (keluar / "aturan_mentor.md").write_text("".join(bagian), encoding="utf-8", newline="\n")

    for asal, nama in SALIN:
        shutil.copyfile(root / asal, keluar / nama)

    print(f"✅ Paket dibuat di: {keluar}")
    for f in sorted(keluar.iterdir()):
        print(f"  {f.name}  ({f.stat().st_size / 1024:.1f} KB)")
    print("Unggah keempat file itu ke ChatGPT Project hanya bila system/ berubah. Progres dibaca mentor dari GitHub.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
