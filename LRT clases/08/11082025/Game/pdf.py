import pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
x, y = 50, 500
vel_y = 0
gravity = 0.5
jump = -10
on_ground = True
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump
        on_ground = False
    if keys[pygame.K_LEFT]:
        x -= 5
    if keys[pygame.K_RIGHT]:
            x += 5
            
    vel_y += gravity
    y += vel_y
    if y >= 500:
        y = 500
        vel_y = 0
        on_ground = True
    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 50, 50))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()