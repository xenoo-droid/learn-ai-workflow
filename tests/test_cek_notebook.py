"""Tes untuk tools/cek_notebook.py. Menjalankan kernel sungguhan, jadi dilewati bila
nbclient/ipykernel belum terpasang (pip install -r requirements-notebook.txt).
"""
import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
spec = importlib.util.spec_from_file_location("cek_notebook", ROOT / "tools" / "cek_notebook.py")
CN = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CN)


def tulis_notebook(path: Path, sel: list):
    import nbformat
    nb = nbformat.v4.new_notebook()
    for kode, tags in sel:
        c = nbformat.v4.new_code_cell(kode)
        if tags:
            c.metadata["tags"] = tags
        nb.cells.append(c)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, str(path))


class TestKumpulkan(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        ev = self.tmp / "state" / "evidence"
        ev.mkdir(parents=True)
        (ev / "baru.yaml").write_text(yaml.safe_dump({"id": "baru", "ujian": {"soal": []}, "bukti": [
            "notebooks/a.ipynb", "notebooks/gambar.png", "https://x/y.ipynb", "../luar.ipynb"]}), encoding="utf-8")
        (ev / "lama.yaml").write_text(yaml.safe_dump({"id": "lama", "bukti": ["notebooks/b.ipynb"]}), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_default_hanya_entri_format_baru(self):
        self.assertEqual([p.as_posix() for p, _ in CN.kumpulkan(self.tmp, False)], ["notebooks/a.ipynb"])

    def test_semua_termasuk_format_lama(self):
        self.assertEqual(sorted(p.as_posix() for p, _ in CN.kumpulkan(self.tmp, True)),
                         ["notebooks/a.ipynb", "notebooks/b.ipynb"])


@unittest.skipUnless(CN.siap(), "nbclient/ipykernel belum terpasang")
class TestJalankan(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_notebook_bersih_lolos_dan_membaca_data_di_sampingnya(self):
        (self.tmp / "nb").mkdir()
        (self.tmp / "nb" / "data.csv").write_text("a\n1\n", encoding="utf-8")
        tulis_notebook(self.tmp / "nb" / "x.ipynb", [("print(open('data.csv').read())", None)])
        sebelum = (self.tmp / "nb" / "x.ipynb").read_bytes()
        lolos, pesan = CN.jalankan(self.tmp, Path("nb/x.ipynb"), batas=120)
        self.assertTrue(lolos, pesan)
        self.assertEqual((self.tmp / "nb" / "x.ipynb").read_bytes(), sebelum, "notebook asli tidak boleh berubah")

    def test_error_terdeteksi(self):
        tulis_notebook(self.tmp / "y.ipynb", [("open('tidak_ada.csv')", None)])
        lolos, pesan = CN.jalankan(self.tmp, Path("y.ipynb"), batas=120)
        self.assertFalse(lolos)
        self.assertIn("FileNotFoundError", pesan)

    def test_tag_raises_exception_dihormati(self):
        tulis_notebook(self.tmp / "z.ipynb", [("1/0", ["raises-exception"]), ("print('lanjut')", None)])
        lolos, pesan = CN.jalankan(self.tmp, Path("z.ipynb"), batas=120)
        self.assertTrue(lolos, pesan)


if __name__ == "__main__":
    unittest.main()
