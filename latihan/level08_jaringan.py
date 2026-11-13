"""
LEVEL 8 — Jaringan Banyak Node dan Konsensus "Rantai Terpanjang" (LATIHAN)
===============================================================================

Artikel GfG hanya punya satu node. Blockchain sesungguhnya terdiri dari
banyak node yang saling bertukar blok. Di sini jaringan disimulasikan di dalam
satu proses Python (objek Node saling memanggil), agar mudah dites.
Versi HTTP sungguhan dengan Flask ada di level08_server.py (demo).

Tujuan belajar:
  * Peer, siaran (broadcast) blok, dan validasi blok yang diterima.
  * Aturan konsensus: rantai VALID terpanjang yang menang.
  * Fork dan cara jaringan kembali sepakat.

Jalankan tes:  python cek_nilai.py 8
"""

import copy
import hashlib
import json

GENESIS_HASH_PREV = "0" * 64


class Node:
    # ====================== SUDAH DISEDIAKAN ======================
    def __init__(self, nama: str, difficulty: int = 2):
        self.nama = nama
        self.difficulty = difficulty
        self.peers = []  # list objek Node lain
        # Genesis dibuat DETERMINISTIK (tanpa timestamp) agar semua node punya genesis yang sama
        genesis = {"index": 0, "transactions": [], "previous_hash": GENESIS_HASH_PREV,
                   "nonce": 0, "miner": "genesis"}
        self._tambang(genesis)
        self.chain = [genesis]

    @staticmethod
    def hash_block(block):
        isi = {k: v for k, v in block.items() if k != "hash"}
        return hashlib.sha256(json.dumps(isi, sort_keys=True).encode()).hexdigest()

    def _tambang(self, block):
        block["nonce"] = 0
        while not self.hash_block(block).startswith("0" * self.difficulty):
            block["nonce"] += 1
        block["hash"] = self.hash_block(block)
        return block

    def blok_valid(self, block, blok_sebelumnya) -> bool:
        """Cek satu blok terhadap blok sebelumnya."""
        return (
            block.get("hash") == self.hash_block(block)
            and block["hash"].startswith("0" * self.difficulty)
            and block["previous_hash"] == blok_sebelumnya["hash"]
            and block["index"] == blok_sebelumnya["index"] + 1
        )

    def rantai_valid(self, chain) -> bool:
        if not chain or chain[0] != self.chain[0]:  # genesis harus sama
            return False
        return all(self.blok_valid(chain[i], chain[i - 1]) for i in range(1, len(chain)))

    def tambang_blok(self, transactions) -> dict:
        """Tambang blok baru di atas rantai sendiri (TANPA menyiarkan)."""
        last = self.chain[-1]
        block = {"index": last["index"] + 1, "transactions": transactions,
                 "previous_hash": last["hash"], "nonce": 0, "miner": self.nama}
        self._tambang(block)
        self.chain.append(block)
        return block

    def tambang_dan_siarkan(self, transactions) -> dict:
        block = self.tambang_blok(transactions)
        self.siarkan_blok(block)
        return block

    # ============ BAGIAN YANG DIKERJAKAN (isi semua TODO) ============
    def hubungkan(self, node_lain: "Node") -> None:
        """Hubungkan dua node secara DUA ARAH. Jangan menambahkan peer ganda,
        dan jangan menghubungkan node dengan dirinya sendiri.
        """
        if node_lain is self:
            return
        if node_lain not in self.peers:
            self.peers.append(node_lain)
        if self not in node_lain.peers:
            node_lain.peers.append(self)

    def terima_blok(self, block: dict) -> bool:
        """Terima blok dari peer. Jika blok valid sebagai kelanjutan blok terakhir
        rantai kita (pakai blok_valid), tambahkan SALINANNYA dan kembalikan True.
        Selain itu kembalikan False (rantai tidak berubah).
        """
        if self.blok_valid(block, self.chain[-1]):
            self.chain.append(copy.deepcopy(block))
            return True
        return False

    def siarkan_blok(self, block: dict) -> int:
        """Kirim blok ke semua peer (panggil peer.terima_blok).
        Kembalikan jumlah peer yang menerima blok tersebut.
        """
        diterima = 0
        for peer in self.peers:
            if peer.terima_blok(block):
                diterima += 1
        return diterima

    def resolve_conflicts(self) -> bool:
        """Aturan konsensus: periksa rantai semua peer. Jika ada rantai yang
        VALID dan LEBIH PANJANG dari rantai kita, ganti rantai kita dengan
        salinan (deepcopy) rantai valid terpanjang. Kembalikan True jika diganti.
        """
        rantai_terpanjang = None
        panjang_maks = len(self.chain)

        for peer in self.peers:
            if len(peer.chain) > panjang_maks and self.rantai_valid(peer.chain):
                panjang_maks = len(peer.chain)
                rantai_terpanjang = peer.chain

        if rantai_terpanjang is not None:
            self.chain = copy.deepcopy(rantai_terpanjang)
            return True
        return False


if __name__ == "__main__":
    a, b, c = Node("A"), Node("B"), Node("C")
    a.hubungkan(b); b.hubungkan(c); a.hubungkan(c)
    a.tambang_dan_siarkan(["tx1"])
    print("Panjang setelah A menambang & menyiarkan:", [len(n.chain) for n in (a, b, c)])

    # Fork: B dan C menambang bersamaan tanpa menyiarkan
    b.tambang_blok(["tx-B"])
    c.tambang_blok(["tx-C1"]); c.tambang_blok(["tx-C2"])
    print("Saat fork:", [len(n.chain) for n in (a, b, c)])
    for n in (a, b, c):
        n.resolve_conflicts()
    print("Setelah resolve_conflicts:", [len(n.chain) for n in (a, b, c)],
          "| semua sama?", a.chain == b.chain == c.chain)
