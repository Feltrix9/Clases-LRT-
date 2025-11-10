import pygame, random, sys, time

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
fondo = pygame.image.load("sprites\Fondo.png").convert()
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

pasto = pygame.image.load("sprites\pasto.png").convert_alpha()
pasto = pygame.transform.scale(pasto, (WIDTH, 40))

plataforma_img = pygame.image.load("sprites\plataforma.png").convert_alpha()
plataforma_img = pygame.transform.scale(plataforma_img, (110, 18))

# Sprite para plataformas que desaparecen (puedes crear una imagen diferente o usar esta temporal)
plataforma_des_img = pygame.Surface((110, 18), pygame.SRCALPHA)
plataforma_des_img.fill((255, 100, 100, 255))  # Rojo semitransparente

sprite_idle = pygame.image.load("sprites\jugador_idle.png").convert_alpha()
sprite_jump = pygame.image.load("sprites\jugador_jump.png").convert_alpha()
sprite_idle = pygame.transform.scale(sprite_idle, (PLAYER_W, PLAYER_H))
sprite_jump = pygame.transform.scale(sprite_jump, (PLAYER_W, PLAYER_H))

# --- Sistema de puntuación ---
font = pygame.font.SysFont(None, 36)
score = 0
scroll_total = 0  # acumulador de scroll hacia arriba


# --- Clase para plataformas que desaparecen ---
class PlataformaDesaparecedora:
    def __init__(self, x, y, width=110, height=18):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = True

    def update(self, jugador, vel_y):
        # Solo verificar colisión si la plataforma está activa
        if self.active and jugador.colliderect(self.rect) and vel_y >= 0:
            # La plataforma desaparece cuando es pisada
            self.active = False
            # No permite saltar - retornamos False para indicar que no hay rebote
            return False
        return True

    def draw(self, screen):
        if self.active:
            screen.blit(plataforma_des_img, (self.rect.x, self.rect.y))


##pygame.mixer.init()
##pygame.mixer.music.load()
##pygame.mixer.music.play()


# --- Pantalla de pausa ---
def pantalla_pausa():
    pausa = True

    # Crear una superficie semitransparente
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Negro semitransparente

    while pausa:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Presionar P para quitar pausa
                    pausa = False
                elif event.key == pygame.K_q:  # Salir del juego desde pausa
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:  # Reiniciar
                    waiting = False
                    main()

        # Dibujar el overlay semitransparente
        screen.blit(overlay, (0, 0))

        # Texto de pausa
        texto_pausa = font.render("PAUSA", True, (255, 255, 255))
        texto_instrucciones = font.render("Presiona P para continuar", True, (255, 255, 255))
        texto_salir = font.render("Presiona Q para salir", True, (255, 255, 255))
        texto_reiniciar = font.render("Presiona R para reiniciar", True, (255, 255, 255))

        screen.blit(texto_pausa, (WIDTH // 2 - texto_pausa.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(texto_instrucciones, (WIDTH // 2 - texto_instrucciones.get_width() // 2, HEIGHT // 2))
        screen.blit(texto_salir, (WIDTH // 2 - texto_salir.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(60)


# Función para pantalla final
def pantalla_gameover(score):
    screen.fill((1, 75, 160))
    text1 = font.render("GAME OVER", True, (0, 0, 0))
    text2 = font.render(f"Puntaje final: {score}", True, (0, 0, 0))
    text3 = font.render("Presiona R para reiniciar o Q para salir", True, (0, 0, 0))
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, 200))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 260))
    screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, 320))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar
                    waiting = False
                    main()
                elif event.key == pygame.K_q:  # Salir
                    pygame.quit();
                    sys.exit()


