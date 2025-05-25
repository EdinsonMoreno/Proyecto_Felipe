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
ROJO = (220, 60, 60)
ROJO_CLARO = (255, 120, 120)
GRIS = (180, 180, 180)
GRIS_OSCURO = (80, 80, 80)
NEGRO = (0,0,0)
BLANCO = (255,255,255)

# Geometría del intercambiador
shell_x, shell_y = 120, 180
shell_w, shell_h = 660, 160
shell_r = shell_h//2
n_tubos = 7
sep_tubos = shell_h // (n_tubos+1)
tube_r = 12
baffles_x = [shell_x+shell_w//5*i for i in range(1,5)]

# Entradas/salidas de carcasa (3 arriba, 3 abajo)
shell_inlets = [shell_x+shell_w//6, shell_x+shell_w//2, shell_x+5*shell_w//6]
shell_outlets = [shell_x+shell_w//6, shell_x+shell_w//2, shell_x+5*shell_w//6]

# Animación
f_anim = 0
n_flechas_rojas = n_tubos
n_flechas_azules = 3  # una por cada entrada/salida

# --- Dibujo de estructura ---
def draw_shell(surface):
    # Shell principal con extremos redondeados
    pygame.draw.rect(surface, GRIS, (shell_x, shell_y, shell_w, shell_h), border_radius=shell_r)
    pygame.draw.rect(surface, NEGRO, (shell_x, shell_y, shell_w, shell_h), 4, border_radius=shell_r)
    # Extremos redondeados
    pygame.draw.ellipse(surface, GRIS, (shell_x-shell_r, shell_y, shell_h, shell_h))
    pygame.draw.ellipse(surface, GRIS, (shell_x+shell_w-shell_r, shell_y, shell_h, shell_h))
    pygame.draw.ellipse(surface, NEGRO, (shell_x-shell_r, shell_y, shell_h, shell_h), 4)
    pygame.draw.ellipse(surface, NEGRO, (shell_x+shell_w-shell_r, shell_y, shell_h, shell_h), 4)
    # Chapas de tubos
    pygame.draw.rect(surface, GRIS_OSCURO, (shell_x-18, shell_y+10, 18, shell_h-20), border_radius=8)
    pygame.draw.rect(surface, GRIS_OSCURO, (shell_x+shell_w, shell_y+10, 18, shell_h-20), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (shell_x-18, shell_y+10, 18, shell_h-20), 2, border_radius=8)
    pygame.draw.rect(surface, NEGRO, (shell_x+shell_w, shell_y+10, 18, shell_h-20), 2, border_radius=8)
    # Tubos internos
    for i in range(n_tubos):
        ty = shell_y + sep_tubos*(i+1)
        pygame.draw.line(surface, ROJO_CLARO, (shell_x, ty), (shell_x+shell_w, ty), tube_r)
        pygame.draw.line(surface, NEGRO, (shell_x, ty), (shell_x+shell_w, ty), 2)
    # Baffles (deflectores)
    for j, bx in enumerate(baffles_x):
        if j%2==0:
            pygame.draw.rect(surface, GRIS_OSCURO, (bx, shell_y, 16, shell_h*0.6))
            pygame.draw.rect(surface, NEGRO, (bx, shell_y, 16, shell_h*0.6), 2)
        else:
            pygame.draw.rect(surface, GRIS_OSCURO, (bx, shell_y+shell_h*0.4, 16, shell_h*0.6))
            pygame.draw.rect(surface, NEGRO, (bx, shell_y+shell_h*0.4, 16, shell_h*0.6), 2)
    # Entradas/salidas tubos (rojo)
    for i in range(n_tubos):
        ty = shell_y + sep_tubos*(i+1)
        pygame.draw.rect(surface, ROJO_CLARO, (shell_x-70, ty-tube_r, 52, tube_r*2), border_radius=8)
        pygame.draw.rect(surface, ROJO_CLARO, (shell_x+shell_w+18, ty-tube_r, 52, tube_r*2), border_radius=8)
        pygame.draw.rect(surface, NEGRO, (shell_x-70, ty-tube_r, 52, tube_r*2), 2, border_radius=8)
        pygame.draw.rect(surface, NEGRO, (shell_x+shell_w+18, ty-tube_r, 52, tube_r*2), 2, border_radius=8)
    # Entradas de carcasa (azul)
    for x in shell_inlets:
        pygame.draw.rect(surface, AZUL_CLARO, (x-24, shell_y-60, 48, 60), border_radius=12)
        pygame.draw.rect(surface, NEGRO, (x-24, shell_y-60, 48, 60), 2, border_radius=12)
    # Salidas de carcasa (azul)
    for x in shell_outlets:
        pygame.draw.rect(surface, AZUL_CLARO, (x-24, shell_y+shell_h, 48, 60), border_radius=12)
        pygame.draw.rect(surface, NEGRO, (x-24, shell_y+shell_h, 48, 60), 2, border_radius=12)

# --- Flechas animadas ---
def draw_flechas_tubos(surface):
    # Flechas rojas: una por tubo, de izquierda a derecha
    for i in range(n_tubos):
        ty = shell_y + sep_tubos*(i+1)
        for k in range(2):
            frac = ((f_anim + i*30 + k*120) % (shell_w+60)) / (shell_w+60)
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

def draw_flechas_shell(surface):
    # Flechas azules: zigzag, una por cada entrada/salida
    for idx, (xin, xout) in enumerate(zip(shell_inlets, shell_outlets)):
        # Trayectoria: entra por arriba, zigzaguea entre baffles, sale por abajo
        path = [
            (xin, shell_y-30),
            (xin, shell_y+20),
            (xin+60*(-1)**idx, shell_y+shell_h//3),
            (xout-60*(-1)**idx, shell_y+2*shell_h//3),
            (xout, shell_y+shell_h-20),
            (xout, shell_y+shell_h+30)
        ]
        frac = ((f_anim + idx*60) % 320) / 320
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

# --- Etiquetas técnicas y flechas indicadoras ---
def draw_labels(surface):
    # Título
    lbl = font.render("Intercambiador de Calor", True, NEGRO)
    screen.blit(lbl, (W//2 - lbl.get_width()//2, 30))
    # Entrada de tubo
    lbl1 = font_small.render("Entrada de tubo", True, NEGRO)
    x1, y1 = shell_x-70, shell_y-40
    screen.blit(lbl1, (x1, y1))
    # Flecha indicadora
    pygame.draw.line(screen, NEGRO, (x1+lbl1.get_width()//2, y1+lbl1.get_height()), (shell_x-10, shell_y+sep_tubos*4), 2)
    pygame.draw.polygon(screen, NEGRO, [(shell_x-10, shell_y+sep_tubos*4), (shell_x-18, shell_y+sep_tubos*4-6), (shell_x-18, shell_y+sep_tubos*4+6)])
    # Salida de tubo
    lbl2 = font_small.render("Salida de tubo", True, NEGRO)
    x2, y2 = shell_x+shell_w+18+10, shell_y-40
    screen.blit(lbl2, (x2, y2))
    pygame.draw.line(screen, NEGRO, (x2+lbl2.get_width()//2, y2+lbl2.get_height()), (shell_x+shell_w+18+10, shell_y+sep_tubos*4), 2)
    pygame.draw.polygon(screen, NEGRO, [(shell_x+shell_w+18+10, shell_y+sep_tubos*4), (shell_x+shell_w+18+2, shell_y+sep_tubos*4-6), (shell_x+shell_w+18+2, shell_y+sep_tubos*4+6)])
    # Entradas de carcasa
    for i, x in enumerate(shell_inlets):
        lblin = font_small.render("Entrada de carcasa", True, NEGRO)
        lx, ly = x-60, shell_y-90
        screen.blit(lblin, (lx, ly))
        pygame.draw.line(screen, NEGRO, (lx+lblin.get_width()//2, ly+lblin.get_height()), (x, shell_y-60), 2)
        pygame.draw.polygon(screen, NEGRO, [(x, shell_y-60), (x-8, shell_y-60-8), (x+8, shell_y-60-8)])
    # Salidas de carcasa
    for i, x in enumerate(shell_outlets):
        lblout = font_small.render("Salida de carcasa", True, NEGRO)
        lx, ly = x-60, shell_y+shell_h+70
        screen.blit(lblout, (lx, ly))
        pygame.draw.line(screen, NEGRO, (lx+lblout.get_width()//2, ly), (x, shell_y+shell_h+60), 2)
        pygame.draw.polygon(screen, NEGRO, [(x, shell_y+shell_h+60), (x-8, shell_y+shell_h+60+8), (x+8, shell_y+shell_h+60+8)])
    # Deflectores
    for i, bx in enumerate(baffles_x):
        lblbaf = font_small.render(" ", False, NEGRO)
        if i%2==0:
            lx, ly = bx+16+20, shell_y+10
        else:
            lx, ly = bx+16+20, shell_y+shell_h*0.4+10
        screen.blit(lblbaf, (lx, ly))
        # Flecha indicadora
        pygame.draw.line(screen, NEGRO, (lx, ly+lblbaf.get_height()//2), (bx+16, ly+lblbaf.get_height()//2), 2)
        pygame.draw.polygon(screen, NEGRO, [(bx+16, ly+lblbaf.get_height()//2), (bx+16-8, ly+lblbaf.get_height()//2-6), (bx+16-8, ly+lblbaf.get_height()//2+6)])
    # Chapa de tubos
    lblchapa = font_small.render(" ", False, NEGRO)
    cx1, cy1 = shell_x-18-lblchapa.get_width()-10, shell_y+shell_h//2-lblchapa.get_height()//2
    cx2, cy2 = shell_x+shell_w+18+10, shell_y+shell_h//2-lblchapa.get_height()//2
    screen.blit(lblchapa, (cx1, cy1))
    pygame.draw.line(screen, NEGRO, (cx1+lblchapa.get_width(), cy1+lblchapa.get_height()//2), (shell_x-18, shell_y+shell_h//2), 2)
    pygame.draw.polygon(screen, NEGRO, [(shell_x-18, shell_y+shell_h//2), (shell_x-18-8, shell_y+shell_h//2-6), (shell_x-18-8, shell_y+shell_h//2+6)])
    screen.blit(lblchapa, (cx2, cy2))
    pygame.draw.line(screen, NEGRO, (cx2, cy2+lblchapa.get_height()//2), (shell_x+shell_w+18, shell_y+shell_h//2), 2)
    pygame.draw.polygon(screen, NEGRO, [(shell_x+shell_w+18, shell_y+shell_h//2), (shell_x+shell_w+18+8, shell_y+shell_h//2-6), (shell_x+shell_w+18+8, shell_y+shell_h//2+6)])

# --- Fondo ---
def draw_background(surface):
    surface.fill(BLANCO)
    pygame.draw.line(surface, GRIS_OSCURO, (0, H-60), (W, H-60), 3)

# --- Main loop ---
while True:
    draw_background(screen)
    draw_shell(screen)
    draw_flechas_tubos(screen)
    draw_flechas_shell(screen)
    draw_labels(screen)
    f_anim += 2
    # Botón Volver centrado abajo
    volver_rect = pygame.Rect(W//2-60, H-70, 120, 40)
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
