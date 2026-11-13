import copy

import pytest

from level03_tampering import Blockchain, cari_tautan_putus, hash_blok, sambung_ulang, ubah_blok


@pytest.fixture
def bc():
    b = Blockchain(difficulty=3)
    for d in ["Ani -> Budi: 5", "Budi -> Citra: 2", "Citra -> Dodi: 1", "Dodi -> Eka: 3"]:
        b.mine_block(d)
    return b


def test_ubah_blok_tidak_mengubah_asli(bc):
    asli = copy.deepcopy(bc.chain)
    palsu = ubah_blok(bc.chain, 1, "data", "Ani -> Budi: 500")
    assert bc.chain == asli, "Rantai asli tidak boleh ikut berubah (pakai deepcopy)"
    assert palsu[1]["data"] == "Ani -> Budi: 500"
    assert palsu[2] == asli[2]


def test_rantai_palsu_tidak_valid(bc):
    palsu = ubah_blok(bc.chain, 2, "data", "PALSU")
    assert bc.chain_valid(palsu) is False


def test_cari_tautan_putus_none_jika_utuh(bc):
    assert cari_tautan_putus(bc.chain) is None


@pytest.mark.parametrize("posisi", [1, 2, 3])
def test_cari_tautan_putus_menunjuk_blok_sesudahnya(bc, posisi):
    palsu = ubah_blok(bc.chain, posisi, "data", "PALSU")
    assert cari_tautan_putus(palsu) == posisi + 1


def test_mengubah_blok_terakhir_tidak_terdeteksi_tautan(bc):
    # Blok terakhir tidak punya "penerus", jadi tautannya tidak bisa putus
    palsu = ubah_blok(bc.chain, len(bc.chain) - 1, "data", "PALSU")
    assert cari_tautan_putus(palsu) is None


def test_sambung_ulang_memperbaiki_semua_tautan(bc):
    palsu = ubah_blok(bc.chain, 1, "data", "PALSU")
    baru = sambung_ulang(palsu, 2)
    assert cari_tautan_putus(baru) is None
    for i in range(1, len(baru)):
        assert baru[i]["previous_hash"] == hash_blok(baru[i - 1])
    # proof tidak berubah
    assert [b["proof"] for b in baru] == [b["proof"] for b in bc.chain]
    # tidak mengubah input
    assert palsu[2]["previous_hash"] == bc.chain[2]["previous_hash"]


def test_kelemahan_pow_gfg(bc):
    """Inti pelajaran: setelah disambung ulang, rantai palsu dianggap VALID."""
    palsu = sambung_ulang(ubah_blok(bc.chain, 1, "data", "Ani -> Budi: 500"), 2)
    assert bc.chain_valid(palsu) is True
