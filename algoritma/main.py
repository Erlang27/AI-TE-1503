"""
main.py
Program utama: Sistem Rekomendasi Rute Transportasi Jakarta
(Search Algorithm + Rule-Based Expert System)

Alur:
  1. User pilih stasiun asal dan tujuan
  2. User jawab 3 pertanyaan (buru-buru? budget tipis? jam sibuk?)
  3. Expert system menyimpulkan kriteria + algoritma yang cocok
  4. Keempat algoritma dijalankan dan dibandingkan
"""

from graph import STASIUN, bangun_graph
from search import bfs, ucs, greedy, a_star
from expert_system import inferensi


def tanya_ya_tidak(pertanyaan):
    while True:
        jawab = input(f"{pertanyaan} (y/n): ").strip().lower()
        if jawab in ("y", "n"):
            return jawab == "y"
        print("  Jawab dengan y atau n.")


def pilih_stasiun(label, daftar):
    while True:
        pilihan = input(f"{label} (nomor): ").strip()
        if pilihan.isdigit() and 1 <= int(pilihan) <= len(daftar):
            return daftar[int(pilihan) - 1]
        print("  Nomor tidak valid.")


def terapkan_pengali_tj(graph, pengali):
    """Buat salinan graph di mana waktu TransJakarta dikali pengali (efek macet).
    Waktu hanya membesar, jadi heuristik jarak lurus tetap admissible."""
    baru = {}
    for simpul, daftar in graph.items():
        baru[simpul] = [
            (t, round(w * pengali) if moda == "TJ" else w, b, moda)
            for t, w, b, moda in daftar
        ]
    return baru


def ringkas_moda(daftar_moda):
    """['MRT','MRT','KRL'] -> 'MRT > KRL'"""
    hasil = []
    for m in daftar_moda:
        if not hasil or hasil[-1] != m:
            hasil.append(m)
    return " > ".join(hasil) if hasil else "-"


def tampilkan(hasil_list, rekomendasi):
    print()
    print(f"{'Algoritma':<10}{'Waktu':>8}{'Biaya':>10}{'Diperiksa':>11}  Moda")
    print("-" * 60)
    for r in hasil_list:
        tanda = " *" if r["algoritma"] == rekomendasi else ""
        if not r["ditemukan"]:
            print(f"{r['algoritma']:<10} rute tidak ditemukan")
            continue
        print(f"{r['algoritma']:<10}{r['waktu']:>5} mnt{'Rp' + str(r['biaya']):>10}"
              f"{r['diperiksa']:>11}  {ringkas_moda(r['moda'])}{tanda}")
    print("(* = rekomendasi expert system)")
    print()
    for r in hasil_list:
        if r["ditemukan"]:
            print(f"Rute {r['algoritma']:<7}: {' -> '.join(r['rute'])}")


def main():
    print("=== Rekomendasi Rute Transportasi Jakarta ===\n")

    daftar = list(STASIUN)
    for i, nama in enumerate(daftar, 1):
        print(f"{i:>2}. {nama}")
    print()

    asal = pilih_stasiun("Stasiun asal", daftar)
    tujuan = pilih_stasiun("Stasiun tujuan", daftar)
    if asal == tujuan:
        print("Asal dan tujuan sama, tidak perlu perjalanan.")
        return

    print()
    fakta_awal = {
        "buru_buru": tanya_ya_tidak("Apakah kamu sedang buru-buru?"),
        "budget_tipis": tanya_ya_tidak("Apakah budget kamu tipis?"),
        "jam_sibuk": tanya_ya_tidak("Apakah sekarang jam sibuk (berangkat/pulang kerja)?"),
    }

    # --- Expert system ---
    fakta, jejak = inferensi(fakta_awal)
    print("\n[Expert System] Aturan yang dipakai:")
    for id_aturan, penjelasan in jejak:
        print(f"  {id_aturan}: {penjelasan}")
    print(f"[Expert System] Kriteria: {fakta['kriteria']} | "
          f"Algoritma rekomendasi: {fakta['algoritma']}")

    # --- Search ---
    graph = terapkan_pengali_tj(bangun_graph(), fakta["pengali_tj"])
    kriteria = fakta["kriteria"]
    hasil = [
        bfs(graph, asal, tujuan),
        ucs(graph, asal, tujuan, kriteria),
        greedy(graph, asal, tujuan, kriteria),
        a_star(graph, asal, tujuan, kriteria),
    ]
    tampilkan(hasil, fakta["algoritma"])


if __name__ == "__main__":
    main()
