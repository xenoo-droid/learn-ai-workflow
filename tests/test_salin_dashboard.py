"""Tes untuk tools/salin_dashboard.py (salin dashboard ke clipboard untuk mentor).
Jalankan dari akar repo:
    python -m unittest discover -s tests -v
"""
import contextlib
import datetime as dt
import importlib.util
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
spec = importlib.util.spec_from_file_location("salin_dashboard", ROOT / "tools" / "salin_dashboard.py")
SD = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SD)
P = SD.P
FIXTURE = ROOT / "tests" / "fixtures" / "state"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(FIXTURE, self.tmp / "state")
        self.repo = P.Repo(self.tmp)
        data, _ = self.repo.load()
        self.repo.dashboard_path.write_text(P.dashboard_file(data), encoding="utf-8")
        self.today = dt.date(2026, 10, 22)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestSusunTeks(Base):
    def test_berisi_dashboard_tanpa_review(self):
        teks = SD.susun_teks(self.repo, self.today)
        self.assertIn("CURRENT QUEST", teks)
        self.assertNotIn("jatuh tempo", teks)
        self.assertNotIn("Antrean legacy", teks)
        self.assertNotIn("Konsep lemah", teks)  # fixture tidak punya konsep lemah
        self.assertNotIn("<!--", teks)

    def test_konsep_lemah_ikut(self):
        data, header = self.repo.load()
        P.find(data, "numpy")[1]["item"]["konsep_lemah"] = ["axis: tertukar axis=0 dan axis=1"]
        self.repo.save(data, header)
        self.repo.dashboard_path.write_text(P.dashboard_file(data), encoding="utf-8")
        self.assertIn("NumPy [numpy]: axis: tertukar", SD.susun_teks(self.repo, self.today))

    def test_dashboard_tidak_sinkron_ditolak(self):
        self.repo.dashboard_path.write_text("dashboard lama\n", encoding="utf-8")
        with self.assertRaisesRegex(P.StateError, "tidak sinkron"):
            SD.susun_teks(self.repo, self.today)

    def test_dashboard_tidak_ada_ditolak(self):
        self.repo.dashboard_path.unlink()
        with self.assertRaisesRegex(P.StateError, "belum ada"):
            SD.susun_teks(self.repo, self.today)


class TestMain(Base):
    def jalan(self, *args, clipboard=None):
        tersalin = []
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = SD.main(["--root", str(self.tmp), "--today", "2026-10-22", *args],
                           clipboard=clipboard or tersalin.append)
        return kode, out.getvalue(), tersalin

    def test_tersalin_ke_clipboard(self):
        kode, keluar, tersalin = self.jalan()
        self.assertEqual(kode, 0)
        self.assertEqual(len(tersalin), 1)
        self.assertIn("CURRENT QUEST", tersalin[0])
        self.assertIn("Tersalin ke clipboard", keluar)

    def test_tanpa_clipboard(self):
        kode, keluar, tersalin = self.jalan("--tanpa-clipboard")
        self.assertEqual(kode, 0)
        self.assertEqual(tersalin, [])
        self.assertIn("CURRENT QUEST", keluar)

    def test_clipboard_gagal_tetap_tampil(self):
        def gagal(_):
            raise OSError("tidak ada clipboard")
        kode, keluar, _ = self.jalan(clipboard=gagal)
        self.assertEqual(kode, 1)
        self.assertIn("CURRENT QUEST", keluar)
        self.assertIn("disalin manual", keluar)

    def test_tidak_mengubah_file(self):
        sebelum = {p: p.read_bytes() for p in (self.tmp / "state").rglob("*") if p.is_file()}
        self.jalan()
        sesudah = {p: p.read_bytes() for p in (self.tmp / "state").rglob("*") if p.is_file()}
        self.assertEqual(sebelum, sesudah)


class TestBelumDiPush(unittest.TestCase):
    def test_hitung_commit(self):
        r = lambda cmd, **kw: subprocess.CompletedProcess(cmd, 0, stdout="2\n", stderr="")  # noqa: E731
        self.assertEqual(SD.belum_di_push(Path("."), runner=r), 2)

    def test_tanpa_upstream_atau_git(self):
        r = lambda cmd, **kw: subprocess.CompletedProcess(cmd, 128, stdout="", stderr="no upstream")  # noqa: E731
        self.assertIsNone(SD.belum_di_push(Path("."), runner=r))

        def tanpa_git(cmd, **kw):
            raise OSError("git tidak ada")
        self.assertIsNone(SD.belum_di_push(Path("."), runner=tanpa_git))


if __name__ == "__main__":
    unittest.main()
