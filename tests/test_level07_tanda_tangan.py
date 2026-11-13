import hashlib
import json

import pytest

import level07_tanda_tangan as m


@pytest.fixture
def ani():
    priv, pub = m.buat_pasangan_kunci()
    return priv, pub, m.alamat_dari_kunci_publik(pub)


def test_format_kunci(ani):
    priv, pub, alamat = ani
    assert len(priv) == 64 and len(pub) == 128  # 32 byte & 64 byte dalam hex
    int(priv, 16); int(pub, 16)


def test_kunci_selalu_baru():
    assert m.buat_pasangan_kunci()[0] != m.buat_pasangan_kunci()[0]


def test_alamat(ani):
    _, pub, alamat = ani
    assert alamat == hashlib.sha256(bytes.fromhex(pub)).hexdigest()[:40]
    assert len(alamat) == 40


def test_pesan_transaksi_kanonik():
    tx1 = {"amount": 5, "recipient": "b", "sender": "a", "signature": "abc"}
    tx2 = {"sender": "a", "recipient": "b", "amount": 5}
    assert m.pesan_transaksi(tx1) == m.pesan_transaksi(tx2)
    assert m.pesan_transaksi(tx2) == json.dumps(tx2, sort_keys=True).encode()


def test_tanda_tangan_valid(ani):
    priv, pub, alamat = ani
    tx = {"sender": alamat, "recipient": "budi", "amount": 5}
    sig = m.tanda_tangani(tx, priv)
    assert isinstance(sig, str)
    assert m.verifikasi(tx, sig, pub) is True


def test_transaksi_diubah_tidak_valid(ani):
    priv, pub, alamat = ani
    tx = {"sender": alamat, "recipient": "budi", "amount": 5}
    sig = m.tanda_tangani(tx, priv)
    for field, nilai in [("amount", 500), ("recipient", "penipu")]:
        palsu = dict(tx, **{field: nilai})
        assert m.verifikasi(palsu, sig, pub) is False


def test_kunci_publik_lain_tidak_valid(ani):
    priv, pub, alamat = ani
    _, pub_lain = m.buat_pasangan_kunci()
    tx = {"sender": alamat, "recipient": "budi", "amount": 5}
    sig = m.tanda_tangani(tx, priv)
    assert m.verifikasi(tx, sig, pub_lain) is False


def test_tanda_tangan_rusak_tidak_melempar_exception(ani):
    _, pub, alamat = ani
    tx = {"sender": alamat, "recipient": "budi", "amount": 5}
    assert m.verifikasi(tx, "00" * 64, pub) is False
    assert m.verifikasi(tx, "bukan-hex", pub) is False


def test_transaksi_sah(ani):
    priv, pub, alamat = ani
    tx = {"sender": alamat, "recipient": "budi", "amount": 5}
    sig = m.tanda_tangani(tx, priv)
    assert m.transaksi_sah(tx, sig, pub) is True


def test_mencuri_atas_nama_orang_lain(ani):
    """Penipu menandatangani dengan kuncinya sendiri tetapi memakai alamat Ani sebagai sender."""
    _, _, alamat_ani = ani
    priv_penipu, pub_penipu = m.buat_pasangan_kunci()
    tx = {"sender": alamat_ani, "recipient": "penipu", "amount": 100}
    sig = m.tanda_tangani(tx, priv_penipu)
    assert m.verifikasi(tx, sig, pub_penipu) is True   # tanda tangannya sendiri valid...
    assert m.transaksi_sah(tx, sig, pub_penipu) is False  # ...tetapi bukan pemilik alamat
