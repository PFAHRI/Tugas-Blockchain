import hashlib

import pytest

import level06_difficulty as m


@pytest.mark.parametrize("d", [1, 2, 3])
def test_tambang(d):
    nonce, h, percobaan = m.tambang("data-uji", d)
    assert h == hashlib.sha256(f"data-uji{nonce}".encode()).hexdigest()
    assert h.startswith("0" * d)
    assert percobaan == nonce + 1
    # nonce harus yang terkecil
    for n in range(nonce):
        assert not hashlib.sha256(f"data-uji{n}".encode()).hexdigest().startswith("0" * d)


def test_ekspektasi_percobaan():
    assert m.ekspektasi_percobaan(1) == 16
    assert m.ekspektasi_percobaan(3) == 4096


def test_ukur_mining_format():
    r = m.ukur_mining(2, n=3)
    assert set(r) == {"difficulty", "rata_percobaan", "rata_detik"}
    assert r["difficulty"] == 2
    assert r["rata_percobaan"] >= 1 and r["rata_detik"] >= 0


def test_mining_lebih_sulit_jika_difficulty_naik():
    mudah = m.ukur_mining(1, n=10)["rata_percobaan"]
    sulit = m.ukur_mining(3, n=10)["rata_percobaan"]
    assert sulit > mudah * 10


@pytest.mark.parametrize("sekarang,aktual,target,harapan", [
    (4, 1.0, 10.0, 5),   # terlalu cepat -> naik
    (4, 30.0, 10.0, 3),  # terlalu lambat -> turun
    (4, 8.0, 10.0, 4),   # wajar -> tetap
    (1, 99.0, 10.0, 1),  # tidak boleh di bawah 1
    (4, 5.0, 10.0, 4),   # tepat setengah -> tetap
    (4, 20.0, 10.0, 4),  # tepat dua kali -> tetap
])
def test_sesuaikan_difficulty(sekarang, aktual, target, harapan):
    assert m.sesuaikan_difficulty(sekarang, aktual, target) == harapan


def test_eksperimen():
    hasil = m.eksperimen((1, 2), n=2)
    assert [h["difficulty"] for h in hasil] == [1, 2]
