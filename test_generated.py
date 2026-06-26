def mlebu(prompt=''): return input(prompt)
def mlebu_angka(prompt=''):
    try:
        return float(input(prompt))
    except ValueError:
        return 0.0

def tambah(a, b):
    return (a + b)

print("============================")
print("  Program BosoJowo Sederhana")
print("============================")
batas = 5
angka = 1
while (angka <= batas):
    if (angka == 3):
        print("Angka 3 - Iki tengah-tengah")
    else:
        print("Angka saiki:")
        print(angka)
    angka = tambah(angka, 1)
print("Program rampung!")
mlebu("Pencet Enter kanggo nutup...")