"""
Skenario Tugas Personal Level 1–5 (JANGAN DIUBAH).

File ini menjalankan semua langkah tugas dengan data pribadi Anda, memakai:
  * kode Level 1–5 Anda di folder latihan/
  * lima modifikasi Anda di tugas_personal/modifikasi.py

Semua hasil dirancang DETERMINISTIK: data yang sama selalu menghasilkan angka
yang sama. Karena itu dosen bisa menghitung ulang hasil Anda dari data yang
tercantum di laporan dan memastikan laporan tidak disalin atau diubah manual.
"""

import datetime
import hashlib
import json

import level01_hash as L1
import level03_tampering as L3
import level04_transaksi as L4
import modifikasi as M


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


def tanggal_plus_satu(tgl: str) -> str:
    return (datetime.date.fromisoformat(tgl) + datetime.timedelta(days=1)).isoformat()


# ---------------------------------------------------------------- per level
def level1(p):
    id_mhs = M.sidik_jari(p["nama"], p["nim4"], p["tanggal_lahir"])
    profil_terbalik = dict(reversed(list(p.items())))
    return {
        "hash_nama": L1.sha256_hex(p["nama"]),
        "hash_profil": L1.hash_dict(p),
        "hash_profil_urutan_terbalik": L1.hash_dict(profil_terbalik),
        "avalanche_tanggal_persen": round(
            L1.persen_bit_berbeda(p["tanggal_lahir"], tanggal_plus_satu(p["tanggal_lahir"])), 2),
        "id_mahasiswa": id_mhs,
    }


def level2(p, id_mhs, difficulty=4):
    bc = M.BlockchainPersonal(p["nim4"], id_mhs, difficulty=difficulty)
    for _ in range(3):
        bc.mine_block()
    return {
        "proof_genesis": bc.chain[0]["proof"],
        "proof_blok": [b["proof"] for b in bc.chain[1:]],
        "pemilik_semua_blok": sorted({b.get("pemilik") for b in bc.chain}, key=str),
        "valid": bc.chain_valid(bc.chain),
    }


def level3(p):
    bc = L3.Blockchain(difficulty=3)
    data = [
        f"{p['nama']} lahir {p['tanggal_lahir']}",
        f"{p['nama']} berasal dari {p['kota_asal']}",
        f"{p['nama']} hobi {p['hobi']}",
        f"{p['nama']} NIM akhir {p['nim4']}",
    ]
    for d in data:
        bc.mine_block(d)
    posisi = 1 + int(p["nim4"]) % 4          # 1..4, berbeda tiap mahasiswa
    palsu, disambung = M.palsukan(bc.chain, posisi)
    return {
        "posisi_dipalsukan": posisi,
        "data_asli": bc.chain[posisi]["data"],
        "data_palsu": palsu[posisi]["data"],
        "valid_asli": bc.chain_valid(bc.chain),
        "tautan_putus_di": L3.cari_tautan_putus(palsu),
        "valid_setelah_dipalsukan": bc.chain_valid(palsu),
        "valid_setelah_disambung_ulang": bc.chain_valid(disambung),
    }


def transaksi_personal(p):
    tgl = datetime.date.fromisoformat(p["tanggal_lahir"])
    a1, a2, a3 = tgl.day, tgl.month, int(p["nim4"]) % 50 + 1
    return [
        (p["nama"], "TEMAN_A", a1),
        ("TEMAN_A", p["nama"], a2),
        (p["nama"], "DOSEN", a3),
    ]


def level4(p):
    bc = L4.Blockchain(difficulty=3)
    tx = transaksi_personal(p)
    bc.add_transaction(*tx[0])
    bc.add_transaction(*tx[1])
    bc.mine_block()
    bc.add_transaction(*tx[2])
    bc.mine_block()
    ditolak = []
    for uji in [(p["nama"], p["nama"], 5), (p["nama"], "TEMAN_B", 0)]:
        try:
            bc.add_transaction(*uji)
            ditolak.append(False)
        except ValueError:
            ditolak.append(True)
    return {
        "riwayat": [[i, t] for i, t in bc.riwayat(p["nama"])],
        "ringkasan_saldo": M.ringkasan_saldo(bc, p["nama"]),
        "kirim_ke_diri_sendiri_ditolak": ditolak[0],
        "amount_nol_ditolak": ditolak[1],
        "jumlah_blok": len(bc.chain),
    }


def level5(p, id_mhs, difficulty=4):
    bc = M.BlockchainDeterministik(p["tanggal_lahir"], id_mhs, difficulty=difficulty)
    tx = [f"{a} -> {b}: {c}" for a, b, c in transaksi_personal(p)]
    bc.new_block(tx[:2])
    bc.new_block(tx[2:])
    bc.new_block([f"{p['nama']} menyelesaikan Level 5"])
    hasil = {
        "nonce": [b["nonce"] for b in bc.chain],
        "hash": [b["hash"] for b in bc.chain],
        "valid": bc.chain_valid(),
    }
    bc.chain[1]["transactions"] = [f"{p['nama']} -> TEMAN_A: 999999"]
    hasil["valid_setelah_dipalsukan"] = bc.chain_valid()
    hasil["percobaan_tambang_ulang"] = bc.tambang_ulang_dari(1)
    hasil["valid_setelah_tambang_ulang"] = bc.chain_valid()
    return hasil


def jalankan(profil: dict) -> dict:
    """Jalankan seluruh tugas. Kembalikan dict hasil + kode verifikasi."""
    p = normalisasi_profil(**profil)
    h1 = level1(p)
    hasil = {
        "profil": p,
        "level1": h1,
        "level2": level2(p, h1["id_mahasiswa"]),
        "level3": level3(p),
        "level4": level4(p),
        "level5": level5(p, h1["id_mahasiswa"]),
    }
    hasil["kode_verifikasi"] = kode_verifikasi(hasil)
    return hasil


def kode_verifikasi(hasil: dict) -> str:
    isi = {k: v for k, v in hasil.items() if k != "kode_verifikasi"}
    return hashlib.sha256(json.dumps(isi, sort_keys=True).encode()).hexdigest()[:12].upper()
