import copy

import pytest

from level08_jaringan import Node


@pytest.fixture
def tiga_node():
    a, b, c = Node("A"), Node("B"), Node("C")
    return a, b, c


def test_hubungkan_dua_arah_tanpa_duplikat(tiga_node):
    a, b, c = tiga_node
    a.hubungkan(b)
    a.hubungkan(b)
    b.hubungkan(a)
    a.hubungkan(a)
    assert a.peers == [b] and b.peers == [a]
    a.hubungkan(c)
    assert a.peers == [b, c] and c.peers == [a]


def test_terima_blok_valid(tiga_node):
    a, b, _ = tiga_node
    blok = a.tambang_blok(["tx1"])
    assert b.terima_blok(blok) is True
    assert b.chain == a.chain
    assert b.chain[-1] is not blok, "simpan salinan, bukan objek yang sama"


def test_terima_blok_ditolak(tiga_node):
    a, b, _ = tiga_node
    blok = a.tambang_blok(["tx1"])
    palsu = copy.deepcopy(blok)
    palsu["transactions"] = ["tx PALSU"]
    assert b.terima_blok(palsu) is False
    blok2 = a.tambang_blok(["tx2"])  # tidak bisa langsung menerima blok #2 tanpa blok #1
    assert b.terima_blok(blok2) is False
    assert len(b.chain) == 1


def test_siarkan_blok(tiga_node):
    a, b, c = tiga_node
    a.hubungkan(b)
    a.hubungkan(c)
    assert a.chain == b.chain == c.chain  # genesis semua node sama
    blok = a.tambang_blok(["tx1"])
    assert a.siarkan_blok(blok) == 2
    assert a.chain == b.chain == c.chain
    assert a.siarkan_blok(blok) == 0  # sudah punya, tidak diterima lagi


def test_resolve_conflicts_pilih_terpanjang(tiga_node):
    a, b, c = tiga_node
    a.hubungkan(b)
    a.hubungkan(c)
    b.tambang_blok(["b1"])
    c.tambang_blok(["c1"])
    c.tambang_blok(["c2"])
    assert a.resolve_conflicts() is True
    assert a.chain == c.chain
    assert a.chain is not c.chain
    assert a.resolve_conflicts() is False  # sudah terpanjang


def test_resolve_conflicts_tolak_rantai_tidak_valid(tiga_node):
    a, b, _ = tiga_node
    a.hubungkan(b)
    for i in range(3):
        b.tambang_blok([f"b{i}"])
    b.chain[2]["transactions"] = ["PALSU"]  # rantai B panjang tapi rusak
    assert a.resolve_conflicts() is False
    assert len(a.chain) == 1


def test_fork_lalu_sepakat(tiga_node):
    a, b, c = tiga_node
    a.hubungkan(b); b.hubungkan(c); a.hubungkan(c)
    a.tambang_dan_siarkan(["tx1"])
    b.tambang_blok(["fork-B"])
    c.tambang_blok(["fork-C1"])
    c.tambang_blok(["fork-C2"])
    for n in (a, b, c):
        n.resolve_conflicts()
    assert a.chain == b.chain == c.chain
    assert len(a.chain) == 4
    assert all("fork-B" not in blok["transactions"] for blok in b.chain)
