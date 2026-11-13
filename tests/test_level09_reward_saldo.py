import pytest

from level09_reward_saldo import MINING_REWARD, SISTEM, Blockchain


@pytest.fixture
def bc():
    return Blockchain(difficulty=2)


def test_saldo_awal_nol(bc):
    assert bc.saldo("ani") == 0


def test_mine_memberi_hadiah(bc):
    blok = bc.mine("ani")
    assert blok["transactions"][0] == {"sender": SISTEM, "recipient": "ani", "amount": MINING_REWARD}
    assert blok["index"] == 1 and blok["previous_hash"] == bc.chain[0]["hash"]
    assert blok["hash"].startswith("00") and blok["hash"] == Blockchain.hash_block(blok)
    assert bc.saldo("ani") == MINING_REWARD


def test_transfer_dan_saldo(bc):
    bc.mine("ani")
    bc.add_transaction("ani", "budi", 4)
    assert bc.saldo("ani") == 6
    assert bc.saldo("ani", termasuk_pending=False) == 10
    assert bc.saldo("budi", termasuk_pending=False) == 0
    blok = bc.mine("citra")
    assert blok["transactions"][1] == {"sender": "ani", "recipient": "budi", "amount": 4}
    assert bc.pending_transactions == []
    assert (bc.saldo("ani"), bc.saldo("budi"), bc.saldo("citra")) == (6, 4, 10)


def test_saldo_tidak_cukup(bc):
    bc.mine("ani")
    with pytest.raises(ValueError):
        bc.add_transaction("budi", "ani", 1)
    with pytest.raises(ValueError):
        bc.add_transaction("ani", "budi", 11)


def test_double_spending_di_mempool(bc):
    bc.mine("ani")
    bc.add_transaction("ani", "budi", 7)
    with pytest.raises(ValueError):
        bc.add_transaction("ani", "citra", 7)  # sisa saldo hanya 3


def test_tidak_boleh_mencetak_koin(bc):
    with pytest.raises(ValueError):
        bc.add_transaction(SISTEM, "ani", 1000)


def test_amount_harus_positif(bc):
    bc.mine("ani")
    for nilai in (0, -5):
        with pytest.raises(ValueError):
            bc.add_transaction("ani", "budi", nilai)


def test_total_suplai(bc):
    assert bc.total_suplai() == 0
    bc.mine("ani"); bc.mine("budi")
    bc.add_transaction("ani", "budi", 3)
    bc.mine("ani")
    assert bc.total_suplai() == 3 * MINING_REWARD


def test_validasi_ekonomi_benar(bc):
    bc.mine("ani")
    bc.add_transaction("ani", "budi", 4)
    bc.mine("budi")
    assert bc.validasi_ekonomi() is True


def test_validasi_ekonomi_hadiah_berlebih(bc):
    bc.mine("ani")
    bc.chain[1]["transactions"][0]["amount"] = 1000
    assert bc.validasi_ekonomi() is False


def test_validasi_ekonomi_coinbase_ganda(bc):
    bc.mine("ani")
    bc.chain[1]["transactions"].append({"sender": SISTEM, "recipient": "ani", "amount": 10})
    assert bc.validasi_ekonomi() is False


def test_validasi_ekonomi_tanpa_coinbase(bc):
    bc.mine("ani")
    bc.chain[1]["transactions"] = []
    assert bc.validasi_ekonomi() is False


def test_validasi_ekonomi_saldo_negatif(bc):
    bc.mine("ani")
    # sisipkan transaksi yang melewati validasi add_transaction
    bc.chain[1]["transactions"].append({"sender": "budi", "recipient": "ani", "amount": 50})
    assert bc.validasi_ekonomi() is False
