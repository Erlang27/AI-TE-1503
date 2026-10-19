# Rekomendasi Rute Transportasi Jakarta

**Tugas 1 - Kecerdasan Buatan (AI)**
Search Algorithm dan Rule-Based Expert System
Kelompok: AI-TE-1503

## Anggota

| Peran | Nama | Branch |
|---|---|---|
| Ketua (manager) | [ISI NAMA KETUA] | `main` |
| Dev 1 | Hue | `dev1-hue` |
| Dev 2 | Bagas | `dev2-bagas` |

## Deskripsi

Program ini merekomendasikan rute antar 16 stasiun/halte di jaringan MRT, KRL, dan TransJakarta Jakarta
(data disederhanakan, waktu dan biaya berupa estimasi).

Program menggabungkan dua komponen:

1. **Rule-Based Expert System** (forward chaining). User menjawab 3 pertanyaan (buru-buru, budget tipis,
   jam sibuk). Aturan IF-THEN menyimpulkan kriteria optimasi (waktu atau biaya), algoritma yang cocok,
   dan efek macet pada TransJakarta.
2. **Search Algorithm**. Empat algoritma dijalankan dan dibandingkan:

| Algoritma | Jenis | Informasi yang dipakai |
|---|---|---|
| BFS | Uninformed | Tidak ada (jumlah perhentian paling sedikit) |
| UCS | Uninformed | Tidak ada (biaya sejauh ini saja) |
| Greedy Best-First | Informed | Heuristik jarak garis lurus ke tujuan |
| A* | Informed | Biaya sejauh ini + heuristik jarak garis lurus |

Heuristik yang dipakai adalah jarak garis lurus (haversine) dengan asumsi kecepatan maksimum 60 km/jam.
Heuristik ini admissible karena `cek_admissible()` di `graph.py` memastikan waktu tiap jalur tidak
lebih kecil dari jarak garis lurusnya.

## Struktur Folder

```
AI-TE-1503/
├── README.md
└── algoritma/
    ├── graph.py           # data stasiun, jalur, heuristik
    ├── search.py          # BFS, UCS, Greedy, A*
    ├── expert_system.py   # aturan IF-THEN + forward chaining
    └── main.py            # program utama
```

## Requirements

- Python 3.8 atau lebih baru
- Tidak ada library tambahan (hanya library standar: `math`, `heapq`, `collections`, `itertools`)

## Cara Pakai

1. Clone repository:
   ```
   git clone https://github.com/<username>/AI-TE-1503.git
   cd AI-TE-1503/algoritma
   ```
2. Jalankan program utama (lihat bagian Running).
3. Pilih nomor stasiun asal dan tujuan.
4. Jawab tiga pertanyaan dengan `y` atau `n`.
5. Program menampilkan aturan expert system yang dipakai, lalu tabel perbandingan keempat algoritma.

## Running

```
cd algoritma
python main.py
```

Tes tiap modul secara terpisah:

```
python graph.py            # cek data graph dan heuristik
python search.py           # contoh perbandingan 4 algoritma
python expert_system.py    # contoh inferensi expert system
```

### Contoh Output

Lebak Bulus ke Jakarta Kota, jawaban `n`, `n`, `n` (tidak buru-buru, budget cukup, bukan jam sibuk):

```
Algoritma    Waktu     Biaya  Diperiksa  Moda
------------------------------------------------------------
BFS          53 mnt   Rp21000         13  MRT > TJ > KRL
UCS          50 mnt   Rp33500         14  MRT > TJ > KRL
Greedy       53 mnt   Rp21000          6  MRT > TJ > KRL
A*           50 mnt   Rp33500         13  MRT > TJ > KRL *
(* = rekomendasi expert system)
```

Dari contoh ini terlihat Greedy memeriksa simpul paling sedikit tetapi hasilnya tidak optimal,
sedangkan UCS dan A* sama-sama optimal dan A* memeriksa simpul sedikit lebih sedikit.

## Aturan Expert System

| ID | Aturan |
|---|---|
| R1 | Jam sibuk, maka macet |
| R2 | Macet, maka waktu TransJakarta dikali 1.5 |
| R3 | Buru-buru, maka kriteria waktu |
| R4 | Tidak buru-buru dan budget tipis, maka kriteria biaya |
| R5 | Tidak buru-buru dan budget cukup, maka kriteria waktu |
| R6 | Kriteria waktu, maka algoritma A* |
| R7 | Kriteria biaya, maka algoritma UCS |
| R8 | Jam Sibuk dan buru-buru, maka sarankan MRT/KRL |

## Catatan

- Data waktu dan biaya adalah estimasi untuk keperluan tugas, bukan data resmi operator.
- Untuk kriteria biaya (Rp), A* memakai h = 0 sehingga perilakunya sama dengan UCS, karena tidak ada
  estimasi biaya yang andal dari jarak garis lurus.

## Keterbatasan
   - (misal: data waktu dan biaya hanya estimasi)
   - (misal: jumlah stasiun masih sedikit)
   - (misal: aturan expert system masih sederhana)
