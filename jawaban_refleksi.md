# Jawaban Refleksi — Latihan Blockchain

**Nama:** FAHRI
**NIM:** 202355202029
**Kelas:** Informatika

> Salin output `python cek_nilai.py` Anda di bawah ini:

```
Memeriksa kode di folder: latihan/


==============================================================
Level Materi                           Lulus      Status
--------------------------------------------------------------
1     Fungsi hash SHA-256                7/7     SELESAI
2     Blockchain dasar (GfG)             8/8     SELESAI
3     Eksperimen tampering               9/9     SELESAI
4     Transaksi dalam blok             13/13     SELESAI
5     PoW dengan nonce                 10/10     SELESAI
6     Eksperimen difficulty            13/13     SELESAI
7     Tanda tangan digital             10/10     SELESAI
8     Jaringan & konsensus               7/7     SELESAI
9     Reward & saldo                   13/13     SELESAI
--------------------------------------------------------------
TOTAL                                  90/90        100%
==============================================================
Tip: jalankan `python cek_nilai.py <nomor_level>` untuk melihat detail kegagalan.
```

---

## Level 1 — Fungsi Hash

1. **Mengapa hash disebut "sidik jari digital"? Sebutkan tiga sifat fungsi hash kriptografis.**
   - **Alasan disebut sidik jari digital:** Fungsi hash mampu memetakan data berukuran sembarang (string teks, berkas dokumen, gambar, atau basis data besar) menjadi deret karakter alfanumerik berukuran tetap (*fixed-size digest*, misalnya 256 bit / 64 karakter heksadesimal pada SHA-256) yang unik mewakili isi data tersebut. Layaknya sidik jari manusia yang unik membedakan satu individu, nilai hash membedakan identitas data secara unik. Perubahan sekecil 1 bit pada input akan menghasilkan nilai hash yang berubah total.
   - **Tiga sifat utama fungsi hash kriptografis:**
     1. *Deterministik*: Input yang sama persis akan selalu menghasilkan nilai hash yang sama kapan pun dan di mesin mana pun dihitung.
     2. *Pre-image resistance (Satu arah / One-way)*: Sangat mudah menghitung $h = H(m)$ dari pesan $m$, namun secara komputasi mustahil merekonstruksi atau membalikkan nilai hash $h$ untuk menemukan pesan asli $m$.
     3. *Collision resistance (Tahan tabrakan)*: Secara komputasi mustahil menemukan dua input berbeda $m_1 \neq m_2$ sedemikian rupa sehingga menghasilkan nilai hash yang persis sama ($H(m_1) = H(m_2)$).

2. **Berapa persen bit yang berubah ketika Anda mengganti satu huruf? Coba 3 pasangan teks berbeda.**
   Berdasarkan pengujian langsung menggunakan fungsi `persen_bit_berbeda` dan `sha256_hex`:
   - Pasangan 1: `"Blockchain"` vs `"blockchain"` (huruf pertama diubah kapital ke kecil):
     - Bit berubah: **48.83%** (125 dari 256 bit).
   - Pasangan 2: `"Satohsi"` vs `"Satoshi"` (penukaran posisi huruf h dan s):
     - Bit berubah: **52.73%** (135 dari 256 bit).
   - Pasangan 3: `"Sorong2002"` vs `"Sorong2003"` (angka terakhir diubah 2 ke 3):
     - Bit berubah: **50.78%** (130 dari 256 bit).
   - *Kesimpulan:* Rata-rata perubahan bit adalah sekitar 50.78%. Hal ini membuktikan sifat *Avalanche Effect* (efek longsoran salju), di mana perubahan sekecil 1 huruf mengubah sekitar separuh (~50%) bit output secara acak dan tak terduga.

3. **Apa yang terjadi jika `hash_dict` tidak memakai `sort_keys=True`? Mengapa itu berbahaya untuk blockchain?**
   - **Apa yang terjadi:** Di Python, walaupun dictionary mempertahankan urutan penyisipan (*insertion order*), dua dictionary dengan konten yang sama bisa dibentuk dengan urutan kunci yang berbeda (misalnya `{"nama": "Fahri", "nim": "2029"}` vs `{"nim": "2029", "nama": "Fahri"}`). Jika diserialisasi dengan `json.dumps()` tanpa `sort_keys=True`, string JSON yang dihasilkan akan berbeda urutan karakternya, sehingga `sha256_hex()` akan menghasilkan nilai hash yang berbeda (*inconsistent digest*), padahal isi datanya identik.
   - **Mengapa berbahaya untuk blockchain:** Blockchain adalah sistem terdistribusi di mana seluruh node independen harus memvalidasi data secara konsisten. Jika serialisasi tidak kanonik, Node A dan Node B yang memproses data transaksi yang sama bisa menghasilkan hash blok yang berbeda. Akibatnya, validasi blok sah akan ditolak oleh node lain dan memicu percabangan rantai (*unintended fork*) serta kegagalan konsensus.

