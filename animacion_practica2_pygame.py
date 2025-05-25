import pygame, sys, math
pygame.init()
W, H = 900, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', int(H*0.045), bold=True)
font_small = pygame.font.SysFont('arial', int(H*0.025), bold=True)

# Paleta profesional
AZUL = (30, 90, 180)
AZUL_CLARO = (120, 180, 255)
AZUL_OSCURO = (20, 40, 80)
AZUL_METAL = (80, 140, 220)
GRIS = (180, 180, 180)
GRIS_OSCURO = (60, 60, 60)
NEGRO = (0,0,0)
BLANCO = (255,255,255)
CARBON = (50,50,50)
ARENA = (220, 200, 140)
GRAVA = (170, 120, 60)
MARRON = (120, 80, 40)

# Geometría tanque (centrado y elevado)
cx, cy = W//2, 90  # Más arriba
r = 90
h = 320
borde = 18

# --- Dibujo de tanque y capas ---
def gradiente_vertical(surface, rect, color1, color2):
    x, y, w, h = rect
    for i in range(h):
        ratio = i / h
        r_ = int(color1[0]*(1-ratio) + color2[0]*ratio)
        g_ = int(color1[1]*(1-ratio) + color2[1]*ratio)
        b_ = int(color1[2]*(1-ratio) + color2[2]*ratio)
        pygame.draw.line(surface, (r_,g_,b_), (x, y+i), (x+w, y+i))

def draw_tank(surface):
    # Sombra base
    pygame.draw.ellipse(surface, (80,80,80,60), (cx-r-10, cy+h-10, 2*r+20, 40))
    # Cuerpo principal con gradiente
    tank = pygame.Surface((2*r, h), pygame.SRCALPHA)
    gradiente_vertical(tank, (0,0,2*r,h), AZUL_CLARO, AZUL)
    pygame.draw.ellipse(tank, AZUL_METAL, (0,0,2*r,40))
    pygame.draw.ellipse(tank, AZUL, (0,h-40,2*r,40))
    pygame.draw.rect(tank, AZUL, (0,20,2*r,h-40))
    pygame.draw.rect(tank, NEGRO, (0,0,2*r,h), 4, border_radius=32)
    surface.blit(tank, (cx-r, cy))
    # Tapa superior
    pygame.draw.ellipse(surface, GRIS, (cx-r-8, cy-24, 2*r+16, 36))
    pygame.draw.ellipse(surface, NEGRO, (cx-r-8, cy-24, 2*r+16, 36), 2)
    # Tapa inferior
    pygame.draw.ellipse(surface, GRIS, (cx-r-8, cy+h-12, 2*r+16, 36))
    pygame.draw.ellipse(surface, NEGRO, (cx-r-8, cy+h-12, 2*r+16, 36), 2)
    # Entrada superior (tubería desde fuera de pantalla)
    pygame.draw.rect(surface, GRIS, (cx-18, cy-80, 36, 56), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (cx-18, cy-80, 36, 56), 2, border_radius=8)
    pygame.draw.ellipse(surface, GRIS, (cx-18, cy-92, 36, 24))
    pygame.draw.ellipse(surface, NEGRO, (cx-18, cy-92, 36, 24), 2)
    # Tubería de entrada desde arriba (fuera de pantalla hasta la tapa)
    pygame.draw.rect(surface, GRIS, (cx-8, 0, 16, cy-80+12), border_radius=6)
    pygame.draw.rect(surface, NEGRO, (cx-8, 0, 16, cy-80+12), 2, border_radius=6)
    # Salida lateral inferior derecha (costado)
    # Bajamos todo 2px (sumamos 2 a la coordenada y)
    # Ancho de la salida: +5 px (de 65 a 70)
    pygame.draw.rect(surface, GRIS, (cx+r-10, cy+h-23, 70, 24), border_radius=8)
    pygame.draw.rect(surface, NEGRO, (cx+r-10, cy+h-23, 70, 24), 2, border_radius=8)
    pygame.draw.ellipse(surface, GRIS, (cx+r+50, cy+h-23, 24, 24))
    pygame.draw.ellipse(surface, NEGRO, (cx+r+50, cy+h-23, 24, 24), 2)
    # Tubería de salida hacia fuera
    pygame.draw.rect(surface, GRIS, (cx+r+62, cy+h-15, 80, 10), border_radius=4)
    pygame.draw.rect(surface, NEGRO, (cx+r+62, cy+h-15, 80, 10), 2, border_radius=4)


