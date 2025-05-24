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
ROJO = (220, 60, 60)
ROJO_CLARO = (255, 120, 120)
GRIS = (200, 200, 200)
GRIS_OSCURO = (80, 80, 80)
NEGRO = (0,0,0)
BLANCO = (255,255,255)

f_anim = 0

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

def draw_plates(surface):
    # Placas paralelas
    for i in range(6):
        px, py = 180+90*i, 180
        sombra(surface, (px, py, 60, 220), 8, (6,6), 50)
        plate = pygame.Surface((60, 220), pygame.SRCALPHA)
        gradiente_rect(plate, (0,0,60,220), (220,220,220), (120,120,120))
        pygame.draw.rect(plate, NEGRO, (0,0,60,220), 4, border_radius=8)
        surface.blit(plate, (px, py))
    # Bordes laterales
    pygame.draw.rect(surface, AZUL, (140, 180, 40, 220), border_radius=12)
    pygame.draw.rect(surface, NEGRO, (140, 180, 40, 220), 2, border_radius=12)
    pygame.draw.rect(surface, ROJO, (720, 180, 40, 220), border_radius=12)
    pygame.draw.rect(surface, NEGRO, (720, 180, 40, 220), 2, border_radius=12)

def draw_flows(surface, anim):
    # Flujo frío (azul, de izquierda a derecha)
    for i in range(3):
        y = 210+60*i+10*math.sin(anim/10+i)
        pygame.draw.line(surface, AZUL, (160, y), (720, y), 12)
        pygame.draw.line(surface, NEGRO, (160, y), (720, y), 2)
        ang = math.atan2(0, 560)
        tip = (720, y)
        left = (720-18*math.cos(ang-0.4), y-18*math.sin(ang-0.4))
        right = (720-18*math.cos(ang+0.4), y-18*math.sin(ang+0.4))
        pygame.draw.polygon(surface, AZUL_CLARO, [tip, left, right])
        pygame.draw.polygon(surface, NEGRO, [tip, left, right], 2)
    # Flujo caliente (rojo, de arriba a abajo)
    for i in range(3):
        x = 220+150*i+10*math.cos(anim/12+i)
        pygame.draw.line(surface, ROJO, (x, 160), (x, 400), 12)
        pygame.draw.line(surface, NEGRO, (x, 160), (x, 400), 2)
        ang = math.atan2(240, 0)
        tip = (x, 400)
        left = (x-18*math.cos(ang-0.4), 400-18*math.sin(ang-0.4))
        right = (x-18*math.cos(ang+0.4), 400-18*math.sin(ang+0.4))
        pygame.draw.polygon(surface, ROJO_CLARO, [tip, left, right])
        pygame.draw.polygon(surface, NEGRO, [tip, left, right], 2)

def draw_labels(surface):
    lbl = font.render("Intercambiador de Calor", True, NEGRO)
    screen.blit(lbl, (W//2 - lbl.get_width()//2, 30))
    # Etiqueta Entrada fría (izquierda, fuera del área de flujo, margen 12px)
    lbl2 = font_small.render("Entrada fría", True, NEGRO)
    screen.blit(lbl2, (120-lbl2.get_width()-12, 210))
    # Etiqueta Salida caliente (derecha, fuera del área de flujo, margen 12px)
    lbl3 = font_small.render("Salida caliente", True, NEGRO)
    screen.blit(lbl3, (720+40+12, 420))
    # Etiqueta Placas paralelas (abajo, centrada, margen 12px)
    lbl4 = font_small.render("Placas paralelas", True, NEGRO)
    screen.blit(lbl4, (W//2 - lbl4.get_width()//2, 420+40+12))

def draw_background(surface):
    surface.fill(BLANCO)
    pygame.draw.line(surface, GRIS_OSCURO, (0, H-60), (W, H-60), 3)

while True:
    draw_background(screen)
    draw_plates(screen)
    draw_flows(screen, f_anim)
    draw_labels(screen)
    f_anim += 1
    # Botón Volver
    volver_rect = pygame.Rect(W-150, H-70, 120, 40)
    sombra(screen, (W-150, H-70, 120, 40), 8, (4,4), 60)
    pygame.draw.rect(screen, AZUL, volver_rect, border_radius=8)
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
