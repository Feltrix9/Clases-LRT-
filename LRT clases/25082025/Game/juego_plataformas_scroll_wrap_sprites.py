import pygame, random

pygame.init()
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LRT game Saltar/ pou")
clock = pygame.time.Clock()

# Colores
AZUL = (135, 206, 235)
VERDE = (0, 200, 0)

# Jugador
PLAYER_W, PLAYER_H = 40, 50
x, y = WIDTH // 2 - PLAYER_W // 2, HEIGHT - PLAYER_H - 10
vel_x, vel_y = 0, 0
speed = 5
gravity = 0.5
jump_power = -12
on_ground = False

# Cargar sprites del jugador
sprite_idle = pygame.image.load("\25082025\Game\jugador_idle.png").convert_alpha()
sprite_jump = pygame.image.load("\25082025\Game\jugador_jump.png").convert_alpha()


# Escalar al tamaño definido del jugador
sprite_idle = pygame.transform.scale(sprite_idle, (PLAYER_W, PLAYER_H))
sprite_jump = pygame.transform.scale(sprite_jump, (PLAYER_W, PLAYER_H))

# Plataformas iniciales
plataformas = [pygame.Rect(0, HEIGHT - 20, WIDTH, 20)]
for i in range(6):
    px = random.randint(0, WIDTH - 110)
    py = HEIGHT - (i * 100) - 120
    plataformas.append(pygame.Rect(px, py, 110, 18))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    vel_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * speed

    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump_power
        on_ground = False

    # Física
    vel_y += gravity
    x += vel_x
    y += vel_y

    jugador = pygame.Rect(x, y, PLAYER_W, PLAYER_H)

    # Wrap horizontal
    if jugador.left > WIDTH:
        x = -PLAYER_W
    elif jugador.right < 0:
        x = WIDTH

    # Colisiones con plataformas (solo si cae)
    on_ground = False
    for p in plataformas:
        if jugador.colliderect(p) and vel_y >= 0:
            y = p.top - PLAYER_H
            vel_y = 0
            on_ground = True

    # Scroll vertical
    if y < HEIGHT // 2:
        shift = HEIGHT // 2 - y
        y = HEIGHT // 2
        for p in plataformas:
            p.y += shift

    # Nuevas plataformas arriba
    while len(plataformas) < 10:
        px = random.randint(0, WIDTH - 110)
        py = min(p.y for p in plataformas) - random.randint(80, 120)
        plataformas.append(pygame.Rect(px, py, 110, 18))

    # Eliminar plataformas que caen muy abajo
    plataformas = [p for p in plataformas if p.y < HEIGHT + 40]

    # Dibujo
    screen.fill(AZUL)
    for p in plataformas:
        pygame.draw.rect(screen, VERDE, p)

    # Dibujar sprite según estado
    sprite = sprite_idle if on_ground else sprite_jump
    screen.blit(sprite, (x, y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
