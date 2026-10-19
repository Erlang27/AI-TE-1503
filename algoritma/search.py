"""
search.py
Empat algoritma pencarian rute:

  UNINFORMED (tanpa informasi tambahan)
    - BFS    : cari rute dengan jumlah perhentian paling sedikit
    - UCS    : cari rute dengan total biaya (waktu atau Rp) paling kecil

  INFORMED (pakai heuristik jarak garis lurus ke tujuan)
    - Greedy : selalu pilih simpul yang tampak paling dekat ke tujuan
    - A*     : gabungan biaya sejauh ini (g) + estimasi sisa (h)

Semua fungsi mengembalikan dictionary hasil (lihat _hasil).
"""

import heapq
from collections import deque
from itertools import count

from graph import heuristik_waktu


def _bobot(kriteria, waktu, biaya):
    """Kembalikan (bobot utama, bobot sekunder).
    Bobot sekunder dipakai sebagai pemutus seri, misalnya kalau dua rute
    sama-sama Rp3.000 maka dipilih yang lebih cepat."""
    if kriteria == "waktu":
        return waktu, biaya
    return biaya, waktu


def _hasil(nama, awal, langkah, diperiksa):
    """Susun hasil. langkah = list of (dari, ke, waktu, biaya, moda)."""
    if langkah is None:
        return {"algoritma": nama, "ditemukan": False, "diperiksa": diperiksa}
    return {
        "algoritma": nama,
        "ditemukan": True,
        "rute": [awal] + [l[1] for l in langkah],
        "waktu": sum(l[2] for l in langkah),
        "biaya": sum(l[3] for l in langkah),
        "moda": [l[4] for l in langkah],
        "diperiksa": diperiksa,   # jumlah simpul yang diperiksa (ukuran efisiensi)
    }


# ---------------------------------------------------------------------------
# BFS (uninformed): antrean FIFO, simpul diperiksa level demi level
# ---------------------------------------------------------------------------
def bfs(graph, awal, tujuan):
    antrean = deque([(awal, [])])
    dikunjungi = {awal}
    diperiksa = 0

    while antrean:
        simpul, langkah = antrean.popleft()
        diperiksa += 1
        if simpul == tujuan:
            return _hasil("BFS", awal, langkah, diperiksa)
        for tetangga, waktu, biaya, moda in graph[simpul]:
            if tetangga not in dikunjungi:
                dikunjungi.add(tetangga)
                antrean.append((tetangga, langkah + [(simpul, tetangga, waktu, biaya, moda)]))

    return _hasil("BFS", awal, None, diperiksa)


# ---------------------------------------------------------------------------
# Kerangka best-first search (dipakai UCS, Greedy, dan A*)
# Bedanya hanya di cara menghitung prioritas:
#   UCS    : prioritas = g
#   Greedy : prioritas = h
#   A*     : prioritas = g + h
# ---------------------------------------------------------------------------
def _best_first(nama, graph, awal, tujuan, kriteria, pakai_g, h):
    urut = count()  # penomoran supaya heap tidak membandingkan list saat prioritas sama
    # isi antrean: (prioritas, g sekunder, urut, g utama, simpul, langkah)
    pq = [(0, 0, next(urut), 0, awal, [])]
    selesai = set()
    diperiksa = 0

    while pq:
        _, g2, _, g1, simpul, langkah = heapq.heappop(pq)
        if simpul in selesai:
            continue
        selesai.add(simpul)
        diperiksa += 1

        if simpul == tujuan:
            return _hasil(nama, awal, langkah, diperiksa)

        for tetangga, waktu, biaya, moda in graph[simpul]:
            if tetangga in selesai:
                continue
            utama, sekunder = _bobot(kriteria, waktu, biaya)
            g1_baru = g1 + utama
            g2_baru = g2 + sekunder
            prioritas = (g1_baru if pakai_g else 0) + h(tetangga, tujuan)
            heapq.heappush(pq, (
                prioritas, g2_baru, next(urut), g1_baru, tetangga,
                langkah + [(simpul, tetangga, waktu, biaya, moda)],
            ))

    return _hasil(nama, awal, None, diperiksa)


def _nol(a, b):
    return 0


# UCS (uninformed): tanpa heuristik
def ucs(graph, awal, tujuan, kriteria="waktu"):
    return _best_first("UCS", graph, awal, tujuan, kriteria, True, _nol)


# Greedy Best-First (informed): hanya melihat heuristik, mengabaikan biaya sejauh ini
def greedy(graph, awal, tujuan, kriteria="waktu"):
    return _best_first("Greedy", graph, awal, tujuan, kriteria, False, heuristik_waktu)


# A* (informed): g + h.
# Heuristik jarak lurus hanya bermakna untuk kriteria waktu. Untuk kriteria biaya
# (Rp) tidak ada estimasi yang pasti, jadi h = 0 dan A* berperilaku seperti UCS.
def a_star(graph, awal, tujuan, kriteria="waktu"):
    h = heuristik_waktu if kriteria == "waktu" else _nol
    return _best_first("A*", graph, awal, tujuan, kriteria, True, h)


if __name__ == "__main__":
    from graph import bangun_graph

    g = bangun_graph()
    for fungsi in (bfs, ucs, greedy, a_star):
        if fungsi is bfs:
            r = fungsi(g, "Lebak Bulus", "Jakarta Kota")
        else:
            r = fungsi(g, "Lebak Bulus", "Jakarta Kota", "waktu")
        print(f"{r['algoritma']:<7} {' -> '.join(r['rute'])}  "
              f"({r['waktu']} menit, Rp{r['biaya']}, diperiksa {r['diperiksa']})")
