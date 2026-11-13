import pytest

from level04_transaksi import Blockchain


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
