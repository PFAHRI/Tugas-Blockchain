"""
Skrip pengecek otomatis latihan Blockchain.

Pemakaian:
    python cek_nilai.py           # cek semua level
    python cek_nilai.py 3         # cek level 3 saja (tampilkan detail kegagalan)
    python cek_nilai.py 1 2 5     # cek beberapa level
    python cek_nilai.py --kunci   # (dosen) jalankan tes terhadap folder kunci_jawaban/
"""

import contextlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.join(ROOT, "tests")

JUDUL = {
    1: "Fungsi hash SHA-256",
    2: "Blockchain dasar (GfG)",
    3: "Eksperimen tampering",
    4: "Transaksi dalam blok",
    5: "PoW dengan nonce",
    6: "Eksperimen difficulty",
    7: "Tanda tangan digital",
    8: "Jaringan & konsensus",
    9: "Reward & saldo",
}


class Pencatat:
    """Plugin pytest kecil untuk menghitung tes lulus/gagal."""

    def __init__(self):
        self.lulus = 0
        self.total = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
            self.total += 1
            if report.passed:
                self.lulus += 1

    def pytest_collectreport(self, report):
        if report.failed:  # error saat import modul (mis. SyntaxError)
            self.total += 1


def file_tes(level):
    for nama in sorted(os.listdir(TESTS)):
        if nama.startswith(f"test_level{level:02d}_"):
            return os.path.join(TESTS, nama)
    return None


def main():
    import pytest

    argumen = sys.argv[1:]
    if "--kunci" in argumen:
        os.environ["BC_KUNCI"] = "1"
        argumen.remove("--kunci")
    levels = [int(a) for a in argumen] if argumen else list(JUDUL)
    detail = len(levels) == 1

    folder = "kunci_jawaban" if os.environ.get("BC_KUNCI") == "1" else "latihan"
    print(f"\nMemeriksa kode di folder: {folder}/\n")

    hasil = []
    for lv in levels:
        path = file_tes(lv)
        if path is None:
            print(f"Level {lv} tidak ditemukan.")
            continue
        p = Pencatat()
        opsi = ["-q", "-p", "no:cacheprovider", "--rootdir", ROOT]
        mulai = time.time()
        if detail:
            pytest.main(opsi + ["--tb=short", path], plugins=[p])
        else:
            with contextlib.redirect_stdout(io.StringIO()):
                pytest.main(opsi + ["--tb=no", "--no-header", path], plugins=[p])
        hasil.append((lv, p.lulus, p.total, time.time() - mulai))

    print("\n" + "=" * 62)
    print(f"{'Level':<6}{'Materi':<28}{'Lulus':>10}{'Status':>12}")
    print("-" * 62)
    total_l = total_t = 0
    for lv, l, t, _ in hasil:
        if t == 0:
            status = "ERROR"
        else:
            status = "SELESAI" if l == t else ("belum" if l == 0 else "sebagian")
        print(f"{lv:<6}{JUDUL[lv]:<28}{f'{l}/{t}':>10}{status:>12}")
        total_l += l
        total_t += t
    print("-" * 62)
    # Nilai = rata-rata persentase kelulusan tiap level (setiap level berbobot sama)
    nilai = sum(100 * l / t for _, l, t, _ in hasil if t) / len(hasil) if hasil else 0
    print(f"{'TOTAL':<34}{f'{total_l}/{total_t}':>10}{f'{nilai:.0f}%':>12}")
    print("=" * 62)
    if not detail:
        print("Tip: jalankan `python cek_nilai.py <nomor_level>` untuk melihat detail kegagalan.\n")


if __name__ == "__main__":
    main()
