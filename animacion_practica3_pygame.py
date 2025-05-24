import pygame, sys, math
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 26, bold=True)
font_small = pygame.font.SysFont('arial', 18)

ROJO = (220, 60, 60)
AZUL = (60, 120, 220)
AZUL_CLARO = (120, 180, 255)
MORADO = (180, 80, 200)
GRIS = (200, 200, 200)
GRIS_OSCURO = (120, 120, 120)
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)
BOTON = (10, 40, 80)

f = 0

while True:
    screen.fill(BLANCO)
    # Placas paralelas
    for i in range(6):
        pygame.draw.rect(screen, GRIS, (180+40*i, 220+10*(i%2), 40, 120), border_radius=8)
        pygame.draw.rect(screen, GRIS_OSCURO, (180+40*i, 220+10*(i%2), 40, 120), 2, border_radius=8)
    # Flechas flujo caliente (rojo)
    for i in range(3):
        y = 250+30*i+10*math.sin(f+i)
        pygame.draw.line(screen, ROJO, (200, y), (600, y), 10)
        # Flecha
        ang = math.atan2(0, 400)
        tip = (600, y)
        left = (600-18*math.cos(ang-0.4), y-18*math.sin(ang-0.4))
        right = (600-18*math.cos(ang+0.4), y-18*math.sin(ang+0.4))
        pygame.draw.polygon(screen, ROJO, [tip, left, right])
    # Flechas flujo frío (azul)
    for i in range(3):
        y = 320+30*i+10*math.cos(f+i)
        pygame.draw.line(screen, AZUL, (600, y), (200, y), 10)
        ang = math.atan2(0, -400)
        tip = (200, y)
        left = (200+18*math.cos(ang-0.4), y+18*math.sin(ang-0.4))
        right = (200+18*math.cos(ang+0.4), y+18*math.sin(ang+0.4))
        pygame.draw.polygon(screen, AZUL, [tip, left, right])
    # Zona de mezcla
    pygame.draw.ellipse(screen, MORADO, (380, 270+10*math.sin(f), 80, 60))
    # Etiquetas
    screen.blit(font_small.render("Entrada caliente", True, ROJO), (180, 230))
    screen.blit(font_small.render("Entrada fría", True, AZUL), (600, 410))
    screen.blit(font_small.render("Zona de intercambio", True, MORADO), (390, 340))
    f += 0.08
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
