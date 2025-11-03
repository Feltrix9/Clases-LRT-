
import pygame, random, sys, os

# ------------------ helper: recursos seguros (sirve en .py y .exe) ------------------
def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# ------------------ init ------------------
pygame.init()
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alterna Horizontal/Vertical cada 100 puntos")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# ------------------ jugador / física ------------------
PLAYER_W, PLAYER_H = 40, 50
speed = 5
gravity = 0.6
jump_power = -12

# ------------------ sprites opcionales ------------------
USE_SPRITES = True
try:
    fondo = pygame.image.load(resource_path("sprites/Fondo.png")).convert()
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    plataforma_img = pygame.image.load(resource_path("sprites/plataforma.png")).convert_alpha()
    plataforma_img = pygame.transform.scale(plataforma_img, (110, 18))
    sprite_idle = pygame.image.load(resource_path("sprites/jugador_idle.png")).convert_alpha()
    sprite_jump = pygame.image.load(resource_path("sprites/jugador_jump.png")).convert_alpha()
    sprite_idle = pygame.transform.scale(sprite_idle, (PLAYER_W, PLAYER_H))
    sprite_jump = pygame.transform.scale(sprite_jump, (PLAYER_W, PLAYER_H))
except Exception:
    USE_SPRITES = False
AZUL = (135, 206, 235)
VERDE = (0, 200, 0)
NEGRO = (15, 15, 15)
ROJO = (200, 50, 50)