def draw_layers(surface):
    # Carbón activado (abajo)
    pygame.draw.ellipse(surface, CARBON, (cx-r+8, cy+h-60, 2*r-16, 60))
    pygame.draw.rect(surface, CARBON, (cx-r+8, cy+2*h//3, 2*r-16, h//3-30))
    # Arena (medio)
    pygame.draw.ellipse(surface, ARENA, (cx-r+8, cy+h//2-20, 2*r-16, 60))
    pygame.draw.rect(surface, ARENA, (cx-r+8, cy+h//3, 2*r-16, h//3-10))
    # Grava (arriba)
    pygame.draw.ellipse(surface, GRAVA, (cx-r+8, cy+20, 2*r-16, 60))
    pygame.draw.rect(surface, GRAVA, (cx-r+8, cy+40, 2*r-16, h//3-20))
    # Líneas divisorias
    pygame.draw.line(surface, BLANCO, (cx-r+16, cy+h//3), (cx+r-16, cy+h//3), 4)
    pygame.draw.line(surface, BLANCO, (cx-r+16, cy+2*h//3), (cx+r-16, cy+2*h//3), 4)

# --- Animación de agua ---
def draw_goticas_agua(surface, t):
    # La caída vertical llega hasta el final del carbón activado
    n = 8  # número de gotas
    # Altura hasta el final del carbón activado
    altura_carbon = cy + h - 30  # 30 px arriba del borde inferior del tanque
    inicio_y = cy - 60
    fin_y = altura_carbon
    trayecto_vertical = fin_y - inicio_y

    # Definir el área de la tubería de salida (rectángulo y elipse)
    tubo_rect = pygame.Rect(cx+r-10, cy+h-23, 70, 24)
    elipse_cx = cx + r + 50 + 12  # centro x de la elipse
    elipse_cy = cy + h - 23 + 12  # centro y de la elipse
    elipse_rx = 12
    elipse_ry = 12

    for i in range(n):
        frac = ((t//6) - i*10) % 80 / 80  # ciclo de caída
        if frac < 0.82:
            # Baja vertical hasta el final del carbón activado
            x = cx
            y = inicio_y + frac*trayecto_vertical/0.82
        else:
            # Curva y sale hacia la derecha
            frac2 = (frac-0.82)/0.18
            x = cx + frac2*200
            y = fin_y + 40*math.sin(frac2*math.pi/2)

        # Verificar si la gota está dentro del área de la tubería de salida
        en_tubo = tubo_rect.collidepoint(x, y)
        # Verificar si está dentro de la elipse de salida
        dx = x - elipse_cx
        dy = y - elipse_cy
        en_elipse = (dx*dx)/(elipse_rx*elipse_rx) + (dy*dy)/(elipse_ry*elipse_ry) <= 1

        # Si la gota está en el tubo o la elipse, NO la dibujamos (desaparece)
        if en_tubo or en_elipse:
            continue

        # Dibuja la gota normalmente
        gota = pygame.Surface((26, 26), pygame.SRCALPHA)
        pygame.draw.circle(gota, (*AZUL_CLARO, 255), (13, 13), 13)
        pygame.draw.circle(gota, (*AZUL, 255), (13, 13), 13, 2)
        pygame.draw.circle(gota, (*BLANCO, 255), (9, 9), 4)
        surface.blit(gota, (int(x)-13, int(y)-13))

    # Onda en la salida (tubería), centrada en la elipse de salida
    for k in range(2):
        amp = 7 - 2 * k
        largo = 38 - 8 * k
        for i in range(0, largo, 2):
            px = elipse_cx + i
            py = elipse_cy + int(math.sin((t/6)+i/7)*amp)
            pygame.draw.circle(surface, AZUL_CLARO, (px, py), 3 - k)

# --- Etiquetas y callouts ---
def draw_labels(surface):
    # Título
    lbl = font.render("Filtrado Multicapa Industrial", True, NEGRO)
    screen.blit(lbl, (W//2 - lbl.get_width()//2, 30))
    # Etiquetas de capas alineadas a la izquierda
    etiquetas = ["Grava", "Arena", "Carbón activado"]
    y_caps = [cy+60, cy+h//2, cy+h-40]
    for i, (etq, ycap) in enumerate(zip(etiquetas, y_caps)):
        lbl_etq = font_small.render(etq, True, NEGRO)
        lx = cx - r - 110
        ly = ycap - lbl_etq.get_height()//2
        screen.blit(lbl_etq, (lx, ly))
        # Línea callout horizontal
        pygame.draw.line(screen, NEGRO, (lx+lbl_etq.get_width()+8, ly+lbl_etq.get_height()//2), (cx-r+8, ycap), 2)
    # Etiqueta Entrada (a la derecha del tubo superior)
    lbl_entrada = font_small.render("Entrada", True, NEGRO)
    ex, ey = cx + 90, cy-80
    screen.blit(lbl_entrada, (ex, ey))
    pygame.draw.line(screen, NEGRO, (ex-8, ey+lbl_entrada.get_height()//2), (cx+18, cy-80), 2)
    # Etiqueta Salida (encima del tubo de salida)
    lbl_salida = font_small.render("Salida", True, NEGRO)
    sx, sy = cx+r+70, cy+h+2
    screen.blit(lbl_salida, (sx, sy))
    pygame.draw.line(screen, NEGRO, (sx+lbl_salida.get_width()//2, sy+lbl_salida.get_height()), (cx+r+82, cy+h+18), 2)

# --- Fondo ---
def draw_background(surface):
    surface.fill((240,240,245))
    pygame.draw.line(surface, GRIS_OSCURO, (0, H-60), (W, H-60), 3)

# --- Main loop ---
onda_anim = 0
while True:
    draw_background(screen)
    draw_tank(screen)
    draw_layers(screen)
    draw_goticas_agua(screen, onda_anim)
    draw_labels(screen)
    onda_anim += 1
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
