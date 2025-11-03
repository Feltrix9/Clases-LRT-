import pygame, random, sys

pygame.init()
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plataformas con movimiento lateral + puntaje")
clock = pygame.time.Clock()

# Jugador
PLAYER_W, PLAYER_H = 40, 50
x, y = WIDTH // 2 - PLAYER_W // 2, HEIGHT - PLAYER_H - 10
vel_x, vel_y = 0, 0
speed = 5
gravity = 0.5
jump_power = -12
on_ground = False
plataforma_bajo_pies = None  # para “llevar” al jugador con la plataforma

# --- Sprites (ajusta rutas) ---
fondo = pygame.image.load("Game/sprites/Fondo.png").convert()
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

pasto = pygame.image.load("sprites/pasto.png").convert_alpha()
pasto = pygame.transform.scale(pasto, (WIDTH, 40))

plataforma_img = pygame.image.load("sprites/plataforma.png").convert_alpha()
plataforma_img = pygame.transform.scale(plataforma_img, (110, 18))

sprite_idle = pygame.image.load("sprites/jugador_idle.png").convert_alpha()
sprite_jump = pygame.image.load("sprites/jugador_jump.png").convert_alpha()
sprite_idle = pygame.transform.scale(sprite_idle, (PLAYER_W, PLAYER_H))
sprite_jump = pygame.transform.scale(sprite_jump, (PLAYER_W, PLAYER_H))

# --- Plataforma con movimiento lateral opcional ---
class Plataforma:
    def __init__(self, x, y, w=110, h=18, move=False, speed=2, rango=80):
        self.rect = pygame.Rect(x, y, w, h)
        self.move = move
        self.speed = speed if move else 0
        self.rango = rango
        self.origen_x = x
        self.dir = 1  # 1 derecha, -1 izquierda

    def update(self):
        """Mueve y devuelve el desplazamiento horizontal (dx) de esta frame."""
        if not self.move:
            return 0
        old_x = self.rect.x
        self.rect.x += self.speed * self.dir
        # rebotar al llegar al rango
        if abs(self.rect.x - self.origen_x) > self.rango:
            self.dir *= -1
            # corregir exceso para no ‘salirse’ del rango
            self.rect.x = self.origen_x + self.rango * self.dir * -1
        return self.rect.x - old_x

    def draw(self, surf):
        surf.blit(plataforma_img, (self.rect.x, self.rect.y))

# Crear plataformas iniciales
plataformas = [Plataforma(0, HEIGHT - 20, WIDTH, 20, move=False)]  # suelo base
for i in range(6):
    px = random.randint(0, WIDTH - 110)
    py = HEIGHT - (i * 100) - 120
    mover = (random.random() < 0.3)  # 30% se mueven
    vel = random.choice([1, 2, 3])
    rango = random.randint(60, 140)
    plataformas.append(Plataforma(px, py, 110, 18, move=mover, speed=vel, rango=rango))

# --- Puntuación por scroll ---
font = pygame.font.SysFont(None, 36)
score = 0
scroll_total = 0  # píxeles que “subió” el mundo

def pantalla_gameover(score):
    screen.fill((200, 50, 50))  # rojo
    t1 = font.render("GAME OVER", True, (0, 0, 0))
    t2 = font.render(f"Puntaje final: {score}", True, (0, 0, 0))
    t3 = font.render("R: reiniciar  |  Q: salir", True, (0, 0, 0))
    screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 200))
    screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 260))
    screen.blit(t3, (WIDTH//2 - t3.get_width()//2, 320))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_r:
                    main()  # reinicia

def generar_mas_plataformas():
    while len(plataformas) < 10:
        px = random.randint(0, WIDTH - 110)
        py = min(p.rect.y for p in plataformas) - random.randint(80, 120)
        mover = (random.random() < 0.3)
        vel = random.choice([1, 2, 3])
        rango = random.randint(60, 140)
        plataformas.append(Plataforma(px, py, 110, 18, move=mover, speed=vel, rango=rango))

def main():
    global x, y, vel_x, vel_y, on_ground, score, scroll_total, plataformas, plataforma_bajo_pies

    # reset estado
    x, y = WIDTH // 2 - PLAYER_W // 2, HEIGHT - PLAYER_H - 10
    vel_x, vel_y = 0, 0
    on_ground = False
    plataforma_bajo_pies = None
    score = 0
    scroll_total = 0

    # reset plataformas
    plataformas[:] = [Plataforma(0, HEIGHT - 20, WIDTH, 20, move=False)]
    for i in range(6):
        px = random.randint(0, WIDTH - 110)
        py = HEIGHT - (i * 100) - 120
        mover = (random.random() < 0.3)
        vel = random.choice([1, 2, 3])
        rango = random.randint(60, 140)
        plataformas.append(Plataforma(px, py, 110, 18, move=mover, speed=vel, rango=rango))

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
            plataforma_bajo_pies = None

        # Física
        vel_y += gravity
        x += vel_x
        y += vel_y

        jugador = pygame.Rect(x, y, PLAYER_W, PLAYER_H)

        # Wrap horizontal
        if jugador.left > WIDTH:
            x = -PLAYER_W
            jugador.x = x
        elif jugador.right < 0:
            x = WIDTH
            jugador.x = x

        # Actualizar plataformas (mover las que se mueven) y guardar dx
        plataformas_dx = {}
        for p in plataformas:
            dx = p.update()
            plataformas_dx[p] = dx

        # Colisiones (solo al caer)
        on_ground = False
        plataforma_bajo_pies = None
        for p in plataformas:
            if jugador.colliderect(p.rect) and vel_y >= 0:
                y = p.rect.top - PLAYER_H
                vel_y = 0
                on_ground = True
                plataforma_bajo_pies = p
                break

        # Si está sobre una plataforma móvil, arrastrar al jugador con su dx
        if on_ground and plataforma_bajo_pies is not None:
            x += plataformas_dx.get(plataforma_bajo_pies, 0)

        # Scroll vertical
        if y < HEIGHT // 2:
            shift = HEIGHT // 2 - y
            y = HEIGHT // 2
            for p in plataformas:
                p.rect.y += shift
            scroll_total += shift
            score = scroll_total // 20  # 1 punto cada 20px de scroll

        # Generar/eliminar plataformas
        generar_mas_plataformas()
        plataformas[:] = [p for p in plataformas if p.rect.y < HEIGHT + 40]

        # GAME OVER
        if y > HEIGHT:
            pantalla_gameover(score)

        # --- Dibujo ---
        screen.blit(fondo, (0, 0))
        screen.blit(pasto, (0, HEIGHT - 40))
        for p in plataformas:
            p.draw(screen)

        # Sprite jugador
        sprite = sprite_idle if on_ground else sprite_jump
        screen.blit(sprite, (x, y))

        # Puntaje
        text = font.render(f"Puntos: {score}", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()
