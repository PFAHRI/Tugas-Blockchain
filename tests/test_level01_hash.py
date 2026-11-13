import hashlib

import level01_hash as m


def test_sha256_hex_sesuai_hashlib():
    for teks in ["", "blockchain", "Universitas Muhammadiyah Sorong", "émoji ✓"]:
        assert m.sha256_hex(teks) == hashlib.sha256(teks.encode("utf-8")).hexdigest()


def test_sha256_hex_panjang_64_dan_deterministik():
    h = m.sha256_hex("abc")
    assert isinstance(h, str) and len(h) == 64
    assert m.sha256_hex("abc") == h


def test_hash_dict_tidak_bergantung_urutan_key():
    a = {"index": 1, "proof": 7, "previous_hash": "0"}
    b = {"previous_hash": "0", "proof": 7, "index": 1}
    assert m.hash_dict(a) == m.hash_dict(b)


def test_hash_dict_berubah_jika_isi_berubah():
    assert m.hash_dict({"x": 1}) != m.hash_dict({"x": 2})


def test_hash_dict_format_kanonik():
    # Harus sama persis dengan json.dumps(..., sort_keys=True) agar kompatibel dengan level lain
    assert m.hash_dict({"b": 2, "a": 1}) == hashlib.sha256(b'{"a": 1, "b": 2}').hexdigest()


def test_bit_berbeda_kasus_ekstrem():
    assert m.bit_berbeda("0" * 64, "0" * 64) == 0
    assert m.bit_berbeda("0" * 64, "f" * 64) == 256
    assert m.bit_berbeda("0" * 63 + "1", "0" * 64) == 1


def test_efek_avalanche():
    p = m.persen_bit_berbeda("Teknologi Blockchain", "teknologi Blockchain")
    assert 30 <= p <= 70, "Perubahan 1 karakter seharusnya mengubah sekitar 50% bit"
