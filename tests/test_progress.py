"""Tes untuk tools/progress.py. Jalankan dari akar repo:
    python -m unittest discover -s tests -v
"""
import contextlib
import datetime as dt
import importlib.util
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from bantuan_uji import lengkapi

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("progress", ROOT / "tools" / "progress.py")
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)

D = dt.date

# State uji dibekukan di tests/fixtures/state (kondisi sebelum Matplotlib Review divalidasi),
# supaya tes tidak ikut berubah ketika state.yaml asli maju setelah tiap milestone.
FIXTURE = ROOT / "tests" / "fixtures" / "state"
FIXTURE_SYSTEM = ROOT / "tests" / "fixtures" / "system"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(FIXTURE, self.tmp / "state")
        shutil.copytree(FIXTURE_SYSTEM, self.tmp / "system")
        (self.tmp / "notebooks").mkdir()
        (self.tmp / "notebooks" / "matplotlib_review.ipynb").write_text("{}", encoding="utf-8")
        self.repo = P.Repo(self.tmp)
        self.today = D(2026, 10, 22)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def entry(self, dir=None, **kw):
        e = {
            "id": "uji-1", "modul": "matplotlib_review", "tanggal": D(2026, 10, 22),
            "jenis": "validasi", "skor_persen": 90, "mode_ai": "assisted",
            "level_soal": "L1, L2, L3", "bukti": ["notebooks/matplotlib_review.ipynb"],
            "pemahaman": "Memilih Axes agar subplot konsisten; log scale untuk data skewed",
            "keputusan": "validated",
        }
        e.update(kw)
        e = lengkapi(e, kw)
        p = (dir or self.tmp) / f"{e['id']}.yaml"
        p.write_text(yaml.safe_dump(e, allow_unicode=True, sort_keys=False), encoding="utf-8")
        return p

    def apply(self, today=None, **kw):
        return P.apply_entry(self.repo, self.entry(**kw), today or self.today)

    def item(self, item_id):
        data, _ = self.repo.load()
        return P.find(data, item_id)[1]["item"]


class TestState(Base):
    def test_state_fixture_konsisten(self):
        errors, _ = P.check(self.repo)
        self.assertEqual(errors, [])

    def test_state_hidup_konsisten(self):
        """state/state.yaml yang sebenarnya harus konsisten (inilah yang dijaga di GitHub)."""
        errors, _ = P.check(P.Repo(ROOT))
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
        with contextlib.redirect_stdout(io.StringIO()):
            rc = P.main(["--root", str(self.tmp), "--today", "2026-10-22", "dashboard", "--tulis"])
        self.assertEqual(rc, 0)
        self.assertTrue((self.tmp / "state" / "dashboard.md").exists())
        errors, warnings = P.check(self.repo)
        self.assertEqual(errors, [])
        self.assertFalse(any("tidak sinkron" in w for w in warnings))


