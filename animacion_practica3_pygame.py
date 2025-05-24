import pygame, sys, math
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 24, bold=True)
font_small = pygame.font.SysFont('arial', 16)

# Colores
AZUL = (30, 120, 220)
AZUL_CLARO = (120, 180, 255)
ROJO = (220, 60, 60)
ROJO_CLARO = (255, 120, 120)
GRIS = (200, 200, 200)
GRIS_OSCURO = (120, 120, 120)
NEGRO = (0,0,0)
BLANCO = (255,255,255)

f_anim = 0

# Gradiente para placas
def gradiente_rect(surface, rect, color1, color2):
    x, y, w, h = rect
    for i in range(h):
        ratio = i / h
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))

def draw_plates(surface):
    # Placas paralelas
    for i in range(6):
        plate = pygame.Surface((60, 220), pygame.SRCALPHA)
        gradiente_rect(plate, (0,0,60,220), (220,220,220), (120,120,120))
        pygame.draw.rect(plate, GRIS_OSCURO, (0,0,60,220), 3, border_radius=8)
        surface.blit(plate, (180+90*i, 180))
    # Bordes laterales
    pygame.draw.rect(surface, AZUL, (140, 180, 40, 220), border_radius=12)
    pygame.draw.rect(surface, ROJO, (720, 180, 40, 220), border_radius=12)

def draw_flows(surface, anim):
    # Flujo frío (azul, de izquierda a derecha)
    for i in range(3):
        y = 210+60*i+10*math.sin(anim/10+i)
        pygame.draw.line(surface, AZUL, (160, y), (720, y), 10)
        ang = math.atan2(0, 560)
        tip = (720, y)
        left = (720-18*math.cos(ang-0.4), y-18*math.sin(ang-0.4))
        right = (720-18*math.cos(ang+0.4), y-18*math.sin(ang+0.4))
        pygame.draw.polygon(surface, AZUL_CLARO, [tip, left, right])
    # Flujo caliente (rojo, de arriba a abajo)
    for i in range(3):
        x = 220+150*i+10*math.cos(anim/12+i)
        pygame.draw.line(surface, ROJO, (x, 160), (x, 400), 10)
        ang = math.atan2(240, 0)
        tip = (x, 400)
        left = (x-18*math.cos(ang-0.4), 400-18*math.sin(ang-0.4))
        right = (x-18*math.cos(ang+0.4), 400-18*math.sin(ang+0.4))
        pygame.draw.polygon(surface, ROJO_CLARO, [tip, left, right])

def draw_labels(surface):
    lbl = font.render("Intercambiador de Calor", True, AZUL)
    surface.blit(lbl, (280, 40))
    lbl2 = font_small.render("Entrada fría", True, AZUL)
    surface.blit(lbl2, (120, 160))
    lbl3 = font_small.render("Salida caliente", True, ROJO)
    surface.blit(lbl3, (720, 420))
    lbl4 = font_small.render("Placas paralelas", True, GRIS_OSCURO)
    surface.blit(lbl4, (400, 420))

while True:
    screen.fill(BLANCO)
    draw_plates(screen)
    draw_flows(screen, f_anim)
    draw_labels(screen)
    f_anim += 1
    # Botón Volver
    volver_rect = pygame.Rect(750, 540, 120, 40)
    pygame.draw.rect(screen, (10, 40, 80), volver_rect, border_radius=8)
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
