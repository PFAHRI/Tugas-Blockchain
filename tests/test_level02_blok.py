import hashlib
import json

import pytest

from level02_blok import Blockchain


@pytest.fixture
def bc():
    return Blockchain(difficulty=3)


def test_hash_blok(bc):
    blok = bc.chain[0]
    harapan = hashlib.sha256(json.dumps(blok, sort_keys=True).encode()).hexdigest()
    assert bc.hash(blok) == harapan


def _lolos(p, prev=1, d=3):
    return hashlib.sha256(str(p**2 - prev**2).encode()).hexdigest().startswith("0" * d)


def test_valid_proof(bc):
    benar = next(p for p in range(1, 10**6) if _lolos(p))
    salah = next(p for p in range(1, 10**6) if not _lolos(p))
    assert bc.valid_proof(1, benar) is True
    assert bc.valid_proof(1, salah) is False


def test_proof_of_work_mencari_proof_terkecil(bc):
    p = bc.proof_of_work(1)
    assert bc.valid_proof(1, p)
    assert all(not bc.valid_proof(1, q) for q in range(1, p))


def test_mine_block_menyambung_rantai(bc):
    assert len(bc.chain) == 1 and bc.chain[0]["previous_hash"] == "0"  # genesis
    b2 = bc.mine_block()
    b3 = bc.mine_block()
    assert len(bc.chain) == 3
    assert b2["index"] == 2 and b3["index"] == 3
    assert b2["previous_hash"] == bc.hash(bc.chain[0])
    assert b3["previous_hash"] == bc.hash(bc.chain[1])
    assert bc.valid_proof(bc.chain[0]["proof"], b2["proof"])


def test_chain_valid_true(bc):
    for _ in range(3):
        bc.mine_block()
    assert bc.chain_valid(bc.chain) is True


def test_chain_valid_mendeteksi_previous_hash_salah(bc):
    for _ in range(3):
        bc.mine_block()
    bc.chain[2]["previous_hash"] = "abc"
    assert bc.chain_valid(bc.chain) is False


def test_chain_valid_mendeteksi_proof_salah(bc):
    for _ in range(2):
        bc.mine_block()
    # ubah proof blok terakhir menjadi tidak valid (tautan hash tetap utuh)
    p = bc.chain[-1]["proof"] + 1
    while bc.valid_proof(bc.chain[-2]["proof"], p):
        p += 1
    bc.chain[-1]["proof"] = p
    assert bc.chain_valid(bc.chain) is False


def test_difficulty_dipakai():
    bc4 = Blockchain(difficulty=4)
    p = bc4.proof_of_work(1)
    assert hashlib.sha256(str(p**2 - 1).encode()).hexdigest().startswith("0000")
