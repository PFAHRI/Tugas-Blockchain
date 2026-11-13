# Laporan Tugas Personal 2 — Blockchain Level 6–9

- **Nama:** FAHRI
- **NIM (4 digit terakhir):** 2029
- **Dibuat:** 2026-11-14 01:33  (waktu proses 0.1 detik)
- **Kode verifikasi:** `4E88B1255ECA`

> Bagian hasil dibuat otomatis. Jangan diubah: dosen menghitung ulang semua angka dari data Anda.
> Isi bagian **Analisis** dengan kata-kata Anda sendiri.

## Level 6 — Mining data pribadi dan jejak difficulty

Data yang ditambang: `FAHRI|2029|2002-09-03`

| Difficulty | Nonce | Percobaan | Teori 16^d | Hash |
|---|---|---|---|---|
| 1 | 0 | 1 | 16 | `0192f6336a588023bf90…` |
| 2 | 865 | 866 | 256 | `0036a0955587ecc1bfa3…` |
| 3 | 1719 | 1.720 | 4.096 | `000587d74a8ff360e5bb…` |
| 4 | 59980 | 59.981 | 65.536 | `00007129792e77de00c3…` |

- Difficulty awal (dari NIM): **2**, target waktu blok 10 detik
- Waktu blok simulasi (dari NIM + tanggal + bulan lahir): 8, 0, 8, 36, 0, 12, 0, 36 detik
- Jejak difficulty (Modifikasi 6): **2, 3, 3, 2, 3, 3, 4, 3**

## Level 7 — Kunci dan tanda tangan dari data pribadi

- Kunci publik (32 karakter awal): `bf6320ff3cffd98b2ea0b1e4b5bf00c2…`
- Alamat Anda: `8e7c53d75056f4f0ea005f7d48a0bb705bc73557`
- Transaksi: kirim **3** ke TEMAN_A
- Tanda tangan: `fcedfa1ea81522c279266c5374ab87a27d10c21a7d77a4ee…`
- Tanda tangan selalu sama saat diulang: True
- Transaksi sah: **True**; setelah amount diubah: **False**
- Penipu memakai alamat Anda: tanda tangannya valid dengan kuncinya = True, transaksinya sah = **False**

## Level 8 — Jaringan dan fork pribadi

- Jumlah node: **4**; blok pribadi tiap node: [3, 1, 3, 1]
- Panjang rantai saat fork: [5, 3, 5, 3]
- Setelah resolve_conflicts: [5, 5, 5, 5], sepakat = **False**
- Setelah blok pemecah seri: [6, 6, 6, 6], sepakat = **True**
- Pemenang fork: **FAHRI-1**; blok terbuang (orphan): **5**
- Hash ujung rantai: `0080557778cb57b8cf2bd394…`

## Level 9 — Ekonomi dengan halving

- Hadiah awal: **39**, halving setiap **3** blok
- Hadiah blok 1–6 (Modifikasi 9): **39, 39, 39, 19, 19, 19**

| Alamat | Saldo |
|---|---|
| FAHRI | 103.0 |
| TEMAN_A | 41.0 |
| TEMAN_B | 30.0 |

- Total suplai: **174.0**
- Belanja melebihi saldo ditolak: True
- Validasi ekonomi: **True**; setelah hadiah blok 1 dicurangi: **False**

## Analisis (isi dengan kata-kata Anda sendiri)