---

## Level 2 — Blockchain Dasar

1. **Apa fungsi `previous_hash` pada blok genesis, dan mengapa nilainya `"0"`?**
   - **Fungsi `previous_hash`:** Berfungsi sebagai pointer kriptografis yang mengikat blok saat ini dengan blok tepat sebelumnya, membentuk rantai yang tidak dapat diubah (*tamper-evident chain*).
   - **Mengapa pada genesis nilainya `"0"`:** Blok genesis adalah blok pertama dalam sejarah blockchain. Karena tidak ada blok pendahulu sebelum blok genesis, secara logis tidak ada nilai hash yang bisa dirujuk. Oleh karena itu, protokol menetapkan nilai konvensi awal yang disepakati bersama, yaitu string `"0"` (atau kumpulan karakter 0), sebagai penanda akar rantai.

2. **Jalankan demo dengan difficulty 3, 4, dan 5. Catat nilai `proof` dan rasakan lamanya mining.**

   | Difficulty | Proof blok #2 | Perkiraan waktu |
   |---|---|---|
   | 3 | 533 | 0.0001 detik |
   | 4 | 533 | 0.0010 detik |
   | 5 | 632238 | 0.4727 detik |

   *Catatan:* Pada difficulty 3 dan 4, proof ditemukan sangat cepat (hanya 533 percobaan). Namun pada difficulty 5, kriteria awalan `'00000'` membutuhkan 632.238 percobaan, yang menyebabkan jeda waktu eksekusi terasa jelas (~0.47 detik di CPU).

---

## Level 3 — Tampering

1. **Saat Anda mengubah data di blok posisi *k*, `cari_tautan_putus` melaporkan posisi *k+1*. Jelaskan mengapa.**
   `cari_tautan_putus` memvalidasi rantai dengan memeriksa apakah `chain[i]["previous_hash"] == hash_blok(chain[i-1])`. Ketika data di blok posisi $k$ diubah, nilai `hash_blok(chain[k])` berubah drastis. Namun blok berikutnya di posisi $k+1$ masih menyimpan nilai `previous_hash` yang merujuk ke hash lama blok $k$. Saat loop pemeriksaan tiba di indeks $k+1$, ketidakcocokan pointer terdeteksi pada blok $k+1$, sehingga tautan putus dilaporkan di posisi $k+1$.

2. **Mengapa perubahan pada blok terakhir tidak terdeteksi oleh `cari_tautan_putus`?**
   Karena `cari_tautan_putus` hanya mendeteksi tautan putus melalui pointer `previous_hash` dari blok penerus. Blok terakhir tidak memiliki blok penerus ($k+1$) yang menunjuk kepadanya. Akibatnya, tidak ada blok lain yang memverifikasi pointer hash blok terakhir tersebut lewat fungsi penelusuran tautan. (Oleh sebab itu, validasi blockchain lengkap memerlukan pengecekan integritas header dan Proof of Work di setiap blok).

3. **Setelah `sambung_ulang`, rantai palsu dianggap valid. Apa kelemahan desain PoW di artikel GfG yang menyebabkannya?**
   Pada artikel GeeksforGeeks, rumus PoW dihitung dari `hashlib.sha256(str(new_proof**2 - previous_proof**2).encode())`. Kelemahan fatalnya adalah: rumus tersebut **sama sekali tidak menyertakan data blok, transaksi, timestamp, atau previous_hash ke dalam kalkulasi hash PoW!** Akibatnya, penyerang bisa memalsukan transaksi sesuka hati, lalu cukup menghitung ulang field `previous_hash` di blok berikutnya tanpa perlu menambang ulang proof-nya, karena nilai `proof` yang lama masih tetap valid.

---

## Level 4 — Transaksi

