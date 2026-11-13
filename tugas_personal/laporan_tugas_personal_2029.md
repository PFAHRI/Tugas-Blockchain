# Laporan Tugas Personal Blockchain Level 1–5

- **Nama:** FAHRI
- **NIM (4 digit terakhir):** 2029
- **Dibuat:** 2026-11-14 01:33  (waktu proses 2.3 detik)
- **Kode verifikasi:** `183FC3734CFD`

> Bagian hasil dibuat otomatis. Jangan diubah: dosen menghitung ulang semua angka dari data Anda.
> Isi bagian **Analisis** dengan kata-kata Anda sendiri.

## Level 1 — Hash data pribadi

| Hasil | Nilai |
|---|---|
| SHA-256 nama | `529ffff646bfe73ef57f9284ece7ea76001ace28f7db67c01742463865950f88` |
| hash_dict profil | `bb663c2e9785a131a448060e761f8572274968c3ef84045302c7c0f97c73d467` |
| hash_dict profil (urutan key dibalik) | `bb663c2e9785a131a448060e761f8572274968c3ef84045302c7c0f97c73d467` |
| Bit berubah: tanggal lahir vs tanggal lahir + 1 hari | 45.7% |
| ID mahasiswa (Modifikasi 1) | `8073b46e` |

## Level 2 — Blockchain personal

- Proof genesis: **2029** (dari NIM)
- Proof blok 2, 3, 4: **3905, 99820, 37541**
- Pemilik setiap blok: `8073b46e`
- Rantai valid: True

## Level 3 — Pemalsuan data pribadi

- Posisi yang dipalsukan: **2**
- Data asli: `FAHRI berasal dari Sorong`
- Data palsu: `FAHRI berasal dari Sorong (DIPALSUKAN)`
- Valid sebelum dipalsukan: True
- Tautan putus di indeks: **3**
- Valid setelah dipalsukan: **False**
- Valid setelah disambung ulang: **True**

## Level 4 — Transaksi dari data pribadi

| Blok | Pengirim | Penerima | Jumlah |
|---|---|---|---|
| 2 | FAHRI | TEMAN_A | 3 |
| 2 | TEMAN_A | FAHRI | 9 |
| 3 | FAHRI | DOSEN | 30 |

- Ringkasan saldo (Modifikasi 4): masuk **9**, keluar **33**, bersih **-24**
- Kirim ke diri sendiri ditolak: True
- Amount 0 ditolak: True

## Level 5 — Proof of Work dengan nonce (deterministik)

| Blok | Nonce | Hash |
|---|---|---|
| 0 | 28130 | `000072742a765dc461b3d224…` |
| 1 | 50177 | `00005f322a5794b9b8520f1f…` |
| 2 | 139572 | `0000fb9b46d853f2c03eaa0d…` |
| 3 | 101492 | `0000d90a6433495bc4b99eef…` |

- Valid: True → setelah blok 1 dipalsukan: **False**
- Percobaan hash untuk menambang ulang blok 1–3: **314.812**
- Valid setelah ditambang ulang: True

## Analisis (isi dengan kata-kata Anda sendiri)

1. **Level 1.** Bandingkan SHA-256 nama Anda dengan milik seorang teman. Apakah ada pola yang mirip? Jelaskan juga mengapa dua hash profil Anda sama, dan mengapa hanya menambah 1 hari pada tanggal lahir mengubah 45.7% bit.

   _Jawaban:_
   - **Perbandingan dengan milik teman:** Nilai SHA-256 nama saya (`529ffff646bfe73ef57f9284ece7ea76001ace28f7db67c01742463865950f88`) sama sekali tidak memiliki kesamaan atau pola kemiripan dengan nama teman, meskipun misalnya sama-sama berawalan huruf atau memiliki panjang karakter yang berdekatan. Fungsi SHA-256 menghasilkan output yang tersebar merata (*uniform distribution*) secara acak semu (*pseudorandom*), sehingga tidak ada relasi visual antara kemiripan teks asli dengan hasil hash-nya.
   - **Dua hash profil bernilai sama:** Nilai hash profil normal dan profil dengan urutan key dibalik menghasilkan nilai heksadesimal yang identik (`bb663c2e9785...`) karena fungsi `hash_dict` menggunakan serialisasi kanonik `json.dumps(data, sort_keys=True)`. Sebelum dilakukan encoding string ke dalam byte dan dihitung nilai SHA-256-nya, seluruh key diurutkan secara alfabetis terlebih dahulu. Dengan demikian, urutan penulisan field dalam dictionary Python tidak mengubah representasi string JSON yang dihasilkan.
   - **Perubahan 1 hari mengubah 45.7% bit:** Karakteristik ini merupakan bukti nyata dari *Avalanche Effect* (efek longsoran salju) pada fungsi hash kriptografis. Walaupun input hanya diubah 1 karakter (tanggal lahir bergeser 1 hari), struktur kompresi blok internal SHA-256 mengacak seluruh status register komputasi di setiap putaran (*round*), sehingga sekitar 45.7% (mendekati probabilitas teoretis 50%) dari seluruh 256 bit digest berubah drastis.

