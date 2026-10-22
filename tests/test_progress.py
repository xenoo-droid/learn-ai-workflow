"""Tes untuk tools/progress.py. Jalankan dari akar repo:
    python -m unittest discover -s tests -v
"""
import datetime as dt
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("progress", ROOT / "tools" / "progress.py")
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)

D = dt.date


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(ROOT / "state", self.tmp / "state")
        self.repo = P.Repo(self.tmp)
        self.today = D(2026, 10, 22)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def entry(self, **kw):
        e = {
            "id": "uji-1", "modul": "matplotlib_review", "tanggal": D(2026, 10, 22),
            "jenis": "validasi", "skor_persen": 90, "mode_ai": "assisted",
            "level_soal": "L1, L2, L3", "bukti": ["notebooks/matplotlib_review.ipynb"],
            "pemahaman": "Memilih Axes agar subplot konsisten; log scale untuk data skewed",
            "keputusan": "validated",
        }
        e.update(kw)
        p = self.tmp / f"{e['id']}.yaml"
        p.write_text(yaml.safe_dump(e, allow_unicode=True, sort_keys=False), encoding="utf-8")
        return p

    def apply(self, today=None, **kw):
        return P.apply_entry(self.repo, self.entry(**kw), today or self.today)

    def item(self, item_id):
        data, _ = self.repo.load()
        return P.find(data, item_id)[1]["item"]


class TestState(Base):
    def test_state_asli_konsisten(self):
        errors, _ = P.check(self.repo)
        self.assertEqual(errors, [])

    def test_roundtrip_tidak_mengubah_data(self):
        data, header = self.repo.load()
        self.repo.save(data, header)
        data2, header2 = self.repo.load()
        self.assertEqual(data, data2)
        self.assertEqual(header, header2)

    def test_dua_quest_aktif_terdeteksi(self):
        data, header = self.repo.load()
        P.find(data, "seaborn")[1]["item"]["status"] = "aktif"
        errors, _ = P.check(self.repo, data)
        self.assertTrue(any("lebih dari satu quest aktif" in e for e in errors))

    def test_lompatan_terdeteksi(self):
        data, _ = self.repo.load()
        P.find(data, "sql_database")[1]["item"]["status"] = "validated_legacy"
        errors, _ = P.check(self.repo, data)
        self.assertTrue(any("melompati roadmap" in e for e in errors))

    def test_validated_tanpa_evidence_ditolak(self):
        data, _ = self.repo.load()
        it = P.find(data, "numpy")[1]["item"]
        it["status"] = "validated"
        errors, _ = P.check(self.repo, data)
        self.assertTrue(any("wajib punya evidence" in e for e in errors))

    def test_portfolio_terkunci_sebelum_prasyarat(self):
        data, _ = self.repo.load()
        P.find(data, "portfolio_1")[1]["item"]["status"] = "validated_legacy"
        errors, _ = P.check(self.repo, data)
        self.assertTrue(any("prasyarat" in e for e in errors))


class TestValidasi(Base):
    def test_lulus_memajukan_quest(self):
        msgs, _ = self.apply()
        it = self.item("matplotlib_review")
        self.assertEqual(it["status"], "validated")
        self.assertEqual(it["review_berikutnya"], D(2026, 10, 29))
        self.assertEqual(self.item("seaborn")["status"], "aktif")
        data, _ = self.repo.load()
        self.assertEqual(data["quest_berikutnya"], "jupyter_colab")
        self.assertEqual(data["kemenangan_terbaru"], "matplotlib_review")
        errors, warnings = P.check(self.repo)
        self.assertEqual(errors, [])
        self.assertFalse(any("tidak sinkron" in w for w in warnings))

    def test_skor_rendah_status_tidak_berubah(self):
        self.apply(skor_persen=70, keputusan="tetap")
        self.assertEqual(self.item("matplotlib_review")["status"], "aktif")
        self.assertEqual(self.item("seaborn")["status"], "belum")
        self.assertTrue((self.tmp / "state" / "evidence" / "uji-1.yaml").exists())

    def test_keputusan_tidak_sesuai_ditolak(self):
        with self.assertRaises(P.StateError):
            self.apply(skor_persen=70, keputusan="validated")

    def test_melompati_modul_ditolak(self):
        with self.assertRaises(P.StateError):
            self.apply(modul="seaborn")

    def test_pemahaman_wajib(self):
        with self.assertRaises(P.StateError):
            self.apply(pemahaman="")

    def test_tanggal_masa_depan_ditolak(self):
        with self.assertRaises(P.StateError):
            self.apply(tanggal=D(2026, 12, 1))

    def test_legacy_naik_ke_validated_dengan_bukti(self):
        self.apply(modul="numpy", id="uji-np")
        self.assertEqual(self.item("numpy")["status"], "validated")
        # quest aktif tidak bergeser karena numpy bukan quest aktif
        self.assertEqual(self.item("matplotlib_review")["status"], "aktif")

    def test_dry_run_tidak_mengubah_file(self):
        before = (self.tmp / "state" / "state.yaml").read_text(encoding="utf-8")
        P.apply_entry(self.repo, self.entry(), self.today, dry=True)
        self.assertEqual(before, (self.tmp / "state" / "state.yaml").read_text(encoding="utf-8"))


