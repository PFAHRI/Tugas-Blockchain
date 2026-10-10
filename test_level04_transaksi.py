import pytest

import datetime
import hashlib
import json

class Blockchain:
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain = []
        self.pending_transactions = []
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof: int, previous_hash: str) -> dict:
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "transactions": self.pending_transactions.copy(),
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def hash(self, block: dict) -> str:
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def add_transaction(self, sender, recipient, amount):
        if not sender or not isinstance(sender, str) or not sender.strip():
            raise ValueError("Sender tidak valid")
        if not recipient or not isinstance(recipient, str) or not recipient.strip():
            raise ValueError("Recipient tidak valid")
        if sender == recipient:
            raise ValueError("Sender dan recipient tidak boleh sama")
        if type(amount) is bool or not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount tidak valid")
        
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        return len(self.chain) + 1

    def mine_block(self):
        previous_block = self.chain[-1]
        previous_proof = previous_block["proof"]
        
        proof = 1
        
        previous_hash = self.hash(previous_block)
        return self.create_block(proof, previous_hash)

    def riwayat(self, nama: str):
        history = []
        for block in self.chain:
            for tx in block["transactions"]:
                if tx["sender"] == nama or tx["recipient"] == nama:
                    history.append((block["index"], tx))
        return history


@pytest.fixture
def bc():
    return Blockchain(difficulty=3)


def test_genesis_punya_transactions_kosong(bc):
    g = bc.chain[0]
    assert set(g) >= {"index", "timestamp", "transactions", "proof", "previous_hash"}
    assert g["transactions"] == []


def test_add_transaction_kembalikan_index_blok_berikutnya(bc):
    assert bc.add_transaction("Ani", "Budi", 5) == 2
    assert bc.pending_transactions == [{"sender": "Ani", "recipient": "Budi", "amount": 5}]


@pytest.mark.parametrize("sender,recipient,amount", [
    ("", "Budi", 5),
    ("Ani", "   ", 5),
    ("Ani", "Ani", 5),
    ("Ani", "Budi", 0),
    ("Ani", "Budi", -3),
    ("Ani", "Budi", "5"),
    ("Ani", "Budi", True),
    (None, "Budi", 5),
])
def test_add_transaction_validasi(bc, sender, recipient, amount):
    with pytest.raises(ValueError):
        bc.add_transaction(sender, recipient, amount)
    assert bc.pending_transactions == []


def test_mine_memasukkan_dan_mengosongkan_pending(bc):
    bc.add_transaction("Ani", "Budi", 5)
    bc.add_transaction("Budi", "Citra", 2.5)
    blok = bc.mine_block()
    assert blok["index"] == 2
    assert blok["transactions"] == [
        {"sender": "Ani", "recipient": "Budi", "amount": 5},
        {"sender": "Budi", "recipient": "Citra", "amount": 2.5},
    ]
    assert bc.pending_transactions == []
    assert blok["previous_hash"] == bc.hash(bc.chain[0])


def test_transaksi_blok_tidak_ikut_berubah_saat_pending_baru(bc):
    bc.add_transaction("Ani", "Budi", 5)
    blok = bc.mine_block()
    bc.add_transaction("Citra", "Dodi", 1)
    assert len(blok["transactions"]) == 1


def test_riwayat(bc):
    bc.add_transaction("Ani", "Budi", 5)
    bc.mine_block()
    bc.add_transaction("Budi", "Citra", 2)
    bc.add_transaction("Citra", "Dodi", 1)
    bc.mine_block()
    bc.add_transaction("Budi", "Eka", 9)  # masih pending -> tidak masuk riwayat
    r = bc.riwayat("Budi")
    assert r == [
        (2, {"sender": "Ani", "recipient": "Budi", "amount": 5}),
        (3, {"sender": "Budi", "recipient": "Citra", "amount": 2}),
    ]
    assert bc.riwayat("Zaki") == []
