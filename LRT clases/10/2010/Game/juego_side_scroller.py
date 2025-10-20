import pygame, random, sys

pygame.init()
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scroller Horizontal + Puntaje")
clock = pygame.time.Clock()

PLAYER_W, PLAYER_H = 40, 50
x, y = 100, HEIGHT - 100
vel_x, vel_y = 0, 0
speed = 5
gravity = 0.6
jump_power = -12
on_ground = False

score = 0
scroll_x_total = 0
CAM_TARGET_X = int(WIDTH * 0.5)

USE_SPRITES = False
try:
    fondo = pygame.image.load("sprites/Fondo.png").convert()
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    plataforma_img = pygame.image.load("sprites/plataforma.png").convert_alpha()
    plataforma_img = pygame.transform.scale(plataforma_img, (110, 18))
    sprite_idle = pygame.image.load("sprites/jugador_idle.png").convert_alpha()
    sprite_jump = pygame.image.load("sprites/jugador_jump.png").convert_alpha()
    sprite_idle = pygame.transform.scale(sprite_idle, (PLAYER_W, PLAYER_H))
    sprite_jump = pygame.transform.scale(sprite_jump, (PLAYER_W, PLAYER_H))
    USE_SPRITES = True
except Exception:
    pass

AZUL = (135, 206, 235)
VERDE = (0, 200, 0)
NEGRO = (10, 10, 10)
font = pygame.font.SysFont(None, 36)

class Plataforma:
    def __init__(self, x, y, w=110, h=18):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surf):
        if USE_SPRITES:
            surf.blit(plataforma_img, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(surf, VERDE, self.rect)

def pantalla_gameover(score):
    screen.fill((200, 50, 50))
    t1 = font.render("GAME OVER", True, NEGRO)
    t2 = font.render(f"Puntaje final: {score}", True, NEGRO)
    t3 = font.render("R: reiniciar  |  Q: salir", True, NEGRO)
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
                    main()

def generar_plataformas_inicial():
    plats = [Plataforma(-200, HEIGHT - 20, WIDTH + 400, 20)]
    current_x = 50
    for _ in range(10):
        gap = random.randint(80, 140)
        plat_y = random.randint(HEIGHT//2, HEIGHT - 120)
        current_x += gap
        plats.append(Plataforma(current_x, plat_y))
    return plats

def generar_plataformas_derecha(plataformas):
    if len(plataformas) < 12:
        max_x = max(p.rect.right for p in plataformas)
        for _ in range(4):
            gap = random.randint(90, 160)
            new_x = max_x + gap
            new_y = random.randint(HEIGHT//2, HEIGHT - 130)
            plataformas.append(Plataforma(new_x, new_y))
            max_x = new_x + 110

def main():
    global x, y, vel_x, vel_y, on_ground, score, scroll_x_total
    x, y = 100, HEIGHT - 100
    vel_x, vel_y = 0, 0
    on_ground = False
    score = 0
    scroll_x_total = 0

    plataformas = generar_plataformas_inicial()

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

        on_ground = False
        for p in plataformas:
            if jugador.colliderect(p.rect) and vel_y >= 0:
                y = p.rect.top - PLAYER_H
                vel_y = 0
                on_ground = True
                break

        if x > CAM_TARGET_X:
            dx = x - CAM_TARGET_X
            x = CAM_TARGET_X
            for p in plataformas:
                p.rect.x -= int(dx)
            scroll_x_total += int(dx)
            score = scroll_x_total // 20

        generar_plataformas_derecha(plataformas)
        plataformas = [p for p in plataformas if p.rect.right > -200]

        if y > HEIGHT:
            pantalla_gameover(score)

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

        text = font.render(f"Puntos: {score}", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
