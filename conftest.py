"""Konfigurasi pytest.

Secara default tes dijalankan terhadap folder `latihan/` (pekerjaan mahasiswa).
Jika variabel lingkungan BC_KUNCI=1, tes dijalankan terhadap `kunci_jawaban/`
(dipakai dosen untuk memastikan kunci jawaban lulus semua tes).
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FOLDER = "kunci_jawaban" if os.environ.get("BC_KUNCI") == "1" else "latihan"
sys.path.insert(0, os.path.join(ROOT, FOLDER))


def pytest_report_header(config):
    return f"Menguji kode di folder: {FOLDER}/"
