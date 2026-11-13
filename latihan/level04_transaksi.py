"""
LEVEL 4 — Transaksi dan Mempool / Pending Transactions
======================================================

Tujuan belajar:
  * Memahami transaksi dalam blok blockchain.
  * Validasi transaksi (sender, recipient, amount).
  * Pengelolaan pending transactions (mempool).
  * Riwayat transaksi per alamat/pengguna.
"""

import datetime
import hashlib
import json


class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.chain = []
        self.pending_transactions = []
        # Blok genesis (blok pertama)
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof: int, previous_hash: str) -> dict:
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "transactions": list(self.pending_transactions),
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def last_block(self) -> dict:
        return self.chain[-1]

    def hash(self, block: dict) -> str:
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def valid_proof(self, previous_proof: int, proof: int) -> bool:
        guess = str(proof**2 - previous_proof**2).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash.startswith("0" * self.difficulty)

    def proof_of_work(self, previous_proof: int) -> int:
        proof = 1
        while not self.valid_proof(previous_proof, proof):
            proof += 1
        return proof

    def add_transaction(self, sender: str, recipient: str, amount: float | int) -> int:
        """Tambahkan transaksi baru ke daftar pending_transactions.

        Validasi:
        - sender dan recipient harus berupa string tidak kosong
        - sender dan recipient tidak boleh sama
        - amount harus berupa int atau float (bukan boolean) dan lebih besar dari 0

        Mengembalikan index blok berikutnya yang akan memuat transaksi ini.
        """
        if not isinstance(sender, str) or not sender.strip():
            raise ValueError("Sender harus berupa string dan tidak boleh kosong.")
        if not isinstance(recipient, str) or not recipient.strip():
            raise ValueError("Recipient harus berupa string dan tidak boleh kosong.")
        if sender.strip() == recipient.strip():
            raise ValueError("Sender dan recipient tidak boleh sama.")
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError("Amount harus berupa int atau float.")
        if amount <= 0:
            raise ValueError("Amount harus lebih besar dari 0.")

        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
        }
        self.pending_transactions.append(transaction)
        return self.last_block()["index"] + 1

    def mine_block(self) -> dict:
        """Tambang blok baru: cari proof, ambil hash blok terakhir, lalu create_block()."""
        prev_block = self.last_block()
        proof = self.proof_of_work(prev_block["proof"])
        previous_hash = self.hash(prev_block)
        return self.create_block(proof, previous_hash)

    def chain_valid(self, chain: list) -> bool:
        for i in range(1, len(chain)):
            prev = chain[i - 1]
            curr = chain[i]
            if curr["previous_hash"] != self.hash(prev):
                return False
            if not self.valid_proof(prev["proof"], curr["proof"]):
                return False
        return True

    def riwayat(self, address: str) -> list:
        """Ambil riwayat transaksi yang melibatkan `address` dari seluruh blok yang sudah ditambang.

        Mengembalikan list tuple: [(index_blok, data_transaksi), ...]
        Transaksi yang masih pending tidak diikutsertakan.
        """
        hasil = []
        for block in self.chain:
            for tx in block.get("transactions", []):
                if tx.get("sender") == address or tx.get("recipient") == address:
                    hasil.append((block["index"], tx))
        return hasil


if __name__ == "__main__":
    bc = Blockchain(difficulty=3)
    bc.add_transaction("Ani", "Budi", 5)
    bc.add_transaction("Budi", "Citra", 2.5)
    blok2 = bc.mine_block()
    print(f"Blok #{blok2['index']} ditambang dengan {len(blok2['transactions'])} transaksi.")

    bc.add_transaction("Citra", "Dodi", 1)
    blok3 = bc.mine_block()
    print(f"Blok #{blok3['index']} ditambang dengan {len(blok3['transactions'])} transaksi.")

    print("\nRiwayat transaksi Budi:")
    for idx, tx in bc.riwayat("Budi"):
        print(f"  Blok #{idx}: {tx['sender']} -> {tx['recipient']} sebesar {tx['amount']}")