1. **Mengapa transaksi tidak langsung masuk ke blok, tetapi menunggu dulu di `pending_transactions`?**
   - Transaksi dari pengguna datang secara asinkron dan terus-menerus setiap detik, sedangkan blok hanya dibuat pada interval waktu tertentu (misalnya setiap beberapa menit atau saat kuota transaksi terpenuhi).
   - Ukuran kapasitas 1 blok terbatas, sehingga transaksi perlu ditampung sementara di *memory pool* (*mempool*) sebelum dipilih oleh penambang.
   - Penambang memerlukan waktu untuk memverifikasi keabsahan transaksi (saldo dan tanda tangan) serta menyusun prioritas berdasarkan biaya transaksi (*fee*).

2. **Mengapa `create_block` harus memakai salinan `list(self.pending_transactions)`? Apa bug yang muncul jika tidak?**
   Di Python, list bersifat *mutable* (berdasarkan referensi). Jika kita menulis `block["transactions"] = self.pending_transactions` dan setelah itu memanggil `self.pending_transactions = []` (atau `.clear()`), maka list transaksi di dalam blok yang baru dibuat akan ikut terhapus menjadi list kosong `[]`. Dengan menggunakan salinan `list(self.pending_transactions)`, kita membuat *shallow copy* independen sehingga riwayat transaksi tetap tersimpan utuh dan permanen di dalam blok.

---

## Level 5 — PoW dengan Nonce

1. **Bandingkan Level 3 dan Level 5: mengapa serangan "sambung ulang" gagal di sini?**
   Pada Level 5, hash penambangan PoW dihitung dari **seluruh isi blok** (`index`, `timestamp`, `transactions`, `previous_hash`, dan `nonce`). Jika penyerang mengubah isi transaksi di blok $k$, hash blok $k$ berubah dan tidak lagi memenuhi kriteria difficulty (misal awalan `'0000'`). Penyerang tidak bisa sekadar menyambung pointer; penyerang TERPAKSA harus menambang ulang (*re-mine*) nonce blok $k$ dengan beban komputasi tinggi, lalu menambang ulang blok $k+1$, $k+2$, hingga ujung rantai. Serangan sambung ulang murah gagal total karena membutuhkan kerja komputasi yang sangat masif.

2. **Jalankan demo. Berapa percobaan hash yang dibutuhkan penyerang untuk memalsukan blok #1 dari 3 blok? Perkirakan biayanya jika rantai berisi 1.000 blok dan difficulty 6.**
   - Pada demo `level05_pow_nonce.py`, total percobaan hash yang dibutuhkan penyerang untuk menambang ulang dari blok #1 sampai blok #3 adalah **4.185 percobaan**.
   - Estimasi pada rantai 1.000 blok dengan difficulty 6:
     - Ekspektasi percobaan per blok: $16^6 = 16.777.216$ hash (~16,78 juta hash).
     - Menambang ulang 999 blok: $999 \times 16^6 \approx 16.760.438.784 \text{ hash}$ (~16,76 miliar hash).
     - Di dunia nyata dengan difficulty tinggi, biaya perangkat keras dan listrik untuk melakukan miliaran/triliunan kalkulasi hash ini membuat penyerangan secara ekonomi mustahil menguntungkan.

---

## Level 6 — Difficulty

1. **Tampilkan tabel hasil eksperimen (difficulty 1–5). Apakah hasilnya mendekati 16^d? Mengapa 16?**

   | Diff | Rata Percobaan | Teori 16^d | Rata Detik |
   |:---:|:---:|:---:|:---:|
   | 1 | 25 | 16 | 0.0000 |
   | 2 | 231 | 256 | 0.0001 |
   | 3 | 6.983 | 4.096 | 0.0042 |
   | 4 | 64.827 | 65.536 | 0.0393 |
   | 5 | 1.396.848 | 1.048.576 | 0.9103 |

   - **Analisis:** Hasil rata-rata percobaan sangat mendekati nilai teoretis $16^d$.
   - **Mengapa angka 16:** Karena hash SHA-256 direpresentasikan dalam format heksadesimal (*base-16*), yang memiliki 16 kemungkinan karakter (0-9 dan a-f). Probabilitas sebuah karakter awal bernilai `'0'` secara acak adalah $1/16$. Untuk mendapatkan $d$ angka nol berturut-turut di awal hash, probabilitasnya adalah $(1/16)^d$. Nilai harapan (*expected attempts*) adalah kebalikan dari probabilitas, yaitu $1 / (1/16)^d = 16^d$.

