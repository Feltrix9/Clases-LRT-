import pygame, random

pygame.init()
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plataformas con Scroll")
clock = pygame.time.Clock()

# Colores
AZUL = (135, 206, 235)
ROJO = (255, 0, 0)
VERDE = (0, 200, 0)

# Jugador
player_w, player_h = 50, 50
x, y = WIDTH // 2, HEIGHT - player_h - 10
vel_y = 0
gravity = 0.5
jump_power = -12
on_ground = False

# Plataformas iniciales
plataformas = [pygame.Rect(0, HEIGHT - 20, WIDTH, 20)]  # piso inicial
for i in range(6):  # generar varias al inicio
    px = random.randint(0, WIDTH - 100)
    py = HEIGHT - (i * 100) - 100
    plataformas.append(pygame.Rect(px, py, 100, 15))

scroll_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 5
    if keys[pygame.K_RIGHT]:
        x += 5
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump_power
        on_ground = False

    # Movimiento vertical
    vel_y += gravity
    y += vel_y

    jugador = pygame.Rect(x, y, player_w, player_h)

    # Colisiones con plataformas
    on_ground = False
    for plataforma in plataformas:
        if jugador.colliderect(plataforma) and vel_y >= 0:
            y = plataforma.top - player_h
            vel_y = 0
            on_ground = True

    # Scroll: si el jugador sube más de la mitad de la pantalla
    if y < HEIGHT // 2:
        scroll_y = HEIGHT // 2 - y
        y = HEIGHT // 2
        for plataforma in plataformas:
            plataforma.y += scroll_y

    # Generar nuevas plataformas arriba
    while len(plataformas) < 8:
        px = random.randint(0, WIDTH - 100)
        py = plataformas[-1].y - random.randint(80, 120)
        plataformas.append(pygame.Rect(px, py, 100, 15))

    # Borrar plataformas que caen fuera de la pantalla
    plataformas = [p for p in plataformas if p.y < HEIGHT]

    # Dibujar
    screen.fill(AZUL)
    for plataforma in plataformas:
        pygame.draw.rect(screen, VERDE, plataforma)
    pygame.draw.rect(screen, ROJO, jugador)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
