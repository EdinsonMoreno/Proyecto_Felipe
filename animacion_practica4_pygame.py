import pygame, sys, math, random
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
NARANJA = (240, 180, 80)
GRIS = (180, 180, 180)
GRIS_OSCURO = (80, 80, 80)
NEGRO = (0,0,0)
BLANCO = (255,255,255)

burbujas = [[random.randint(250, 600), random.randint(350, 470)] for _ in range(12)]
f_anim = 0

def sombra(surface, rect, radio=18, offset=(8,8), alpha=60):
    sombra = pygame.Surface((rect[2]+20, rect[3]+20), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0,0,0,alpha), (offset[0], offset[1], rect[2], rect[3]), 0)
    surface.blit(sombra, (rect[0]-10, rect[1]-10))

def gradiente_rect(surface, rect, color1, color2):
    x, y, w, h = rect
    for i in range(w):
        ratio = i / w
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (x + i, y), (x + i, y + h))

def draw_tank(surface):
    # Sombra
    sombra(surface, (190, 420, 500, 40), 18, (8,8), 70)
    # Tanque principal
    tank = pygame.Surface((500, 120), pygame.SRCALPHA)
    gradiente_rect(tank, (0,0,500,120), (180,200,220), (120,120,120))
    pygame.draw.rect(tank, NEGRO, (0,0,500,120), 6, border_radius=40)
    surface.blit(tank, (190, 300))
    # Tapa y conectores
    pygame.draw.ellipse(surface, GRIS, (170, 320, 40, 40))
    pygame.draw.ellipse(surface, NEGRO, (170, 320, 40, 40), 2)
    pygame.draw.ellipse(surface, GRIS, (670, 320, 40, 40))
    pygame.draw.ellipse(surface, NEGRO, (670, 320, 40, 40), 2)
    # Tubos
    pygame.draw.rect(surface, GRIS, (210, 260, 20, 60), border_radius=8)
    pygame.draw.rect(surface, GRIS, (670, 260, 20, 60), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (210, 260, 20, 60), 2, border_radius=8)
    pygame.draw.rect(surface, NEGRO, (670, 260, 20, 60), 2, border_radius=8)

def draw_fire(surface, anim):
    # Fuego animado
    for i in range(8):
        x = 260 + i*30 + 10*math.sin(anim/8+i)
        y = 390 + 10*math.cos(anim/10+i)
        color = (255, min(255, 180+20*i), 60)
        pygame.draw.polygon(surface, color, [(x, y), (x+10, y-30), (x+20, y)])
        pygame.draw.polygon(surface, NEGRO, [(x, y), (x+10, y-30), (x+20, y)], 2)
    # Llama principal
    pygame.draw.ellipse(surface, (255,220,120), (340, 390, 80, 30))
    pygame.draw.ellipse(surface, NEGRO, (340, 390, 80, 30), 2)

def draw_bubbles(surface, anim):
    # Burbujas en tubos
    for i, (bx, by) in enumerate(burbujas):
        pygame.draw.ellipse(surface, AZUL_CLARO, (bx, by, 16, 16))
        pygame.draw.ellipse(surface, NEGRO, (bx, by, 16, 16), 2)
        burbujas[i][1] -= 1 + 0.5*math.sin(anim/10+i)
        if burbujas[i][1] < 320:
            burbujas[i][1] = 470

def draw_labels(surface):
    lbl = font.render("Caldera Horizontal", True, NEGRO)
    screen.blit(lbl, (W//2 - lbl.get_width()//2, 30))
    # Etiqueta Entrada de agua (izquierda, fuera del tubo, margen 12px)
    lbl2 = font_small.render("Entrada de agua", True, NEGRO)
    screen.blit(lbl2, (210-lbl2.get_width()-12, 250))
    # Etiqueta Salida de vapor (derecha, fuera del tubo, margen 12px)
    lbl3 = font_small.render("Salida de vapor", True, NEGRO)
    screen.blit(lbl3, (670+40+12, 250))
    # Etiqueta Zona de combustión (abajo del tanque, margen 12px)
    lbl4 = font_small.render("Zona de combustión", True, NEGRO)
    screen.blit(lbl4, (340+80, 430+30))

def draw_background(surface):
    surface.fill(BLANCO)
    pygame.draw.line(surface, GRIS_OSCURO, (0, H-60), (W, H-60), 3)

while True:
    draw_background(screen)
    draw_tank(screen)
    draw_fire(screen, f_anim)
    draw_bubbles(screen, f_anim)
    draw_labels(screen)
    f_anim += 1
    # Botón Volver
    volver_rect = pygame.Rect(W-150, H-70, 120, 40)
    sombra(screen, (W-150, H-70, 120, 40), 8, (4,4), 60)
    pygame.draw.rect(screen, ROJO, volver_rect, border_radius=8)
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
