"""
Skenario Tugas Personal 2, Level 6–9 (JANGAN DIUBAH).

Menjalankan semua langkah tugas dengan data pribadi Anda, memakai:
  * kode Level 6–9 Anda di folder latihan/
  * empat modifikasi Anda di tugas_personal_2/modifikasi_2.py

Semua hasil yang dilaporkan DETERMINISTIK (data sama = hasil sama), sehingga
dosen bisa menghitung ulang hasil Anda dari data di laporan.
"""

import datetime
import hashlib
import json

import level06_difficulty as L6
import level07_tanda_tangan as L7
import modifikasi_2 as M


# ---------------------------------------------------------------- data diri
def normalisasi_profil(nama, nim4, tanggal_lahir, kota_asal, hobi) -> dict:
    """Rapikan dan periksa data. Lempar ValueError jika ada yang salah."""
    nama = " ".join(str(nama).split()).upper()
    nim4 = str(nim4).strip()
    tanggal_lahir = str(tanggal_lahir).strip()
    kota_asal = " ".join(str(kota_asal).split())
    hobi = " ".join(str(hobi).split())

    if not nama or nama.startswith("ISI "):
        raise ValueError("NAMA belum diisi")
    if len(nim4) != 4 or not nim4.isdigit():
        raise ValueError("NIM_4 harus tepat 4 digit angka, misalnya '0427'")
    try:
        datetime.date.fromisoformat(tanggal_lahir)
    except ValueError:
        raise ValueError("TANGGAL_LAHIR harus berformat YYYY-MM-DD, misalnya '2004-08-17'")
    if not kota_asal or kota_asal.upper().startswith("ISI "):
        raise ValueError("KOTA_ASAL belum diisi")
    if not hobi or hobi.upper().startswith("ISI "):
        raise ValueError("HOBI belum diisi")
    return {"nama": nama, "nim4": nim4, "tanggal_lahir": tanggal_lahir,
            "kota_asal": kota_asal, "hobi": hobi}


def digit_pribadi(p) -> str:
    """8 digit dari NIM_4 + tanggal + bulan lahir, contoh '0427' + '17' + '08'."""
    t = datetime.date.fromisoformat(p["tanggal_lahir"])
    return f"{p['nim4']}{t.day:02d}{t.month:02d}"


# ---------------------------------------------------------------- per level
def level6(p):
    data = f"{p['nama']}|{p['nim4']}|{p['tanggal_lahir']}"
    mining = []
    for d in (1, 2, 3, 4):
        nonce, h, percobaan = L6.tambang(data, d)
        mining.append({"difficulty": d, "nonce": nonce, "hash": h,
                       "percobaan": percobaan, "teori": L6.ekspektasi_percobaan(d)})
    awal = 1 + int(p["nim4"]) % 4
    daftar_waktu = [int(c) * 4 for c in digit_pribadi(p)]   # 0..36 detik
    return {
        "data_ditambang": data,
        "mining": mining,
        "difficulty_awal": awal,
        "daftar_waktu_detik": daftar_waktu,
        "target_detik": 10,
        "jejak_difficulty": M.jejak_difficulty(awal, daftar_waktu, 10),
    }


def level7(p):
    priv, pub = M.kunci_dari_data(p["nama"], p["nim4"], p["tanggal_lahir"])
    alamat = L7.alamat_dari_kunci_publik(pub)
    hari = datetime.date.fromisoformat(p["tanggal_lahir"]).day
    tx = {"sender": alamat, "recipient": "TEMAN_A", "amount": hari}
    ttd = M.tanda_tangani_deterministik(tx, priv)
    ttd_ulang = M.tanda_tangani_deterministik(tx, priv)

    palsu = dict(tx, amount=hari + 1000)
    priv_t, pub_t = M.kunci_dari_data("TEMAN PENIPU", "9999", "2000-01-01")
    tx_curian = {"sender": alamat, "recipient": "TEMAN PENIPU", "amount": 500}
    ttd_curian = M.tanda_tangani_deterministik(tx_curian, priv_t)
    return {
        "kunci_publik_awal": pub[:32],
        "alamat": alamat,
        "transaksi": tx,
        "tanda_tangan": ttd,
        "tanda_tangan_selalu_sama": ttd == ttd_ulang,
        "sah": L7.transaksi_sah(tx, ttd, pub),
        "sah_setelah_amount_diubah": L7.transaksi_sah(palsu, ttd, pub),
        "ttd_penipu_valid_dengan_kuncinya": L7.verifikasi(tx_curian, ttd_curian, pub_t),
        "transaksi_penipu_sah": L7.transaksi_sah(tx_curian, ttd_curian, pub_t),
    }


