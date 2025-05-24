import pygame, sys, math
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()

ROJO = (220, 60, 60)
AZUL = (60, 120, 220)
MORADO = (180, 80, 200)
GRIS = (200, 200, 200)
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)

f = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    screen.fill(BLANCO)
    # Placas
    for i in range(6):
        pygame.draw.rect(screen, GRIS, (180+40*i, 220+10*(i%2), 40, 120), border_radius=8)
    # Flujo rojo
    for i in range(3):
        pygame.draw.line(screen, ROJO, (200, 250+30*i), (600, 250+30*i+10*math.sin(f+i)), 10)
    # Flujo azul
    for i in range(3):
        pygame.draw.line(screen, AZUL, (600, 320+30*i), (200, 320+30*i+10*math.cos(f+i)), 10)
    # Mezcla central
    pygame.draw.ellipse(screen, MORADO, (380, 270+10*math.sin(f), 80, 60))
    f += 0.08
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
