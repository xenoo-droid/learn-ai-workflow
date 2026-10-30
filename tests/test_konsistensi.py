"""Tes konsistensi antar dokumen: kurikulum, paket ChatGPT Project, tautan, portofolio, dan bank dataset.
Jalankan dari akar repo:
    python -m unittest discover -s tests -v
"""
import importlib.util
import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def muat(nama):
    spec = importlib.util.spec_from_file_location(nama, ROOT / "tools" / f"{nama}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P = muat("progress")
BP = muat("bangun_paket")

# Dokumen yang dijaga (arsip dan paket turunan tidak ikut)
DOKUMEN = sorted(
    [ROOT / "README.md"]
    + list((ROOT / "system").glob("*.md"))
    + list((ROOT / "docs").glob("*.md"))
    + [p for p in ROOT.glob("*/README.md") if p.parent.name not in ("archive", "paket_project")]
    + [p for p in ROOT.glob("*/*/README.md") if p.parts[-3] not in ("archive", "paket_project")]
)
PAGAR = re.compile(r"^```.*?^```", re.S | re.M)
TAUTAN = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
PATH_INLINE = re.compile(r"`((?:system|docs|state|tools|tests|notebooks|assets|projects|src|\.github)/[^`<>*\s]+)`")
# path yang baru muncul saat sistem berjalan, jadi wajar belum ada di repo
DIBUAT_SAAT_JALAN = {"state/inbox/ditolak", "paket_project"}


def tanpa_blok_kode(teks: str) -> str:
    return PAGAR.sub("", teks)


class TestKurikulumLengkap(unittest.TestCase):
    def test_setiap_quest_punya_daftar_wajib(self):
        kur = P.baca_kurikulum(P.Repo(ROOT))
        kosong = [q for q, v in kur.items() if not v["kunci"]]
        self.assertEqual(kosong, [], "quest tanpa item Wajib yang bisa dibaca script")

    def test_kunci_wajib_unik_per_quest(self):
        kur = P.baca_kurikulum(P.Repo(ROOT))
        for q, v in kur.items():
            ganda = {k for k in v["kunci"] if v["kunci"].count(k) > 1}
            self.assertFalse(ganda, f"{q}: item Wajib ganda {ganda}")

    def test_modul_review_menyebut_jumlah_minimal(self):
        data, _ = P.Repo(ROOT).load()
        kur = P.baca_kurikulum(P.Repo(ROOT))
        for r in P.leaves(data):
            if P.tipe_of(r["item"]) == "review":
                self.assertRegex(" ".join(kur[r["item"]["id"]]["wajib"]), r"≥\s*\d+", r["item"]["id"])


class TestPaketProject(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def bangun(self):
        keluar = self.tmp / "paket"
        self.assertEqual(BP.main(["--root", str(ROOT), "--keluar", str(keluar)]), 0)
        return keluar

    def test_paket_memuat_semua_sumber(self):
        keluar = self.bangun()
        for asal, nama in BP.SALIN:
            self.assertEqual((keluar / nama).read_bytes(), (ROOT / asal).read_bytes(), nama)
        gabung = (keluar / "aturan_mentor.md").read_text(encoding="utf-8")
        for _, asal in BP.GABUNG:
            isi = BP.FRONT.sub("", BP.baca(ROOT / asal), count=1).strip()
            self.assertIn(isi, gabung, asal)
        self.assertLessEqual(len(list(keluar.iterdir())), 5, "ChatGPT Project Free dibatasi 5 file")

    def test_paket_lokal_tidak_basi(self):
        lokal = ROOT / "paket_project"
        if not lokal.is_dir():
            self.skipTest("paket_project/ belum dibangun (folder ini diabaikan git)")
        baru = self.bangun()
        for f in baru.iterdir():
            self.assertTrue((lokal / f.name).is_file(), f"{f.name} belum ada di paket_project/")
            self.assertEqual((lokal / f.name).read_bytes(), f.read_bytes(),
                             f"paket_project/{f.name} basi; jalankan: python tools/bangun_paket.py")


class TestTautan(unittest.TestCase):
    def test_tautan_markdown_relatif_ada(self):
        rusak = []
        for doc in DOKUMEN:
            for t in TAUTAN.findall(tanpa_blok_kode(doc.read_text(encoding="utf-8"))):
                if t.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                tujuan = (doc.parent / t.split("#", 1)[0]).resolve()
                if not tujuan.exists():
                    rusak.append(f"{doc.relative_to(ROOT)} → {t}")
        self.assertEqual(rusak, [])

    def test_path_repo_yang_disebut_ada(self):
        hilang = []
        for doc in DOKUMEN:
            if doc.name == "changelog.md":  # catatan sejarah boleh menyebut file lama dan singkatan
                continue
            for t in PATH_INLINE.findall(tanpa_blok_kode(doc.read_text(encoding="utf-8"))):
                t = t.rstrip("/.,:;)")
                if t in DIBUAT_SAAT_JALAN or any(t.startswith(x + "/") for x in DIBUAT_SAAT_JALAN):
                    continue
                if not (ROOT / t).exists():
                    hilang.append(f"{doc.relative_to(ROOT)} → {t}")
        self.assertEqual(hilang, [])


class TestPortfolio(unittest.TestCase):
    def test_setiap_portfolio_ada_di_world_yang_benar(self):
        teks = (ROOT / "docs" / "portfolio.md").read_text(encoding="utf-8")
        bagian = {int(m.group(1)): m.start() for m in re.finditer(r"^# 🌍 WORLD (\d+)", teks, re.M)}
        batas = sorted(bagian.values()) + [len(teks)]
        isi = {w: teks[pos:batas[batas.index(pos) + 1]] for w, pos in bagian.items()}
        data, _ = P.Repo(ROOT).load()
        for r in P.leaves(data):
            it = r["item"]
            if P.tipe_of(it) in ("portfolio", "capstone"):
                w = r["world"]["id"]
                self.assertIn(w, isi, f"portfolio.md tidak punya bagian WORLD {w}")
                self.assertIn(f"`{it['id']}`", isi[w], f"{it['id']} tidak ada di bagian WORLD {w} portfolio.md")


class TestBankDataset(unittest.TestCase):
    def test_setiap_file_tercatat_di_katalog(self):
        folder = ROOT / "assets" / "data"
        katalog = (folder / "README.md").read_text(encoding="utf-8")
        for f in folder.iterdir():
            if f.name in ("README.md", ".gitkeep"):
                continue
            self.assertIn(f"`{f.name}`", katalog, f"{f.name} belum dicatat di assets/data/README.md")
        for nama in re.findall(r"^\| `([^`]+\.(?:csv|db))` \|", katalog, re.M):
            self.assertTrue((folder / nama).is_file(), f"katalog menyebut {nama} tetapi filenya tidak ada")


if __name__ == "__main__":
    unittest.main()
