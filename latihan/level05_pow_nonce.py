"""
LEVEL 5 — Proof of Work dengan Nonce & Hash Blok Terintegrasi
=============================================================

Tujuan belajar:
  * Memahami perbaikan desain PoW: hash blok dihitung dari seluruh isi blok termasuk nonce.
  * Blok menyimpan field 'hash' dan 'nonce'.
  * Saat menghitung hash, key 'hash' diabaikan.
  * Perubahan sekecil apapun pada transaksi/data membatalkan hash dan Proof of Work.
  * Tambang ulang (re-mining) berantai untuk memulihkan validitas.
"""

import datetime
import hashlib
import json


class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.difficulty = difficulty
        self.chain = []
        # Buat blok genesis
        self.new_block(transactions=[], previous_hash="0")

    @staticmethod
    def hash_block(block: dict) -> str:
        """Hitung SHA-256 dari blok secara kanonik, mengabaikan key 'hash' jika ada.
        Dict asli tidak boleh diubah.
        """
        data = {k: v for k, v in block.items() if k != "hash"}
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def proof_of_work(self, block: dict) -> int:
        """Cari nonce terkecil mulai dari 0 sehingga hash_block(block)
        diawali dengan '0' * self.difficulty.
        Memperbarui field 'nonce' dan 'hash' di blok, serta mengembalikan jumlah percobaan (nonce + 1).
        """
        target = "0" * self.difficulty
        nonce = 0
        while True:
            block["nonce"] = nonce
            h = self.hash_block(block)
            if h.startswith(target):
                block["hash"] = h
                return nonce + 1
            nonce += 1

    def new_block(self, transactions: list, previous_hash: str = None) -> dict:
        """Buat blok baru, tambang dengan proof_of_work, tambahkan ke chain, lalu kembalikan blok."""
        if previous_hash is None:
            previous_hash = self.chain[-1]["hash"] if self.chain else "0"

        block = {
            "index": len(self.chain),
            "timestamp": str(datetime.datetime.now()),
            "transactions": transactions,
            "previous_hash": previous_hash,
            "nonce": 0,
        }
        self.proof_of_work(block)
        self.chain.append(block)
        return block

    def chain_valid(self, chain: list = None) -> bool:
        """Validasi integritas seluruh rantai blockchain:
        1. Hash di dalam blok harus cocok dengan Blockchain.hash_block(blok)
        2. Hash harus memenuhi target difficulty (diawali '0' * difficulty)
        3. Untuk blok setelah genesis, previous_hash harus cocok dengan hash blok sebelumnya
        4. Indeks blok harus berurutan
        """
        if chain is None:
            chain = self.chain

        target = "0" * self.difficulty
        for i, block in enumerate(chain):
            # 1. Pastikan hash di blok sesuai dengan isi blok (kecuali key 'hash')
            if block.get("hash") != self.hash_block(block):
                return False

            # 2. Pastikan hash memenuhi target difficulty
            if not block.get("hash", "").startswith(target):
                return False

            # 3. Untuk blok setelah genesis, pastikan previous_hash cocok dengan hash blok sebelumnya
            if i > 0:
                if block.get("previous_hash") != chain[i - 1].get("hash"):
                    return False
                if block.get("index") != i:
                    return False

        return True

    def tambang_ulang_dari(self, mulai: int) -> int:
        """Menambang ulang blok mulai dari indeks `mulai` sampai akhir rantai.
        Previous hash setiap blok diperbarui dari hash blok sebelumnya.
        Mengembalikan total percobaan (usaha) yang dilakukan.
        """
        total_usaha = 0
        for i in range(mulai, len(self.chain)):
            if i > 0:
                self.chain[i]["previous_hash"] = self.chain[i - 1]["hash"]
            usaha = self.proof_of_work(self.chain[i])
            total_usaha += usaha
        return total_usaha


if __name__ == "__main__":
    bc = Blockchain(difficulty=3)
    for tx in (["Ani->Budi 5"], ["Budi->Citra 2"], ["Citra->Dodi 1"]):
        b = bc.new_block(tx)
        print(f"Blok #{b['index']} ditambang: nonce={b['nonce']}, hash={b['hash']}")

    print("\nRantai valid?", bc.chain_valid())

    print("\nSimulasi pemalsuan transaksi di blok #1:")
    bc.chain[1]["transactions"] = ["Ani->Budi 500"]
    print("Rantai setelah dipalsukan valid?", bc.chain_valid())

    print("\nMenambang ulang mulai dari blok #1...")
    usaha = bc.tambang_ulang_dari(1)
    print(f"Selesai ditambang ulang dengan total {usaha} percobaan.")
    print("Rantai setelah ditambang ulang valid?", bc.chain_valid())
