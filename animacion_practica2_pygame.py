import pygame, sys
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 26, bold=True)
font_small = pygame.font.SysFont('arial', 18)

AZUL = (30, 120, 220)
AZUL_OSCURO = (10, 40, 80)
ARENA = (220, 200, 120)
CARBON = (60, 60, 60)
GRAVA = (180, 180, 180)
AGUA = (80, 180, 255)
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)
BOTON = AZUL_OSCURO

# Gradiente simulado
def gradiente_rect(surface, rect, color1, color2, vertical=True):
    x, y, w, h = rect
    for i in range(h if vertical else w):
        ratio = i / (h if vertical else w)
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        if vertical:
            pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))
        else:
            pygame.draw.line(surface, (r, g, b), (x + i, y), (x + i, y + h))

gota_y = 80
tanque_nivel = 0

while True:
    screen.fill(BLANCO)
    # Tubería superior
    pygame.draw.rect(screen, (120,120,120), (440, 60, 40, 80), border_radius=12)
    # Flecha entrada
    pygame.draw.polygon(screen, AZUL, [(460, 50), (470, 80), (450, 80)])
    # Columnas de filtrado
    for idx, (x, color, label) in enumerate([(200, CARBON, 'Carbón'), (400, GRAVA, 'Grava'), (600, ARENA, 'Arena')]):
        gradiente_rect(screen, (x, 180, 80, 300), color, (80,80,80))
        pygame.draw.rect(screen, NEGRO, (x, 180, 80, 300), 3, border_radius=18)
        # Material
        mat_color = (60,60,60) if idx==0 else (200,200,200) if idx==1 else (220,200,120)
        pygame.draw.ellipse(screen, mat_color, (x+10, 420, 60, 40))
        # Etiqueta
        label_surf = font_small.render(label, True, AZUL_OSCURO)
        screen.blit(label_surf, (x+10, 490))
    # Tubería inferior
    pygame.draw.rect(screen, (120,120,120), (440, 480, 40, 80), border_radius=12)
    # Flecha salida
    pygame.draw.polygon(screen, AZUL, [(460, 570), (470, 540), (450, 540)])
    # Válvulas
    pygame.draw.circle(screen, (200, 120, 40), (480, 180), 16)
    pygame.draw.circle(screen, (200, 120, 40), (480, 480), 16)
    # Gota animada
    color_gota = AGUA if gota_y < 250 else (120,180,255) if gota_y < 400 else (180,220,255)
    pygame.draw.ellipse(screen, color_gota, (440, gota_y, 40, 60))
    if gota_y < 420:
        gota_y += 2
    else:
        if tanque_nivel < 100:
            tanque_nivel += 1.5
        gota_y = 80
    # Tanque de salida
    gradiente_rect(screen, (750, 320, 60, 100), (120,120,120), (80,180,255))
    pygame.draw.rect(screen, NEGRO, (750, 320, 60, 100), 2, border_radius=10)
    pygame.draw.rect(screen, AGUA, (755, 420-tanque_nivel, 50, tanque_nivel), border_radius=8)
    # Etiquetas
    screen.blit(font_small.render("Entrada", True, AZUL_OSCURO), (445, 40))
    screen.blit(font_small.render("Salida", True, AZUL_OSCURO), (755, 430))
    # Flechas de flujo
    for i in range(3):
        pygame.draw.line(screen, AZUL, (240+200*i, 160), (240+200*i, 180), 6)
        pygame.draw.polygon(screen, AZUL, [(240+200*i, 180), (250+200*i, 170), (230+200*i, 170)])
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