class TestRetensi(Base):
    def test_retrieval_legacy_langsung_retained(self):
        self.apply(modul="numpy", id="uji-r", jenis="retrieval", mode_ai="independent",
                   skor_persen=85, keputusan="retained", pemahaman=None)
        it = self.item("numpy")
        self.assertEqual(it["status"], "retained")
        self.assertEqual(it["review_berikutnya"], D(2026, 11, 21))

    def test_retrieval_wajib_independent(self):
        with self.assertRaises(P.StateError):
            self.apply(modul="numpy", jenis="retrieval", mode_ai="assisted", keputusan="retained")

    def test_retrieval_gagal_menandai_perlu_review(self):
        self.apply(modul="numpy", jenis="retrieval", mode_ai="independent",
                   skor_persen=60, keputusan="tetap")
        it = self.item("numpy")
        self.assertEqual(it["status"], "validated_legacy")
        self.assertTrue(it["perlu_review"])
        self.assertEqual(it["review_berikutnya"], D(2026, 10, 25))

    def test_jeda_minimal_7_hari(self):
        self.apply()  # matplotlib_review validated 2026-10-22
        with self.assertRaises(P.StateError):
            self.apply(id="uji-r", modul="matplotlib_review", jenis="retrieval",
                       mode_ai="independent", tanggal=D(2026, 10, 25), keputusan="retained",
                       today=D(2026, 10, 25))
        self.apply(id="uji-r2", modul="matplotlib_review", jenis="retrieval",
                   mode_ai="independent", tanggal=D(2026, 10, 29), keputusan="retained",
                   today=D(2026, 10, 29))
        it = self.item("matplotlib_review")
        self.assertEqual(it["status"], "retained")
        self.assertEqual(it["review_berikutnya"], D(2026, 11, 21))

    def test_mastery_butuh_retained_dan_dua_konteks(self):
        with self.assertRaises(P.StateError):  # masih legacy
            self.apply(modul="numpy", jenis="mastery", mode_ai="independent",
                       konteks=["a", "b"], keputusan="mastered")
        self.apply(modul="numpy", id="uji-r", jenis="retrieval", mode_ai="independent",
                   keputusan="retained")
        with self.assertRaises(P.StateError):  # konteks kurang
            self.apply(modul="numpy", id="uji-m", jenis="mastery", mode_ai="independent",
                       konteks=["satu"], keputusan="mastered")
        self.apply(modul="numpy", id="uji-m2", jenis="mastery", mode_ai="independent",
                   konteks=["proyek A", "proyek B"], keputusan="mastered")
        self.assertEqual(self.item("numpy")["status"], "mastered")


class TestDueDanDashboard(Base):
    def test_due(self):
        data, _ = self.repo.load()
        jatuh, legacy = P.due(data, self.today)
        self.assertEqual([i["id"] for i, _ in jatuh], ["savefig"])
        self.assertEqual(legacy[0]["id"], "python_fundamentals")
        # 8 modul World 1 + NumPy + Pandas + 11 quest Matplotlib = 21
        self.assertEqual(len(legacy), 21)

    def test_dashboard_memuat_elemen_wajib(self):
        data, _ = self.repo.load()
        out = P.render_dashboard(data)
        for s in ("WORLD 1", "CLEARED", "BOSS BATTLE", "CURRENT QUEST", "NEXT QUEST",
                  "LATEST WIN", "CURRENT POSITION", "SEABORN", "LOCKED"):
            self.assertIn(s, out)
        self.assertNotIn("COMPLETED", out)

    def test_dashboard_dari_cli_tulis(self):
        rc = P.main(["--root", str(self.tmp), "--today", "2026-10-22", "dashboard", "--tulis"])
        self.assertEqual(rc, 0)
        self.assertTrue((self.tmp / "state" / "dashboard.md").exists())
        errors, warnings = P.check(self.repo)
        self.assertEqual(errors, [])
        self.assertFalse(any("tidak sinkron" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()
