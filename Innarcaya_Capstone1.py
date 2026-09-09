print("===== THRIFTBOOKZ - STOK TOKO BUKU PRELOVED =====\n")

# 1. Daftar Nilai/Kategori yang Dianggap Valid

# Kondisi, skala IOBA/ABAA (ioba.org/conditions-definitions):
# F  Fine       hampir sempurna
# VG Very Good  bekas rapi, utuh
# G  Good       bekas rata-rata, cacat wajib dicatat
# FR Fair       aus berat, teks lengkap
# P  Poor       hanya layak reading copy
KONDISI = ("F", "VG", "G", "FR", "P")

# Aturan IOBA: semua cacat harus dicatat mulai dari Good ke bawah.
WAJIB_CATATAN = ("G", "FR", "P")

STATUS = ("tersedia", "dibooking", "terjual", "depresiasi")

# Kategori = satu kolom berformat BENTUK-PEMBACA-SUBJEK, contoh N-ANK-SAI.
# Format tetap, jadi pencarian per bagian cukup pakai substring.
#
# BENTUK  (BISAC)  F=Fiksi  N=Nonfiksi
# PEMBACA (BISAC)  ANK=anak 0-11  RMJ=remaja 12-18  DWS=dewasa
#                  SUM=semua umur
# SUBJEK  fiksi   : SAS sastra, HIS historis, FAN fantasi, MIS misteri,
#                   ROM romansa, KOM komik
#         nonfiksi: SEJ sejarah, POL politik, PDK pendidikan, BIO biografi,
#                   SAI sains, AGM agama, PRK praktis (bisnis, hobi, masak,
#                   pengembangan diri, kesehatan), LAI lainnya.
BENTUK = ("F", "N")
PEMBACA = ("ANK", "RMJ", "DWS", "SUM")
SUBJEK = ("SAS", "HIS", "FAN", "MIS", "ROM", "KOM",
          "SEJ", "POL", "PDK", "BIO", "SAI", "AGM", "PRK", "LAI")


# 2. Data Awal

DATA = [
    {"id": "BK001", "judul": "Bumi Manusia", "penulis": "Pramoedya A. Toer",
     "kategori": "F-DWS-HIS", "kondisi": "VG", "beli": 45000, "jual": 95000,
     "status": "terjual", "catatan": "hal 40-42 ada garis pensil"},
    {"id": "BK002", "judul": "Animal Farm", "penulis": "George Orwell",
     "kategori": "F-SUM-SAS", "kondisi": "G", "beli": 40000, "jual": 90000,
     "status": "tersedia", "catatan": "sudut tertekuk, punggung pudar"},
    {"id": "BK003", "judul": "Animal Farm", "penulis": "George Orwell",
     "kategori": "F-SUM-SAS", "kondisi": "F", "beli": 55000, "jual": 120000,
     "status": "dibooking", "catatan": "Rani, DP 50rb, tempo 3 hari"},
    {"id": "BK004", "judul": "Ensiklopedia Dinosaurus", "penulis": "Tim BIP",
     "kategori": "N-ANK-SAI", "kondisi": "G", "beli": 35000, "jual": 80000,
     "status": "tersedia", "catatan": "ada bekas krayon"},
    {"id": "BK005", "judul": "Sapiens", "penulis": "Yuval Noah Harari",
     "kategori": "N-DWS-SEJ", "kondisi": "FR", "beli": 50000, "jual": 110000,
     "status": "tersedia", "catatan": "sampul sobek, halaman lengkap"},
    {"id": "BK006", "judul": "Laut Bercerita", "penulis": "Leila S. Chudori",
     "kategori": "F-RMJ-HIS", "kondisi": "P", "beli": 30000, "jual": 55000,
     "status": "depresiasi", "catatan": "kena rembes air"},
]


# 3. Fungsi Pencarian dan Penjumlahan

def cari(daftar, kunci, nilai):
    hasil = []
    for b in daftar:
        if str(nilai).lower() in str(b[kunci]).lower():
            hasil.append(b)
    return hasil


def total(daftar, kunci):
    jumlah = 0
    for b in daftar:
        jumlah += b[kunci]
    return jumlah


# 4. Fungsi Input dengan Validasi

def isi_teks(label, wajib=True):
    while True:
        nilai = input(f"  {label}: ").strip()
        if nilai == "" and wajib:
            print("  Tidak boleh kosong. Coba lagi.")
            continue
        break
    return nilai


def isi_angka(label):
    while True:
        nilai = input(f"  {label} (angka polos, contoh 10000): ").strip()
        if not nilai.isdigit():
            print("  Tanpa titik, koma, atau Rp. 10.000 -> tulis 10000.")
            continue
        break
    return int(nilai)


