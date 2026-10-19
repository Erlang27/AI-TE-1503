"""
graph.py
Data graph jaringan transportasi Jakarta (MRT, KRL, TransJakarta) yang disederhanakan.

Node  = stasiun / halte
Edge  = jalur langsung antar dua stasiun, punya atribut:
        waktu (menit), biaya (Rp, estimasi), moda (MRT/KRL/TJ)

CATATAN: waktu dan biaya adalah ESTIMASI untuk keperluan tugas, bukan data resmi.
"""

import math

# ---------------------------------------------------------------------------
# 1. Koordinat stasiun (lat, lon) -> dipakai untuk heuristik (informed search)
# ---------------------------------------------------------------------------
STASIUN = {
    "Lebak Bulus":      (-6.2893, 106.7742),
    "Fatmawati":        (-6.2924, 106.7923),
    "Blok M":           (-6.2442, 106.7983),
    "Senayan":          (-6.2273, 106.8023),
    "Istora":           (-6.2223, 106.8045),
    "Bendungan Hilir":  (-6.2146, 106.8186),
    "Dukuh Atas":       (-6.2008, 106.8230),
    "Bundaran HI":      (-6.1936, 106.8228),
    "Tanah Abang":      (-6.1858, 106.8115),
    "Gondangdia":       (-6.1860, 106.8325),
    "Gambir":           (-6.1767, 106.8306),
    "Manggarai":        (-6.2077, 106.8505),
    "Tebet":            (-6.2260, 106.8586),
    "Pasar Minggu":     (-6.2842, 106.8445),
    "Depok":            (-6.3917, 106.8176),
    "Jakarta Kota":     (-6.1376, 106.8133),
    "Juanda": 		(-6.1666, 106.8307),
}

# ---------------------------------------------------------------------------
# 2. Daftar jalur: (stasiun A, stasiun B, waktu menit, biaya Rp, moda)
#    Semua jalur dua arah.
# ---------------------------------------------------------------------------
JALUR = [
    # MRT Jakarta (Lebak Bulus - Bundaran HI)
    ("Lebak Bulus",     "Fatmawati",        4, 4000, "MRT"),
    ("Fatmawati",       "Blok M",           9, 7000, "MRT"),
    ("Blok M",          "Senayan",          6, 4000, "MRT"),
    ("Senayan",         "Istora",           2, 3000, "MRT"),
    ("Istora",          "Bendungan Hilir",  3, 3000, "MRT"),
    ("Bendungan Hilir", "Dukuh Atas",       4, 3000, "MRT"),
    ("Dukuh Atas",      "Bundaran HI",      2, 3000, "MRT"),

    # KRL Commuter Line
    ("Tanah Abang",     "Dukuh Atas",       4, 3000, "KRL"),
    ("Dukuh Atas",      "Manggarai",        7, 3000, "KRL"),
    ("Gondangdia",      "Manggarai",        7, 3000, "KRL"),
    ("Gambir",          "Gondangdia",       3, 3000, "KRL"),
    ("Gambir",          "Jakarta Kota",    10, 3000, "KRL"),
    ("Manggarai",       "Tebet",            4, 3000, "KRL"),
    ("Tebet",           "Pasar Minggu",    12, 3000, "KRL"),
    ("Pasar Minggu",    "Depok",           17, 3000, "KRL"),

    # TransJakarta (lebih murah tapi lebih lambat karena macet)
    ("Blok M",          "Bundaran HI",     20, 3500, "TJ"),
    ("Bundaran HI",     "Gambir",          10, 3500, "TJ"),
    ("Gambir",          "Jakarta Kota",    15, 3500, "TJ"),
    ("Gambir",          "Juanda",           3, 3000, "KRL"),
    ("Juanda",          "Jakarta Kota",     8, 3000, "KRL"),
]


# ---------------------------------------------------------------------------
# 3. Membangun graph (adjacency list)
#    graph["Gambir"] -> [(tetangga, waktu, biaya, moda), ...]
# ---------------------------------------------------------------------------
def bangun_graph():
    graph = {nama: [] for nama in STASIUN}
    for a, b, waktu, biaya, moda in JALUR:
        graph[a].append((b, waktu, biaya, moda))
        graph[b].append((a, waktu, biaya, moda))
    return graph


# ---------------------------------------------------------------------------
# 4. Heuristik untuk informed search (Greedy & A*)
#    Jarak garis lurus (haversine) antar dua stasiun, dalam km.
# ---------------------------------------------------------------------------
def jarak_km(a, b):
    lat1, lon1 = map(math.radians, STASIUN[a])
    lat2, lon2 = map(math.radians, STASIUN[b])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    x = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(x))


# Anggap kecepatan maksimum kendaraan 60 km/jam = 1 km per menit.
# Jadi estimasi waktu minimal = jarak_km (menit). Tidak mungkin lebih cepat dari ini,
# sehingga heuristik ini "admissible" (tidak pernah melebihi biaya sebenarnya).
def heuristik_waktu(sekarang, tujuan):
    return jarak_km(sekarang, tujuan) * 1.0


def cek_admissible():
    """Pastikan waktu tiap jalur >= jarak garis lurus, supaya A* menjamin hasil optimal."""
    aman = True
    for a, b, waktu, _, _ in JALUR:
        j = jarak_km(a, b)
        if waktu < j:
            print(f"[PERINGATAN] {a} - {b}: waktu {waktu} menit < jarak {j:.1f} km")
            aman = False
    return aman


if __name__ == "__main__":
    graph = bangun_graph()
    print(f"Jumlah stasiun : {len(graph)}")
    print(f"Jumlah jalur   : {len(JALUR)}")
    print(f"Heuristik admissible? {cek_admissible()}")
    print()
    print("Tetangga Gambir:")
    for tetangga, waktu, biaya, moda in graph["Gambir"]:
        print(f"  -> {tetangga:<14} {waktu:>2} menit  Rp{biaya:<5} {moda}")
    print()
    print(f"Jarak lurus Lebak Bulus - Jakarta Kota: {jarak_km('Lebak Bulus', 'Jakarta Kota'):.1f} km")
