import pygame, sys, math, random
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()

AZUL = (60, 120, 220)
GRIS = (180, 180, 180)
NARANJA = (255, 180, 60)
ROJO = (220, 60, 60)
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)

burbujas = [[random.randint(250, 600), random.randint(350, 470)] for _ in range(12)]
f = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    screen.fill(BLANCO)
    # Tanque
    pygame.draw.ellipse(screen, GRIS, (200, 300, 500, 180))
    # Fuego
    pygame.draw.ellipse(screen, NARANJA, (400, 400+10*math.sin(f*2), 100, 40+10*math.sin(f*2)))
    pygame.draw.ellipse(screen, ROJO, (420, 420+10*math.sin(f*2), 60, 20+10*math.sin(f*2)))
    # Tubos
    for i in range(3):
        pygame.draw.line(screen, AZUL, (250, 350+30*i), (650, 350+30*i), 14)
    # Burbujas
    for b in burbujas:
        pygame.draw.ellipse(screen, BLANCO, (b[0], b[1], 18, 18))
        b[1] -= 1.2
        if b[1] < 320:
            b[1] = 470
    f += 0.07
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