def isi_pilihan(label, pilihan):
    while True:
        nilai = input(f"  {label} {'/'.join(pilihan)}: ").strip()
        sah = ""
        for p in pilihan:
            if nilai.lower() == p.lower():
                sah = p
        if sah == "":
            print("  Pilihan tidak dikenal. Coba lagi.")
            continue
        break
    return sah


def isi_kategori():
    bentuk = isi_pilihan("Bentuk", BENTUK)
    pembaca = isi_pilihan("Pembaca", PEMBACA)
    subjek = isi_pilihan("Subjek", SUBJEK)
    return f"{bentuk}-{pembaca}-{subjek}"


def isi_catatan(kondisi):
    if kondisi in WAJIB_CATATAN:
        print(f"  Kondisi {kondisi}: aturan IOBA mewajibkan cacat dicatat.")
        return isi_teks("Sebutkan cacatnya")
    return isi_teks("Catatan (boleh kosong)", False)


# 5. Fungsi Tampilan

def tabel(daftar, judul):
    print(f"\n=== {judul} ===")
    if len(daftar) == 0:
        print("(tidak ada data)\n")
        return
    print("-" * 70)
    print("ID\t|Judul\t\t|Kategori\t|Kondisi\t|Harga\t|Status")
    print("-" * 70)
    for b in daftar:
        print(f"{b['id']}\t|{b['judul'][:15]}\t|{b['kategori']}\t|"
              f"{b['kondisi']}\t\t|{b['jual']:,}\t|{b['status']}")
    print("-" * 70)
    print(f"Jumlah: {len(daftar)} buku\n")


def rincian(b):
    margin = b["jual"] - b["beli"]
    print("\n== Rincian Buku ==")
    print(f"{b['id']} | {b['judul']} - {b['penulis']}")
    print(f"Kategori\t: {b['kategori']}")
    print(f"Kondisi\t\t: {b['kondisi']}")
    print(f"Modal / Jual\t: Rp{b['beli']:,} -> Rp{b['jual']:,}")
    print(f"Margin\t\t: Rp{margin:,}")
    print(f"Status\t\t: {b['status']}")
    print(f"Catatan\t\t: {b['catatan']}\n")


def minta_buku(daftar):
    hasil = cari(daftar, "id", isi_teks("ID buku"))
    if len(hasil) == 0:
        print("  ID tidak ditemukan.\n")
        return None
    return hasil[0]


# 6. CREATE - Tambah Buku Masuk
# Dipakai saat satu buku fisik masuk gudang. Borongan 3 buku judul sama
# berarti fungsi ini dijalankan 3 kali. Harga beli wajib dicatat sekarang,
# karena setelah bercampur di rak modalnya tidak bisa dilacak lagi.

def tambah(daftar):
    print("\n== Tambah Buku Masuk ==")
    print("Satu data = satu buku fisik.")

    b = {}
    b["id"] = f"BK{len(daftar) + 1:03d}"
    b["judul"] = isi_teks("Judul").title()
    b["penulis"] = isi_teks("Penulis").title()
    b["kategori"] = isi_kategori()
    b["kondisi"] = isi_pilihan("Kondisi", KONDISI)
    b["beli"] = isi_angka("Harga beli")
    b["jual"] = isi_angka("Harga jual")

    if b["jual"] <= b["beli"]:
        print("  Catatan: harga jual tidak di atas modal.")

    b["status"] = "tersedia"
    b["catatan"] = isi_catatan(b["kondisi"])

    daftar.append(b)
    print(f"\n{b['id']} tercatat, status tersedia.\n")


# 7. READ - Lihat Stok dan Laporan

def lihat(daftar):
    tabel(daftar, "Rekapitulasi Stok Buku")

    terjual = cari(daftar, "status", "terjual")
    depresiasi = cari(daftar, "status", "depresiasi")

    omzet = total(terjual, "jual")
    laba = omzet - total(terjual, "beli")
    rugi = total(depresiasi, "beli")

    print("== Posisi Stok ==")
    for s in STATUS:
        print(f"{s}\t\t: {len(cari(daftar, 'status', s))} buku")

    print("\n== Laporan Keuangan ==")
    print(f"Modal koleksi\t: Rp{total(daftar, 'beli'):,}")
    print(f"Omzet\t\t: Rp{omzet:,}")
    print(f"Laba kotor\t: Rp{laba:,}")
    print(f"Rugi depresiasi\t: Rp{rugi:,}")
    print(f"Laba bersih\t: Rp{laba - rugi:,}")

    if omzet > 0:
        persen_margin = (laba / omzet) * 100
        print(f"Margin\t\t: {persen_margin:.1f}%")
    print()


