import pygame, sys, random
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()

AZUL = (60, 120, 220)
GRIS = (180, 180, 180)
NUBE = (200, 200, 200)
TECHO = (120, 80, 40)
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)

gotas = [[random.randint(320, 580), 120+random.randint(0,30), random.uniform(2, 4)] for _ in range(10)]
nivel = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    screen.fill(BLANCO)
    # Nube
    pygame.draw.ellipse(screen, NUBE, (350, 80, 200, 60))
    # Techo
    pygame.draw.polygon(screen, TECHO, [(300, 200), (600, 160), (620, 200), (320, 240)])
    # Tanque
    pygame.draw.rect(screen, GRIS, (700, 320, 60, 180), border_radius=18)
    pygame.draw.rect(screen, AZUL, (710, 480-nivel, 40, nivel), border_radius=8)
    pygame.draw.rect(screen, NEGRO, (700, 320, 60, 180), 3, border_radius=18)
    # Gotas
    for g in gotas:
        pygame.draw.ellipse(screen, AZUL, (g[0], g[1], 16, 28))
        g[1] += g[2]
        if g[1] > 200:
            g[1] = 120
            if nivel < 150:
                nivel += 2
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
