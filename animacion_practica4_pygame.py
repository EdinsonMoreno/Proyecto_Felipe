import pygame, sys, math, random
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 24, bold=True)
font_small = pygame.font.SysFont('arial', 16)

# Colores
AZUL = (30, 120, 220)
AZUL_CLARO = (120, 180, 255)
ROJO = (220, 60, 60)
NARANJA = (255, 180, 60)
GRIS = (180, 180, 180)
GRIS_OSCURO = (100, 100, 100)
NEGRO = (0,0,0)
BLANCO = (255,255,255)

burbujas = [[random.randint(250, 600), random.randint(350, 470)] for _ in range(12)]
f_anim = 0

# Gradiente horizontal para tanque
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
    sombra = pygame.Surface((520, 60), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0,0,0,40), (0, 40, 520, 20))
    surface.blit(sombra, (180, 420))
    # Tanque principal
    tank = pygame.Surface((500, 120), pygame.SRCALPHA)
    gradiente_rect(tank, (0,0,500,120), (180,200,220), (120,120,120))
    pygame.draw.rect(tank, GRIS_OSCURO, (0,0,500,120), 6, border_radius=40)
    surface.blit(tank, (190, 300))
    # Tapa y conectores
    pygame.draw.ellipse(surface, GRIS, (170, 320, 40, 40))
    pygame.draw.ellipse(surface, GRIS_OSCURO, (170, 320, 40, 40), 2)
    pygame.draw.ellipse(surface, GRIS, (670, 320, 40, 40))
    pygame.draw.ellipse(surface, GRIS_OSCURO, (670, 320, 40, 40), 2)
    # Tubos
    pygame.draw.rect(surface, GRIS, (210, 260, 20, 60), border_radius=8)
    pygame.draw.rect(surface, GRIS, (670, 260, 20, 60), border_radius=8)
    pygame.draw.rect(surface, GRIS_OSCURO, (210, 260, 20, 60), 2, border_radius=8)
    pygame.draw.rect(surface, GRIS_OSCURO, (670, 260, 20, 60), 2, border_radius=8)

def draw_fire(surface, anim):
    # Fuego animado
    for i in range(8):
        x = 260 + i*30 + 10*math.sin(anim/8+i)
        y = 390 + 10*math.cos(anim/10+i)
        color = (255, min(255, 180+20*i), 60)
        pygame.draw.polygon(surface, color, [(x, y), (x+10, y-30), (x+20, y)])
    # Llama principal
    pygame.draw.ellipse(surface, (255,220,120), (340, 390, 80, 30))

def draw_bubbles(surface, anim):
    # Burbujas en tubos
    for i, (bx, by) in enumerate(burbujas):
        pygame.draw.ellipse(surface, AZUL_CLARO, (bx, by, 16, 16))
        burbujas[i][1] -= 1 + 0.5*math.sin(anim/10+i)
        if burbujas[i][1] < 320:
            burbujas[i][1] = 470

def draw_labels(surface):
    lbl = font.render("Caldera Horizontal", True, ROJO)
    surface.blit(lbl, (320, 40))
    lbl2 = font_small.render("Entrada de agua", True, AZUL)
    surface.blit(lbl2, (210, 250))
    lbl3 = font_small.render("Salida de vapor", True, ROJO)
    surface.blit(lbl3, (670, 250))
    lbl4 = font_small.render("Zona de combustión", True, NARANJA)
    surface.blit(lbl4, (340, 430))

while True:
    screen.fill(BLANCO)
    draw_tank(screen)
    draw_fire(screen, f_anim)
    draw_bubbles(screen, f_anim)
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
