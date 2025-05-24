import pygame, sys, math, random
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 24, bold=True)
font_small = pygame.font.SysFont('arial', 16)

# Colores
AZUL = (60, 120, 220)
AZUL_CLARO = (120, 180, 255)
GRIS = (180, 180, 180)
NEGRO = (0,0,0)
BLANCO = (255,255,255)
NUBE = (200, 200, 200)
TECHO = (120, 80, 40)
VERDE = (60, 200, 80)

lluvia = [[random.randint(350, 540), 120+random.randint(0,30), random.uniform(2, 4)] for _ in range(12)]
nivel = 0
f_anim = 0

def draw_nube(surface, anim):
    # Nube con sombra
    sombra = pygame.Surface((220, 60), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0,0,0,30), (0, 30, 220, 30))
    surface.blit(sombra, (350, 80))
    pygame.draw.ellipse(surface, NUBE, (370, 80, 180, 60))
    pygame.draw.ellipse(surface, NUBE, (350, 100, 60, 40))
    pygame.draw.ellipse(surface, NUBE, (500, 100, 60, 40))
    # Gotas de lluvia
    for i, (gx, gy, vel) in enumerate(lluvia):
        pygame.draw.ellipse(surface, AZUL_CLARO, (gx, gy, 10, 22))
        lluvia[i][1] += vel
        if lluvia[i][1] > 180:
            lluvia[i][1] = 120

def draw_techo(surface):
    # Techo
    pygame.draw.polygon(surface, TECHO, [(340, 180), (560, 180), (520, 220), (380, 220)])
    pygame.draw.rect(surface, (80,60,30), (380, 220, 140, 16), border_radius=4)
    # Flecha de bajada
    pygame.draw.polygon(surface, AZUL, [(450, 220), (470, 250), (430, 250)])

def draw_tuberia(surface):
    # Tubería
    pygame.draw.rect(surface, GRIS, (440, 250, 20, 80), border_radius=8)
    pygame.draw.rect(surface, GRIS, (440, 330, 80, 20), border_radius=8)
    pygame.draw.rect(surface, GRIS, (520, 250, 20, 100), border_radius=8)
    pygame.draw.rect(surface, GRIS, (440, 350, 100, 20), border_radius=8)
    pygame.draw.rect(surface, GRIS, (540, 350, 20, 120), border_radius=8)
    # Flechas de flujo
    pygame.draw.polygon(surface, AZUL, [(450, 320), (470, 340), (430, 340)])
    pygame.draw.polygon(surface, AZUL, [(550, 400), (570, 420), (530, 420)])

def draw_tanque(surface, nivel):
    # Sombra
    sombra = pygame.Surface((120, 40), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0,0,0,40), (0, 20, 120, 20))
    surface.blit(sombra, (520, 450))
    # Tanque
    pygame.draw.ellipse(surface, GRIS, (520, 350, 120, 60))
    pygame.draw.rect(surface, GRIS, (520, 380, 120, 120), border_radius=30)
    pygame.draw.ellipse(surface, GRIS, (520, 480, 120, 40))
    pygame.draw.rect(surface, NEGRO, (520, 350, 120, 170), 3, border_radius=30)
    # Nivel de agua
    pygame.draw.rect(surface, AZUL, (530, 480-nivel, 100, nivel), border_radius=18)
    # Etiquetas
    lbl = font_small.render("Tanque de captación", True, AZUL)
    surface.blit(lbl, (530, 340))    # Flecha de llenado
    pygame.draw.polygon(surface, AZUL_CLARO, [(580, 480-nivel), (600, 480-nivel-20), (560, 480-nivel-20)])

def draw_labels(surface):
    lbl = font.render("Captación de Lluvia", True, AZUL)
    surface.blit(lbl, (300, 40))
    lbl2 = font_small.render("Nube", True, NUBE)
    surface.blit(lbl2, (370, 70))
    lbl3 = font_small.render("Techo", True, TECHO)
    surface.blit(lbl3, (380, 230))
    lbl4 = font_small.render("Tubería", True, GRIS)
    surface.blit(lbl4, (520, 330))

while True:
    screen.fill(BLANCO)
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
