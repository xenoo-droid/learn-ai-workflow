#!/usr/bin/env python3
"""cek_notebook.py - pastikan notebook bukti bisa dijalankan ulang dari awal sampai akhir.

Rubrik (system/03_rubrik_validasi.md bagian 3) meminta bukti yang bisa dibuka kembali.
Script ini menjalankan setiap notebook `.ipynb` yang dirujuk di `bukti:` sebuah Evidence
Entry, di salinan sementara (notebook aslinya tidak diubah), dengan folder kerja = folder
notebook itu, sehingga file data harus ada di samping notebook (aturan notebooks/README.md).

    python tools\\cek_notebook.py                    cek notebook dari entri format baru (punya ujian:)
    python tools\\cek_notebook.py --semua            cek notebook dari semua entri, termasuk format lama
    python tools\\cek_notebook.py --entri e.yaml     cek notebook dari satu entri (dipakai simpan.py)
    python tools\\cek_notebook.py nb1.ipynb nb2.ipynb  cek notebook tertentu

Sel yang memang sengaja menampilkan error (misalnya contoh exception) diberi tag
`raises-exception` di Jupyter (View → Cell Toolbar → Tags), maka tidak dianggap gagal.

Kebutuhan tambahan: pip install -r requirements-notebook.txt
Kode keluar: 0 semua lolos, 1 ada yang gagal, 2 nbclient/ipykernel belum terpasang.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

BATAS_DETIK = 600
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def notebook_dari_entri(root: Path, e: dict) -> list:
    out = []
    for b in (e.get("bukti") or []) if isinstance(e, dict) else []:
        if isinstance(b, str) and not b.startswith(("http://", "https://")) and b.lower().endswith(".ipynb"):
            p = Path(b.replace("\\", "/"))
            if not p.is_absolute() and ".." not in p.parts:
                out.append(p)
    return out


def kumpulkan(root: Path, semua: bool) -> list:
    """Daftar (path notebook, id entri) dari state/evidence/."""
    hasil, terlihat = [], set()
    for f in sorted((root / "state" / "evidence").glob("*.yaml")):
        try:
            e = yaml.safe_load(f.read_text(encoding="utf-8-sig"))
        except (yaml.YAMLError, UnicodeDecodeError):
            continue
        if not isinstance(e, dict) or (not semua and e.get("ujian") is None):
            continue
        for p in notebook_dari_entri(root, e):
            if p not in terlihat:
                terlihat.add(p)
                hasil.append((p, e.get("id")))
    return hasil


def jalankan(root: Path, rel: Path, batas: int = BATAS_DETIK):
    """Jalankan satu notebook. Kembalikan (lolos, pesan)."""
    import nbformat
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError, CellTimeoutError, DeadKernelError

    asli = (root / rel).resolve()
    if not asli.is_file():
        return False, "file tidak ditemukan"
    with tempfile.TemporaryDirectory() as tmp:
        # salin seluruh folder notebook supaya file data di sampingnya ikut, tanpa menyentuh aslinya
        kerja = Path(tmp) / "nb"
        shutil.copytree(asli.parent, kerja, ignore=shutil.ignore_patterns(".ipynb_checkpoints"))
        nb = nbformat.read(str(kerja / asli.name), as_version=4)
        nama_kernel = (nb.metadata.get("kernelspec") or {}).get("name") or "python3"
        os.environ.setdefault("MPLBACKEND", "Agg")  # grafik tidak membuka jendela
        client = NotebookClient(nb, timeout=batas, kernel_name="python3" if nama_kernel.startswith("python") else nama_kernel,
                                resources={"metadata": {"path": str(kerja)}})
        try:
            client.execute()
        except CellExecutionError as x:
            baris = [b for b in ANSI.sub("", str(x)).splitlines() if b.strip()]
            inti = next((b for b in reversed(baris) if "Error" in b or "Exception" in b), baris[-1] if baris else "")
            return False, f"sel error: {inti.strip()[:300]}"
        except CellTimeoutError:
            return False, f"sel melebihi batas waktu {batas} detik"
        except DeadKernelError:
            return False, "kernel berhenti (kehabisan memori?)"
        except Exception as x:  # noqa: BLE001 - kernel tidak ada, dsb.
            return False, f"{type(x).__name__}: {str(x).strip()[:300]}"
    return True, "lolos"


def siap() -> bool:
    try:
        import ipykernel  # noqa: F401
        import nbclient  # noqa: F401
        import nbformat  # noqa: F401
    except ImportError:
        return False
    return True


def main(argv=None) -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Jalankan ulang notebook bukti dari Evidence Entry")
    ap.add_argument("notebook", nargs="*", help="path notebook relatif terhadap repo")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--semua", action="store_true", help="termasuk entri format lama (tanpa ujian:)")
    ap.add_argument("--entri", default=None, help="cek notebook dari satu berkas entri")
    ap.add_argument("--batas", type=int, default=BATAS_DETIK, help="batas detik per sel")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()

    if a.notebook:
        daftar = [(Path(n.replace("\\", "/")), None) for n in a.notebook]
    elif a.entri:
        e = yaml.safe_load(Path(a.entri).read_text(encoding="utf-8-sig"))
        daftar = [(p, e.get("id") if isinstance(e, dict) else None) for p in notebook_dari_entri(root, e)]
    else:
        daftar = kumpulkan(root, a.semua)

    if not daftar:
        print("Tidak ada notebook bukti untuk dicek.")
        return 0
    if not siap():
        print("⚠️  nbclient/ipykernel belum terpasang. Pasang dengan: pip install -r requirements-notebook.txt")
        return 2

    gagal = 0
    for rel, eid in daftar:
        lolos, pesan = jalankan(root, rel, a.batas)
        asal = f"  (entri {eid})" if eid else ""
        print(f"{'✅' if lolos else '❌'} {rel.as_posix()}{asal}: {pesan}")
        gagal += not lolos
    if gagal:
        print(f"\n{gagal} notebook gagal dijalankan ulang. Perbaiki errornya, atau pastikan file data ada di samping notebook.")
        return 1
    print(f"\nSemua {len(daftar)} notebook bisa dijalankan ulang.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
