import pygame, random, sys

pygame.init()
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego Plataformas Mejorado + Puntaje")
clock = pygame.time.Clock()

# Jugador
PLAYER_W, PLAYER_H = 40, 50
x, y = WIDTH // 2 - PLAYER_W // 2, HEIGHT - PLAYER_H - 10
vel_x, vel_y = 0, 0
speed = 5
gravity = 0.5
jump_power = -12
on_ground = False

# --- Sprites ---
fondo = pygame.image.load("09\8092025\Game\sprites\Fondo.png").convert()
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

pasto = pygame.image.load("09\8092025\Game\sprites\pasto.png").convert_alpha()
pasto = pygame.transform.scale(pasto, (WIDTH, 40))

plataforma_img = pygame.image.load("09\8092025\Game\sprites\plataforma.png").convert_alpha()
plataforma_img = pygame.transform.scale(plataforma_img, (110, 18))

sprite_idle = pygame.image.load("09\8092025\Game\sprites\jugador_idle.png").convert_alpha()
sprite_jump = pygame.image.load("09\8092025\Game\sprites\jugador_jump.png").convert_alpha()
sprite_idle = pygame.transform.scale(sprite_idle, (PLAYER_W, PLAYER_H))
sprite_jump = pygame.transform.scale(sprite_jump, (PLAYER_W, PLAYER_H))

# Plataformas iniciales
plataformas = [pygame.Rect(0, HEIGHT - 20, WIDTH, 20)]
for i in range(6):
    px = random.randint(0, WIDTH - 110)
    py = HEIGHT - (i * 100) - 120
    plataformas.append(pygame.Rect(px, py, 110, 18))

# --- Sistema de puntuación ---
font = pygame.font.SysFont(None, 36)
score = 0
scroll_total = 0  # acumulador de scroll hacia arriba

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
        scroll_total += shift
        score = scroll_total // 20  # cada 20px de scroll suma 1 punto

    # Nuevas plataformas arriba
    while len(plataformas) < 10:
        px = random.randint(0, WIDTH - 110)
        py = min(p.y for p in plataformas) - random.randint(80, 120)
        plataformas.append(pygame.Rect(px, py, 110, 18))

    # Eliminar plataformas que caen muy abajo
    plataformas = [p for p in plataformas if p.y < HEIGHT + 40]

    # --- GAME OVER ---
    if y > HEIGHT:
        print(f"Game Over: caíste de la última plataforma. Puntaje final: {score}")
        pygame.quit()
        sys.exit()

    # --- Dibujo ---
    screen.blit(fondo, (0, 0))
    screen.blit(pasto, (0, HEIGHT - 40))

    for p in plataformas:
        screen.blit(plataforma_img, (p.x, p.y))

    sprite = sprite_idle if on_ground else sprite_jump
    screen.blit(sprite, (x, y))

    # Mostrar puntaje en pantalla
    text = font.render(f"Puntos: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
