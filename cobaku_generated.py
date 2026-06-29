def mlebu(prompt=''): return input(prompt)
def mlebu_angka(prompt=''):
    try:
        return float(input(prompt))
    except ValueError:
        return 0.0

def main():
    print("Halo! Ini program pertamaku!")
    nama = "Galuh"
    print("Nama saya:")
    print(nama)
    angka = 5
    if (angka > 3):
        print("Angkanya besar!")
    else:
        print("Angkanya kecil!")

main()