2. **Level 2.** Kode Anda dan teman sama persis, tetapi proof Anda (3905, 99820, 37541) berbeda. Jelaskan penyebabnya.

   _Jawaban:_
   - Perbedaan deret proof ini berakar dari **proof blok genesis** yang dipersonalisasi menggunakan 4 digit terakhir NIM masing-masing mahasiswa. Pada blockchain saya, proof genesis dimulai dari angka `2029` (dari NIM 202355202029), sedangkan mahasiswa lain memiliki nilai awal yang berbeda.
   - Algoritma Proof of Work pada Level 2 mencari bilangan bulat `proof` baru sedemikian rupa sehingga `(proof**2 - previous_proof**2)` menghasilkan hash dengan awalan nol yang memenuhi kriteria *difficulty*. Karena `previous_proof` untuk blok kedua diambil dari proof genesis saya (`2029`), nilai `proof` blok kedua yang lolos kriteria adalah `3905`.
   - Selanjutnya, blok ketiga menggunakan `3905` sebagai dasar perhitungannya dan menghasilkan `99820`, kemudian blok keempat menghasilkan `37541`. Karena adanya ketergantungan berantai (*cascading dependency*) terhadap nilai seed awal blok genesis, seluruh angka proof blok berikutnya menjadi unik dan spesifik untuk setiap mahasiswa.

3. **Level 3.** Anda memalsukan posisi 2 dan tautan putus terdeteksi di indeks 3, sedangkan valid setelah dipalsukan = False. Jelaskan hasil ini, lalu bandingkan dengan teman yang posisi pemalsuannya berbeda.

   _Jawaban:_
   - **Penyebab terdeteksi di indeks 3:** Posisi pemalsuan dihitung dari formula `1 + int(nim4) % 4`. Untuk NIM `2029`, sisa baginya adalah `2029 % 4 = 1`, sehingga posisi yang dipalsukan adalah indeks `1 + 1 = 2` (blok data asal kota). Ketika data blok indeks 2 dimanipulasi dengan menambahkan teks `(DIPALSUKAN)`, hash blok 2 berubah total. Blok penerusnya (indeks 3) masih menyimpan `previous_hash` yang menunjuk ke hash lama blok 2. Saat validasi memeriksa blok 3, terjadi ketidakcocokan pointer (`chain[3]['previous_hash'] != hash_blok(chain[2])`), sehingga sistem mendeteksi kerusakan tautan tepat di posisi 3 dan status validitas rantai menjadi `False`.
   - **Perbandingan dengan teman:** Teman dengan sisa bagi NIM yang berbeda memalsukan blok pada posisi lain (posisi 1, 3, atau 4). Jika teman memalsukan blok indeks 1, maka tautan putus terdeteksi di indeks 2. Khusus teman yang memalsukan blok indeks 4 (blok terakhir), fungsi `cari_tautan_putus` tidak akan mendeteksi kerusakan tautan karena tidak ada blok indeks 5 yang memegang pointer hash ke blok tersebut.
   - **Kelemahan PoW GfG:** Setelah dieksekusi `sambung_ulang`, status rantai palsu kembali menjadi `True`. Hal ini membuktikan bahwa algoritma PoW ala GeeksforGeeks memiliki kelemahan mendasar: PoW-nya tidak mengikat data transaksi atau pointer hash, sehingga penyerang dapat memalsukan isi blok dan menyambung ulang hash pointer tanpa perlu menambang ulang proof-nya.

