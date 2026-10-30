"""Bantuan bersama untuk tes: Evidence Entry contoh yang lengkap (cakupan + rekaman ujian).

Cakupan mengikuti tests/fixtures/system/09_kurikulum.md, dan skor tiap soal disamakan dengan
skor_persen supaya hitungan ulang di progress.py cocok.
"""

CAKUPAN = {
    "matplotlib_review": ["subplots", "errorbar"],
    "numpy": ["Membuat array", "Broadcasting, vectorization, ufunc", "Agregasi dengan axis"],
    "seaborn": ["histplot", "kdeplot", "boxplot"],
}


def rekaman_ujian(jenis, modul, skor):
    if not isinstance(skor, (int, float)):
        return None
    if jenis == "validasi":
        return {
            "soal": [
                {"level": "L1", "pertanyaan": "Soal 1", "skor": skor},
                {"level": "L2", "pertanyaan": "Soal 2", "skor": skor},
                {"level": "L1", "pertanyaan": "Soal 3", "skor": skor},
            ],
            "challenge": {"level": "L3" if modul == "matplotlib_review" else "L2",
                          "deskripsi": "Challenge dataset baru", "skor": skor},
        }
    if jenis == "retrieval":
        return {"soal": [
            {"level": "L2", "pertanyaan": "Retrieval 1", "skor": skor},
            {"level": "L1", "pertanyaan": "Retrieval 2", "skor": skor},
        ]}
    return None


def lengkapi(e: dict, kw: dict) -> dict:
    """Isi cakupan dan ujian otomatis kecuali tes menentukannya sendiri."""
    if "cakupan" not in kw and e.get("modul") in CAKUPAN:
        e["cakupan"] = CAKUPAN[e["modul"]]
    if "ujian" not in kw:
        u = rekaman_ujian(e.get("jenis"), e.get("modul"), e.get("skor_persen"))
        if u is not None:
            e["ujian"] = u
    return {k: v for k, v in e.items() if v is not None or k in kw}
