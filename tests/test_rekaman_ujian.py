"""Tes untuk aturan rekaman ujian di tools/progress.py: cakupan, soal/challenge, konsep lemah, statistik.
Jalankan dari akar repo:
    python -m unittest discover -s tests -v
"""
import contextlib
import io
import unittest

from test_progress import Base, P, D  # Base tidak punya tes sendiri, jadi tidak dijalankan dua kali


def soal(*skor_level):
    return [{"level": lv, "pertanyaan": f"Soal {i}", "skor": s} for i, (s, lv) in enumerate(skor_level, 1)]


class TestParseKurikulum(unittest.TestCase):
    TEKS = (
        "# World\n\n"
        "#### `a` — A\n"
        "- **Wajib:** `histplot` (`bins`, `hue`), `set_xlim`/`set_ylim`, format (`png`, `pdf`), Colab: upload file\n"
        "- **Fokus ujian:** x, y\n"
        "#### `b` — B\n"
        "- **Wajib:**\n"
        "  - Membuat array: `np.array`, `arange`\n"
        "  - Broadcasting, vectorization\n"
        "- **Fokus retrieval:** z\n"
        "## Bagian lain\n"
        "- **Wajib:** bukan milik quest mana pun\n"
    )

    def test_koma_di_dalam_kurung_tidak_memecah(self):
        k = P.parse_kurikulum(self.TEKS)
        self.assertEqual(k["a"]["kunci"], ["histplot", "set_xlim/set_ylim", "format", "colab: upload file"])

    def test_daftar_bertingkat_satu_butir_satu_item(self):
        k = P.parse_kurikulum(self.TEKS)
        self.assertEqual(k["b"]["kunci"], ["membuat array", "broadcasting, vectorization"])
        self.assertEqual(set(k), {"a", "b"})

    def test_norm_item_menerima_salinan_mentah(self):
        self.assertEqual(P.norm_item("`barplot` (`estimator`, `errorbar`)"), "barplot")
        self.assertEqual(P.norm_item("  Barplot  "), "barplot")


class TestCakupan(Base):
    def test_validasi_tanpa_cakupan_ditolak(self):
        with self.assertRaisesRegex(P.StateError, "cakupan wajib diisi"):
            self.apply(cakupan=[])

    def test_review_butuh_minimal_n_quest(self):
        with self.assertRaisesRegex(P.StateError, "minimal 2 id quest"):
            self.apply(cakupan=["subplots"])

    def test_review_item_asing_hanya_peringatan(self):
        msgs, _ = self.apply(cakupan=["subplots", "errorbar", "pie chart"])
        self.assertTrue(any("tidak dikenal" in m and "pie chart" in m for m in msgs))
        self.assertEqual(self.item("matplotlib_review")["status"], "validated")

    def test_materi_harus_mencakup_semua_wajib(self):
        self.apply()  # review lulus, seaborn menjadi quest aktif
        with self.assertRaises(P.StateError) as cm:
            self.apply(id="sb-1", modul="seaborn", cakupan=["histplot", "kdeplot"])
        self.assertIn("Yang belum: `boxplot`", str(cm.exception))
        self.assertEqual(self.item("seaborn")["status"], "aktif")

    def test_materi_menerima_item_disalin_dari_kurikulum(self):
        self.apply()
        self.apply(id="sb-1", modul="seaborn",
                   cakupan=["`histplot` (`bins`, `hue`)", "`kdeplot`", "Boxplot"])
        self.assertEqual(self.item("seaborn")["status"], "validated")

    def test_legacy_dengan_bukti_lama_tidak_wajib_rekaman(self):
        self.apply(modul="numpy", id="np-lama", cakupan=None, ujian=None)
        self.assertEqual(self.item("numpy")["status"], "validated")

    def test_retrieval_cukup_sebagian_wajib(self):
        self.apply(modul="numpy", id="np-r", jenis="retrieval", mode_ai="independent",
                   keputusan="retained", cakupan=["Agregasi dengan `axis`: `sum`, `mean`"])
        self.assertEqual(self.item("numpy")["status"], "retained")

    def test_retrieval_tanpa_item_wajib_ditolak(self):
        with self.assertRaisesRegex(P.StateError, "minimal satu item Wajib"):
            self.apply(modul="numpy", id="np-r", jenis="retrieval", mode_ai="independent",
                       keputusan="retained", cakupan=["pandas groupby"])

    def test_quest_tanpa_kurikulum_ditolak(self):
        (self.tmp / "system" / "09_kurikulum.md").write_text("# kosong\n", encoding="utf-8")
        with self.assertRaisesRegex(P.StateError, "belum punya daftar Wajib"):
            self.apply()