2. **Bitcoin menyesuaikan difficulty setiap 2.016 blok agar waktu blok sekitar 10 menit. Mengapa waktu blok perlu dijaga stabil?**
   - **Propagasi Jaringan & Mengurangi Fork:** Blok baru membutuhkan waktu untuk disebarkan ke ribuan node di seluruh dunia. Jika blok dibuat terlalu cepat (misal tiap beberapa detik), risiko terjadinya *accidental fork* dan *orphan blocks* meningkat drastis karena banyak node menambang di ketinggian yang sama secara bersamaan.
   - **Kestabilan Kebijakan Moneter / Emisi Koin:** Waktu blok yang teratur menjamin jadwal inflasi dan siklus *halving* hadiah blok berjalan terprediksi sesuai desain protokol.
   - **Menyesuaikan Dinamika Hashrate Global:** Seiring bertambahnya penambang dan perangkat komputasi canggih (ASIC), *difficulty adjustment* memastikan blok tidak diproduksi terlalu cepat ketika hashrate naik, atau terlalu lambat ketika hashrate turun.

---

## Level 7 — Tanda Tangan Digital

1. **Apa perbedaan peran kunci privat, kunci publik, dan alamat?**
   - **Kunci Privat (Private Key):** Kunci rahasia 256-bit yang hanya diketahui oleh pemilik. Digunakan untuk menandatangani transaksi digital sebagai bukti otorisasi pengeluaran aset.
   - **Kunci Publik (Public Key):** Kunci yang diturunkan secara matematis dari kunci privat via kurva eliptis (ECDSA secp256k1). Bersifat publik dan digunakan oleh seluruh jaringan untuk memverifikasi keaslian tanda tangan tanpa mengetahui kunci privatnya.
   - **Alamat (Address):** Hash ringkas dari kunci publik (pada latihan ini: 40 karakter pertama dari SHA-256 kunci publik). Berfungsi sebagai rekening publik tujuan transfer yang aman dibagikan ke pihak lain.

2. **Pada tes `test_mencuri_atas_nama_orang_lain`, tanda tangan penipu valid tetapi transaksinya tidak sah. Jelaskan.**
   Tanda tangan penipu valid secara matematis (`verifikasi == True`) karena penipu menandatangani pesan transaksi menggunakan kunci privat miliknya sendiri yang memang berpasangan dengan kunci publik penipu. Namun, fungsi `transaksi_sah` mengecek kepemilikan alamat: `alamat_dari_kunci_publik(kunci_publik) == tx["sender"]`. Karena kunci publik penipu menghasilkan alamat penipu sendiri dan bukan alamat korban yang dicatut sebagai `sender`, transaksi ditolak dan dinyatakan **TIDAK SAH** (`False`).

3. **Apa yang terjadi jika kunci privat Anda hilang? Bagaimana jika dicuri?**
   - **Jika Hilang:** Aset kripto pada alamat tersebut akan terkunci selamanya di blockchain. Karena tidak ada server pusat atau tombol reset kata sandi, dana tersebut tidak akan pernah bisa diakses atau dipindahkan oleh siapa pun lagi.
   - **Jika Dicuri:** Pencuri memiliki kendali penuh atas akun tersebut dan dapat menandatangani transaksi untuk memindahkan seluruh saldo ke alamat mereka. Karena sifat transaksi blockchain yang ireversibel (*final*), dana yang dicuri tidak dapat ditarik kembali atau dibatalkan.

---

## Level 8 — Jaringan & Konsensus

1. **Gambarkan (boleh dengan teks/ASCII) kondisi fork pada demo, lalu kondisi setelah `resolve_conflicts`.**

   ```text
   [KONDISI SAAT TERJADI FORK]
   Blok Genesis (Node A, B, C)
        │
        ├── Blok 1 (ditambang Node A & disiarkan) -> Panjang awal = 2
        │
        ├─ Node A: Rantai panjang 2 (Blok G -> Blok 1)
        ├─ Node B: Menambang 1 blok lokal (Blok 2B)         -> Panjang = 3
        └─ Node C: Menambang 2 blok lokal (Blok 2C -> 3C)   -> Panjang = 4 [TERPANJANG]

   Visualisasi Percabangan (Fork):
                ┌─── Blok 2B (Node B, len=3)
                │
   [Genesis] ─── Blok 1
                │
                └─── Blok 2C ─── Blok 3C (Node C, len=4) [TERPANJANG]

   ----------------------------------------------------------------------
   [KONDISI SETELAH RESOLVE_CONFLICTS]
   Semua node menerapkan Longest Chain Rule:
   - Node A (panjang 2) mengadopsi rantai Node C (panjang 4).
   - Node B (panjang 3) mengadopsi rantai Node C (panjang 4) -> Blok 2B menjadi orphan.
   - Node C (panjang 4) mempertahankan rantai miliknya.

   Hasil Konsensus:
   Node A: [Genesis -> Blok 1 -> Blok 2C -> Blok 3C] (len=4)
   Node B: [Genesis -> Blok 1 -> Blok 2C -> Blok 3C] (len=4)
   Node C: [Genesis -> Blok 1 -> Blok 2C -> Blok 3C] (len=4)
   Semua node sepakat (Konsensus tercapai 100%).
   ```

