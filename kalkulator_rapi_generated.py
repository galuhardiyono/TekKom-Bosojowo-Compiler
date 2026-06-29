def mlebu(prompt=''): return input(prompt)
def mlebu_angka(prompt=''):
    try:
        return float(input(prompt))
    except ValueError:
        return 0.0

def tambah(a, b):
    return (a + b)

def kurang(a, b):
    return (a - b)

def ping(a, b):
    return (a * b)

def poro(a, b):
    return (a / b)

def tampil_menu():
    print("===================================")
    print("       KALKULATOR BOSO JOWO")
    print("===================================")
    print("1. Tambah  (+)  → Nambah angka")
    print("2. Sudo    (-)  → Ngurangi angka")
    print("3. Ping    (*)  → Ngalino angka")
    print("4. Poro    (/)  → Mbagi angka")
    print("===================================")

def main():
    tampil_menu()
    pilihan = mlebu_angka("Pilihno operasi (1/2/3/4)  : ")
    angka1 = mlebu_angka("Lebokno angka kapisan      : ")
    angka2 = mlebu_angka("Lebokno angka kapindho     : ")
    hasil = 0
    if (pilihan == 1):
        hasil = tambah(angka1, angka2)
        print("Operasine  : Tambah (+)")
    else:
        if (pilihan == 2):
            hasil = kurang(angka1, angka2)
            print("Operasine  : Sudo (-)")
        else:
            if (pilihan == 3):
                hasil = ping(angka1, angka2)
                print("Operasine  : Ping (*)")
            else:
                if (pilihan == 4):
                    hasil = poro(angka1, angka2)
                    print("Operasine  : Poro (/)")
                else:
                    print("Pilihan ora ono! Pilihno maneh 1-4.")
    if ((pilihan >= 1) and (pilihan <= 4)):
        print("-----------------------------------")
        print("Hasile yaiku:")
        print(hasil)
        print("===================================")
    mlebu("Pencet Enter kanggo nutup...")

main()