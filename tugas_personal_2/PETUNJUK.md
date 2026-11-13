# Tugas Personal 2: Level 6–9 dengan Data Diri Anda

Lanjutan dari Tugas Personal 1. Anda memodifikasi kode Level 6–9 supaya memakai data diri Anda:
nama, 4 digit terakhir NIM, tanggal lahir, kota asal, dan hobi. Hasil mining, kunci dan tanda tangan,
jalannya fork di jaringan, serta ekonomi koin Anda **berbeda dari teman-teman Anda**.

## Prasyarat

Level 6–9 di folder `latihan/` harus sudah lulus:

```bash
python cek_nilai.py 6 7 8 9      # harus SELESAI semua
```

## Langkah pengerjaan

**1. Isi data diri** di `tugas_personal_2/data_saya.py`. Isinya harus sama dengan Tugas Personal 1,
jadi Anda boleh menyalin file `tugas_personal/data_saya.py`.

**2. Kerjakan empat modifikasi** di `tugas_personal_2/modifikasi_2.py`.

| No | Memodifikasi | Yang Anda buat |
|---|---|---|
| 6 | Level 6 | `jejak_difficulty()`: menerapkan `sesuaikan_difficulty` berulang kali pada deret waktu blok |
| 7 | Level 7 | `kunci_dari_data()`: pasangan kunci yang selalu sama, dibuat dari data diri. `tanda_tangani_deterministik()`: tanda tangan yang selalu sama (RFC 6979) |
| 8 | Level 8 | `NodePersonal`: node yang menandai setiap blok tambangannya. `semua_sepakat()`: memeriksa apakah semua node punya rantai yang sama |
| 9 | Level 9 | `BlockchainHalving`: hadiah mining berkurang separuh secara berkala, seperti Bitcoin |

**3. Periksa modifikasi**, lalu jalankan tugas:

```bash
python tugas_personal_2/jalankan_tugas_2.py --cek     # memeriksa keempat modifikasi dengan data uji
python tugas_personal_2/jalankan_tugas_2.py           # menjalankan tugas dengan data Anda
```

Program membuat file `tugas_personal_2/laporan_tugas_personal_2_<NIM_4>.md`.

**4. Isi bagian Analisis** di laporan itu. Beberapa soal meminta Anda membandingkan hasil dengan teman.

**5. Serahkan dua file** kepada dosen:
- `laporan_tugas_personal_2_<NIM_4>.md`
- `modifikasi_2.py`

## Mengapa hasil Anda berbeda?

| Level | Hasil yang berbeda per mahasiswa | Ditentukan oleh |
|---|---|---|
| 6 | Nonce dan jumlah percobaan untuk difficulty 1–4 | Data yang ditambang: nama, NIM, tanggal lahir |
| 6 | Jejak difficulty | Difficulty awal dari NIM; waktu blok dari digit NIM, tanggal, dan bulan lahir |
| 7 | Kunci publik, alamat, tanda tangan | Kunci dibuat dari hash nama, NIM, dan tanggal lahir |
| 8 | Jumlah node, panjang fork, pemenang, blok terbuang | Jumlah node = 3 + (NIM mod 3); blok pribadi tiap node dari digit NIM dan tanggal lahir |
| 9 | Hadiah per blok, saldo, total suplai | Hadiah awal = 20 + (NIM mod 30); halving setiap 2 + (NIM mod 3) blok |

Sebagian mahasiswa akan mendapat jaringan yang **sempat tidak sepakat** di Level 8 (dua node sama panjang).
Itu bukan kesalahan. Laporan akan menunjukkan bagaimana satu blok tambahan menyelesaikannya.

## Peringatan keamanan

Di Modifikasi 7, kunci privat dibuat dari data diri supaya hasilnya bisa diperiksa dosen. **Jangan pernah
melakukan ini di dunia nyata.** Siapa pun yang tahu nama, NIM, dan tanggal lahir Anda bisa membuat ulang
kunci privat Anda. Laporan sengaja tidak mencantumkan kunci privat Anda.

## Aturan

- **Jangan mengubah** `skenario_2.py` dan `jalankan_tugas_2.py`.
- **Jangan mengedit** angka di laporan. Dosen menghitung ulang semua hasil dari data di laporan Anda.
  Laporan yang diedit atau disalin dari teman langsung terdeteksi sebagai TIDAK COCOK.
- **Privasi:** `data_saya.py` dan laporan berisi data pribadi Anda. Serahkan hanya kepada dosen.
