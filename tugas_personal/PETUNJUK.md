# Tugas Personal: Blockchain dengan Data Diri Anda (Level 1–5)

Di latihan Level 1–5, semua mahasiswa menjalankan kode yang sama dan mendapat hasil yang sama.
Di tugas ini Anda **memodifikasi** kode Level 1–5 supaya memakai data diri Anda: nama, 4 digit terakhir
NIM, tanggal lahir, kota asal, dan hobi. Akibatnya hash, proof, nonce, dan hasil pemalsuan Anda
**berbeda dari teman-teman Anda**. Anda lalu melaporkan dan menjelaskan hasil itu.

## Prasyarat

Level 1–5 di folder `latihan/` harus sudah lulus:

```bash
python cek_nilai.py 1 2 3 4 5      # harus SELESAI semua
```

## Langkah pengerjaan

**1. Isi data diri** di `tugas_personal/data_saya.py`.

**2. Kerjakan lima modifikasi** di `tugas_personal/modifikasi.py` (ganti setiap `raise NotImplementedError`).

| No | Memodifikasi | Yang Anda buat | Data yang dipakai |
|---|---|---|---|
| 1 | Level 1 | `sidik_jari()`: ID mahasiswa 8 karakter dari hash data diri | nama, NIM, tanggal lahir |
| 2 | Level 2 | `BlockchainPersonal`: proof genesis = NIM Anda, setiap blok punya field `pemilik` | NIM, ID mahasiswa |
| 3 | Level 3 | `palsukan()`: memalsukan satu blok berisi data diri Anda, lalu menyambung ulang rantai | posisi blok ditentukan NIM |
| 4 | Level 4 | `ringkasan_saldo()`: total uang masuk, keluar, dan bersih milik Anda | jumlah transaksi dari tanggal & bulan lahir, NIM |
| 5 | Level 5 | `BlockchainDeterministik`: timestamp diganti tanggal lahir agar nonce selalu sama | tanggal lahir, ID mahasiswa |

**3. Periksa modifikasi**, lalu jalankan tugas:

```bash
python tugas_personal/jalankan_tugas.py --cek     # memeriksa kelima modifikasi dengan data uji
python tugas_personal/jalankan_tugas.py           # menjalankan tugas dengan data Anda
```

Program membuat file `tugas_personal/laporan_tugas_personal_<NIM_4>.md`.

**4. Isi bagian Analisis** di laporan itu. Pertanyaannya menyebut angka-angka **milik Anda**, jadi
jawaban Anda pasti berbeda dari teman. Untuk beberapa soal, Anda perlu membandingkan hasil dengan teman.

**5. Serahkan dua file** kepada dosen:
- `laporan_tugas_personal_<NIM_4>.md`
- `modifikasi.py`

## Mengapa hasil Anda berbeda?

| Level | Hasil yang berbeda per mahasiswa | Penyebabnya |
|---|---|---|
| 1 | Hash nama, hash profil, ID mahasiswa | Input hash berbeda |
| 2 | Proof blok 2–4 | Proof genesis = NIM Anda, dan setiap proof bergantung pada proof sebelumnya |
| 3 | Posisi yang dipalsukan dan hasil deteksinya | Posisi = 1 + (NIM mod 4) |
| 4 | Transaksi dan ringkasan saldo | Jumlah = tanggal lahir, bulan lahir, (NIM mod 50) + 1 |
| 5 | Nonce, hash, dan biaya pemalsuan | Isi blok memuat tanggal lahir, ID, dan transaksi Anda |

## Aturan

- **Jangan mengubah** `skenario.py` dan `jalankan_tugas.py`.
- **Jangan mengedit** angka di laporan. Dosen menghitung ulang semua hasil dari data di laporan Anda
  dengan program verifikasi. Laporan yang diedit atau disalin dari teman langsung terdeteksi
  sebagai TIDAK COCOK.
- **Privasi:** `data_saya.py` dan laporan berisi data pribadi Anda. Serahkan hanya kepada dosen.
  Jangan unggah ke repositori publik atau grup terbuka.