1. **Level 6.** Bandingkan kolom Percobaan dengan Teori 16^d pada tabel Anda. Mengapa bisa berbeda jauh? Lalu jelaskan jejak difficulty Anda (2, 3, 3, 2, 3, 3, 4, 3): pada langkah mana difficulty naik, tetap, dan turun, dan mengapa?

   _Jawaban:_
   - **Perbandingan Percobaan vs Teori $16^d$:**
     Nilai Teori $16^d$ adalah nilai ekspektasi rata-rata matematis dari distribusi geometrik proses penambangan berbasis fungsi hash SHA-256. Setiap digit heksadesimal memiliki 16 kemungkinan (0-f), sehingga peluang mendapatkan karakter '0' di depan adalah $(1/16)^d$. Pada penambangan blok tunggal secara individual, proses penemuan nonce adalah fenomena probabilistik murni:
     - Difficulty 1: Teori = 16, Percobaan = 1 (sangat beruntung, langsung menemukan hash berawalan '0' pada nonce pertama `0`).
     - Difficulty 2: Teori = 256, Percobaan = 866 (di atas rata-rata teoretis karena kombinasi data membutuhkan lebih banyak variasi nonce).
     - Difficulty 3: Teori = 4.096, Percobaan = 1.720 (lebih cepat dari ekspektasi rata-rata).
     - Difficulty 4: Teori = 65.536, Percobaan = 59.981 (sangat mendekati ekspektasi rata-rata teoretis).
     Jika dilakukan ribuan kali penambangan, nilai rata-rata empiris akan selalu konvergen menuju $16^d$.
   - **Jejak Difficulty (2, 3, 3, 2, 3, 3, 4, 3):**
     Aturan penyesuaian difficulty dengan target waktu blok 10 detik adalah:
     - Waktu aktual < 5 detik (target / 2) $\rightarrow$ Difficulty naik (+1) karena blok ditambang terlalu cepat.
     - Waktu aktual > 20 detik (target * 2) $\rightarrow$ Difficulty turun (-1) karena penambangan terlalu lambat.
     - Waktu aktual antara 5 hingga 20 detik $\rightarrow$ Difficulty tetap.
     Dengan deret waktu simulasi pribadi saya `[8, 0, 8, 36, 0, 12, 0, 36]` detik:
     1. Langkah 1 (waktu 8s): Di antara 5s dan 20s $\rightarrow$ **Tetap di 2**.
     2. Langkah 2 (waktu 0s): $0 < 5$s (terlalu cepat) $\rightarrow$ **Naik menjadi 3**.
     3. Langkah 3 (waktu 8s): Di antara 5s dan 20s $\rightarrow$ **Tetap di 3**.
     4. Langkah 4 (waktu 36s): $36 > 20$s (terlalu lambat) $\rightarrow$ **Turun menjadi 2**.
     5. Langkah 5 (waktu 0s): $0 < 5$s (terlalu cepat) $\rightarrow$ **Naik menjadi 3**.
     6. Langkah 6 (waktu 12s): Di antara 5s dan 20s $\rightarrow$ **Tetap di 3**.
     7. Langkah 7 (waktu 0s): $0 < 5$s (terlalu cepat) $\rightarrow$ **Naik menjadi 4**.
     8. Langkah 8 (waktu 36s): $36 > 20$s (terlalu lambat) $\rightarrow$ **Turun menjadi 3**.

2. **Level 7.** Mengapa tanda tangan Anda selalu sama setiap kali program dijalankan, padahal di Level 7 asli berubah-ubah? Mengapa transaksi penipu tidak sah walaupun tanda tangannya valid?

   _Jawaban:_
   - **Mengapa Tanda Tangan Selalu Sama:**
     Pada implementasi ECDSA standar di Level 7 asli, algoritma menggunakan generator bilangan acak sistem untuk memilih nilai rahasia sementara (*ephemeral key* $k$). Hal ini membuat tanda tangan selalu menghasilkan pasangan $(r, s)$ yang berbeda di setiap penjalanan. Namun pada Modifikasi 7, digunakan standar **RFC 6979** melalui fungsi `sign_deterministic`. Standar ini menurunkan nilai $k$ secara deterministik dari HMAC hash pesan transaksi dan kunci privat. Karena kunci privat dan data transaksi saya selalu sama di setiap eksekusi, nilai $k$ dan hasil tanda tangan digital heksadesimalnya selalu identik 100%.
   - **Mengapa Transaksi Penipu Tidak Sah:**
     Tanda tangan penipu secara matematis valid terhadap kunci publiknya sendiri (`verifikasi == True`) karena penipu memang menandatangani transaksi tersebut menggunakan kunci privat miliknya. Namun, fungsi konsensus `transaksi_sah` menerapkan verifikasi kepemilikan alamat:
     `alamat_dari_kunci_publik(kunci_publik) == tx["sender"]`
     Penipu mencantumkan alamat saya di kolom `sender`, tetapi menggunakan kunci publik miliknya. Karena penurunan kunci publik penipu menghasilkan alamat penipu dan bukan alamat saya yang tertera pada `sender`, transaksi ditolak sebagai **TIDAK SAH** (`False`).

3. **Keamanan kunci.** Kunci privat Anda dibuat dari nama, NIM, dan tanggal lahir. Mengapa cara ini SANGAT BERBAHAYA di dunia nyata? Siapa saja yang bisa mencuri dana alamat Anda? (Cari tahu istilah *brain wallet*.)

   _Jawaban:_
   - **Bahaya Brain Wallet dan Entropi Rendah:**
     Pembuatan kunci privat dari teks atau informasi yang mudah ditebak dikenal sebagai **Brain Wallet**. Cara ini sangat berbahaya karena ruang pencarian (*keyspace*) dari data identitas pribadi memiliki entropi yang sangat rendah. Kunci privat kriptografi seharusnya memiliki entropi 256 bit murni ($2^{256}$ kemungkinan acak tak tertebak).
   - **Pihak yang Berpotensi Mencuri Dana:**
     1. Siapa pun yang mengetahui data pribadi mahasiswa (teman sekelas, dosen, staf akademik kampus) atau yang mengakses basis data publik mahasiswa seperti PDDikti.
     2. Program otomatis peretas di blockchain publik (*sweeper bots*) yang menjalankan serangan kamus (*dictionary attacks*) berisi kombinasi nama umum, tanggal lahir, dan nomor induk untuk menguras saldo alamat mana pun yang cocok secara otomatis.

