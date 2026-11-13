"""
LEVEL 7 — Kunci Publik/Privat dan Tanda Tangan Digital (LATIHAN)
======================================================================

Di level sebelumnya siapa pun bisa menulis transaksi atas nama orang lain.
Sekarang setiap transaksi harus ditandatangani dengan kunci privat pengirim.
Kurva yang dipakai: SECP256k1 (kurva yang sama dengan Bitcoin dan Ethereum).

Butuh library:  pip install ecdsa

Tujuan belajar:
  * Pasangan kunci privat/publik dan alamat (address).
  * Menandatangani dan memverifikasi transaksi.
  * Mengapa transaksi yang diubah setelah ditandatangani menjadi tidak sah.

Jalankan tes:  python cek_nilai.py 7
"""

import hashlib
import json

from ecdsa import BadSignatureError, SECP256k1, SigningKey, VerifyingKey


def buat_pasangan_kunci():
    """Buat kunci SECP256k1 baru. Kembalikan (kunci_privat_hex, kunci_publik_hex).
    Petunjuk: SigningKey.generate(curve=SECP256k1), .to_string().hex(), .get_verifying_key()
    """
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()
    return sk.to_string().hex(), vk.to_string().hex()


def alamat_dari_kunci_publik(kunci_publik_hex: str) -> str:
    """Alamat = 40 karakter pertama dari SHA-256(bytes kunci publik)."""
    pub_bytes = bytes.fromhex(kunci_publik_hex)
    return hashlib.sha256(pub_bytes).hexdigest()[:40]


def pesan_transaksi(tx: dict) -> bytes:
    """Bytes kanonik yang ditandatangani: JSON (sort_keys=True) dari HANYA key
    'sender', 'recipient', 'amount' (key lain seperti 'signature' diabaikan).
    """
    data = {
        "sender": tx["sender"],
        "recipient": tx["recipient"],
        "amount": tx["amount"],
    }
    return json.dumps(data, sort_keys=True).encode()


def tanda_tangani(tx: dict, kunci_privat_hex: str) -> str:
    """Tandatangani pesan_transaksi(tx). Kembalikan tanda tangan dalam hex."""
    sk = SigningKey.from_string(bytes.fromhex(kunci_privat_hex), curve=SECP256k1)
    pesan = pesan_transaksi(tx)
    sig = sk.sign(pesan)
    return sig.hex()


def verifikasi(tx: dict, tanda_tangan_hex: str, kunci_publik_hex: str) -> bool:
    """True jika tanda tangan cocok dengan transaksi dan kunci publik.
    Kembalikan False (jangan melempar exception) jika tidak cocok / format salah.
    """
    try:
        vk = VerifyingKey.from_string(bytes.fromhex(kunci_publik_hex), curve=SECP256k1)
        sig_bytes = bytes.fromhex(tanda_tangan_hex)
        pesan = pesan_transaksi(tx)
        return vk.verify(sig_bytes, pesan)
    except (BadSignatureError, ValueError, Exception):
        return False


def transaksi_sah(tx: dict, tanda_tangan_hex: str, kunci_publik_hex: str) -> bool:
    """Transaksi sah jika (1) tanda tangan valid DAN
    (2) tx['sender'] sama dengan alamat dari kunci publik tersebut.
    """
    if tx.get("sender") != alamat_dari_kunci_publik(kunci_publik_hex):
        return False
    return verifikasi(tx, tanda_tangan_hex, kunci_publik_hex)


if __name__ == "__main__":
    priv, pub = buat_pasangan_kunci()
    alamat = alamat_dari_kunci_publik(pub)
    tx = {"sender": alamat, "recipient": "alamat_budi", "amount": 5}
    sig = tanda_tangani(tx, priv)
    print("Alamat Ani :", alamat)
    print("Tanda tangan:", sig[:32], "...")
    print("Sah?", transaksi_sah(tx, sig, pub))
    tx["amount"] = 500
    print("Setelah amount diubah jadi 500, sah?", transaksi_sah(tx, sig, pub))
