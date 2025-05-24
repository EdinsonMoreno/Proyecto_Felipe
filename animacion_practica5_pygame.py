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
GRIS = (180, 180, 180)
GRIS_OSCURO = (80, 80, 80)
NEGRO = (0,0,0)
BLANCO = (255,255,255)
NUBE = (200, 200, 200)
TECHO = (120, 80, 40)
VERDE = (60, 200, 120)

lluvia = [[random.randint(350, 540), 120+random.randint(0,30), random.uniform(2, 4)] for _ in range(12)]
nivel = 0
f_anim = 0

def sombra(surface, rect, radio=18, offset=(8,8), alpha=60):
    sombra = pygame.Surface((rect[2]+20, rect[3]+20), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0,0,0,alpha), (offset[0], offset[1], rect[2], rect[3]), 0)
    surface.blit(sombra, (rect[0]-10, rect[1]-10))

def draw_nube(surface, anim):
    # Nube con sombra
    sombra(surface, (370, 110, 180, 40), 18, (8,8), 50)
    pygame.draw.ellipse(surface, NUBE, (370, 80, 180, 60))
    pygame.draw.ellipse(surface, NUBE, (350, 100, 60, 40))
    pygame.draw.ellipse(surface, NUBE, (500, 100, 60, 40))
    pygame.draw.ellipse(surface, NEGRO, (370, 80, 180, 60), 2)
    pygame.draw.ellipse(surface, NEGRO, (350, 100, 60, 40), 2)
    pygame.draw.ellipse(surface, NEGRO, (500, 100, 60, 40), 2)
    # Gotas de lluvia
    for i, (gx, gy, vel) in enumerate(lluvia):
        pygame.draw.ellipse(surface, AZUL_CLARO, (gx, gy, 10, 22))
        pygame.draw.ellipse(surface, NEGRO, (gx, gy, 10, 22), 2)
        lluvia[i][1] += vel
        if lluvia[i][1] > 180:
            lluvia[i][1] = 120

def draw_techo(surface):
    # Techo
    pygame.draw.polygon(surface, TECHO, [(340, 180), (560, 180), (520, 220), (380, 220)])
    pygame.draw.polygon(surface, NEGRO, [(340, 180), (560, 180), (520, 220), (380, 220)], 2)
    pygame.draw.rect(surface, (80,60,30), (380, 220, 140, 16), border_radius=4)
    pygame.draw.rect(surface, NEGRO, (380, 220, 140, 16), 2, border_radius=4)
    # Flecha de bajada
    pygame.draw.polygon(surface, AZUL, [(450, 220), (470, 250), (430, 250)])
    pygame.draw.polygon(surface, NEGRO, [(450, 220), (470, 250), (430, 250)], 2)

def draw_tuberia(surface):
    # Tubería
    pygame.draw.rect(surface, GRIS, (440, 250, 20, 80), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (440, 250, 20, 80), 2, border_radius=8)
    pygame.draw.rect(surface, GRIS, (440, 330, 80, 20), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (440, 330, 80, 20), 2, border_radius=8)
    pygame.draw.rect(surface, GRIS, (520, 250, 20, 100), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (520, 250, 20, 100), 2, border_radius=8)
    pygame.draw.rect(surface, GRIS, (440, 350, 100, 20), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (440, 350, 100, 20), 2, border_radius=8)
    pygame.draw.rect(surface, GRIS, (540, 350, 20, 120), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (540, 350, 20, 120), 2, border_radius=8)
    # Flechas de flujo
    pygame.draw.polygon(surface, AZUL, [(450, 320), (470, 340), (430, 340)])
    pygame.draw.polygon(surface, NEGRO, [(450, 320), (470, 340), (430, 340)], 2)
    pygame.draw.polygon(surface, AZUL, [(550, 400), (570, 420), (530, 420)])
    pygame.draw.polygon(surface, NEGRO, [(550, 400), (570, 420), (530, 420)], 2)

def draw_tanque(surface, nivel):
    sombra(surface, (520, 480, 120, 40), 18, (8,8), 70)
    # Tanque
    pygame.draw.ellipse(surface, GRIS, (520, 350, 120, 60))
    pygame.draw.ellipse(surface, NEGRO, (520, 350, 120, 60), 2)
    pygame.draw.rect(surface, GRIS, (520, 380, 120, 120), border_radius=30)
    pygame.draw.rect(surface, NEGRO, (520, 380, 120, 120), 2, border_radius=30)
    pygame.draw.ellipse(surface, GRIS, (520, 480, 120, 40))
    pygame.draw.ellipse(surface, NEGRO, (520, 480, 120, 40), 2)
    # Nivel de agua con reflejo
    pygame.draw.rect(surface, AZUL, (530, 480-nivel, 100, nivel), border_radius=18)
    pygame.draw.rect(surface, NEGRO, (530, 480-nivel, 100, nivel), 2, border_radius=18)
    pygame.draw.arc(surface, (255,255,255,60), (540, 480-nivel+10, 80, 30), math.radians(200), math.radians(320), 4)
    # Etiqueta (abajo del tanque, margen 12px)
    lbl = font_small.render("Tanque de captación", True, NEGRO)
    surface.blit(lbl, (520+60-lbl.get_width()//2, 480+40+12))
    # Flecha de llenado
    pygame.draw.polygon(surface, AZUL_CLARO, [(580, 480-nivel), (600, 480-nivel-20), (560, 480-nivel-20)])
    pygame.draw.polygon(surface, NEGRO, [(580, 480-nivel), (600, 480-nivel-20), (560, 480-nivel-20)], 2)

def draw_labels(surface):
    lbl = font.render("Captación de Lluvia", True, NEGRO)
    screen.blit(lbl, (W//2 - lbl.get_width()//2, 30))
    # Etiqueta Nube (arriba, margen 12px)
    lbl2 = font_small.render("Nube", True, NEGRO)
    screen.blit(lbl2, (370+90-lbl2.get_width()//2, 80-12-lbl2.get_height()))
    # Etiqueta Techo (abajo del techo, margen 12px)
    lbl3 = font_small.render("Techo", True, NEGRO)
    screen.blit(lbl3, (380+70-lbl3.get_width()//2, 220+16+12))
    # Etiqueta Tubería (a la derecha de la tubería, margen 12px)
    lbl4 = font_small.render("Tubería", True, NEGRO)
    surface.blit(lbl4, (540+20+12, 350+60))

def draw_background(surface):
    surface.fill(BLANCO)
    pygame.draw.line(surface, GRIS_OSCURO, (0, H-60), (W, H-60), 3)

while True:
    draw_background(screen)
    draw_nube(screen, f_anim)
    draw_techo(screen)
    draw_tuberia(screen)
    draw_tanque(screen, nivel)
    draw_labels(screen)
    # Animación de llenado
    if nivel < 120:
        nivel += 0.5 + 0.2*math.sin(f_anim/10)
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