4. **Level 8.** Jaringan Anda punya 4 node dan pemenangnya FAHRI-1 dengan 5 blok terbuang. Jelaskan mengapa node itu menang. Mengapa jaringan Anda sempat tidak sepakat, dan bagaimana blok pemecah seri menyelesaikannya?

   _Jawaban:_
   - **Mengapa FAHRI-1 Menang:**
     Pada jaringan simulasi fork, terdapat 4 node yang menambang blok privat. Node FAHRI-1 menambang 3 blok (panjang 5), FAHRI-2 menambang 1 blok (panjang 3), FAHRI-3 menambang 3 blok (panjang 5), dan FAHRI-4 menambang 1 blok (panjang 3). Berdasarkan aturan konsensus Nakamoto (*Longest Chain Rule*), node selalu mengadopsi rantai terpanjang yang valid. Karena FAHRI-1 pada akhirnya menjadi node dengan rantai terpanjang, node-node lain mengadopsi rantainya dan membuang blok pribadi mereka. Total blok pribadi milik FAHRI-2 (1 blok), FAHRI-3 (3 blok), dan FAHRI-4 (1 blok) gugur menjadi **blok yatim (*orphan blocks*)**, yaitu total $1 + 3 + 1 = 5$ blok yang terbuang.
   - **Penyebab Jaringan Sempat Tidak Sepakat (*Tie Condition*):**
     Saat awal terjadi fork, node FAHRI-1 dan FAHRI-3 sama-sama memiliki panjang rantai 5 (`panjang_saat_fork: [5, 3, 5, 3]`). Ketika `resolve_conflicts` dijalankan, FAHRI-1 tidak mengganti rantainya ke FAHRI-3 karena panjangnya sama (tidak lebih panjang), dan sebaliknya FAHRI-3 juga mempertahankan rantainya sendiri. Akibatnya jaringan terbelah dua (*network split / tie*) sehingga `sepakat` bernilai `False`.
   - **Penyelesaian oleh Blok Pemecah Seri (*Tie-Breaker*):**
     Kondisi seri ini diselesaikan secara otomatis dengan menambang 1 blok baru di atas salah satu cabang (FAHRI-1). Penambahan blok ini membuat panjang rantai FAHRI-1 naik menjadi 6 (`[6, 6, 6, 6]`), menjadikannya definitif lebih panjang dari cabang FAHRI-3 (yang masih panjang 5). Seluruh node di jaringan langsung mematuhi *Longest Chain Rule* dan beralih mengadopsi rantai FAHRI-1, sehingga konsensus bulat 100% tercapai (`sepakat = True`).