# --- Función mejorada para generar plataformas ---
def generar_plataformas(plataformas, plataformas_desaparecedoras, min_total=8):  # Reducido a 8
    if not plataformas and not plataformas_desaparecedoras:
        return

    # Encontrar la posición Y más baja
    all_platforms_y = [p.y for p in plataformas] + [p_des.rect.y for p_des in plataformas_desaparecedoras if
                                                    p_des.active]
    py_base = min(all_platforms_y) if all_platforms_y else HEIGHT - 100

    total_actual = len(plataformas) + len([p for p in plataformas_desaparecedoras if p.active])

    while total_actual < min_total:
        px = random.randint(0, WIDTH - 110)
        py = py_base - random.randint(80, 120)

        # Obtener las últimas 3 plataformas generadas para verificar distribución
        ultimas_plataformas = []
        if plataformas:
            ultimas_plataformas.extend([('normal', p.y) for p in plataformas[-3:]])
        if plataformas_desaparecedoras:
            ultimas_plataformas.extend(
                [('desaparecedora', p.rect.y) for p in plataformas_desaparecedoras[-3:] if p.active])

        # Ordenar por posición Y (más alta primero)
        ultimas_plataformas.sort(key=lambda x: x[1])

        # REGLAS DE DISTRIBUCIÓN MEJORADA:
        es_desaparecedora = False

        # 1. Nunca poner plataforma desaparecedora al principio (primeras 2 plataformas desde abajo)
        if py > HEIGHT - 250:
            es_desaparecedora = False
        # 2. Verificar si hay plataformas desaparecedoras consecutivas
        elif len(ultimas_plataformas) >= 2:
            ultimas_dos = [tipo for tipo, y_pos in ultimas_plataformas[:2]]
            if ultimas_dos.count('desaparecedora') >= 1:  # Si hay al menos 1 desaparecedora en las últimas
                es_desaparecedora = False  # No poner otra seguida
            else:
                # 20% de probabilidad para plataformas desaparecedoras (reducida)
                es_desaparecedora = random.random() < 0.2
        else:
            # 20% de probabilidad para plataformas desaparecedoras (reducida)
            es_desaparecedora = random.random() < 0.2

        # Garantizar al menos una plataforma normal en cada grupo de 3
        plataformas_recientes = [tipo for tipo, y_pos in ultimas_plataformas[:3]]
        if plataformas_recientes.count('normal') == 0:
            es_desaparecedora = False

        if es_desaparecedora:
            plataformas_desaparecedoras.append(PlataformaDesaparecedora(px, py))
        else:
            plataformas.append(pygame.Rect(px, py, 110, 18))

        total_actual += 1
        py_base = py


# --- Juego principal ---
def main():
    global x, y, vel_x, vel_y, on_ground, score, scroll_total

    # Reset
    x, y = WIDTH // 2 - PLAYER_W // 2, HEIGHT - PLAYER_H - 10
    vel_x, vel_y = 0, 0
    on_ground = False
    score = 0
    scroll_total = 0

    # Listas separadas para plataformas normales y las que desaparecen
    plataformas = [pygame.Rect(0, HEIGHT - 20, WIDTH, 20)]  # Plataforma base
    plataformas_desaparecedoras = []

    # Generar plataformas iniciales (solo normales para el inicio)
    for i in range(4):  # Reducido a 4 plataformas iniciales
        px = random.randint(0, WIDTH - 110)
        py = HEIGHT - (i * 100) - 120
        plataformas.append(pygame.Rect(px, py, 110, 18))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Tecla P para pausa
                    pantalla_pausa()

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

        # Colisiones con plataformas normales
        on_ground = False
        for p in plataformas[:]:
            if jugador.colliderect(p) and vel_y >= 0:
                y = p.top - PLAYER_H
                vel_y = 0
                on_ground = True

        # Colisiones con plataformas que desaparecen
        for p_des in plataformas_desaparecedoras[:]:
            collision_result = p_des.update(jugador, vel_y)
            if not p_des.active:
                # Si la plataforma se desactivó, no hace nada (no permite saltar)
                pass

        # Scroll vertical
        if y < HEIGHT // 2:
            shift = HEIGHT // 2 - y
            y = HEIGHT // 2
            for p in plataformas:
                p.y += shift
            for p_des in plataformas_desaparecedoras:
                p_des.rect.y += shift
            scroll_total += shift
            score = scroll_total // 50

        # Nuevas plataformas usando la función mejorada (mínimo 8 en total)
        generar_plataformas(plataformas, plataformas_desaparecedoras, min_total=8)

        # Limpiar plataformas fuera de pantalla
        plataformas[:] = [p for p in plataformas if p.y < HEIGHT + 40]
        plataformas_desaparecedoras[:] = [p_des for p_des in plataformas_desaparecedoras
                                          if p_des.rect.y < HEIGHT + 40 and p_des.active]

        if y > HEIGHT:
            pantalla_gameover(score)

        # Dibujos
        screen.blit(fondo, (0, 0))
        screen.blit(pasto, (0, HEIGHT - 40))

        # Dibujar plataformas normales
        for p in plataformas:
            screen.blit(plataforma_img, (p.x, p.y))

        # Dibujar plataformas que desaparecen
        for p_des in plataformas_desaparecedoras:
            p_des.draw(screen)

        sprite = sprite_idle if on_ground else sprite_jump
        screen.blit(sprite, (x, y))

        text = font.render(f"Puntos: {score}", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        # Instrucción de pausa
        texto_pausa = font.render("P: Pausa", True, (0, 0, 0))
        screen.blit(texto_pausa, (WIDTH - 100, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()