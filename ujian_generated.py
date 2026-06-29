def mlebu(prompt=''): return input(prompt)
def mlebu_angka(prompt=''):
    try:
        return float(input(prompt))
    except ValueError:
        return 0.0

def tambah(a, b):
    return (a + b)

def main():
    print("=== Ujian Akhir Boso Jowo ===")
    angka_awal = 1
    while (angka_awal <= 3):
        print("Iterasi ke-")
        print(angka_awal)
        angka_awal = (angka_awal + 1)
    tes_optimasi = 52
    if (tes_optimasi > 50):
        print("Optimasi Matematika Berhasil!")
    else:
        print("Gagal Optimasi")
    hasil = tambah(10, 20)
    print("Hasil Tambah:")
    print(hasil)

main()