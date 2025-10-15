# Ejercicio 1: Contador de pares e impares
def main():
    N = int(input().strip())
    numeros = [int(input().strip()) for _ in range(N)]
    pares = [n for n in numeros if n % 2 == 0]
    impares = [n for n in numeros if n % 2 != 0]
    print("PARES:", len(pares))
    print("IMPARES:", len(impares))
    print("LISTA_PARES:", sorted(pares))

if __name__ == "__main__":
    main()