def level8(p):
    nama_depan = p["nama"].split()[0]
    n = 3 + int(p["nim4"]) % 3                       # 3, 4, atau 5 node
    nodes = [M.NodePersonal(f"{nama_depan}-{i + 1}", p["nim4"]) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            nodes[i].hubungkan(nodes[j])
    nodes[0].tambang_dan_siarkan([f"{p['nama']} membuka jaringan"])

    digit = digit_pribadi(p)
    blok_pribadi = [1 + int(digit[i]) % 3 for i in range(n)]   # 1..3 blok per node
    for node, k in zip(nodes, blok_pribadi):
        for b in range(k):
            node.tambang_blok([f"blok pribadi {b + 1}"])
    panjang_fork = [len(x.chain) for x in nodes]

    for node in nodes:
        node.resolve_conflicts()
    panjang_1 = [len(x.chain) for x in nodes]
    sepakat_1 = M.semua_sepakat(nodes)

    hasil = {
        "jumlah_node": n,
        "blok_pribadi_per_node": blok_pribadi,
        "panjang_saat_fork": panjang_fork,
        "panjang_setelah_resolve": panjang_1,
        "sepakat_setelah_resolve": sepakat_1,
        "perlu_pemecah_seri": not sepakat_1,
    }
    if not sepakat_1:
        nodes[0].tambang_dan_siarkan([f"{p['nama']} pemecah seri"])
        for node in nodes:
            node.resolve_conflicts()
        hasil["panjang_setelah_pemecah_seri"] = [len(x.chain) for x in nodes]
        hasil["sepakat_setelah_pemecah_seri"] = M.semua_sepakat(nodes)

    rantai = nodes[0].chain
    hasil["pemenang_fork"] = rantai[2]["miner"]
    hasil["blok_terbuang"] = sum(blok_pribadi) - sum(
        1 for b in rantai if any(str(t).startswith("blok pribadi") for t in b["transactions"]))
    hasil["hash_ujung"] = rantai[-1]["hash"]
    return hasil


def level9(p):
    tgl = datetime.date.fromisoformat(p["tanggal_lahir"])
    hadiah_awal = 20 + int(p["nim4"]) % 30          # 20..49
    interval = 2 + int(p["nim4"]) % 3               # 2..4
    bc = M.BlockchainHalving(hadiah_awal, interval, difficulty=2)
    saya = p["nama"]

    bc.mine(saya)
    bc.mine(saya)
    bc.add_transaction(saya, "TEMAN_A", tgl.month)
    bc.mine("TEMAN_A")
    bc.add_transaction("TEMAN_A", "TEMAN_B", int(p["nim4"]) % 7 + 1)
    bc.add_transaction(saya, "TEMAN_B", tgl.day % 5 + 1)
    bc.mine(saya)
    try:
        bc.add_transaction(saya, "TEMAN_C", bc.saldo(saya) + 1)
        boros_ditolak = False
    except ValueError:
        boros_ditolak = True
    bc.mine(saya)
    bc.mine("TEMAN_B")

    hasil = {
        "hadiah_awal": hadiah_awal,
        "interval_halving": interval,
        "hadiah_per_blok": [b["transactions"][0]["amount"] for b in bc.chain[1:]],
        "saldo": {a: bc.saldo(a) for a in (saya, "TEMAN_A", "TEMAN_B")},
        "total_suplai": bc.total_suplai(),
        "belanja_melebihi_saldo_ditolak": boros_ditolak,
        "validasi_ekonomi": bc.validasi_ekonomi(),
        "hash_ujung": bc.chain[-1]["hash"],
    }
    bc.chain[1]["transactions"][0]["amount"] += 1
    hasil["validasi_setelah_hadiah_dicurangi"] = bc.validasi_ekonomi()
    return hasil


def jalankan(profil: dict) -> dict:
    """Jalankan seluruh tugas. Kembalikan dict hasil + kode verifikasi."""
    p = normalisasi_profil(**profil)
    hasil = {
        "tugas": "personal-2 (Level 6-9)",
        "profil": p,
        "level6": level6(p),
        "level7": level7(p),
        "level8": level8(p),
        "level9": level9(p),
    }
    hasil["kode_verifikasi"] = kode_verifikasi(hasil)
    return hasil


def kode_verifikasi(hasil: dict) -> str:
    isi = {k: v for k, v in hasil.items() if k != "kode_verifikasi"}
    return hashlib.sha256(json.dumps(isi, sort_keys=True).encode()).hexdigest()[:12].upper()