# ------------------ clases ------------------
class Plataforma:
    def __init__(self, x, y, w=110, h=18):
        self.rect = pygame.Rect(x, y, w, h)
    def draw(self, surf):
        if USE_SPRITES:
            surf.blit(plataforma_img, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(surf, VERDE, self.rect)

# ------------------ estado global del juego ------------------
mode = "H"  # "H" horizontal, "V" vertical (se alterna cada 100 puntos)
x = 0
y = 0
vel_x = 0
vel_y = 0
on_ground = False
plataformas = []

# puntuación
total_score = 0          # puntaje total mostrado
segment_score = 0        # puntaje desde el último cambio (0..100)
scroll_accum = 0         # píxeles acumulados de scroll de este segmento (para calcular puntos)
POINTS_PER_PIXELS = 20   # 1 punto por cada 20 píxeles de avance/ascenso

# cámara
CAM_TARGET_X = int(WIDTH * 0.5)
CAM_TARGET_Y = int(HEIGHT * 0.5)

# ------------------ util: pantallas ------------------
def pantalla_gameover(puntos):
    screen.fill(ROJO)
    t1 = font.render("GAME OVER", True, NEGRO)
    t2 = font.render(f"Puntaje total: {puntos}", True, NEGRO)
    t3 = font.render("R: reiniciar  |  Q: salir", True, NEGRO)
    screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 220))
    screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 260))
    screen.blit(t3, (WIDTH//2 - t3.get_width()//2, 300))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_r:
                    main()

# ------------------ generadores de plataformas ------------------
def setup_horizontal():
    global x, y, vel_x, vel_y, on_ground, plataformas, scroll_accum, segment_score
    x, y = 100, HEIGHT - 100
    vel_x = 0
    vel_y = 0
    on_ground = False
    scroll_accum = 0
    segment_score = 0
    plataformas = []
    # suelo largo
    plataformas.append(Plataforma(-200, HEIGHT - 20, WIDTH + 400, 20))
    current_x = 50
    for _ in range(10):
        gap = random.randint(80, 140)
        plat_y = random.randint(HEIGHT//2, HEIGHT - 120)
        current_x += gap
        plataformas.append(Plataforma(current_x, plat_y))

def setup_vertical():
    global x, y, vel_x, vel_y, on_ground, plataformas, scroll_accum, segment_score
    x, y = WIDTH // 2 - PLAYER_W // 2, HEIGHT - 100
    vel_x = 0
    vel_y = 0
    on_ground = False
    scroll_accum = 0
    segment_score = 0
    plataformas = []
    # plataforma piso
    plataformas.append(Plataforma(0, HEIGHT - 20, WIDTH, 20))
    # “columna” hacia arriba
    base_y = HEIGHT - 120
    for _ in range(7):
        px = random.randint(0, WIDTH - 110)
        plataformas.append(Plataforma(px, base_y))
        base_y -= random.randint(80, 120)

def generar_plataformas_derecha():
    # Mantener ~12 en pantalla y agregar a la derecha del máximo
    if len(plataformas) < 12:
        max_x = max(p.rect.right for p in plataformas)
        for _ in range(4):
            gap = random.randint(90, 160)
            new_x = max_x + gap
            new_y = random.randint(HEIGHT//2, HEIGHT - 130)
            plataformas.append(Plataforma(new_x, new_y))
            max_x = new_x + 110

def generar_plataformas_arriba():
    # Mantener ~10 y agregar por encima del mínimo y
    while len(plataformas) < 10:
        min_y = min(p.rect.y for p in plataformas)
        px = random.randint(0, WIDTH - 110)
        py = min_y - random.randint(80, 120)
        plataformas.append(Plataforma(px, py))

# ------------------ lógica de puntaje/cambio de modo ------------------
def acumular_puntaje_por_scroll(pixels):
    """pixels > 0: sumar al scroll acumulado, convertir en puntos para total y segmento"""
    global total_score, segment_score, scroll_accum, mode
    scroll_accum += pixels
    # puntos ganados desde el último cálculo
    gained = scroll_accum // POINTS_PER_PIXELS
    if gained > 0:
        total_score += gained
        segment_score += gained
        scroll_accum -= gained * POINTS_PER_PIXELS
        # ¿cambio de modo?
        if segment_score >= 100:
            # alternar modo
            if mode == "H":
                mode = "V"
                setup_vertical()
            else:
                mode = "H"
                setup_horizontal()

# ------------------ bucle principal ------------------
def main():
    global x, y, vel_x, vel_y, on_ground, mode

    # arranca en horizontal
    mode = "H"
    setup_horizontal()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # entrada horizontal/vertical (izq-der igual; salto con espacio)
        vel_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * speed
        if keys[pygame.K_SPACE] and on_ground:
            vel_y = jump_power
            on_ground = False

        # física
        vel_y += gravity
        x += vel_x
        y += vel_y

        jugador = pygame.Rect(x, y, PLAYER_W, PLAYER_H)

        # colisiones (solo hacia abajo)
        on_ground = False
        for p in plataformas:
            if jugador.colliderect(p.rect) and vel_y >= 0:
                y = p.rect.top - PLAYER_H
                vel_y = 0
                on_ground = True
                break

        # cámara y generación según modo
        if mode == "H":
            # cámara horizontal: si el jugador pasa CAM_TARGET_X, empujar mundo a la izquierda
            if x > CAM_TARGET_X:
                dx = x - CAM_TARGET_X
                x = CAM_TARGET_X
                for p in plataformas:
                    p.rect.x -= int(dx)
                # puntaje por avance horizontal
                acumular_puntaje_por_scroll(int(dx))
            # mantenimiento plataformas
            generar_plataformas_derecha()
            # limpiar muy a la izquierda
            plataformas[:] = [p for p in plataformas if p.rect.right > -200]
        else:
            # cámara vertical: si el jugador sube más allá de CAM_TARGET_Y, empujar mundo hacia abajo
            if y < CAM_TARGET_Y:
                dy = CAM_TARGET_Y - y
                y = CAM_TARGET_Y
                for p in plataformas:
                    p.rect.y += int(dy)
                # puntaje por ascenso vertical
                acumular_puntaje_por_scroll(int(dy))
            # generar arriba y limpiar abajo
            generar_plataformas_arriba()
            plataformas[:] = [p for p in plataformas if p.rect.y < HEIGHT + 60]

        # condiciones de derrota (caer por abajo)
        if y > HEIGHT:
            pantalla_gameover(total_score)

        # ------------------ dibujo ------------------
        if USE_SPRITES:
            screen.blit(fondo, (0, 0))
        else:
            screen.fill(AZUL)

        for p in plataformas:
            p.draw(screen)

        if USE_SPRITES:
            sprite = sprite_idle if on_ground else sprite_jump
            screen.blit(sprite, (x, y))
        else:
            pygame.draw.rect(screen, NEGRO, jugador)

        # HUD
        modo_txt = "Horizontal" if mode == "H" else "Vertical"
        to_next = 100 - segment_score
        hud1 = font.render(f"Puntos: {total_score}", True, (0, 0, 0))
        hud2 = font.render(f"Modo: {modo_txt}", True, (0, 0, 0))
        hud3 = font.render(f"Para cambiar: {to_next}", True, (0, 0, 0))
        screen.blit(hud1, (10, 10))
        screen.blit(hud2, (10, 40))
        screen.blit(hud3, (10, 70))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
