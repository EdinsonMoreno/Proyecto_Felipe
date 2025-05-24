import pygame, sys, math
pygame.init()
W, H = 900, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', int(H*0.045), bold=True)
font_small = pygame.font.SysFont('arial', int(H*0.025))

# Paleta profesional
AZUL = (30, 90, 180)
AZUL_CLARO = (120, 180, 255)
AZUL_OSCURO = (20, 40, 80)
GRIS = (180, 180, 180)
GRIS_OSCURO = (80, 80, 80)
NEGRO = (0,0,0)
BLANCO = (255,255,255)
CARBON = (60,60,60)
GRAVA = (180,180,180)
ARENA = (220,200,120)
VERDE = (60, 200, 120)

agua_nivel = [420, 420, 420]
gota_anim = 0

# --- Utilidades visuales ---
def sombra(surface, rect, radio=18, offset=(8,8), alpha=60):
    sombra = pygame.Surface((rect[2]+20, rect[3]+20), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0,0,0,alpha), (offset[0], offset[1], rect[2], rect[3]), 0)
    surface.blit(sombra, (rect[0]-10, rect[1]-10))

def gradiente_rect(surface, rect, color1, color2):
    x, y, w, h = rect
    for i in range(h):
        ratio = i / h
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))

def draw_column(surface, x, y, color1, color2, label, nivel, mat_labels, col_num):
    sombra(surface, (x-8, y+320, 80, 30), 12, (8,8), 60)
    col = pygame.Surface((60, 320), pygame.SRCALPHA)
    gradiente_rect(col, (0,0,60,320), color1, color2)
    pygame.draw.rect(col, NEGRO, (0,0,60,320), 4, border_radius=18)
    surface.blit(col, (x, y))
    # Materiales internos
    pygame.draw.rect(surface, CARBON, (x+8, y+240, 44, 40), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (x+8, y+240, 44, 40), 2, border_radius=8)
    pygame.draw.rect(surface, GRAVA, (x+8, y+180, 44, 60), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (x+8, y+180, 44, 60), 2, border_radius=8)
    pygame.draw.rect(surface, ARENA, (x+8, y+60, 44, 120), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (x+8, y+60, 44, 120), 2, border_radius=8)
    # Nivel de agua con reflejo
    pygame.draw.rect(surface, AZUL_CLARO, (x+12, nivel, 36, 320-nivel), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (x+12, nivel, 36, 320-nivel), 2, border_radius=8)
    pygame.draw.arc(surface, (255,255,255,60), (x+14, nivel+10, 32, 40), math.radians(200), math.radians(320), 4)
    # Etiqueta columna (arriba, margen 12px)
    lbl = font_small.render(f"Columna {col_num}", True, NEGRO)
    surface.blit(lbl, (x+30-lbl.get_width()//2, y-12-lbl.get_height()))
    # Tapa
    pygame.draw.ellipse(surface, GRIS, (x-2, y-18, 64, 24))
    pygame.draw.ellipse(surface, NEGRO, (x-2, y-18, 64, 24), 2)
    # Etiquetas materiales (a la derecha, margen 12px)
    for i, (mat, cy) in enumerate(zip(mat_labels, [260, 210, 110])):
        lbl = font_small.render(mat, True, NEGRO)
        surface.blit(lbl, (x+60+12, y+cy))

def draw_tuberias(surface):
    # Tubería superior
    pygame.draw.rect(surface, GRIS, (120, 40, 540, 24), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (120, 40, 540, 24), 2, border_radius=8)
    # Etiqueta 'Tubería' (arriba, centrada, margen 10px)
    tub_lbl = font_small.render("Tubería", True, NEGRO)
    surface.blit(tub_lbl, (390-tub_lbl.get_width()//2, 40-10-tub_lbl.get_height()))
    # Válvulas numeradas
    for i in range(3):
        pygame.draw.circle(surface, GRIS, (180+220*i, 52), 14)
        pygame.draw.circle(surface, NEGRO, (180+220*i, 52), 14, 2)
        pygame.draw.line(surface, GRIS_OSCURO, (180+220*i-8, 52), (180+220*i+8, 52), 3)
        # Etiqueta lateral de válvula
        val_lbl = font_small.render(f"Válvula {i+1}", True, NEGRO)
        surface.blit(val_lbl, (180+220*i- val_lbl.get_width()//2, 52+18))
    # Tubería de bajada
    for i in range(3):
        pygame.draw.rect(surface, GRIS, (170+220*i, 64, 20, 120), border_radius=8)
        pygame.draw.rect(surface, NEGRO, (170+220*i, 64, 20, 120), 2, border_radius=8)
    # Tubería de salida
    pygame.draw.rect(surface, GRIS, (120, 360, 540, 18), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (120, 360, 540, 18), 2, border_radius=8)
    # Flechas de flujo
    for i in range(3):
        pygame.draw.polygon(surface, AZUL, [(180+220*i, 120), (190+220*i, 140), (170+220*i, 140)])
        pygame.draw.polygon(surface, NEGRO, [(180+220*i, 120), (190+220*i, 140), (170+220*i, 140)], 2)
    for i in range(3):
        pygame.draw.polygon(surface, AZUL, [(180+220*i, 360), (190+220*i, 380), (170+220*i, 380)])
        pygame.draw.polygon(surface, NEGRO, [(180+220*i, 360), (190+220*i, 380), (170+220*i, 380)], 2)

def draw_gotas(surface, anim):
    # Gotas animadas bajando por cada columna
    for i in range(3):
        y = 64 + (anim*3 + i*40) % 120
        pygame.draw.ellipse(surface, AZUL_CLARO, (180+220*i-6, y, 12, 18))
        pygame.draw.ellipse(surface, NEGRO, (180+220*i-6, y, 12, 18), 2)

def draw_labels(surface):
    lbl = font.render("Filtrado Multicapa", True, NEGRO)
    screen.blit(lbl, (W//2 - lbl.get_width()//2, 30))

def draw_background(surface):
    surface.fill(BLANCO)
    pygame.draw.line(surface, GRIS_OSCURO, (0, H-60), (W, H-60), 3)

while True:
    draw_background(screen)
    draw_tuberias(screen)
    draw_column(screen, 160, 80, (180,180,180), (120,120,120), "Columna 1", agua_nivel[0], ["Carbón", "Grava", "Arena"], 1)
    draw_column(screen, 380, 80, (180,180,180), (120,120,120), "Columna 2", agua_nivel[1], ["Carbón", "Grava", "Arena"], 2)
    draw_column(screen, 600, 80, (180,180,180), (120,120,120), "Columna 3", agua_nivel[2], ["Carbón", "Grava", "Arena"], 3)
    draw_gotas(screen, gota_anim)
    draw_labels(screen)
    # Animación de nivel de agua
    for i in range(3):
        if agua_nivel[i] > 120:
            agua_nivel[i] -= 0.5 + 0.2*i
    gota_anim += 1
    # Botón Volver
    volver_rect = pygame.Rect(W-150, H-70, 120, 40)
    sombra(screen, (W-150, H-70, 120, 40), 8, (4,4), 60)
    pygame.draw.rect(screen, AZUL_OSCURO, volver_rect, border_radius=8)
    pygame.draw.rect(screen, NEGRO, volver_rect, 2, border_radius=8)
    text = font_small.render("Volver", True, BLANCO)
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
