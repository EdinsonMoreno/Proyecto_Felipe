import pygame, sys, math
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 24, bold=True)
font_small = pygame.font.SysFont('arial', 16)

# Colores
AZUL = (30, 120, 220)
AZUL_OSCURO = (10, 40, 80)
AZUL_CLARO = (120, 180, 255)
GRIS = (180, 180, 180)
GRIS_OSCURO = (100, 100, 100)
NEGRO = (0,0,0)
BLANCO = (255,255,255)
CARBON = (60,60,60)
GRAVA = (180,180,180)
ARENA = (220,200,120)
AMARILLO = (255, 220, 60)
VERDE = (60, 200, 80)

agua_nivel = [420, 420, 420]
gota_anim = 0

# Gradiente vertical para materiales
def gradiente_rect(surface, rect, color1, color2):
    x, y, w, h = rect
    for i in range(h):
        ratio = i / h
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))

def draw_column(surface, x, y, color1, color2, label, nivel, mat_labels):
    # Sombra
    sombra = pygame.Surface((80, 30), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0,0,0,40), (0, 10, 80, 20))
    surface.blit(sombra, (x-10, y+320))
    # Columna
    col = pygame.Surface((60, 320), pygame.SRCALPHA)
    gradiente_rect(col, (0,0,60,320), color1, color2)
    pygame.draw.rect(col, GRIS_OSCURO, (0,0,60,320), 4, border_radius=18)
    surface.blit(col, (x, y))
    # Materiales internos
    pygame.draw.rect(surface, CARBON, (x+8, y+240, 44, 40), border_radius=8)
    pygame.draw.rect(surface, GRAVA, (x+8, y+180, 44, 60), border_radius=8)
    pygame.draw.rect(surface, ARENA, (x+8, y+60, 44, 120), border_radius=8)
    # Etiquetas materiales
    for i, (mat, cy) in enumerate(zip(mat_labels, [260, 210, 110])):
        lbl = font_small.render(mat, True, NEGRO)
        surface.blit(lbl, (x+65, y+cy))
    # Nivel de agua
    pygame.draw.rect(surface, AZUL_CLARO, (x+12, nivel, 36, 320-nivel), border_radius=8)
    # Etiqueta columna
    lbl = font_small.render(label, True, AZUL_OSCURO)
    surface.blit(lbl, (x+5, y-22))
    # Tapa
    pygame.draw.ellipse(surface, GRIS, (x-2, y-18, 64, 24))
    pygame.draw.ellipse(surface, GRIS_OSCURO, (x-2, y-18, 64, 24), 2)

def draw_tuberias(surface):
    # Tubería superior
    pygame.draw.rect(surface, GRIS, (120, 40, 540, 24), border_radius=8)
    pygame.draw.rect(surface, GRIS_OSCURO, (120, 40, 540, 24), 2, border_radius=8)
    # Válvulas
    for i in range(3):
        pygame.draw.circle(surface, (200,200,200), (180+220*i, 52), 14)
        pygame.draw.circle(surface, (120,120,120), (180+220*i, 52), 14, 2)
        pygame.draw.line(surface, (80,80,80), (180+220*i-8, 52), (180+220*i+8, 52), 3)
    # Tubería de bajada
    for i in range(3):
        pygame.draw.rect(surface, GRIS, (170+220*i, 64, 20, 120), border_radius=8)
        pygame.draw.rect(surface, GRIS_OSCURO, (170+220*i, 64, 20, 120), 2, border_radius=8)
    # Tubería de salida
    pygame.draw.rect(surface, GRIS, (120, 360, 540, 18), border_radius=8)
    pygame.draw.rect(surface, GRIS_OSCURO, (120, 360, 540, 18), 2, border_radius=8)
    # Flechas de flujo
    for i in range(3):
        pygame.draw.polygon(surface, AZUL, [(180+220*i, 120), (190+220*i, 140), (170+220*i, 140)])
    for i in range(3):
        pygame.draw.polygon(surface, AZUL, [(180+220*i, 360), (190+220*i, 380), (170+220*i, 380)])

def draw_gotas(surface, anim):
    # Gotas animadas bajando por cada columna
    for i in range(3):
        y = 64 + (anim*3 + i*40) % 120
        pygame.draw.ellipse(surface, AZUL, (180+220*i-6, y, 12, 18))

def draw_labels(surface):
    # Etiquetas generales
    lbl = font.render("Filtrado Multicapa", True, AZUL_OSCURO)
    surface.blit(lbl, (320, 10))
    lbl2 = font_small.render("Carbón", True, CARBON)
    surface.blit(lbl2, (700, 300))
    lbl3 = font_small.render("Grava", True, GRAVA)
    surface.blit(lbl3, (700, 220))
    lbl4 = font_small.render("Arena", True, ARENA)
    surface.blit(lbl4, (700, 120))

while True:
    screen.fill(BLANCO)
    draw_tuberias(screen)
    draw_column(screen, 160, 80, (180,180,180), (120,120,120), "Columna 1", agua_nivel[0], ["Carbón", "Grava", "Arena"])
    draw_column(screen, 380, 80, (180,180,180), (120,120,120), "Columna 2", agua_nivel[1], ["Carbón", "Grava", "Arena"])
    draw_column(screen, 600, 80, (180,180,180), (120,120,120), "Columna 3", agua_nivel[2], ["Carbón", "Grava", "Arena"])
    draw_gotas(screen, gota_anim)
    draw_labels(screen)
    # Animación de nivel de agua
    for i in range(3):
        if agua_nivel[i] > 120:
            agua_nivel[i] -= 0.5 + 0.2*i
    gota_anim += 1
    # Botón Volver
    volver_rect = pygame.Rect(750, 540, 120, 40)
    pygame.draw.rect(screen, AZUL_OSCURO, volver_rect, border_radius=8)
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
