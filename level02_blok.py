"""
LEVEL 2 — Blockchain Dasar ala GeeksforGeeks, tanpa Flask (LATIHAN)
=========================================================================

Kode ini adalah port dari artikel:
https://www.geeksforgeeks.org/python/create-simple-blockchain-using-python/
dengan dua perubahan: (1) tanpa Flask agar bisa dijalankan di terminal,
(2) tingkat kesulitan (difficulty) dijadikan parameter, bukan '00000' tetap.

Tujuan belajar:
  * Struktur blok: index, timestamp, proof, previous_hash.
  * Menghubungkan blok dengan hash blok sebelumnya.
  * Proof of Work sederhana dan validasi rantai.

Jalankan tes:  python cek_nilai.py 2
"""

import datetime
import hashlib
import json


class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.chain = []
        # Blok genesis (blok pertama)
        self.create_block(proof=1, previous_hash="0")

    # ---------- SUDAH DISEDIAKAN ----------
    def create_block(self, proof: int, previous_hash: str) -> dict:
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.chain.append(block)
        return block

    def last_block(self) -> dict:
        """(Di artikel GfG bernama print_previous_block)."""
        return self.chain[-1]

    # ---------- BAGIAN YANG DIKERJAKAN (isi semua TODO) ----------
    def hash(self, block: dict) -> str:
        """SHA-256 dari blok yang diserialisasi JSON dengan sort_keys=True."""
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def valid_proof(self, previous_proof: int, proof: int) -> bool:
        """True jika SHA-256(str(proof**2 - previous_proof**2)) diawali `difficulty` angka nol."""
        guess = str(proof**2 - previous_proof**2).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash.startswith("0" * self.difficulty)

    def proof_of_work(self, previous_proof: int) -> int:
        """Cari bilangan bulat terkecil mulai dari 1 yang lolos valid_proof()."""
        new_proof = 1
        while not self.valid_proof(previous_proof, new_proof):
            new_proof += 1
        return new_proof

    def mine_block(self) -> dict:
        """Tambang blok baru: cari proof, hitung hash blok terakhir, lalu create_block()."""
        previous_block = self.last_block()
        previous_proof = previous_block["proof"]
        proof = self.proof_of_work(previous_proof)
        previous_hash = self.hash(previous_block)
        return self.create_block(proof, previous_hash)

    def chain_valid(self, chain: list) -> bool:
        """Periksa setiap blok (mulai blok ke-2):
        1. previous_hash == hash(blok sebelumnya)
        2. valid_proof(proof blok sebelumnya, proof blok ini) bernilai True
        """
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i-1]
            if current_block["previous_hash"] != self.hash(previous_block):
                return False
            if not self.valid_proof(previous_block["proof"], current_block["proof"]):
                return False
        return True


if __name__ == "__main__":
    bc = Blockchain(difficulty=4)
    for _ in range(4):
        b = bc.mine_block()
        print(f"Blok #{b['index']} ditambang, proof={b['proof']}")
    print(json.dumps(bc.chain, indent=2))
    print("Rantai valid?", bc.chain_valid(bc.chain))
