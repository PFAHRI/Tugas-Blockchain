"""
Menjalankan Tugas Personal Level 1–5 dan membuat laporan.

Pemakaian (dari folder blockchain-latihan):
    python tugas_personal/jalankan_tugas.py              # periksa modifikasi + buat laporan
    python tugas_personal/jalankan_tugas.py --cek        # hanya periksa modifikasi
    python tugas_personal/jalankan_tugas.py --data file.py   # pakai file data lain

Laporan disimpan sebagai tugas_personal/laporan_tugas_personal_<NIM_4>.md
"""

import datetime
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
    else:      # mahasiswa: modifikasi dari tugas_personal/, kode level dari latihan/
        sys.path[:0] = [HERE, os.path.join(ROOT, "latihan")]


def muat_data(path: str) -> dict:
    spec = importlib.util.spec_from_file_location("data_saya", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {"nama": mod.NAMA, "nim4": mod.NIM_4, "tanggal_lahir": mod.TANGGAL_LAHIR,
            "kota_asal": mod.KOTA_ASAL, "hobi": mod.HOBI}


# ------------------------------------------------------------------ pemeriksaan
def pemeriksaan() -> bool:
    """Periksa kelima modifikasi dengan data uji. Kembalikan True jika semua lolos."""
    import level01_hash as L1
    import level02_blok as L2
    import level03_tampering as L3
    import level04_transaksi as L4
    import modifikasi as M

    def cek1():
        s = M.sidik_jari("UJI COBA", "0042", "2000-01-31")
        assert isinstance(s, str) and len(s) == 8, "harus string 8 karakter"
        assert s == L1.sha256_hex("0042:UJI COBA:2000-01-31")[:8], "format f\"{nim4}:{nama}:{tanggal_lahir}\" belum tepat"
        assert s != M.sidik_jari("UJI COBA", "0043", "2000-01-31"), "NIM berbeda harus menghasilkan ID berbeda"

    def cek2():
        bc = M.BlockchainPersonal("0042", "abcd1234", difficulty=2)
        assert isinstance(bc, L2.Blockchain), "harus turunan Blockchain Level 2"
        assert len(bc.chain) == 1, "baru dibuat harus berisi 1 blok (genesis)"
        assert bc.chain[0]["proof"] == 42, "proof genesis harus int(nim4)"
        bc.mine_block(); bc.mine_block()
        assert all(b.get("pemilik") == "abcd1234" for b in bc.chain), "setiap blok harus punya 'pemilik'"
        assert bc.chain_valid(bc.chain), "rantai hasil mining harus valid"

    def cek3():
        bc = L3.Blockchain(difficulty=2)
        for d in ["a", "b", "c"]:
            bc.mine_block(d)
        asli = json.dumps(bc.chain, sort_keys=True)
        palsu, disambung = M.palsukan(bc.chain, 2)
        assert json.dumps(bc.chain, sort_keys=True) == asli, "rantai asli tidak boleh berubah"
        assert palsu[2]["data"] == "b (DIPALSUKAN)", "data harus ditambah ' (DIPALSUKAN)'"
        assert L3.cari_tautan_putus(palsu) == 3, "rantai palsu belum disambung ulang"
        assert L3.cari_tautan_putus(disambung) is None, "rantai disambung masih putus"

    def cek4():
        bc = L4.Blockchain(difficulty=2)
        bc.add_transaction("UJI", "A", 5); bc.add_transaction("A", "UJI", 3); bc.mine_block()
        bc.add_transaction("UJI", "B", 1); bc.mine_block()
        bc.add_transaction("C", "UJI", 100)  # masih pending, tidak dihitung
        r = M.ringkasan_saldo(bc, "UJI")
        assert r == {"masuk": 3, "keluar": 6, "bersih": -3}, f"hasil {r}, seharusnya masuk 3, keluar 6, bersih -3"

    def cek5():
        a = M.BlockchainDeterministik("2000-01-31", "abcd1234", difficulty=2)
        b = M.BlockchainDeterministik("2000-01-31", "abcd1234", difficulty=2)
        for bc in (a, b):
            bc.new_block(["x"]); bc.new_block(["y"])
        g = a.chain[0]
        assert g["timestamp"] == "2000-01-31", "timestamp genesis harus tanggal lahir"
        assert g["transactions"] == ["GENESIS abcd1234"], "transaksi genesis harus ['GENESIS <id_mhs>']"
        assert a.chain[2]["timestamp"] == "2000-01-31 #2", "timestamp blok harus f\"{tanggal_lahir} #{index}\""
        assert [x["hash"] for x in a.chain] == [x["hash"] for x in b.chain], "hasil belum deterministik"
        assert a.chain_valid(), "rantai harus valid"

    semua_ok = True
    print("\nPemeriksaan modifikasi (memakai data uji, bukan data Anda):")
    for no, fungsi in enumerate([cek1, cek2, cek3, cek4, cek5], start=1):
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
        except Exception as e:  # error lain, misalnya kode level belum lengkap
            semua_ok = False
            print(f"  [ERROR] Modifikasi {no}: {type(e).__name__}: {e}")
    return semua_ok


# ------------------------------------------------------------------ laporan
def tulis_laporan(h: dict, path: str, durasi: float):
    p, l1, l2, l3, l4, l5 = (h[k] for k in ("profil", "level1", "level2", "level3", "level4", "level5"))
    putus = l3["tautan_putus_di"]
    baris = [
        "# Laporan Tugas Personal Blockchain Level 1–5",
        "",
        f"- **Nama:** {p['nama']}",
        f"- **NIM (4 digit terakhir):** {p['nim4']}",
        f"- **Dibuat:** {datetime.datetime.now():%Y-%m-%d %H:%M}  (waktu proses {durasi:.1f} detik)",
        f"- **Kode verifikasi:** `{h['kode_verifikasi']}`",
        "",
        "> Bagian hasil dibuat otomatis. Jangan diubah: dosen menghitung ulang semua angka dari data Anda.",
        "> Isi bagian **Analisis** dengan kata-kata Anda sendiri.",
        "",
        "## Level 1 — Hash data pribadi",
        "",
        "| Hasil | Nilai |", "|---|---|",
        f"| SHA-256 nama | `{l1['hash_nama']}` |",
        f"| hash_dict profil | `{l1['hash_profil']}` |",
        f"| hash_dict profil (urutan key dibalik) | `{l1['hash_profil_urutan_terbalik']}` |",
        f"| Bit berubah: tanggal lahir vs tanggal lahir + 1 hari | {l1['avalanche_tanggal_persen']}% |",
        f"| ID mahasiswa (Modifikasi 1) | `{l1['id_mahasiswa']}` |",
        "",
        "## Level 2 — Blockchain personal",
        "",
        f"- Proof genesis: **{l2['proof_genesis']}** (dari NIM)",
        f"- Proof blok 2, 3, 4: **{', '.join(map(str, l2['proof_blok']))}**",
        f"- Pemilik setiap blok: `{', '.join(map(str, l2['pemilik_semua_blok']))}`",
        f"- Rantai valid: {l2['valid']}",
        "",
        "## Level 3 — Pemalsuan data pribadi",
        "",
        f"- Posisi yang dipalsukan: **{l3['posisi_dipalsukan']}**",
        f"- Data asli: `{l3['data_asli']}`",
        f"- Data palsu: `{l3['data_palsu']}`",
        f"- Valid sebelum dipalsukan: {l3['valid_asli']}",
        f"- Tautan putus di indeks: **{putus}**",
        f"- Valid setelah dipalsukan: **{l3['valid_setelah_dipalsukan']}**",
        f"- Valid setelah disambung ulang: **{l3['valid_setelah_disambung_ulang']}**",
        "",
        "## Level 4 — Transaksi dari data pribadi",
        "",
        "| Blok | Pengirim | Penerima | Jumlah |", "|---|---|---|---|",
    ]
    baris += [f"| {i} | {t['sender']} | {t['recipient']} | {t['amount']} |" for i, t in l4["riwayat"]]
    r = l4["ringkasan_saldo"]
    baris += [
        "",
        f"- Ringkasan saldo (Modifikasi 4): masuk **{r['masuk']}**, keluar **{r['keluar']}**, bersih **{r['bersih']}**",
        f"- Kirim ke diri sendiri ditolak: {l4['kirim_ke_diri_sendiri_ditolak']}",
        f"- Amount 0 ditolak: {l4['amount_nol_ditolak']}",
        "",
        "## Level 5 — Proof of Work dengan nonce (deterministik)",
        "",
        "| Blok | Nonce | Hash |", "|---|---|---|",
    ]
    baris += [f"| {i} | {n} | `{hs[:24]}…` |" for i, (n, hs) in enumerate(zip(l5["nonce"], l5["hash"]))]
    baris += [
        "",
        f"- Valid: {l5['valid']} → setelah blok 1 dipalsukan: **{l5['valid_setelah_dipalsukan']}**",
        f"- Percobaan hash untuk menambang ulang blok 1–3: **{l5['percobaan_tambang_ulang']:,}**".replace(",", "."),
        f"- Valid setelah ditambang ulang: {l5['valid_setelah_tambang_ulang']}",
        "",
        "## Analisis (isi dengan kata-kata Anda sendiri)",
        "",
        "1. **Level 1.** Bandingkan SHA-256 nama Anda dengan milik seorang teman. Apakah ada pola yang mirip? "
        f"Jelaskan juga mengapa dua hash profil Anda sama, dan mengapa hanya menambah 1 hari pada tanggal lahir mengubah {l1['avalanche_tanggal_persen']}% bit.",
        "",
        "   _Jawaban:_",
        "",
        f"2. **Level 2.** Kode Anda dan teman sama persis, tetapi proof Anda ({', '.join(map(str, l2['proof_blok']))}) berbeda. Jelaskan penyebabnya.",
        "",
        "   _Jawaban:_",
        "",
        f"3. **Level 3.** Anda memalsukan posisi {l3['posisi_dipalsukan']} dan "
        f"{'tautan putus terdeteksi di indeks ' + str(putus) if putus is not None else 'tidak ada tautan putus yang terdeteksi (None)'}, "
        f"sedangkan valid setelah dipalsukan = {l3['valid_setelah_dipalsukan']}. "
        "Jelaskan hasil ini, lalu bandingkan dengan teman yang posisi pemalsuannya berbeda.",
        "",
        "   _Jawaban:_",
        "",
        f"4. **Level 4.** Jelaskan dari mana angka masuk {r['masuk']}, keluar {r['keluar']}, dan bersih {r['bersih']} berasal. "
        "Mengapa transaksi ke diri sendiri perlu ditolak?",
        "",
        "   _Jawaban:_",
        "",
        f"5. **Level 5.** Penyerang butuh {l5['percobaan_tambang_ulang']:,} percobaan hash untuk memalsukan rantai Anda. ".replace(",", ".")
        + "Mengapa nonce Anda selalu sama setiap kali program dijalankan, padahal di demo Level 5 asli nonce berubah-ubah?",
        "",
        "   _Jawaban:_",
        "",
        "6. **Etika data.** Anda baru saja menyimpan nama dan tanggal lahir di dalam blockchain. "
        "Jika ini blockchain publik, apa risikonya? Kaitkan dengan sifat immutability dan UU No. 27 Tahun 2022 "
        "tentang Pelindungan Data Pribadi, terutama hak untuk menghapus data.",
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

    import skenario
    try:
        profil = muat_data(path_data)
        skenario.normalisasi_profil(**profil)
    except (ValueError, AttributeError) as e:
        print(f"\nData di {os.path.basename(path_data)} belum benar: {e}")
        sys.exit(1)

    print("\nMenjalankan tugas dengan data Anda (sekitar 5-30 detik)...")
    mulai = time.time()
    hasil = skenario.jalankan(profil)
    durasi = time.time() - mulai

    nama_file = f"laporan_tugas_personal_{hasil['profil']['nim4']}.md"
    out = os.path.join(os.path.dirname(path_data), nama_file)
    tulis_laporan(hasil, out, durasi)
    print(f"\nID mahasiswa     : {hasil['level1']['id_mahasiswa']}")
    print(f"Kode verifikasi  : {hasil['kode_verifikasi']}")
    print(f"Laporan disimpan : {out}")
    print("Buka laporan itu, isi bagian Analisis, lalu serahkan ke dosen.")


if __name__ == "__main__":
    main()