class TestKeamananEntri(Base):
    """Entri bisa datang dari pihak otomatis (mis. ChatGPT Work), jadi diperiksa ketat."""

    def test_bukti_harus_ada_di_repo(self):
        with self.assertRaisesRegex(P.StateError, "bukti tidak ditemukan"):
            self.apply(bukti=["notebooks/tidak_ada.ipynb"])

    def test_bukti_url_diterima(self):
        self.apply(bukti=["https://github.com/xenoo-droid/learn-ai-workflow/blob/main/x.ipynb"])
        self.assertEqual(self.item("matplotlib_review")["status"], "validated")

    def test_bukti_di_luar_repo_ditolak(self):
        for b in ("../rahasia.txt", "/etc/passwd", "C:/Windows/win.ini"):
            with self.assertRaises(P.StateError, msg=b):
                self.apply(bukti=[b])

    def test_bukti_boleh_garis_miring_windows(self):
        self.apply(bukti=["notebooks\\matplotlib_review.ipynb"])
        self.assertEqual(self.item("matplotlib_review")["status"], "validated")

    def test_id_berbahaya_ditolak(self):
        for bad in ("../../x", "a.b", "a/b", "ab", "x" * 81, ""):
            p = self.entry(id="aman-1")
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
            data["id"] = bad
            p.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
            with self.assertRaises(P.StateError, msg=repr(bad)):
                P.apply_entry(self.repo, p, self.today)
        self.assertEqual(list((self.tmp / "state" / "evidence").glob("*")),
                         [self.tmp / "state" / "evidence" / "matplotlib-savefig.yaml"])

    def test_id_ganda_ditolak(self):
        self.apply(id="sekali-saja")
        with self.assertRaisesRegex(P.StateError, "sudah pernah dipakai"):
            self.apply(id="sekali-saja", modul="numpy")

    def test_entri_bukan_pemetaan_ditolak(self):
        p = self.tmp / "daftar.yaml"
        p.write_text("- a\n- b\n", encoding="utf-8")
        with self.assertRaises(P.StateError):
            P.apply_entry(self.repo, p, self.today)

    def test_yaml_rusak_ditolak(self):
        p = self.tmp / "rusak.yaml"
        p.write_text("id: [belum ditutup\n  modul: x: y", encoding="utf-8")
        with self.assertRaises(P.StateError):
            P.apply_entry(self.repo, p, self.today)

    def test_entri_terlalu_besar_ditolak(self):
        p = self.tmp / "besar.yaml"
        p.write_text("x: " + "a" * (P.BATAS_ENTRI_BYTE + 10), encoding="utf-8")
        with self.assertRaisesRegex(P.StateError, "ukuran"):
            P.apply_entry(self.repo, p, self.today)


class TestInbox(Base):
    def setUp(self):
        super().setUp()
        self.inbox = self.tmp / "state" / "inbox"
        self.inbox.mkdir()
        (self.inbox / "README.md").write_text("abaikan", encoding="utf-8")

    def jalan(self, *extra):
        with contextlib.redirect_stdout(io.StringIO()):
            return P.main(["--root", str(self.tmp), "--today", "2026-10-22", "inbox", *extra])

    def test_inbox_kosong_aman(self):
        self.assertEqual(self.jalan(), 0)
        self.assertEqual(self.item("matplotlib_review")["status"], "aktif")

    def test_tanpa_folder_inbox_aman(self):
        shutil.rmtree(self.inbox)
        self.assertEqual(self.jalan(), 0)

    def test_entri_valid_diterapkan_dan_inbox_dikosongkan(self):
        self.entry(dir=self.inbox)
        self.assertEqual(self.jalan(), 0)
        self.assertEqual(self.item("matplotlib_review")["status"], "validated")
        self.assertEqual(self.item("seaborn")["status"], "aktif")
        self.assertFalse((self.inbox / "uji-1.yaml").exists())
        self.assertTrue((self.tmp / "state" / "evidence" / "uji-1.yaml").exists())
        self.assertTrue((self.inbox / "README.md").exists())  # README tidak disentuh
        errors, warnings = P.check(self.repo)
        self.assertEqual(errors, [])
        self.assertFalse(any("tidak sinkron" in w for w in warnings))

    def test_entri_ditolak_dipindah_dengan_alasan(self):
        self.entry(dir=self.inbox, skor_persen=70, keputusan="validated")  # keputusan tak cocok
        self.assertEqual(self.jalan(), 1)
        self.assertEqual(self.item("matplotlib_review")["status"], "aktif")
        self.assertFalse((self.inbox / "uji-1.yaml").exists())
        self.assertTrue((self.inbox / "ditolak" / "uji-1.yaml").exists())
        alasan = (self.inbox / "ditolak" / "uji-1.yaml.alasan.txt").read_text(encoding="utf-8")
        self.assertIn("hasil perhitungan", alasan)
        self.assertFalse((self.tmp / "state" / "evidence" / "uji-1.yaml").exists())

    def test_satu_ditolak_tidak_menghentikan_yang_lain(self):
        self.entry(dir=self.inbox, id="a-rusak", skor_persen=10, keputusan="validated")
        self.entry(dir=self.inbox, id="b-bagus")
        self.assertEqual(self.jalan(), 1)
        self.assertEqual(self.item("matplotlib_review")["status"], "validated")
        self.assertTrue((self.inbox / "ditolak" / "a-rusak.yaml").exists())

    def test_urutan_nama_berkas_dihormati(self):
        self.entry(dir=self.inbox, id="b-seaborn", modul="seaborn")  # butuh review lulus lebih dulu
        self.entry(dir=self.inbox, id="a-review")
        self.assertEqual(self.jalan(), 0)
        self.assertEqual(self.item("matplotlib_review")["status"], "validated")
        self.assertEqual(self.item("seaborn")["status"], "validated")

    def test_entri_dengan_nama_berkas_sama_ditolak_ganda(self):
        self.entry(dir=self.inbox, skor_persen=10, keputusan="validated")
        self.assertEqual(self.jalan(), 1)
        self.entry(dir=self.inbox, skor_persen=10, keputusan="validated")
        self.assertEqual(self.jalan(), 1)
        self.assertTrue((self.inbox / "ditolak" / "uji-1-2.yaml").exists())

    def test_dry_run_tidak_mengubah_apa_pun(self):
        self.entry(dir=self.inbox)
        before = (self.tmp / "state" / "state.yaml").read_text(encoding="utf-8")
        self.assertEqual(self.jalan("--dry"), 0)
        self.assertEqual(before, (self.tmp / "state" / "state.yaml").read_text(encoding="utf-8"))
        self.assertTrue((self.inbox / "uji-1.yaml").exists())
        self.assertFalse((self.tmp / "state" / "evidence" / "uji-1.yaml").exists())