5. **Level 9.** Dengan hadiah awal 39 dan halving setiap 3 blok, berapa batas total suplai jika mining berjalan selamanya? Tunjukkan perhitungannya, lalu kaitkan dengan batas 21 juta Bitcoin.

   _Jawaban:_
   - **Perhitungan Batas Total Suplai:**
     Dengan hadiah awal $H_0 = 39$ dan interval halving $I = 3$ blok menggunakan pembagian bilangan bulat (*integer division* `//`):
     - Periode 0 (Blok 1–3)  : Hadiah = 39 $\rightarrow 3 \times 39 = 117$ koin
     - Periode 1 (Blok 4–6)  : Hadiah = 19 ($39 // 2 = 19$) $\rightarrow 3 \times 19 = 57$ koin
     - Periode 2 (Blok 7–9)  : Hadiah = 9  ($19 // 2 = 9$)  $\rightarrow 3 \times 9 = 27$ koin
     - Periode 3 (Blok 10–12): Hadiah = 4  ($9 // 2 = 4$)   $\rightarrow 3 \times 4 = 12$ koin
     - Periode 4 (Blok 13–15): Hadiah = 2  ($4 // 2 = 2$)   $\rightarrow 3 \times 2 = 6$ koin
     - Periode 5 (Blok 16–18): Hadiah = 1  ($2 // 2 = 1$)   $\rightarrow 3 \times 1 = 3$ koin
     - Periode 6 (Blok 19–dst): Hadiah = 0  ($1 // 2 = 0$)   $\rightarrow$ Emisi koin berhenti selamanya.
     - **Total Suplai Riil Sistem:**
       $$\text{Total Suplai} = 117 + 57 + 27 + 12 + 6 + 3 = 222 \text{ koin}$$
     - **Secara Teoretis Deret Geometri Tak Hingga:**
       $$\text{Suplai Teoretis} = I \times H_0 \times \sum_{k=0}^{\infty} \left(\frac{1}{2}\right)^k = 3 \times 39 \times 2 = 234 \text{ koin}$$
       (Perbedaan 12 koin terjadi akibat pemotongan desimal bilangan bulat pada nilai ganjil).
   - **Kaitannya dengan Batas 21 Juta Bitcoin:**
     Prinsip ini mencerminkan mekanisme moneter Bitcoin yang menerapkan hadiah awal 50 BTC dengan interval halving setiap 210.000 blok. Melalui formula deret geometri $210.000 \times 50 \times 2 = 21.000.000$ BTC, Bitcoin menjamin kelangkaan terprogram (*digital scarcity*) dan mencegah devaluasi inflasioner.

---

## Data verifikasi (JANGAN DIUBAH)

<!-- DATA-VERIFIKASI -->
```json
{
  "tugas": "personal-2 (Level 6-9)",
  "profil": {
    "nama": "FAHRI",
    "nim4": "2029",
    "tanggal_lahir": "2002-09-03",
    "kota_asal": "Sorong",
    "hobi": "Coding"
  },
  "level6": {
    "data_ditambang": "FAHRI|2029|2002-09-03",
    "mining": [
      {
        "difficulty": 1,
        "nonce": 0,
        "hash": "0192f6336a588023bf903573c41f0dcbb4d5abec878c6e9957aca16d7d51c3e0",
        "percobaan": 1,
        "teori": 16
      },
      {
        "difficulty": 2,
        "nonce": 865,
        "hash": "0036a0955587ecc1bfa3b01d8a29043af8f7589687473db99b68e0339305af95",
        "percobaan": 866,
        "teori": 256
      },
      {
        "difficulty": 3,
        "nonce": 1719,
        "hash": "000587d74a8ff360e5bb23a04626a0b41f789d28b97047b6013b40ec1d70ff3a",
        "percobaan": 1720,
        "teori": 4096
      },
      {
        "difficulty": 4,
        "nonce": 59980,
        "hash": "00007129792e77de00c311e692c601fcb7a9b0cea3e1e7fc54d7fb95f1f70b43",
        "percobaan": 59981,
        "teori": 65536
      }
    ],
    "difficulty_awal": 2,
    "daftar_waktu_detik": [
      8,
      0,
      8,
      36,
      0,
      12,
      0,
      36
    ],
    "target_detik": 10,
    "jejak_difficulty": [
      2,
      3,
      3,
      2,
      3,
      3,
      4,
      3
    ]
  },
  "level7": {
    "kunci_publik_awal": "bf6320ff3cffd98b2ea0b1e4b5bf00c2",
    "alamat": "8e7c53d75056f4f0ea005f7d48a0bb705bc73557",
    "transaksi": {
      "sender": "8e7c53d75056f4f0ea005f7d48a0bb705bc73557",
      "recipient": "TEMAN_A",
      "amount": 3
    },
    "tanda_tangan": "fcedfa1ea81522c279266c5374ab87a27d10c21a7d77a4eecb240351ce66f4808aaa0e6c76ef25a37a25bc1e7f4ba37a14a82246a8ce809dcfaa5c9fa6a36c96",
    "tanda_tangan_selalu_sama": true,
    "sah": true,
    "sah_setelah_amount_diubah": false,
    "ttd_penipu_valid_dengan_kuncinya": true,
    "transaksi_penipu_sah": false
  },
  "level8": {
    "jumlah_node": 4,
    "blok_pribadi_per_node": [
      3,
      1,
      3,
      1
    ],
    "panjang_saat_fork": [
      5,
      3,
      5,
      3
    ],
    "panjang_setelah_resolve": [
      5,
      5,
      5,
      5
    ],
    "sepakat_setelah_resolve": false,
    "perlu_pemecah_seri": true,
    "panjang_setelah_pemecah_seri": [
      6,
      6,
      6,
      6
    ],
    "sepakat_setelah_pemecah_seri": true,
    "pemenang_fork": "FAHRI-1",
    "blok_terbuang": 5,
    "hash_ujung": "0080557778cb57b8cf2bd39474096ba1e4eea8f03c8dd9f8846205e176dff984"
  },
  "level9": {
    "hadiah_awal": 39,
    "interval_halving": 3,
    "hadiah_per_blok": [
      39,
      39,
      39,
      19,
      19,
      19
    ],
    "saldo": {
      "FAHRI": 103.0,
      "TEMAN_A": 41.0,
      "TEMAN_B": 30.0
    },
    "total_suplai": 174.0,
    "belanja_melebihi_saldo_ditolak": true,
    "validasi_ekonomi": true,
    "hash_ujung": "00ce27fadc94ffc1508e606d66393ee94bd5d8252ba66093c3f5fd5fbf4fe929",
    "validasi_setelah_hadiah_dicurangi": false
  },
  "kode_verifikasi": "4E88B1255ECA"
}
```