class TestUjian(Base):
    def ujian(self, s, ch=None):
        u = {"soal": s}
        if ch is not None:
            u["challenge"] = ch
        return u

    def test_ujian_wajib_ada(self):
        with self.assertRaisesRegex(P.StateError, "kolom ujian wajib diisi"):
            self.apply(ujian=None)

    def test_skor_dihitung_ulang(self):
        u = self.ujian(soal((100, "L1"), (80, "L2"), (60, "L1")), {"level": "L3", "deskripsi": "c", "skor": 90})
        self.apply(ujian=u, skor_persen=85)  # 0.5*80 + 0.5*90
        self.assertEqual(self.item("matplotlib_review")["status"], "validated")

    def test_skor_tidak_cocok_ditolak(self):
        u = self.ujian(soal((100, "L1"), (80, "L2"), (60, "L1")), {"level": "L3", "deskripsi": "c", "skor": 50})
        with self.assertRaisesRegex(P.StateError, "tidak sama dengan hitungan"):
            self.apply(ujian=u, skor_persen=90)  # hitungan sebenarnya 65

    def test_jumlah_soal_review_harus_tiga(self):
        u = self.ujian(soal((90, "L2"), (90, "L1")), {"level": "L3", "deskripsi": "c", "skor": 90})
        with self.assertRaisesRegex(P.StateError, "jumlah soal 2"):
            self.apply(ujian=u)

    def test_challenge_review_wajib_l3(self):
        u = self.ujian(soal((90, "L2"), (90, "L1"), (90, "L1")), {"level": "L2", "deskripsi": "c", "skor": 90})
        with self.assertRaisesRegex(P.StateError, "wajib level L3"):
            self.apply(ujian=u)

    def test_minimal_satu_soal_l2(self):
        self.apply()
        u = self.ujian(soal((90, "L1"), (90, "L1"), (90, "L1")), {"level": "L1", "deskripsi": "c", "skor": 90})
        with self.assertRaisesRegex(P.StateError, "minimal satu soal level L2"):
            self.apply(id="sb-1", modul="seaborn", ujian=u)

    def test_challenge_wajib_untuk_validasi(self):
        with self.assertRaisesRegex(P.StateError, "challenge wajib diisi"):
            self.apply(ujian=self.ujian(soal((90, "L2"), (90, "L1"), (90, "L1"))))

    def test_retrieval_tanpa_challenge(self):
        u = self.ujian(soal((90, "L2"), (90, "L1")), {"level": "L2", "deskripsi": "c", "skor": 90})
        with self.assertRaisesRegex(P.StateError, "tanpa challenge"):
            self.apply(modul="numpy", jenis="retrieval", mode_ai="independent", keputusan="retained", ujian=u)

    def test_soal_tanpa_pertanyaan_ditolak(self):
        u = self.ujian([{"level": "L2", "skor": 90}] + soal((90, "L1"), (90, "L1")),
                       {"level": "L3", "deskripsi": "c", "skor": 90})
        with self.assertRaisesRegex(P.StateError, "pertanyaan wajib diisi"):
            self.apply(ujian=u)

    def test_tersimpan_di_evidence(self):
        self.apply()
        isi = (self.tmp / "state" / "evidence" / "uji-1.yaml").read_text(encoding="utf-8")
        self.assertIn("pertanyaan: Soal 1", isi)
        self.assertIn("cakupan:", isi)


class TestKonsepLemah(Base):
    def test_kesalahan_dicatat_walau_gagal(self):
        self.apply(skor_persen=60, keputusan="tetap", kesalahan=["errorbar: tertukar yerr dan xerr"])
        it = self.item("matplotlib_review")
        self.assertEqual(it["status"], "aktif")
        self.assertEqual(it["konsep_lemah"], ["errorbar: tertukar yerr dan xerr"])
        errors, _ = P.check(self.repo)
        self.assertEqual(errors, [])

    def test_kesalahan_konsep_sama_ditimpa_dan_teratasi_dihapus(self):
        self.apply(skor_persen=60, keputusan="tetap", kesalahan=["errorbar: lama", "subplots: sharex"])
        self.apply(id="uji-2", skor_persen=60, keputusan="tetap", kesalahan=["Errorbar: baru"])
        self.assertEqual(self.item("matplotlib_review")["konsep_lemah"], ["subplots: sharex", "Errorbar: baru"])
        self.apply(id="uji-3", teratasi=["errorbar", "subplots"])
        self.assertNotIn("konsep_lemah", self.item("matplotlib_review"))

    def test_konsep_lemah_bukan_daftar_ditolak_check(self):
        data, _ = self.repo.load()
        P.find(data, "numpy")[1]["item"]["konsep_lemah"] = "axis"
        errors, _ = P.check(self.repo, data)
        self.assertTrue(any("konsep_lemah" in e for e in errors))


class TestStatistikDanCli(Base):
    def jalan(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = P.main(["--root", str(self.tmp), "--today", "2026-10-22", *args])
        return kode, out.getvalue()

    def test_statistik(self):
        self.apply(skor_persen=70, keputusan="tetap", kesalahan=["errorbar: yerr"])
        self.apply(id="uji-2")
        kode, out = self.jalan("statistik")
        self.assertEqual(kode, 0)
        self.assertIn("Tren skor", out)
        self.assertIn("2 percobaan (skor: 70, 90)", out)
        self.assertIn("Matplotlib Review: errorbar: yerr", out)

    def test_statistik_tanpa_evidence_berskor(self):
        kode, out = self.jalan("statistik")
        self.assertEqual(kode, 0)
        self.assertIn("(belum ada)", out)

    def test_cli_cakupan(self):
        kode, out = self.jalan("cakupan", "numpy")
        self.assertEqual(kode, 0)
        self.assertIn('- "membuat array"', out)
        kode, out = self.jalan("cakupan", "matplotlib_review")
        self.assertIn("modul review", out)
        self.assertIn("- errorbar", out)


if __name__ == "__main__":
    unittest.main()