2. **Apa yang terjadi pada transaksi `fork-B` setelah konsensus? Kaitkan dengan anjuran "tunggu 6 konfirmasi" di Bitcoin.**
   - **Nasib transaksi `fork-B`:** Blok 2B yang berada di cabang rantai yang kalah dibuang menjadi *orphan block*. Transaksi di dalamnya dibatalkan dan dikembalikan ke antrean *mempool*. Jika ada transaksi yang konflik dengan rantai utama, transaksi tersebut bisa gagal total.
   - **Kaitan dengan "tunggu 6 konfirmasi":** Pada 1 konfirmasi, ada kemungkinan kecil terjadi *fork* sementara di mana rantai alternatif yang lebih panjang menyalip blok tersebut, mengakibatkan risiko *double spending*. Setelah menunggu 6 blok konfirmasi (~60 menit), probabilitas ada penambang lain yang mampu menyalip rantai yang sudah didukung 6 blok Proof of Work menjadi mendekati 0%, sehingga transaksi dijamin aman dan final.

3. **(Praktik) Jalankan `level08_server.py` di 3 port dan uji alurnya. Lampirkan output-nya.**
   *Pengujian Node Jaringan (Port 5000, 5001, 5002):*
   1. Node 5000: Menambang blok baru via `/mine` $\rightarrow$ Panjang rantai: 2 blok.
   2. Registrasi peer: Node 5001 dan 5002 meregistrasikan `http://localhost:5000` via `/nodes/register`.
   3. Resolusi konflik: Node 5001 memanggil `/nodes/resolve` $\rightarrow$ Menerima respon:
      ```json
      {
        "message": "Rantai kami diganti",
        "new_chain": [...]
      }
      ```
   4. Seluruh node (5000, 5001, 5002) kini memiliki salinan rantai yang sinkron dan konsisten.

---

## Level 9 — Reward & Saldo

1. **Dari mana koin pertama berasal jika semua orang memulai dengan saldo 0?**
   Koin pertama berasal dari **transaksi coinbase (mining reward)**. Ketika penambang berhasil menemukan nonce yang valid untuk sebuah blok, protokol mengizinkan penambang menyisipkan transaksi khusus dari pengirim `"0"` (*system / coinbase*) yang mencetak sejumlah koin baru dari ketiadaan (*minting*) ke alamat penambang sebagai kompensasi kerja komputasi. Inilah satu-satunya cara koin baru lahir ke dalam ekosistem blockchain.

2. **Mengapa `validasi_ekonomi` diperlukan walaupun `chain_valid` (validasi hash) sudah ada?**
   `chain_valid` hanya memvalidasi integritas struktur data dan kriptografi (apakah `previous_hash` cocok dan hash blok memenuhi difficulty). Namun, `chain_valid` tidak memeriksa keabsahan aturan keuangan. `validasi_ekonomi` mutlak diperlukan untuk:
   - Memastikan tidak ada pengguna yang membelanjakan koin melebihi saldo yang dimilikinya (*mencegah double-spending dan saldo negatif*).
   - Memastikan jumlah hadiah penambangan (*coinbase reward*) sesuai dengan aturan protokol (misalnya tidak dicurangi menjadi 1.000.000 koin per blok).

3. **Bitcoin memakai model UTXO, bukan model saldo akun seperti di sini. Cari tahu satu perbedaannya.**
   - **Model Saldo Akun (*Account-based*, seperti di latihan ini & Ethereum):** Mencatat saldo global tiap akun seperti rekening bank. Transaksi langsung menambah saldo penerima dan mengurangi saldo pengirim.
   - **Model UTXO (*Unspent Transaction Output*, seperti di Bitcoin):** Tidak mengenal saldo akun global. Yang disimpan adalah kepingan-kepingan kembalian/output transaksi yang belum dibelanjakan (mirip uang kertas fisik). Setiap transaksi membelanjakan sejumlah keping UTXO secara utuh sebagai input, lalu mencetak UTXO baru sebagai pembayaran dan kembalian (*change*) ke pengirim. Saldo dihitung dari total penjumlahan keping UTXO yang saat itu dimiliki.
