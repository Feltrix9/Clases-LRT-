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
fondo = pygame.image.load("Game\sprites\Fondo.png").convert()
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

pasto = pygame.image.load("Game\sprites\pasto.png").convert_alpha()
pasto = pygame.transform.scale(pasto, (WIDTH, 40))

plataforma_img = pygame.image.load("Game\sprites\plataforma.png").convert_alpha()
plataforma_img = pygame.transform.scale(plataforma_img, (110, 18))

sprite_idle = pygame.image.load("Game\sprites\jugador_idle.png").convert_alpha()
sprite_jump = pygame.image.load("Game\sprites\jugador_jump.png").convert_alpha()
sprite_idle = pygame.transform.scale(sprite_idle, (PLAYER_W, PLAYER_H))
sprite_jump = pygame.transform.scale(sprite_jump, (PLAYER_W, PLAYER_H))


# --- Sistema de puntuación ---
font = pygame.font.SysFont(None, 36)
score = 0
scroll_total = 0  # acumulador de scroll hacia arriba

# Función para pantalla final
def pantalla_gameover(score):
    screen.fill((200, 50, 50))  # rojo
    text1 = font.render("GAME OVER", True, (0, 0, 0))
    text2 = font.render(f"Puntaje final: {score}", True, (0, 0, 0))
    text3 = font.render("Presiona R para reiniciar o Q para salir", True, (0, 0, 0))
    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, 200))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, 260))
    screen.blit(text3, (WIDTH//2 - text3.get_width()//2, 320))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar
                    waiting = False
                    main()
                elif event.key == pygame.K_q:  # Salir
                    pygame.quit(); sys.exit()

# --- Juego principal ---
def main():
    global x, y, vel_x, vel_y, on_ground, score, scroll_total, plataformas

    # Reset
    x, y = WIDTH // 2 - PLAYER_W // 2, HEIGHT - PLAYER_H - 10
    vel_x, vel_y = 0, 0
    on_ground = False
    score = 0
    scroll_total = 0

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

        vel_y += gravity
        x += vel_x
        y += vel_y

        jugador = pygame.Rect(x, y, PLAYER_W, PLAYER_H)

        # Wrap horizontal
        if jugador.left > WIDTH:
            x = -PLAYER_W
        elif jugador.right < 0:
            x = WIDTH

        # Colisiones
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
            score = scroll_total // 20

        # Nuevas plataformas
        while len(plataformas) < 10:
            px = random.randint(0, WIDTH - 110)
            py = min(p.y for p in plataformas) - random.randint(80, 120)
            plataformas.append(pygame.Rect(px, py, 110, 18))

        plataformas[:] = [p for p in plataformas if p.y < HEIGHT + 40]

        # GAME OVER
        if y > HEIGHT:
            pantalla_gameover(score)

        # Dibujos
        screen.blit(fondo, (0, 0))
        screen.blit(pasto, (0, HEIGHT - 40))

        for p in plataformas:
            screen.blit(plataforma_img, (p.x, p.y))

        sprite = sprite_idle if on_ground else sprite_jump
        screen.blit(sprite, (x, y))

        text = font.render(f"Puntos: {score}", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()
