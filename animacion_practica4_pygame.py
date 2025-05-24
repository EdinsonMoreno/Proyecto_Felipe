import pygame, sys, math, random
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 26, bold=True)
font_small = pygame.font.SysFont('arial', 18)

AZUL = (60, 120, 220)
GRIS = (180, 180, 180)
NARANJA = (255, 180, 60)
ROJO = (220, 60, 60)
GRIS_OSCURO = (100, 100, 100)
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)
BOTON = (10, 40, 80)

burbujas = [[random.randint(250, 600), random.randint(350, 470)] for _ in range(12)]
f = 0

while True:
    screen.fill(BLANCO)
    # Sombra tanque
    sombra = pygame.Surface((520, 60), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0,0,0,40), (0, 0, 520, 60))
    screen.blit(sombra, (190, 440))
    # Tanque horizontal
    pygame.draw.ellipse(screen, GRIS, (200, 300, 500, 180))
    pygame.draw.ellipse(screen, GRIS_OSCURO, (200, 300, 500, 180), 4)
    # Fuego animado
    pygame.draw.ellipse(screen, NARANJA, (400, 400+10*math.sin(f*2), 100, 40+10*math.sin(f*2)))
    pygame.draw.ellipse(screen, ROJO, (420, 420+10*math.sin(f*2), 60, 20+10*math.sin(f*2)))
    # Tubos
    for i in range(3):
        pygame.draw.line(screen, AZUL, (250, 350+30*i), (650, 350+30*i), 14)
        pygame.draw.circle(screen, GRIS_OSCURO, (250, 350+30*i), 8)
        pygame.draw.circle(screen, GRIS_OSCURO, (650, 350+30*i), 8)
    # Burbujas
    for b in burbujas:
        pygame.draw.ellipse(screen, BLANCO, (b[0], b[1], 18, 18))
        b[1] -= 1.2
        if b[1] < 320:
            b[1] = 470
    # Válvulas
    pygame.draw.circle(screen, (200, 120, 40), (250, 350), 14)
    pygame.draw.circle(screen, (200, 120, 40), (650, 410), 14)
    # Etiquetas
    screen.blit(font_small.render("Tanque de agua", True, AZUL), (350, 320))
    screen.blit(font_small.render("Fuego", True, ROJO), (430, 460))
    screen.blit(font_small.render("Tuberías", True, AZUL), (600, 370))
    # Flechas de flujo
    for i in range(3):
        x = 350+100*i
        pygame.draw.polygon(screen, AZUL, [(x+40, 350+30*i), (x+60, 345+30*i), (x+60, 355+30*i)])
    f += 0.07
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