4. **Level 4.** Jelaskan dari mana angka masuk 9, keluar 33, dan bersih -24 berasal. Mengapa transaksi ke diri sendiri perlu ditolak?

   _Jawaban:_
   - **Asal Usul Angka Saldo:**
     1. Transaksi 1: `FAHRI` mengirim ke `TEMAN_A` sebesar tanggal lahir saya (tanggal 3 September), yaitu **3** koin $\rightarrow$ keluar 3 koin.
     2. Transaksi 2: `TEMAN_A` mengirim ke `FAHRI` sebesar bulan lahir saya (bulan 9 / September), yaitu **9** koin $\rightarrow$ masuk 9 koin.
     3. Transaksi 3: `FAHRI` mengirim ke `DOSEN` sebesar `(int(nim4) % 50) + 1` = `(2029 % 50) + 1` = `29 + 1` = **30** koin $\rightarrow$ keluar 30 koin.
     - **Total Masuk:** 9 koin.
     - **Total Keluar:** $3 + 30 = 33$ koin.
     - **Saldo Bersih:** $9 - 33 = -24$ koin (saldo mengalami defisit pada simulasi pencatatan sederhana Level 4).
   - **Alasan Transaksi ke Diri Sendiri Harus Ditolak:**
     1. *Mencegah Spam Buku Besar:* Transaksi ke diri sendiri tidak mengubah saldo bersih maupun kepemilikan aset, tetapi tetap mengonsumsi kapasitas blok (*block space*) dan membebani seluruh node penyimpan riwayat transaksi.
     2. *Mencegah Manipulasi Volume (Wash Trading):* Aktor jahat dapat memanfaatkan transaksi berulang ke dirinya sendiri untuk menciptakan volume perdagangan fiktif demi memanipulasi persepsi pasar.
     3. *Efisiensi Komputasi Jaringan:* Menghilangkan beban validasi CPU yang tidak menghasilkan dampak ekonomi riil.

5. **Level 5.** Penyerang butuh 314.812 percobaan hash untuk memalsukan rantai Anda. Mengapa nonce Anda selalu sama setiap kali program dijalankan, padahal di demo Level 5 asli nonce berubah-ubah?

   _Jawaban:_
   - Pada simulasi Tugas Personal Modifikasi 5, proses penambangan Proof of Work dijalankan secara **deterministik**: iterasi pencarian nonce selalu dimulai dari angka tetap `nonce = 0` dan bertambah secara sekuensial satu per satu (`nonce += 1`). Selain itu, seluruh isi komponen blok (timestamp yang dibekukan/deterministik, data transaksi, dan previous_hash) bernilai identik di setiap eksekusi. Karena fungsi hash SHA-256 bersifat deterministik murni, angka nonce pertama yang menghasilkan hash dengan awalan empat nol (`0000`) akan selalu jatuh pada iterasi yang persis sama di setiap penjalanan program.
   - Sebaliknya, pada implementasi demo Level 5 asli di artikel referensi, timestamp blok diambil secara dinamis dari waktu riil sistem (`time.time()`) atau urutan transaksi diacak, sehingga data input blok selalu berubah dan nilai nonce yang ditemukan menjadi berbeda-beda di setiap uji coba.

