# Ejercicio 3: Ruta en grilla 5x5
def dentro(x, y):
    return 0 <= x < 5 and 0 <= y < 5

def main():
    ruta = input().strip().upper()
    x, y = 0, 0
    validos = 0
    for m in ruta:
        nx, ny = x, y
        if m == 'U': ny -= 1
        elif m == 'D': ny += 1
        elif m == 'L': nx -= 1
        elif m == 'R': nx += 1
        if dentro(nx, ny):
            x, y = nx, ny
            validos += 1
    print(f"POSICION_FINAL: ({x},{y})")
    print(f"PASOS_VALIDOS: {validos}")

if __name__ == "__main__":
    main()
