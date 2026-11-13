"""
Menjalankan Tugas Personal 2 (Level 6–9) dan membuat laporan.

Pemakaian (dari folder blockchain-latihan):
    python tugas_personal_2/jalankan_tugas_2.py              # periksa modifikasi + buat laporan
    python tugas_personal_2/jalankan_tugas_2.py --cek        # hanya periksa modifikasi
    python tugas_personal_2/jalankan_tugas_2.py --data file.py   # pakai file data lain

Laporan disimpan sebagai tugas_personal_2/laporan_tugas_personal_2_<NIM_4>.md
"""

import datetime
import hashlib
import importlib.util
import json
import os
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def atur_path(kunci: bool):
    if kunci:  # (dosen) kode level dan modifikasi dari kunci_jawaban/
        sys.path[:0] = [os.path.join(ROOT, "kunci_jawaban"), HERE]
    else:      # mahasiswa: modifikasi dari tugas_personal_2/, kode level dari latihan/
        sys.path[:0] = [HERE, os.path.join(ROOT, "latihan")]


def muat_data(path: str) -> dict:
    spec = importlib.util.spec_from_file_location("data_saya", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {"nama": mod.NAMA, "nim4": mod.NIM_4, "tanggal_lahir": mod.TANGGAL_LAHIR,
            "kota_asal": mod.KOTA_ASAL, "hobi": mod.HOBI}


# ------------------------------------------------------------------ pemeriksaan
def pemeriksaan() -> bool:
    """Periksa keempat modifikasi dengan data uji. Kembalikan True jika semua lolos."""
    from ecdsa import SECP256k1, SigningKey

    import level07_tanda_tangan as L7
    import level08_jaringan as L8
    import level09_reward_saldo as L9
    import modifikasi_2 as M

    def cek6():
        assert M.jejak_difficulty(4, [1, 5, 30, 8], 10) == [5, 5, 4, 4], \
            "jejak_difficulty(4, [1, 5, 30, 8], 10) seharusnya [5, 5, 4, 4]"
        assert M.jejak_difficulty(1, [99, 99], 10) == [1, 1], "difficulty tidak boleh di bawah 1"
        assert M.jejak_difficulty(3, [], 10) == [], "daftar waktu kosong harus menghasilkan []"

    def cek7():
        priv, pub = M.kunci_dari_data("UJI COBA", "0042", "2000-01-31")
        secret = int(hashlib.sha256(b"0042:UJI COBA:2000-01-31").hexdigest(), 16) % SECP256k1.order
        harapan = SigningKey.from_secret_exponent(secret, curve=SECP256k1).to_string().hex()
        assert priv == harapan, "kunci privat belum dibuat dari SHA-256(f\"{nim4}:{nama}:{tanggal_lahir}\")"
        assert len(pub) == 128, "kunci publik harus 128 karakter hex"
        assert (priv, pub) == M.kunci_dari_data("UJI COBA", "0042", "2000-01-31"), "kunci harus selalu sama"
        tx = {"sender": L7.alamat_dari_kunci_publik(pub), "recipient": "X", "amount": 3}
        s1 = M.tanda_tangani_deterministik(tx, priv)
        assert s1 == M.tanda_tangani_deterministik(tx, priv), "tanda tangan harus selalu sama (sign_deterministic)"
        assert L7.verifikasi(tx, s1, pub), "tanda tangan harus lolos L7.verifikasi"

    def cek8():
        a = M.NodePersonal("UJI-1", "0042")
        b = M.NodePersonal("UJI-2", "0042")
        assert isinstance(a, L8.Node), "NodePersonal harus turunan Node Level 8"
        a.hubungkan(b)
        blok = a.tambang_dan_siarkan(["x"])
        assert blok["transactions"] == ["UJI-1#0042", "x"], \
            f"transaksi blok {blok['transactions']}, seharusnya ['UJI-1#0042', 'x']"
        assert M.semua_sepakat([a, b]) is True, "dua node dengan rantai sama harus sepakat"
        b.tambang_blok(["y"])
        assert M.semua_sepakat([a, b]) is False, "rantai berbeda harus menghasilkan False"

    def cek9():
        bc = M.BlockchainHalving(40, 2, difficulty=1)
        assert isinstance(bc, L9.Blockchain), "BlockchainHalving harus turunan Blockchain Level 9"
        assert [bc.hadiah(i) for i in range(1, 6)] == [40, 40, 20, 20, 10], "rumus hadiah(index) belum tepat"
        for _ in range(5):
            bc.mine("UJI")
        assert [b["transactions"][0]["amount"] for b in bc.chain[1:]] == [40, 40, 20, 20, 10], \
            "mine() harus memakai hadiah(index) untuk coinbase"
        assert bc.total_suplai() == 130, "total suplai seharusnya 130"
        assert bc.validasi_ekonomi() is True, "validasi_ekonomi() harus menerima hadiah halving yang benar"
        bc.chain[3]["transactions"][0]["amount"] = 40
        assert bc.validasi_ekonomi() is False, "validasi_ekonomi() harus menolak hadiah yang tidak sesuai halving"

    semua_ok = True
    print("\nPemeriksaan modifikasi (memakai data uji, bukan data Anda):")
    for no, fungsi in zip((6, 7, 8, 9), (cek6, cek7, cek8, cek9)):
        try:
            fungsi()
            print(f"  [OK]    Modifikasi {no}")
        except NotImplementedError as e:
            semua_ok = False
            asal = os.path.basename(traceback.extract_tb(e.__traceback__)[-1].filename)
            if asal.startswith("level0"):
                print(f"  [BELUM] Modifikasi {no}: kode {asal} di latihan/ belum lengkap ({e})")
            else:
                print(f"  [BELUM] Modifikasi {no}: {e}")
        except AssertionError as e:
            semua_ok = False
            print(f"  [GAGAL] Modifikasi {no}: {e}")
        except Exception as e:
            semua_ok = False
            print(f"  [ERROR] Modifikasi {no}: {type(e).__name__}: {e}")
    return semua_ok


# ------------------------------------------------------------------ laporan
def _ribuan(x) -> str:
    return f"{x:,}".replace(",", ".")


def tulis_laporan(h: dict, path: str, durasi: float):
    p, l6, l7, l8, l9 = (h[k] for k in ("profil", "level6", "level7", "level8", "level9"))
    saya = p["nama"]
    baris = [
        "# Laporan Tugas Personal 2 — Blockchain Level 6–9",
        "",
        f"- **Nama:** {p['nama']}",
        f"- **NIM (4 digit terakhir):** {p['nim4']}",
        f"- **Dibuat:** {datetime.datetime.now():%Y-%m-%d %H:%M}  (waktu proses {durasi:.1f} detik)",
        f"- **Kode verifikasi:** `{h['kode_verifikasi']}`",
        "",
        "> Bagian hasil dibuat otomatis. Jangan diubah: dosen menghitung ulang semua angka dari data Anda.",
        "> Isi bagian **Analisis** dengan kata-kata Anda sendiri.",
        "",
        "## Level 6 — Mining data pribadi dan jejak difficulty",
        "",
        f"Data yang ditambang: `{l6['data_ditambang']}`",
        "",
        "| Difficulty | Nonce | Percobaan | Teori 16^d | Hash |", "|---|---|---|---|---|",
    ]
    baris += [f"| {m['difficulty']} | {m['nonce']} | {_ribuan(m['percobaan'])} | {_ribuan(m['teori'])} | `{m['hash'][:20]}…` |"
              for m in l6["mining"]]
    baris += [
        "",
        f"- Difficulty awal (dari NIM): **{l6['difficulty_awal']}**, target waktu blok {l6['target_detik']} detik",
        f"- Waktu blok simulasi (dari NIM + tanggal + bulan lahir): {', '.join(f'{w:g}' for w in l6['daftar_waktu_detik'])} detik",
        f"- Jejak difficulty (Modifikasi 6): **{', '.join(map(str, l6['jejak_difficulty']))}**",
        "",
        "## Level 7 — Kunci dan tanda tangan dari data pribadi",
        "",
        f"- Kunci publik (32 karakter awal): `{l7['kunci_publik_awal']}…`",
        f"- Alamat Anda: `{l7['alamat']}`",
        f"- Transaksi: kirim **{l7['transaksi']['amount']}** ke {l7['transaksi']['recipient']}",
        f"- Tanda tangan: `{l7['tanda_tangan'][:48]}…`",
        f"- Tanda tangan selalu sama saat diulang: {l7['tanda_tangan_selalu_sama']}",
        f"- Transaksi sah: **{l7['sah']}**; setelah amount diubah: **{l7['sah_setelah_amount_diubah']}**",
        f"- Penipu memakai alamat Anda: tanda tangannya valid dengan kuncinya = {l7['ttd_penipu_valid_dengan_kuncinya']}, "
        f"transaksinya sah = **{l7['transaksi_penipu_sah']}**",
        "",
        "## Level 8 — Jaringan dan fork pribadi",
        "",
        f"- Jumlah node: **{l8['jumlah_node']}**; blok pribadi tiap node: {l8['blok_pribadi_per_node']}",
        f"- Panjang rantai saat fork: {l8['panjang_saat_fork']}",
        f"- Setelah resolve_conflicts: {l8['panjang_setelah_resolve']}, sepakat = **{l8['sepakat_setelah_resolve']}**",
    ]
    if l8["perlu_pemecah_seri"]:
        baris.append(f"- Setelah blok pemecah seri: {l8['panjang_setelah_pemecah_seri']}, "
                     f"sepakat = **{l8['sepakat_setelah_pemecah_seri']}**")
    baris += [
        f"- Pemenang fork: **{l8['pemenang_fork']}**; blok terbuang (orphan): **{l8['blok_terbuang']}**",
        f"- Hash ujung rantai: `{l8['hash_ujung'][:24]}…`",
        "",
        "## Level 9 — Ekonomi dengan halving",
        "",
        f"- Hadiah awal: **{l9['hadiah_awal']}**, halving setiap **{l9['interval_halving']}** blok",
        f"- Hadiah blok 1–6 (Modifikasi 9): **{', '.join(map(str, l9['hadiah_per_blok']))}**",
        "",
        "| Alamat | Saldo |", "|---|---|",
    ]
    baris += [f"| {a} | {s} |" for a, s in l9["saldo"].items()]
    baris += [
        "",
        f"- Total suplai: **{l9['total_suplai']}**",
        f"- Belanja melebihi saldo ditolak: {l9['belanja_melebihi_saldo_ditolak']}",
        f"- Validasi ekonomi: **{l9['validasi_ekonomi']}**; setelah hadiah blok 1 dicurangi: **{l9['validasi_setelah_hadiah_dicurangi']}**",
        "",
        "## Analisis (isi dengan kata-kata Anda sendiri)",
        "",
        f"1. **Level 6.** Bandingkan kolom Percobaan dengan Teori 16^d pada tabel Anda. Mengapa bisa berbeda jauh? "
        f"Lalu jelaskan jejak difficulty Anda ({', '.join(map(str, l6['jejak_difficulty']))}): pada langkah mana difficulty naik, tetap, dan turun, dan mengapa?",
        "",
        "   _Jawaban:_",
        "",
        "2. **Level 7.** Mengapa tanda tangan Anda selalu sama setiap kali program dijalankan, padahal di Level 7 asli berubah-ubah? "
        "Mengapa transaksi penipu tidak sah walaupun tanda tangannya valid?",
        "",
        "   _Jawaban:_",
        "",
        f"3. **Keamanan kunci.** Kunci privat Anda dibuat dari nama, NIM, dan tanggal lahir. Mengapa cara ini SANGAT BERBAHAYA "
        "di dunia nyata? Siapa saja yang bisa mencuri dana alamat Anda? (Cari tahu istilah *brain wallet*.)",
        "",
        "   _Jawaban:_",
        "",
        f"4. **Level 8.** Jaringan Anda punya {l8['jumlah_node']} node dan pemenangnya {l8['pemenang_fork']} dengan "
        f"{l8['blok_terbuang']} blok terbuang. Jelaskan mengapa node itu menang. "
        + ("Mengapa jaringan Anda sempat tidak sepakat, dan bagaimana blok pemecah seri menyelesaikannya?"
           if l8["perlu_pemecah_seri"] else
           "Cari teman yang jaringannya sempat tidak sepakat: apa penyebabnya dan bagaimana diselesaikan?"),
        "",
        "   _Jawaban:_",
        "",
        f"5. **Level 9.** Dengan hadiah awal {l9['hadiah_awal']} dan halving setiap {l9['interval_halving']} blok, "
        "berapa batas total suplai jika mining berjalan selamanya? Tunjukkan perhitungannya, lalu kaitkan dengan batas 21 juta Bitcoin.",
        "",
        "   _Jawaban:_",
        "",
        "---",
        "",
        "## Data verifikasi (JANGAN DIUBAH)",
        "",
        "<!-- DATA-VERIFIKASI -->",
        "```json",
        json.dumps(h, indent=2, ensure_ascii=False),
        "```",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(baris))


# ------------------------------------------------------------------ main
def main():
    args = sys.argv[1:]
    kunci = "--kunci" in args
    hanya_cek = "--cek" in args
    path_data = os.path.join(HERE, "data_saya.py")
    if "--data" in args:
        path_data = os.path.abspath(args[args.index("--data") + 1])
    atur_path(kunci)

    if not pemeriksaan():
        print("\nPerbaiki modifikasi yang belum lolos, lalu jalankan lagi.")
        sys.exit(1)
    print("Semua modifikasi lolos pemeriksaan.")
    if hanya_cek:
        return

    import skenario_2
    try:
        profil = muat_data(path_data)
        skenario_2.normalisasi_profil(**profil)
    except (ValueError, AttributeError) as e:
        print(f"\nData di {os.path.basename(path_data)} belum benar: {e}")
        sys.exit(1)

    print("\nMenjalankan tugas dengan data Anda...")
    mulai = time.time()
    hasil = skenario_2.jalankan(profil)
    durasi = time.time() - mulai

    nama_file = f"laporan_tugas_personal_2_{hasil['profil']['nim4']}.md"
    out = os.path.join(os.path.dirname(path_data), nama_file)
    tulis_laporan(hasil, out, durasi)
    print(f"\nAlamat Anda      : {hasil['level7']['alamat']}")
    print(f"Kode verifikasi  : {hasil['kode_verifikasi']}")
    print(f"Laporan disimpan : {out}")
    print("Buka laporan itu, isi bagian Analisis, lalu serahkan ke dosen.")


if __name__ == "__main__":
    main()