6. **Etika data.** Anda baru saja menyimpan nama dan tanggal lahir di dalam blockchain. Jika ini blockchain publik, apa risikonya? Kaitkan dengan sifat immutability dan UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi, terutama hak untuk menghapus data.

   _Jawaban:_
   - **Risiko Menyimpan Data Pribadi di Blockchain Publik:**
     Blockchain publik bersifat terbuka dan dapat dibaca oleh siapa saja di seluruh dunia (*transparent ledger*). Menyimpan informasi identitas pribadi (Personally Identifiable Information / PII) seperti nama lengkap, NIM, dan tanggal lahir secara mentah (*plaintext*) membuka celah pencurian identitas, profiling tanpa izin, manipulasi kredensial perbankan, dan serangan rekayasa sosial (*social engineering*).
   - **Benturan Sifat Immutability dengan UU No. 27 Tahun 2022 (UU PDP):**
     Karakteristik fundamental blockchain adalah *immutability* (data yang sudah tertulis di dalam blok tidak dapat diubah, disunting, atau dihapus). Hal ini bertentangan secara langsung dengan Pasal 43 dan Pasal 44 UU PDP yang menjamin **Hak Subjek Data Pribadi untuk Menghapus dan/atau Memusnahkan Data Pribadi miliknya** (*Right to Erasure / Right to be Forgotten*).
   - **Solusi Arsitektur yang Benar:**
     Dalam perancangan sistem informasi modern berbasis blockchain, data pribadi sensitif tidak boleh disimpan langsung di rantai utama (*on-chain*). Arsitektur yang patuh hukum adalah menyimpan data mentah di database terenkripsi *off-chain*, sedangkan blockchain hanya menyimpan nilai hash kriptografis atau bukti *Zero-Knowledge Proof* (ZKP) sebagai verifikasi keaslian tanpa membuka data rahasia.

---

## Data verifikasi (JANGAN DIUBAH)

<!-- DATA-VERIFIKASI -->
```json
{
  "profil": {
    "nama": "FAHRI",
    "nim4": "2029",
    "tanggal_lahir": "2002-09-03",
    "kota_asal": "Sorong",
    "hobi": "Coding"
  },
  "level1": {
    "hash_nama": "529ffff646bfe73ef57f9284ece7ea76001ace28f7db67c01742463865950f88",
    "hash_profil": "bb663c2e9785a131a448060e761f8572274968c3ef84045302c7c0f97c73d467",
    "hash_profil_urutan_terbalik": "bb663c2e9785a131a448060e761f8572274968c3ef84045302c7c0f97c73d467",
    "avalanche_tanggal_persen": 45.7,
    "id_mahasiswa": "8073b46e"
  },
  "level2": {
    "proof_genesis": 2029,
    "proof_blok": [
      3905,
      99820,
      37541
    ],
    "pemilik_semua_blok": [
      "8073b46e"
    ],
    "valid": true
  },
  "level3": {
    "posisi_dipalsukan": 2,
    "data_asli": "FAHRI berasal dari Sorong",
    "data_palsu": "FAHRI berasal dari Sorong (DIPALSUKAN)",
    "valid_asli": true,
    "tautan_putus_di": 3,
    "valid_setelah_dipalsukan": false,
    "valid_setelah_disambung_ulang": true
  },
  "level4": {
    "riwayat": [
      [
        2,
        {
          "sender": "FAHRI",
          "recipient": "TEMAN_A",
          "amount": 3
        }
      ],
      [
        2,
        {
          "sender": "TEMAN_A",
          "recipient": "FAHRI",
          "amount": 9
        }
      ],
      [
        3,
        {
          "sender": "FAHRI",
          "recipient": "DOSEN",
          "amount": 30
        }
      ]
    ],
    "ringkasan_saldo": {
      "masuk": 9,
      "keluar": 33,
      "bersih": -24
    },
    "kirim_ke_diri_sendiri_ditolak": true,
    "amount_nol_ditolak": true,
    "jumlah_blok": 3
  },
  "level5": {
    "nonce": [
      28130,
      50177,
      139572,
      101492
    ],
    "hash": [
      "000072742a765dc461b3d224b4c46ef7f3c1de3dbe02f5190fece6cff333d829",
      "00005f322a5794b9b8520f1fb9cacec9f2cabc7a4b79acbe19df892ed5ed0f0c",
      "0000fb9b46d853f2c03eaa0d9c3601a9fd8ba5b1863c6d4c8af8c594119d3eba",
      "0000d90a6433495bc4b99eefbc586de78de458abe435245920c455a6a916e457"
    ],
    "valid": true,
    "valid_setelah_dipalsukan": false,
    "percobaan_tambang_ulang": 314812,
    "valid_setelah_tambang_ulang": true
  },
  "kode_verifikasi": "183FC3734CFD"
}
```
