import pygame, sys, random, math
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 26, bold=True)
font_small = pygame.font.SysFont('arial', 18)

AZUL = (60, 120, 220)
GRIS = (180, 180, 180)
NUBE = (200, 200, 200)
TECHO = (120, 80, 40)
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)
BOTON = (10, 40, 80)

# Gotas de lluvia
lluvia = [[random.randint(350, 540), 120+random.randint(0,30), random.uniform(2, 4)] for _ in range(12)]
nivel = 0

while True:
    screen.fill(BLANCO)
    # Nube con sombra
    sombra = pygame.Surface((220, 60), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0,0,0,40), (0, 20, 220, 40))
    screen.blit(sombra, (340, 100))
    pygame.draw.ellipse(screen, NUBE, (350, 80, 200, 60))
    # Gotas
    for g in lluvia:
        pygame.draw.ellipse(screen, AZUL, (g[0], g[1], 16, 28))
        g[1] += g[2]
        if g[1] > 200:
            g[1] = 120
            if nivel < 150:
                nivel += 2
    # Techo
    pygame.draw.polygon(screen, TECHO, [(300, 200), (600, 160), (620, 200), (320, 240)])
    pygame.draw.line(screen, NEGRO, (300, 200), (600, 160), 4)
    # Flecha de flujo (techo a tanque)
    pygame.draw.line(screen, AZUL, (460, 200), (730, 320), 6)
    ang = math.atan2(320-200, 730-460)
    tip = (730, 320)
    left = (730-18*math.cos(ang-0.4), 320-18*math.sin(ang-0.4))
    right = (730-18*math.cos(ang+0.4), 320-18*math.sin(ang+0.4))
    pygame.draw.polygon(screen, AZUL, [tip, left, right])
    # Tanque
    pygame.draw.rect(screen, GRIS, (700, 320, 60, 180), border_radius=18)
    pygame.draw.rect(screen, AZUL, (710, 480-nivel, 40, nivel), border_radius=8)
    pygame.draw.rect(screen, NEGRO, (700, 320, 60, 180), 3, border_radius=18)
    # Etiquetas
    screen.blit(font_small.render("Nube", True, AZUL), (370, 70))
    screen.blit(font_small.render("Techo", True, TECHO), (320, 220))
    screen.blit(font_small.render("Tanque", True, AZUL), (710, 510))
    # Flecha de nivel
    pygame.draw.line(screen, AZUL, (760, 500), (760, 480-nivel), 4)
    pygame.draw.polygon(screen, AZUL, [(760, 480-nivel), (752, 490-nivel), (768, 490-nivel)])
    # Botón Volver
    volver_rect = pygame.Rect(750, 540, 120, 40)
    pygame.draw.rect(screen, BOTON, volver_rect, border_radius=8)
    text = font.render("Volver", True, (255, 255, 255))
    text_rect = text.get_rect(center=volver_rect.center)
    screen.blit(text, text_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if volver_rect.collidepoint(event.pos):
                pygame.quit(); sys.exit()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()
