import pygame, sys
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()

AZUL = (30, 120, 220)
GRIS = (120, 120, 120)
ARENA = (220, 200, 120)
CARBON = (60, 60, 60)
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)

gota_y = 80
tanque_nivel = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    screen.fill(BLANCO)
    # Columnas
    pygame.draw.rect(screen, CARBON, (200, 180, 80, 300), border_radius=18)
    pygame.draw.rect(screen, GRIS, (400, 180, 80, 300), border_radius=18)
    pygame.draw.rect(screen, ARENA, (600, 180, 80, 300), border_radius=18)
    # Tanque salida
    pygame.draw.rect(screen, AZUL, (750, 420-tanque_nivel, 60, tanque_nivel), border_radius=10)
    pygame.draw.rect(screen, NEGRO, (750, 320, 60, 100), 2, border_radius=10)
    # Gota
    color_gota = AZUL if gota_y < 250 else (120,180,255) if gota_y < 400 else (180,220,255)
    pygame.draw.ellipse(screen, color_gota, (440, gota_y, 40, 60))
    if gota_y < 420:
        gota_y += 2
    else:
        if tanque_nivel < 100:
            tanque_nivel += 1.5
        gota_y = 80
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