class TestModulBerquest(Base):
    def test_entri_untuk_modul_induk_ditolak(self):
        with self.assertRaises(P.StateError) as cm:
            self.apply(modul="matplotlib")
        self.assertIn("id quest yang benar-benar diuji", str(cm.exception))
        self.assertIn("matplotlib_review", str(cm.exception))

    def test_dashboard_dengan_modul_berquest_setelah_quest_aktif(self):
        data, _ = self.repo.load()
        w2 = next(w for w in data["worlds"] if w["id"] == 2)
        k = next(i for i, m in enumerate(w2["modul"]) if m["id"] == "jupyter_colab")
        w2["modul"][k] = {"id": "jupyter_colab", "nama": "Jupyter / Google Colab",
                          "quest": [{"id": "jq1", "nama": "Q1", "status": "belum"}]}
        teks = P.render_dashboard(data)
        self.assertIn("Jupyter / Google Colab", teks)

    def test_state_hidup_memakai_quest_untuk_seaborn(self):
        data, _ = P.Repo(ROOT).load()
        _, rec = P.find(data, "seaborn")
        self.assertIsNone(rec, "seaborn harus berupa modul dengan quest, bukan satu item")


class TestKurikulum(unittest.TestCase):
    """Setiap quest di state.yaml harus punya rincian di system/09_kurikulum.md, dan sebaliknya."""

    def test_id_state_dan_kurikulum_sama(self):
        import re
        data, _ = P.Repo(ROOT).load()
        state_ids = [r["item"]["id"] for r in P.leaves(data)]
        teks = (ROOT / "system" / "09_kurikulum.md").read_text(encoding="utf-8")
        kur_ids = re.findall(r"^#### `([a-z0-9_]+)`", teks, re.M)
        self.assertEqual(len(kur_ids), len(set(kur_ids)), "id ganda di kurikulum")
        self.assertEqual(sorted(set(state_ids) - set(kur_ids)), [], "quest di state tanpa rincian kurikulum")
        self.assertEqual(sorted(set(kur_ids) - set(state_ids)), [], "id di kurikulum yang tidak ada di state")


if __name__ == "__main__":
    unittest.main()
