def mlebu(prompt=''): return input(prompt)
def mlebu_angka(prompt=''):
    try:
        return float(input(prompt))
    except ValueError:
        return 0.0

print("===============================")
print("       KALKULATOR JOWO")
print("===============================")
print("1. Tambah (+)")
print("2. Sudo (-)")
print("3. Ping (*)")
print("4. Poro (/)")
print("===============================")
pilihan = mlebu_angka("Pilih operasi (1/2/3/4): ")
angka1 = mlebu_angka("Lebokno angka pertama: ")
angka2 = mlebu_angka("Lebokno angka keloro: ")
hasil = 0
if (pilihan == 1):
    hasil = (angka1 + angka2)
else:
    if (pilihan == 2):
        hasil = (angka1 - angka2)
    else:
        if (pilihan == 3):
            hasil = (angka1 * angka2)
        else:
            if (pilihan == 4):
                hasil = (angka1 / angka2)
            else:
                print("Pilihan ora ono!")
if ((pilihan >= 1) and (pilihan <= 4)):
    print("Hasile iku: ")
    print(hasil)
mlebu("Pencet Enter kanggo nutup...")