# 8. SEARCH - Cari dan Cek Ketersediaan
# Dipakai saat pembeli bertanya "buku X masih ada?". Satu kata kunci
# dicek ke judul, penulis, dan kode kategori sekaligus, jadi "orwell",
# "animal", maupun "ANK" sama-sama bisa dipakai.

def cek(daftar):
    print("\n== Cari / Cek Stok ==")
    kata = isi_teks("Kata kunci judul / penulis / kode kategori").lower()

    hasil = []
    for b in daftar:
        gabungan = b["judul"] + b["penulis"] + b["kategori"]
        if kata in gabungan.lower():
            hasil.append(b)

    tabel(hasil, f"Hasil Pencarian '{kata}'")

    siap = cari(hasil, "status", "tersedia")
    if len(siap) > 0:
        print(f"JAWABAN: masih ada {len(siap)} buku.")
        for b in siap:
            print(f"{b['id']}\t|Rp{b['jual']:,}\t|kondisi {b['kondisi']}"
                  f"\t|{b['catatan']}")
    else:
        print("JAWABAN: judul ini sedang kosong.")
    print()


# 9. UPDATE - Ubah Data Buku
# Paling sering dipakai untuk mengubah status:
#   tersedia -> dibooking -> terjual, atau apa pun -> depresiasi.
# Juga untuk menurunkan harga dan merevisi kondisi.
# Harga beli TIDAK PERNAH diubah, itu fakta historis dasar hitung margin.

def ubah(daftar):
    tabel(daftar, "Daftar Buku")
    b = minta_buku(daftar)
    if b == None:
        return

    rincian(b)
    print("1. Status\t2. Harga jual\t3. Kondisi\t4. Kategori\t0. Batal")
    pilih = input("  Pilih: ").strip()

    if pilih == "1":
        status_lama = b["status"]
        b["status"] = isi_pilihan("Status", STATUS)

        if b["status"] == "terjual":
            print(f"  Margin buku ini: Rp{b['jual'] - b['beli']:,}")
        else:
            b["catatan"] = isi_teks("Catatan", False)

        if b["status"] == "depresiasi":
            print(f"  Modal hangus Rp{b['beli']:,}. Data tidak dihapus,")
            print("  supaya kerugian tetap terlihat di laporan.")

        print(f"  {status_lama} -> {b['status']}")

    elif pilih == "2":
        b["jual"] = isi_angka("Harga jual baru")
        if b["jual"] < b["beli"]:
            print("  Catatan: di bawah modal, ini jual rugi.")

    elif pilih == "3":
        b["kondisi"] = isi_pilihan("Kondisi", KONDISI)
        b["catatan"] = isi_catatan(b["kondisi"])

    elif pilih == "4":
        b["kategori"] = isi_kategori()

    else:
        print("  Dibatalkan.\n")
        return

    print("  Data diperbarui.\n")


# 10. DELETE - Hapus Data Salah Input
# Hanya untuk data yang seharusnya tidak pernah ada: duplikat, salah
# input, data uji. Buku terjual atau rusak JANGAN dihapus, ubah statusnya
# saja, supaya omzet dan kerugian tetap muncul di laporan.

def hapus(daftar):
    tabel(daftar, "Daftar Buku")
    b = minta_buku(daftar)
    if b == None:
        return

    rincian(b)
    if b["status"] == "terjual":
        print(f"  Perhatian: omzet Rp{b['jual']:,} akan hilang dari laporan.")
    elif b["status"] == "depresiasi":
        print(f"  Perhatian: kerugian Rp{b['beli']:,} akan hilang dari laporan.")

    konfirmasi = isi_teks(f"Ketik ulang '{b['id']}' untuk hapus")
    if konfirmasi.upper() == b["id"]:
        daftar.remove(b)
        print(f"  {b['id']} dihapus.\n")
    else:
        print("  Dibatalkan.\n")


# 11. Menu Utama

while True:
    print("=" * 50)
    print("\tBUKUBEKAS - Stok Toko Buku Preloved\n")
    print("1. Tambah buku masuk\t\t4. Ubah data buku")
    print("2. Lihat stok & laporan\t\t5. Hapus data salah input")
    print("3. Cari / cek stok\t\t0. Keluar")
    print("=" * 50)

    menu = input("  Pilih menu: ").strip()

    if menu == "1":
        tambah(DATA)
    elif menu == "2":
        lihat(DATA)
    elif menu == "3":
        cek(DATA)
    elif menu == "4":
        ubah(DATA)
    elif menu == "5":
        hapus(DATA)
    elif menu == "0":
        print("\nProgram selesai. Terima kasih.\n")
        break
    else:
        print("  Menu tidak ada. Masukkan angka antara 0-5.")