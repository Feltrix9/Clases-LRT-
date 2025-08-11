import pygame

# Inicializar pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego con Plataformas")
clock = pygame.time.Clock()

# Colores
AZUL_CIELO = (135, 206, 235)
ROJO = (255, 0, 0)
VERDE = (0, 200, 0)

# Jugador
x, y = 50, 500
width, height = 50, 50
vel_y = 0
gravity = 0.5
jump_power = -10
on_ground = False

# Plataformas (rectángulos)
plataformas = [
    pygame.Rect(0, 550, 800, 50),   # piso
    pygame.Rect(200, 400, 150, 20), # plataforma 1
    pygame.Rect(500, 300, 150, 20)  # plataforma 2
]

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento lateral
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 5
    if keys[pygame.K_RIGHT]:
        x += 5

    # Salto
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump_power
        on_ground = False

    # Aplicar gravedad
    vel_y += gravity
    y += vel_y

    # Crear rectángulo del jugador
    jugador = pygame.Rect(x, y, width, height)

    # Comprobar colisiones
    on_ground = False
    for plataforma in plataformas:
        if jugador.colliderect(plataforma) and vel_y >= 0:
            y = plataforma.top - height  # Colocar encima
            vel_y = 0
            on_ground = True

    # Dibujar
    screen.fill(AZUL_CIELO)
    for plataforma in plataformas:
        pygame.draw.rect(screen, VERDE, plataforma)
    pygame.draw.rect(screen, ROJO, (x, y, width, height))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
