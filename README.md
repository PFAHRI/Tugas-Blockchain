# Latihan Python: Memahami Blockchain dari Nol

Paket latihan untuk mata kuliah **Teknologi Blockchain**. Latihan ini dikembangkan dari artikel
[Create simple Blockchain using Python (GeeksforGeeks)](https://www.geeksforgeeks.org/python/create-simple-blockchain-using-python/).
Artikel itu dikembangkan menjadi 9 level, mulai dari fungsi hash sampai mata uang kripto sederhana.

Setiap level berisi file Python dengan bagian `# TODO` yang harus Anda lengkapi. Pekerjaan Anda
diperiksa oleh **tes otomatis**, jadi Anda langsung tahu apakah jawaban sudah benar.

---

## 1. Persiapan

Butuh **Python 3.8 atau lebih baru**.

```bash
# (disarankan) buat virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## 2. Struktur folder

```
blockchain-latihan/
├── latihan/                 <- KERJAKAN DI SINI
│   ├── level01_hash.py
│   ├── ...
│   ├── level09_reward_saldo.py
│   └── level08_server.py    <- demo Flask (sudah lengkap, tidak perlu diubah)
├── tests/                   <- tes otomatis (JANGAN diubah)
├── tugas_personal/          <- tugas personal 1: Level 1–5 dengan data diri (lihat PETUNJUK.md)
├── tugas_personal_2/        <- tugas personal 2: Level 6–9 dengan data diri (lihat PETUNJUK.md)
├── jawaban_refleksi.md      <- jawaban pertanyaan refleksi Anda
├── cek_nilai.py             <- skrip pengecek
└── requirements.txt
```

## 3. Cara mengerjakan

1. Buka file level, misalnya `latihan/level01_hash.py`.
2. Baca docstring di awal file (tujuan belajar) dan docstring setiap fungsi (spesifikasi).
3. Ganti setiap baris `raise NotImplementedError(...)` dengan kode Anda. Baris `# Petunjuk:` membantu Anda.
4. Cek pekerjaan Anda:

```bash
python cek_nilai.py 1        # cek level 1 dan lihat detail kegagalan
python cek_nilai.py          # ringkasan semua level
```

5. Jalankan file level secara langsung untuk melihat demonya, misalnya `python latihan/level03_tampering.py`.
6. Jawab pertanyaan refleksi di `jawaban_refleksi.md`.

> **Aturan:** jangan mengubah folder `tests/`, nama fungsi, atau parameter fungsi.
> Tes memanggil fungsi dengan nama persis seperti di file latihan.

Kerjakan **berurutan**. Setiap file bisa dites sendiri, tetapi konsep di setiap level dibangun di atas level sebelumnya.

---

## 4. Peta level

| Level | File | Konsep | Kaitan dengan artikel GfG |
|---|---|---|---|
| 1 | `level01_hash.py` | SHA-256, deterministik, efek avalanche, serialisasi kanonik | Dasar "fingerprinting" |
| 2 | `level02_blok.py` | Struktur blok, rantai hash, Proof of Work, validasi | Kode GfG tanpa Flask |
| 3 | `level03_tampering.py` | Memalsukan data, mendeteksi tautan putus | Menemukan **kelemahan** PoW GfG |
| 4 | `level04_transaksi.py` | Mempool, transaksi, validasi input | Blok GfG belum berisi data |
| 5 | `level05_pow_nonce.py` | Nonce, hash seluruh blok, immutability | **Memperbaiki** kelemahan di Level 3 |
| 6 | `level06_difficulty.py` | Difficulty, probabilitas, difficulty adjustment | `'00000'` di GfG ditulis langsung (hard-coded) |
| 7 | `level07_tanda_tangan.py` | Kunci privat/publik, alamat, ECDSA SECP256k1 | Tidak ada di GfG |
| 8 | `level08_jaringan.py` | Peer, broadcast, fork, konsensus rantai terpanjang | GfG hanya satu node |
| 9 | `level09_reward_saldo.py` | Coinbase, saldo, total suplai, double spending | Menuju cryptocurrency |

---

## 5. Pertanyaan refleksi

Tulis jawaban Anda di `jawaban_refleksi.md`. Jawab dengan kalimat Anda sendiri, dan sertakan
hasil percobaan (output program) jika diminta.

**Level 1**
1. Mengapa hash disebut "sidik jari digital"? Sebutkan tiga sifat fungsi hash kriptografis.
2. Berapa persen bit yang berubah ketika Anda mengganti satu huruf? Coba 3 pasangan teks berbeda.
3. Apa yang terjadi jika `hash_dict` **tidak** memakai `sort_keys=True`? Mengapa itu berbahaya untuk blockchain?

**Level 2**
1. Apa fungsi `previous_hash` pada blok genesis, dan mengapa nilainya `"0"`?
2. Jalankan demo dengan difficulty 3, 4, dan 5. Catat nilai `proof` dan rasakan lamanya mining.

**Level 3**
1. Saat Anda mengubah data di blok posisi *k*, `cari_tautan_putus` melaporkan posisi *k+1*. Jelaskan mengapa.
2. Mengapa perubahan pada **blok terakhir** tidak terdeteksi oleh `cari_tautan_putus`?
3. Setelah `sambung_ulang`, rantai palsu dianggap valid. Apa kelemahan desain PoW di artikel GfG yang menyebabkannya?

**Level 4**
1. Mengapa transaksi tidak langsung masuk ke blok, tetapi menunggu dulu di `pending_transactions`?
2. Mengapa `create_block` harus memakai salinan `list(self.pending_transactions)`? Apa bug yang muncul jika tidak?

**Level 5**
1. Bandingkan Level 3 dan Level 5: mengapa serangan "sambung ulang" gagal di sini?
2. Jalankan demo. Berapa percobaan hash yang dibutuhkan penyerang untuk memalsukan blok #1 dari 3 blok?
   Perkirakan biayanya jika rantai berisi 1.000 blok dan difficulty 6.

**Level 6**
1. Tampilkan tabel hasil eksperimen (difficulty 1–5). Apakah hasilnya mendekati 16^d? Mengapa 16?
2. Bitcoin menyesuaikan difficulty setiap 2.016 blok agar waktu blok sekitar 10 menit.
   Mengapa waktu blok perlu dijaga stabil?

**Level 7**
1. Apa perbedaan peran kunci privat, kunci publik, dan alamat?
2. Pada tes `test_mencuri_atas_nama_orang_lain`, tanda tangan penipu valid tetapi transaksinya tidak sah. Jelaskan.
3. Apa yang terjadi jika kunci privat Anda hilang? Bagaimana jika dicuri?

**Level 8**
1. Gambarkan (boleh dengan teks/ASCII) kondisi fork pada demo, lalu kondisi setelah `resolve_conflicts`.
2. Apa yang terjadi pada transaksi `fork-B` setelah konsensus? Kaitkan dengan anjuran "tunggu 6 konfirmasi" di Bitcoin.
3. (Praktik) Jalankan `level08_server.py` di 3 port dan uji alurnya. Lampirkan output-nya.

**Level 9**
1. Dari mana koin pertama berasal jika semua orang memulai dengan saldo 0?
2. Mengapa `validasi_ekonomi` diperlukan walaupun `chain_valid` (validasi hash) sudah ada?
3. Bitcoin memakai model UTXO, bukan model saldo akun seperti di sini. Cari tahu satu perbedaannya.

---

## 6. Tugas personal

Folder `tugas_personal/` berisi tugas memodifikasi Level 1–5 dengan data diri Anda (nama, 4 digit
terakhir NIM, tanggal lahir, kota asal, hobi). Hasil setiap mahasiswa berbeda dan diverifikasi
otomatis oleh dosen. Baca `tugas_personal/PETUNJUK.md`.

Setelah Level 6–9 selesai, kerjakan tugas lanjutannya di folder `tugas_personal_2/`: modifikasi
difficulty, kunci dan tanda tangan, jaringan node, serta halving hadiah mining dengan data diri Anda.
Baca `tugas_personal_2/PETUNJUK.md`.

## 7. Tantangan lanjutan (opsional, nilai tambah)

- Gabungkan Level 7 dan Level 9: `add_transaction` hanya menerima transaksi yang ditandatangani dengan benar.
- Hitung **Merkle root** dari transaksi dan simpan di header blok.
- Tambahkan endpoint `/transactions/new` dan `/mine` ke `level08_server.py`, plus siaran blok otomatis ke peer.
- Simpan blockchain ke file JSON agar tidak hilang saat program dihentikan.
- Ganti Proof of Work dengan Proof of Stake sederhana, lalu bandingkan keduanya.
