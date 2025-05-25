import pygame, sys, math
pygame.init()
W, H = 900, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', int(H*0.045), bold=True)
font_small = pygame.font.SysFont('arial', int(H*0.025))

# Paleta técnica
AZUL = (30, 90, 180)
AZUL_CLARO = (120, 180, 255)
ROJO = (220, 60, 60)
ROJO_CLARO = (255, 120, 120)
GRIS = (200, 200, 200)
GRIS_OSCURO = (80, 80, 80)
NEGRO = (0,0,0)
BLANCO = (255,255,255)

# Parámetros geométricos
shell_x, shell_y = 120, 180
shell_w, shell_h = 660, 160
n_tubos = 7
sep_tubos = shell_h // (n_tubos+1)
tube_r = 12
baffles_x = [shell_x+shell_w//4, shell_x+shell_w//2, shell_x+3*shell_w//4]

# Flechas animadas
f_anim = 0
flechas_azules = 3
flechas_rojas = 3

# --- Dibujo de estructura ---
def draw_shell(surface):
    # Shell principal
    pygame.draw.rect(surface, GRIS, (shell_x, shell_y, shell_w, shell_h), border_radius=40)
    pygame.draw.rect(surface, NEGRO, (shell_x, shell_y, shell_w, shell_h), 4, border_radius=40)
    # Chapas de tubos
    pygame.draw.rect(surface, GRIS_OSCURO, (shell_x-18, shell_y, 18, shell_h), border_radius=8)
    pygame.draw.rect(surface, GRIS_OSCURO, (shell_x+shell_w, shell_y, 18, shell_h), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (shell_x-18, shell_y, 18, shell_h), 2, border_radius=8)
    pygame.draw.rect(surface, NEGRO, (shell_x+shell_w, shell_y, 18, shell_h), 2, border_radius=8)
    # Tubos internos
    for i in range(n_tubos):
        ty = shell_y + sep_tubos*(i+1)
        pygame.draw.line(surface, ROJO_CLARO, (shell_x, ty), (shell_x+shell_w, ty), tube_r)
        pygame.draw.line(surface, NEGRO, (shell_x, ty), (shell_x+shell_w, ty), 2)
    # Baffles (deflectores)
    for i, bx in enumerate(baffles_x):
        if i%2==0:
            pygame.draw.rect(surface, GRIS_OSCURO, (bx, shell_y, 16, shell_h*0.6))
            pygame.draw.rect(surface, NEGRO, (bx, shell_y, 16, shell_h*0.6), 2)
        else:
            pygame.draw.rect(surface, GRIS_OSCURO, (bx, shell_y+shell_h*0.4, 16, shell_h*0.6))
            pygame.draw.rect(surface, NEGRO, (bx, shell_y+shell_h*0.4, 16, shell_h*0.6), 2)
    # Entradas/salidas
    # Tubos (rojo)
    pygame.draw.rect(surface, ROJO_CLARO, (shell_x-70, shell_y+sep_tubos*(n_tubos//2+1)-tube_r, 52, tube_r*2), border_radius=8)
    pygame.draw.rect(surface, ROJO_CLARO, (shell_x+shell_w+18, shell_y+sep_tubos*(n_tubos//2+1)-tube_r, 52, tube_r*2), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (shell_x-70, shell_y+sep_tubos*(n_tubos//2+1)-tube_r, 52, tube_r*2), 2, border_radius=8)
    pygame.draw.rect(surface, NEGRO, (shell_x+shell_w+18, shell_y+sep_tubos*(n_tubos//2+1)-tube_r, 52, tube_r*2), 2, border_radius=8)
    # Carcasa (azul)
    pygame.draw.rect(surface, AZUL_CLARO, (shell_x+shell_w//2-24, shell_y-60, 48, 60), border_radius=12)
    pygame.draw.rect(surface, AZUL_CLARO, (shell_x+shell_w//2-24, shell_y+shell_h, 48, 60), border_radius=12)
    pygame.draw.rect(surface, NEGRO, (shell_x+shell_w//2-24, shell_y-60, 48, 60), 2, border_radius=12)
    pygame.draw.rect(surface, NEGRO, (shell_x+shell_w//2-24, shell_y+shell_h, 48, 60), 2, border_radius=12)

# --- Flechas animadas ---
def draw_flechas_tubos(surface, anim):
    # Flechas rojas: rectas, de izquierda a derecha, por los tubos
    for i in range(flechas_rojas):
        frac = ((anim/2 + i*60) % (shell_w+60)) / (shell_w+60)
        for t in [2, 4, 6]:
            ty = shell_y + sep_tubos*(t)
            x = shell_x - 30 + frac*(shell_w+60)
            # Cuerpo flecha
            pygame.draw.line(surface, ROJO, (x, ty), (x+36, ty), 8)
            pygame.draw.line(surface, NEGRO, (x, ty), (x+36, ty), 2)
            # Cabeza flecha
            tip = (x+36, ty)
            left = (x+24, ty-8)
            right = (x+24, ty+8)
            pygame.draw.polygon(surface, ROJO, [tip, left, right])
            pygame.draw.polygon(surface, NEGRO, [tip, left, right], 2)

def draw_flechas_shell(surface, anim):
    # Flechas azules: serpenteantes, de arriba a abajo y viceversa
    for i in range(flechas_azules):
        frac = ((anim + i*80) % (2*shell_h+120)) / (2*shell_h+120)
        # Trayectoria: entra por arriba, baja, sube, baja, sale por abajo
        path = [
            (shell_x+shell_w//2, shell_y-30),
            (shell_x+shell_w//2, shell_y+20),
            (shell_x+shell_w//2+60, shell_y+shell_h//3),
            (shell_x+shell_w//2-60, shell_y+2*shell_h//3),
            (shell_x+shell_w//2, shell_y+shell_h-20),
            (shell_x+shell_w//2, shell_y+shell_h+30)
        ]
        # Interpolación a lo largo del path
        total = len(path)-1
        seg = int(frac*total)
        seg_frac = (frac*total) % 1
        if seg < total:
            x1, y1 = path[seg]
            x2, y2 = path[seg+1]
            x = x1 + (x2-x1)*seg_frac
            y = y1 + (y2-y1)*seg_frac
            # Cuerpo flecha
            pygame.draw.line(surface, AZUL, (x1, y1), (x, y), 8)
            pygame.draw.line(surface, NEGRO, (x1, y1), (x, y), 2)
            # Cabeza flecha
            ang = math.atan2(y2-y1, x2-x1)
            tip = (x, y)
            left = (x-14*math.cos(ang-0.4), y-14*math.sin(ang-0.4))
            right = (x-14*math.cos(ang+0.4), y-14*math.sin(ang+0.4))
            pygame.draw.polygon(surface, AZUL, [tip, left, right])
            pygame.draw.polygon(surface, NEGRO, [tip, left, right], 2)

# --- Etiquetas técnicas ---
def draw_labels(surface):
    # Título
    lbl = font.render("Intercambiador de Calor - Shell & Tube", True, NEGRO)
    screen.blit(lbl, (W//2 - lbl.get_width()//2, 30))
    # Entradas/salidas
    lbl1 = font_small.render("Entrada de tubo", True, NEGRO)
    screen.blit(lbl1, (shell_x-70, shell_y+sep_tubos*(n_tubos//2+1)-tube_r-30))
    lbl2 = font_small.render("Salida de tubo", True, NEGRO)
    screen.blit(lbl2, (shell_x+shell_w+18+10, shell_y+sep_tubos*(n_tubos//2+1)-tube_r-30))
    lbl3 = font_small.render("Entrada de carcasa", True, NEGRO)
    screen.blit(lbl3, (shell_x+shell_w//2-24, shell_y-60-30))
    lbl4 = font_small.render("Salida de carcasa", True, NEGRO)
    screen.blit(lbl4, (shell_x+shell_w//2-24, shell_y+shell_h+60-10))
    # Deflectores
    for i, bx in enumerate(baffles_x):
        lblbaf = font_small.render("Deflector", True, NEGRO)
        if i%2==0:
            screen.blit(lblbaf, (bx+16+10, shell_y+10))
        else:
            screen.blit(lblbaf, (bx+16+10, shell_y+shell_h*0.4+10))
    # Chapa de tubos
    lblchapa = font_small.render("Chapa de tubos", True, NEGRO)
    screen.blit(lblchapa, (shell_x-18-lblchapa.get_width()-10, shell_y+shell_h//2-lblchapa.get_height()//2))
    screen.blit(lblchapa, (shell_x+shell_w+18+10, shell_y+shell_h//2-lblchapa.get_height()//2))

# --- Fondo ---
def draw_background(surface):
    surface.fill(BLANCO)
    pygame.draw.line(surface, GRIS_OSCURO, (0, H-60), (W, H-60), 3)

# --- Main loop ---
while True:
    draw_background(screen)
    draw_shell(screen)
    draw_flechas_tubos(screen, f_anim)
    draw_flechas_shell(screen, f_anim)
    draw_labels(screen)
    f_anim += 2
    # Botón Volver
    volver_rect = pygame.Rect(W-150, H-70, 120, 40)
    pygame.draw.rect(screen, GRIS_OSCURO, volver_rect, border_radius=8)
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
