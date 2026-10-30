"""Tes untuk tools/simpan.py (satu perintah simpan progres). Jalankan dari akar repo:
    python -m unittest discover -s tests -v

Tes memakai repo git sementara dengan remote bare sungguhan, jadi pull, commit, dan push
benar-benar dijalankan (tanpa jaringan).
"""
import contextlib
import datetime as dt
import importlib.util
import io
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

from bantuan_uji import lengkapi

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("simpan", ROOT / "tools" / "simpan.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

D = dt.date
FIXTURE = ROOT / "tests" / "fixtures" / "state"
FIXTURE_SYSTEM = ROOT / "tests" / "fixtures" / "system"


def git(cwd, *args, check=True):
    r = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode != 0:
        raise AssertionError(f"git {' '.join(args)}: {r.stderr}")
    return r.stdout.strip()


def siapkan_identitas(repo):
    git(repo, "config", "user.name", "Penguji")
    git(repo, "config", "user.email", "penguji@example.com")
    git(repo, "config", "commit.gpgsign", "false")


class TestBersihkanTeks(unittest.TestCase):
    def test_pagar_yaml_dibuang(self):
        teks = "Ini entrinya:\n```yaml\nid: a\nmodul: b\n```\nSelesai."
        self.assertEqual(S.bersihkan_teks(teks), "id: a\nmodul: b\n")

    def test_pagar_tanpa_bahasa(self):
        self.assertEqual(S.bersihkan_teks("```\nid: a\n```"), "id: a\n")

    def test_bom_dan_crlf(self):
        self.assertEqual(S.bersihkan_teks("﻿id: a\r\nmodul: b\r\n"), "id: a\nmodul: b\n")

    def test_teks_polos_tidak_berubah(self):
        self.assertEqual(S.bersihkan_teks("id: a\nmodul: b\n"), "id: a\nmodul: b\n")

    def test_indentasi_seragam_dirapikan(self):
        self.assertEqual(S.bersihkan_teks("  id: a\n  modul: b\n"), "id: a\nmodul: b\n")


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.remote = self.tmp / "remote.git"
        self.work = self.tmp / "work"
        git(self.tmp, "init", "--bare", "-b", "main", str(self.remote))
        self.work.mkdir()
        git(self.work, "init", "-b", "main")
        siapkan_identitas(self.work)
        shutil.copytree(FIXTURE, self.work / "state")
        shutil.copytree(FIXTURE_SYSTEM, self.work / "system")
        (self.work / "notebooks").mkdir()
        (self.work / "notebooks" / "matplotlib_review.ipynb").write_text("{}", encoding="utf-8")
        (self.work / "README.md").write_text("awal\n", encoding="utf-8")
        git(self.work, "add", "-A")
        git(self.work, "commit", "-m", "awal")
        git(self.work, "remote", "add", "origin", str(self.remote))
        git(self.work, "push", "-u", "origin", "main")
        self.repo = S.P.Repo(self.work)
        self.today = D(2026, 10, 22)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def teks(self, **kw):
        e = {
            "id": "uji-1", "modul": "matplotlib_review", "tanggal": D(2026, 10, 22),
            "jenis": "validasi", "skor_persen": 90, "mode_ai": "assisted",
            "level_soal": "L1, L2, L3", "bukti": ["notebooks/matplotlib_review.ipynb"],
            "pemahaman": "Memilih Axes agar subplot konsisten; log scale untuk data skewed",
            "keputusan": "validated",
        }
        e.update(kw)
        e = lengkapi(e, kw)
        isi = yaml.safe_dump(e, allow_unicode=True, sort_keys=False)
        return f"Berikut entrinya:\n```yaml\n{isi}```\n"

    def jalankan(self, teks=None, **kw):
        kw.setdefault("bangun", False)
        kw.setdefault("cek_nb", False)  # notebook uji berisi "{}"; cek notebook diuji terpisah di bawah
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = S.proses(self.work, self.teks() if teks is None else teks, self.today, **kw)
        return kode, out.getvalue()

    def jumlah_commit(self):
        return int(git(self.work, "rev-list", "--count", "HEAD"))

    def status_item(self, item_id):
        data, _ = self.repo.load()
        return S.P.find(data, item_id)[1]["item"]["status"]


class TestSimpan(Base):
    def test_alur_lengkap_satu_perintah(self):
        # file bukti baru: belum pernah di-commit, harus ikut masuk ke commit yang sama
        (self.work / "notebooks" / "baru.ipynb").write_text("{}", encoding="utf-8")
        kode, _ = self.jalankan(self.teks(bukti=["notebooks/baru.ipynb"]))
        self.assertEqual(kode, 0)
        self.assertEqual(self.status_item("matplotlib_review"), "validated")
        errors, _ = S.P.check(self.repo)
        self.assertEqual(errors, [])
        self.assertTrue((self.work / "state" / "evidence" / "uji-1.yaml").exists())
        # commit sampai ke remote, berisi state + bukti dalam SATU commit
        self.assertEqual(git(self.remote, "log", "-1", "--format=%s", "main"),
                         "progres: matplotlib_review validasi (90%)")
        berkas = git(self.remote, "show", "--name-only", "--format=", "main").splitlines()
        for f in ("state/state.yaml", "state/dashboard.md", "state/evidence/uji-1.yaml",
                  "notebooks/baru.ipynb"):
            self.assertIn(f, berkas)
        self.assertEqual(git(self.work, "status", "--porcelain"), "")

    def test_file_lain_tidak_ikut_commit(self):
        (self.work / "README.md").write_text("sedang diubah\n", encoding="utf-8")
        kode, _ = self.jalankan()
        self.assertEqual(kode, 0)
        berkas = git(self.remote, "show", "--name-only", "--format=", "main").splitlines()
        self.assertNotIn("README.md", berkas)
        self.assertEqual((self.work / "README.md").read_text(encoding="utf-8"), "sedang diubah\n")

    def test_tidak_perlu_pull_manual_setelah_ada_commit_lain(self):
        lain = self.tmp / "lain"
        git(self.tmp, "clone", str(self.remote), str(lain))
        siapkan_identitas(lain)
        (lain / "catatan.txt").write_text("dari tempat lain\n", encoding="utf-8")
        git(lain, "add", "-A")
        git(lain, "commit", "-m", "commit dari tempat lain")
        git(lain, "push")
        kode, _ = self.jalankan()
        self.assertEqual(kode, 0)
        self.assertTrue((self.work / "catatan.txt").exists())
        self.assertEqual(git(self.remote, "log", "-1", "--format=%s", "main"),
                         "progres: matplotlib_review validasi (90%)")

    def test_entri_ditolak_tidak_mengubah_apa_pun(self):
        sebelum = (self.work / "state" / "state.yaml").read_bytes()
        n = self.jumlah_commit()
        with self.assertRaises(S.P.StateError):
            self.jalankan(self.teks(skor_persen=70))  # keputusan 'validated' tidak cocok dengan skor 70
        self.assertEqual((self.work / "state" / "state.yaml").read_bytes(), sebelum)
        self.assertEqual(self.jumlah_commit(), n)
        self.assertFalse((self.work / "state" / "evidence" / "uji-1.yaml").exists())

    def test_bukti_tidak_ada_ditolak(self):
        with self.assertRaises(S.P.StateError) as cm:
            self.jalankan(self.teks(bukti=["notebooks/tidak_ada.ipynb"]))
        self.assertIn("bukti tidak ditemukan", str(cm.exception))

    def test_dry_tidak_mengubah_apa_pun(self):
        sebelum = (self.work / "state" / "state.yaml").read_bytes()
        n = self.jumlah_commit()
        kode, keluar = self.jalankan(dry=True)
        self.assertEqual(kode, 0)
        self.assertIn("DRY-RUN", keluar)
        self.assertEqual((self.work / "state" / "state.yaml").read_bytes(), sebelum)
        self.assertEqual(self.jumlah_commit(), n)

    def test_teks_bukan_entri_ditolak(self):
        with self.assertRaises(S.P.StateError):
            self.jalankan("ini bukan entri sama sekali")

    def test_yaml_rusak_ditolak(self):
        with self.assertRaises(S.P.StateError):
            self.jalankan("```yaml\nid: [rusak\n```")

    def test_pulih_bila_check_gagal(self):
        sebelum = (self.work / "state" / "state.yaml").read_bytes()
        dashboard = (self.work / "state" / "dashboard.md").read_bytes()
        asli = S.P.check
        S.P.check = lambda repo, data=None: (["error buatan"], [])
        try:
            with self.assertRaises(S.P.StateError):
                self.jalankan()
        finally:
            S.P.check = asli
        self.assertEqual((self.work / "state" / "state.yaml").read_bytes(), sebelum)
        self.assertEqual((self.work / "state" / "dashboard.md").read_bytes(), dashboard)
        self.assertFalse((self.work / "state" / "evidence" / "uji-1.yaml").exists())

    def test_tanpa_push_hanya_commit_lokal(self):
        n = self.jumlah_commit()
        kode, _ = self.jalankan(push=False)
        self.assertEqual(kode, 0)
        self.assertEqual(self.jumlah_commit(), n + 1)
        self.assertEqual(git(self.remote, "log", "-1", "--format=%s", "main"), "awal")

    def test_tanpa_git_hanya_ubah_file(self):
        n = self.jumlah_commit()
        kode, _ = self.jalankan(pakai_git=False)
        self.assertEqual(kode, 0)
        self.assertEqual(self.status_item("matplotlib_review"), "validated")
        self.assertEqual(self.jumlah_commit(), n)

    def test_push_gagal_progres_tetap_terterap_dan_kode_1(self):
        def runner(cmd, **kw):
            if cmd[:2] == ["git", "push"]:
                return subprocess.CompletedProcess(cmd, 1, stdout="", stderr="ditolak remote")
            return subprocess.run(cmd, **kw)
        kode, keluar = self.jalankan(runner=runner)
        self.assertEqual(kode, 1)
        self.assertIn("SUDAH diterapkan", keluar)
        self.assertEqual(self.status_item("matplotlib_review"), "validated")
        self.assertEqual(git(self.work, "log", "-1", "--format=%s"), "progres: matplotlib_review validasi (90%)")

    def test_id_ganda_ditolak_pada_simpan_kedua(self):
        self.jalankan()
        with self.assertRaises(S.P.StateError):
            self.jalankan()


class TestCekNotebook(Base):
    def test_notebook_gagal_membatalkan_tanpa_perubahan(self):
        sebelum = (self.work / "state" / "state.yaml").read_bytes()
        n = self.jumlah_commit()
        with self.assertRaises(S.P.StateError) as cm:
            self.jalankan(cek_nb=True, pemeriksa_nb=lambda rel: (False, "sel error: FileNotFoundError"))
        self.assertIn("tidak bisa dijalankan ulang", str(cm.exception))
        self.assertIn("--tanpa-cek-notebook", str(cm.exception))
        self.assertEqual((self.work / "state" / "state.yaml").read_bytes(), sebelum)
        self.assertEqual(self.jumlah_commit(), n)

    def test_notebook_lolos_lanjut_menyimpan(self):
        dicek = []
        kode, keluar = self.jalankan(cek_nb=True, pemeriksa_nb=lambda rel: (dicek.append(rel.as_posix()) or (True, "lolos")))
        self.assertEqual(kode, 0)
        self.assertEqual(dicek, ["notebooks/matplotlib_review.ipynb"])
        self.assertIn("✅ notebook", keluar)

    def test_bukti_bukan_notebook_tidak_dicek(self):
        (self.work / "notebooks" / "grafik.png").write_bytes(b"png")
        kode, _ = self.jalankan(self.teks(bukti=["notebooks/grafik.png"]), cek_nb=True,
                                pemeriksa_nb=lambda rel: (False, "tidak boleh dipanggil"))
        self.assertEqual(kode, 0)


class TestCli(Base):
    def test_main_dari_berkas(self):
        berkas = self.tmp / "entri.yaml"
        berkas.write_text(self.teks(), encoding="utf-8")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = S.main(["--root", str(self.work), "--berkas", str(berkas), "--today", "2026-10-22",
                           "--tanpa-paket", "--tidak-buka", "--tanpa-cek-notebook"])
        self.assertEqual(kode, 0, out.getvalue())
        self.assertEqual(self.status_item("matplotlib_review"), "validated")

    def test_main_berkas_tidak_ada(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = S.main(["--root", str(self.work), "--berkas", str(self.tmp / "tidak-ada.yaml")])
        self.assertEqual(kode, 1)
        self.assertIn("tidak ditemukan", out.getvalue())


if __name__ == "__main__":
    unittest.main()
