"""
TUGAS PERSONAL — Lima Modifikasi Level 1–5 (DIKERJAKAN MAHASISWA)
===========================================================

Setiap fungsi/kelas di bawah memodifikasi kode level sebelumnya agar memakai
data pribadi mahasiswa. Hasilnya berbeda untuk setiap mahasiswa.

Jalankan:  python tugas_latihan/jalankan_tugas.py
"""

import level01_hash as L1
import level02_blok as L2
import level03_tampering as L3
import level05_pow_nonce as L5


# ============================================================== MODIFIKASI 1
def sidik_jari(nama: str, nim4: str, tanggal_lahir: str) -> str:
    """ID mahasiswa = 8 karakter pertama dari sha256_hex(f"{nim4}:{nama}:{tanggal_lahir}").

    Gunakan sha256_hex dari Level 1 (sudah diimpor sebagai L1).
    Contoh bentuk hasil: 'a3f09c1e'
    """
    return L1.sha256_hex(f"{nim4}:{nama}:{tanggal_lahir}")[:8]


# ============================================================== MODIFIKASI 2
class BlockchainPersonal(L2.Blockchain):
    """Blockchain Level 2 yang dipersonalisasi:
      * proof blok genesis = int(nim4)   (bukan 1 seperti di GfG)
      * SETIAP blok (termasuk genesis) punya field tambahan "pemilik" = id_mhs
    """

    def __init__(self, nim4: str, id_mhs: str, difficulty: int = 4):
        self.difficulty = difficulty
        self.id_mhs = id_mhs
        self.chain = []
        self.create_block(proof=int(nim4), previous_hash="0")

    def create_block(self, proof: int, previous_hash: str) -> dict:
        block = super().create_block(proof, previous_hash)
        block["pemilik"] = self.id_mhs
        return block


# ============================================================== MODIFIKASI 3
def palsukan(chain: list, posisi: int):
    """Simulasi pemalsuan di Level 3.

    1. palsu     = ubah_blok(...) : data blok `posisi` ditambah teks " (DIPALSUKAN)"
    2. disambung = sambung_ulang(palsu, posisi + 1)
    Kembalikan tuple (palsu, disambung). Rantai asli tidak boleh berubah.
    """
    data_baru = f"{chain[posisi]['data']} (DIPALSUKAN)"
    palsu = L3.ubah_blok(chain, posisi, "data", data_baru)
    disambung = L3.sambung_ulang(palsu, posisi + 1)
    return palsu, disambung


# ============================================================== MODIFIKASI 4
def ringkasan_saldo(bc, nama: str) -> dict:
    """Dari bc.riwayat(nama) (Level 4), hitung:
      {"masuk": total amount yang DITERIMA nama,
       "keluar": total amount yang DIKIRIM nama,
       "bersih": masuk - keluar}
    """
    masuk = 0
    keluar = 0
    for _, tx in bc.riwayat(nama):
        if tx.get("recipient") == nama:
            masuk += tx.get("amount", 0)
        if tx.get("sender") == nama:
            keluar += tx.get("amount", 0)
    return {
        "masuk": masuk,
        "keluar": keluar,
        "bersih": masuk - keluar,
    }


# ============================================================== MODIFIKASI 5
class BlockchainDeterministik(L5.Blockchain):
    """Blockchain Level 5 tanpa jam komputer, agar hasilnya bisa dihitung ulang dosen:
      * genesis: {"index": 0, "timestamp": tanggal_lahir,
                  "transactions": [f"GENESIS {id_mhs}"], "previous_hash": "0"*64, "nonce": 0}
        lalu ditambang dengan self.proof_of_work dan dimasukkan ke self.chain
      * new_block(): sama seperti Level 5, tetapi timestamp = f"{tanggal_lahir} #{index}"
    """

    def __init__(self, tanggal_lahir: str, id_mhs: str, difficulty: int = 4):
        self.difficulty = difficulty
        self.tanggal_lahir = tanggal_lahir
        self.id_mhs = id_mhs
        self.chain = []
        genesis = {
            "index": 0,
            "timestamp": tanggal_lahir,
            "transactions": [f"GENESIS {id_mhs}"],
            "previous_hash": "0" * 64,
            "nonce": 0,
        }
        self.proof_of_work(genesis)
        self.chain.append(genesis)

    def new_block(self, transactions: list) -> dict:
        index = len(self.chain)
        previous_hash = self.chain[-1]["hash"]
        block = {
            "index": index,
            "timestamp": f"{self.tanggal_lahir} #{index}",
            "transactions": transactions,
            "previous_hash": previous_hash,
            "nonce": 0,
        }
        self.proof_of_work(block)
        self.chain.append(block)
        return block
