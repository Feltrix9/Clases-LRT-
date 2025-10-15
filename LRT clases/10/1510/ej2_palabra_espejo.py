# Ejercicio 2: Palabra espejo
def main():
    palabra = input().strip()
    reversa = palabra[::-1]
    print("AL_REVES:", reversa)
    print("PALINDROMO: SI" if palabra == reversa else "PALINDROMO: NO")

if __name__ == "__main__":
    main()
