"""
LEVEL 6 — Eksperimen Tingkat Kesulitan (Difficulty) (LATIHAN)
===================================================================

Tujuan belajar:
  * Setiap tambahan 1 angka nol heksadesimal membuat mining ~16x lebih sulit.
  * Mengukur rata-rata percobaan dan waktu secara empiris.
  * Konsep penyesuaian difficulty (difficulty adjustment) agar waktu blok stabil.

Jalankan tes:      python cek_nilai.py 6
Jalankan eksperimen: python latihan/level06_difficulty.py
(jika matplotlib terpasang, grafik disimpan sebagai grafik_difficulty.png)
"""

import hashlib
import time


def tambang(data: str, difficulty: int):
    """Cari nonce terkecil (mulai 0) sehingga SHA-256(f"{data}{nonce}") diawali
    `difficulty` angka nol. Kembalikan tuple (nonce, hash_hex, jumlah_percobaan).
    """
    target = "0" * difficulty
    nonce = 0
    while True:
        teks = f"{data}{nonce}".encode()
        h = hashlib.sha256(teks).hexdigest()
        if h.startswith(target):
            return nonce, h, nonce + 1
        nonce += 1


def ekspektasi_percobaan(difficulty: int) -> int:
    """Rata-rata teoretis jumlah percobaan = 16 ** difficulty. Jelaskan alasannya di refleksi."""
    return 16 ** difficulty


def ukur_mining(difficulty: int, n: int = 5) -> dict:
    """Tambang `n` kali dengan data berbeda (mis. f"blok-{i}") lalu kembalikan dict:
    {'difficulty': d, 'rata_percobaan': float, 'rata_detik': float}
    """
    total_percobaan = 0
    t0 = time.perf_counter()
    for i in range(n):
        data = f"blok-{i}"
        _, _, percobaan = tambang(data, difficulty)
        total_percobaan += percobaan
    durasi = time.perf_counter() - t0
    return {
        "difficulty": difficulty,
        "rata_percobaan": total_percobaan / n,
        "rata_detik": durasi / n,
    }


def sesuaikan_difficulty(sekarang: int, waktu_aktual: float, waktu_target: float) -> int:
    """Aturan sederhana penyesuaian difficulty:
      * waktu_aktual < waktu_target / 2  -> naik 1
      * waktu_aktual > waktu_target * 2  -> turun 1 (minimal 1)
      * selain itu                        -> tetap
    """
    if waktu_aktual < waktu_target / 2:
        return sekarang + 1
    elif waktu_aktual > waktu_target * 2:
        return max(1, sekarang - 1)
    else:
        return sekarang


def eksperimen(daftar_difficulty=(1, 2, 3, 4), n: int = 5) -> list:
    """Kembalikan list hasil ukur_mining() untuk setiap difficulty di daftar."""
    return [ukur_mining(d, n) for d in daftar_difficulty]


if __name__ == "__main__":
    hasil = eksperimen((1, 2, 3, 4, 5), n=5)
    print(f"{'Diff':>4} | {'Rata percobaan':>15} | {'Teori 16^d':>11} | {'Rata detik':>10}")
    print("-" * 52)
    for h in hasil:
        print(f"{h['difficulty']:>4} | {h['rata_percobaan']:>15.0f} | "
              f"{ekspektasi_percobaan(h['difficulty']):>11} | {h['rata_detik']:>10.4f}")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        xs = [h["difficulty"] for h in hasil]
        plt.semilogy(xs, [h["rata_detik"] for h in hasil], "o-")
        plt.xlabel("Difficulty (jumlah angka nol)")
        plt.ylabel("Rata-rata waktu mining (detik, skala log)")
        plt.title("Pengaruh difficulty terhadap waktu mining")
        plt.grid(True, which="both", alpha=0.3)
        plt.savefig("grafik_difficulty.png", dpi=120, bbox_inches="tight")
        print("Grafik disimpan: grafik_difficulty.png")
    except ImportError:
        print("(matplotlib belum terpasang — lewati grafik)")
