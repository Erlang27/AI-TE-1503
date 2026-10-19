"""
expert_system.py
Rule-Based Expert System dengan forward chaining.

Input (fakta awal dari user):
    buru_buru   : True/False
    budget_tipis: True/False
    jam_sibuk   : True/False

Output (fakta hasil inferensi):
    kriteria    : "waktu" atau "biaya"  -> kriteria optimasi rute
    algoritma   : algoritma search yang direkomendasikan
    pengali_tj  : pengali waktu TransJakarta (macet saat jam sibuk)
    + jejak aturan yang dipakai (penjelasan / explanation facility)

Cara kerja forward chaining:
  Ulangi: cek tiap aturan, kalau kondisinya terpenuhi dan kesimpulannya belum ada,
  tambahkan kesimpulan ke daftar fakta. Berhenti kalau tidak ada fakta baru.
  Urutan aturan = prioritas (aturan yang lebih atas menang kalau ada konflik).
"""

# Format aturan: (id, penjelasan, kondisi(fakta) -> bool, kesimpulan dict)
ATURAN = [
    ("R1", "Jam sibuk -> jalan raya macet",
     lambda f: f.get("jam_sibuk"),
     {"macet": True}),

    ("R2", "Macet -> waktu tempuh TransJakarta dikali 1.5",
     lambda f: f.get("macet"),
     {"pengali_tj": 1.5}),

    ("R3", "Buru-buru -> utamakan waktu tercepat",
     lambda f: f.get("buru_buru"),
     {"kriteria": "waktu"}),

    ("R4", "Tidak buru-buru dan budget tipis -> utamakan biaya termurah",
     lambda f: not f.get("buru_buru") and f.get("budget_tipis"),
     {"kriteria": "biaya"}),

    ("R5", "Tidak buru-buru dan budget cukup -> utamakan waktu tercepat",
     lambda f: not f.get("buru_buru") and not f.get("budget_tipis"),
     {"kriteria": "waktu"}),

    ("R6", "Kriteria waktu -> gunakan A* (heuristik jarak lurus berguna untuk waktu)",
     lambda f: f.get("kriteria") == "waktu",
     {"algoritma": "A*"}),

    ("R7", "Kriteria biaya -> gunakan UCS (tidak ada heuristik yang andal untuk Rp)",
     lambda f: f.get("kriteria") == "biaya",
     {"algoritma": "UCS"}),
]


def inferensi(fakta_awal):
    """Jalankan forward chaining. Kembalikan (fakta akhir, jejak aturan)."""
    fakta = dict(fakta_awal)
    jejak = []
    ada_perubahan = True

    while ada_perubahan:
        ada_perubahan = False
        for id_aturan, penjelasan, kondisi, kesimpulan in ATURAN:
            # lewati kalau kesimpulan aturan ini sudah ada di fakta
            if any(k in fakta for k in kesimpulan):
                continue
            if kondisi(fakta):
                fakta.update(kesimpulan)
                jejak.append((id_aturan, penjelasan))
                ada_perubahan = True

    fakta.setdefault("pengali_tj", 1.0)
    return fakta, jejak


if __name__ == "__main__":
    hasil, jejak = inferensi({"buru_buru": False, "budget_tipis": True, "jam_sibuk": True})
    print(hasil)
    for id_aturan, penjelasan in jejak:
        print(f"  {id_aturan}: {penjelasan}")
