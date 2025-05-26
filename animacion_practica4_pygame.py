import pygame, sys, math, random
pygame.init()
W, H = 900, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', int(H*0.045), bold=True)
font_small = pygame.font.SysFont('arial', int(H*0.025))
font_tiny = pygame.font.SysFont('arial', int(H*0.020))

# Paleta profesional mejorada
AZUL = (30, 90, 180)
AZUL_CLARO = (120, 180, 255)
AZUL_OSCURO = (10, 60, 120)
AZUL_AGUA = (80, 160, 200, 180)  # Semitransparente para agua
ROJO = (220, 60, 60)
ROJO_FUEGO = (255, 80, 40)
NARANJA = (255, 140, 60)
AMARILLO = (255, 220, 80)
GRIS = (180, 180, 180)
GRIS_METAL = (160, 170, 185)
GRIS_OSCURO = (80, 80, 80)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VAPOR_COLOR = (240, 240, 250, 120)  # Blanco semitransparente

# Inicializar burbujas para el interior de la caldera
burbujas_internas = []
for _ in range(15):
    burbujas_internas.append({
        'x': random.randint(375, 425),  # Dentro de la caldera
        'y': random.randint(350, 420),  # Área del agua
        'size': random.randint(3, 8),
        'speed': random.uniform(0.5, 1.5),
        'fase': random.uniform(0, math.pi * 2)
    })

# Partículas de vapor
particulas_vapor = []
for _ in range(20):
    particulas_vapor.append({
        'x': random.randint(380, 420),
        'y': random.randint(200, 250),
        'size': random.randint(8, 20),
        'speed': random.uniform(0.3, 0.8),
        'alpha': random.randint(60, 120),
        'fase': random.uniform(0, math.pi * 2)
    })

# Partículas de humo adicionales para realismo
particulas_humo = []
for _ in range(8):
    particulas_humo.append({
        'x': random.randint(320, 480),
        'y': random.randint(470, 490),
        'size': random.randint(12, 25),
        'speed': random.uniform(0.2, 0.6),
        'alpha': random.randint(30, 80),
        'drift': random.uniform(-0.5, 0.5)
    })

# Llamas de fuego
llamas = []
for _ in range(12):
    llamas.append({
        'x': random.randint(320, 480),
        'y': random.randint(480, 500),
        'altura': random.randint(25, 45),
        'ancho': random.randint(8, 15),
        'fase': random.uniform(0, math.pi * 2),
        'intensidad': random.uniform(0.7, 1.0)
    })

# Indicadores LED de estado
indicadores_led = [
    {'x': 380, 'y': 260, 'color': (0, 255, 0), 'estado': 'activo'},    # Verde - Sistema activo
    {'x': 400, 'y': 260, 'color': (255, 255, 0), 'estado': 'calentando'}, # Amarillo - Calentando
    {'x': 420, 'y': 260, 'color': (255, 0, 0), 'estado': 'presion'}     # Rojo - Presión alta
]

f_anim = 0

def sombra(surface, rect, radio=18, offset=(8,8), alpha=60):
    sombra_surf = pygame.Surface((rect[2]+20, rect[3]+20), pygame.SRCALPHA)
    pygame.draw.rect(sombra_surf, (0,0,0,alpha), (offset[0], offset[1], rect[2], rect[3]), border_radius=radio)
    surface.blit(sombra_surf, (rect[0]-10, rect[1]-10))

def gradiente_vertical(surface, rect, color1, color2):
    x, y, w, h = rect
    for i in range(h):
        ratio = i / h
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))

def draw_boiler_base(surface):
    """Dibuja las patas de soporte de la caldera"""
    # Patas metálicas (4 patas)
    pata_w, pata_h = 15, 60
    patas_x = [350, 380, 420, 450]
    
    for px in patas_x:
        # Sombra de la pata
        sombra(surface, (px, 460, pata_w, pata_h), 8, (4,4), 40)
        # Pata metálica con gradiente
        pata_surf = pygame.Surface((pata_w, pata_h), pygame.SRCALPHA)
        gradiente_vertical(pata_surf, (0, 0, pata_w, pata_h), GRIS_METAL, GRIS_OSCURO)
        surface.blit(pata_surf, (px, 460))
        pygame.draw.rect(surface, NEGRO, (px, 460, pata_w, pata_h), 2, border_radius=4)

def draw_boiler_body(surface):
    """Dibuja el cuerpo principal de la caldera cilíndrica vertical"""
    # Posición y dimensiones de la caldera
    caldera_x, caldera_y = 350, 250
    caldera_w, caldera_h = 100, 210
    
    # Sombra principal de la caldera
    sombra(surface, (caldera_x, caldera_y, caldera_w, caldera_h), 25, (8,8), 80)
    
    # Cuerpo principal con gradiente metálico
    cuerpo_surf = pygame.Surface((caldera_w, caldera_h), pygame.SRCALPHA)
    gradiente_vertical(cuerpo_surf, (0, 0, caldera_w, caldera_h), AZUL_CLARO, GRIS_METAL)
    surface.blit(cuerpo_surf, (caldera_x, caldera_y))
    
    # Borde del cuerpo
    pygame.draw.rect(surface, NEGRO, (caldera_x, caldera_y, caldera_w, caldera_h), 4, border_radius=20)
    
    # Tapas superior e inferior (cilindros)
    # Tapa superior
    pygame.draw.ellipse(surface, GRIS_METAL, (caldera_x-5, caldera_y-10, caldera_w+10, 25))
    pygame.draw.ellipse(surface, NEGRO, (caldera_x-5, caldera_y-10, caldera_w+10, 25), 3)
    
    # Tapa inferior  
    pygame.draw.ellipse(surface, GRIS_METAL, (caldera_x-5, caldera_y+caldera_h-10, caldera_w+10, 25))
    pygame.draw.ellipse(surface, NEGRO, (caldera_x-5, caldera_y+caldera_h-10, caldera_w+10, 25), 3)

def draw_water_level(surface, anim):
    """Dibuja el nivel de agua visible dentro de la caldera"""
    # Ventana transparente en el lateral de la caldera
    ventana_x, ventana_y = 365, 300
    ventana_w, ventana_h = 70, 120
    
    # Marco de la ventana de inspección
    pygame.draw.rect(surface, GRIS_OSCURO, (ventana_x-3, ventana_y-3, ventana_w+6, ventana_h+6), border_radius=8)
    pygame.draw.rect(surface, BLANCO, (ventana_x, ventana_y, ventana_w, ventana_h), border_radius=5)
    pygame.draw.rect(surface, NEGRO, (ventana_x, ventana_y, ventana_w, ventana_h), 2, border_radius=5)
    
    # Nivel de agua (75% de la ventana)
    nivel_agua = int(ventana_h * 0.75)
    agua_y = ventana_y + ventana_h - nivel_agua
    
    # Superficie del agua con ondulación
    superficie_puntos = []
    for i in range(ventana_w + 1):
        onda = 3 * math.sin((i / 10) + anim / 8)
        superficie_puntos.append((ventana_x + i, agua_y + onda))
    
    # Dibujar agua con transparencia
    agua_surf = pygame.Surface((ventana_w, nivel_agua + 10), pygame.SRCALPHA)
    puntos_agua = [(0, nivel_agua)] + [(p[0] - ventana_x, p[1] - agua_y) for p in superficie_puntos] + [(ventana_w, nivel_agua)]
    if len(puntos_agua) > 2:
        pygame.draw.polygon(agua_surf, AZUL_AGUA, puntos_agua)
    surface.blit(agua_surf, (ventana_x, agua_y))

def draw_bubbles_internal(surface, anim):
    """Dibuja burbujas animadas dentro del nivel de agua"""
    for burbuja in burbujas_internas:
        # Movimiento oscilante
        offset_x = 5 * math.sin(anim / 10 + burbuja['fase'])
        x = burbuja['x'] + offset_x
        y = burbuja['y']
        
        # Dibujar burbuja con transparencia
        burbuja_surf = pygame.Surface((burbuja['size']*2, burbuja['size']*2), pygame.SRCALPHA)
        pygame.draw.circle(burbuja_surf, (200, 220, 255, 150), (burbuja['size'], burbuja['size']), burbuja['size'])
        pygame.draw.circle(burbuja_surf, AZUL_CLARO, (burbuja['size'], burbuja['size']), burbuja['size'], 1)
        surface.blit(burbuja_surf, (x - burbuja['size'], y - burbuja['size']))
        
        # Mover burbuja hacia arriba
        burbuja['y'] -= burbuja['speed']
        
        # Reiniciar burbuja cuando llega arriba
        if burbuja['y'] < 300:
            burbuja['y'] = random.randint(400, 420)
            burbuja['x'] = random.randint(375, 425)
            burbuja['size'] = random.randint(3, 8)

def draw_steam(surface, anim):
    """Dibuja vapor animado saliendo de las tuberías"""
    for particula in particulas_vapor:
        # Movimiento ondulante hacia arriba
        offset_x = 15 * math.sin(anim / 15 + particula['fase'])
        x = particula['x'] + offset_x
        y = particula['y']
        
        # Dibujar partícula de vapor
        vapor_surf = pygame.Surface((particula['size']*2, particula['size']*2), pygame.SRCALPHA)
        alpha = max(0, particula['alpha'] - int(particula['y'] / 3))  # Se desvanece al subir
        color_vapor = (*VAPOR_COLOR[:3], alpha)
        pygame.draw.circle(vapor_surf, color_vapor, (particula['size'], particula['size']), particula['size'])
        surface.blit(vapor_surf, (x - particula['size'], y - particula['size']))
        
        # Mover vapor hacia arriba y expandir
        particula['y'] -= particula['speed']
        particula['size'] += 0.1
        
        # Reiniciar partícula cuando desaparece
        if particula['y'] < 50 or particula['size'] > 25:
            particula['y'] = random.randint(200, 250)
            particula['x'] = random.randint(380, 420)
            particula['size'] = random.randint(8, 12)
            particula['alpha'] = random.randint(80, 120)

def draw_smoke(surface, anim):
    """Dibuja humo animado saliendo de las chimeneas"""
    for particula in particulas_humo:
        # Movimiento suave y deriva
        x = particula['x'] + particula['drift'] * 10
        y = particula['y'] - particula['speed']
        
        # Dibujar partícula de humo
        humo_surf = pygame.Surface((particula['size']*2, particula['size']*2), pygame.SRCALPHA)
        alpha = max(0, particula['alpha'] - int(particula['y'] / 5))  # Se desvanece al subir
        pygame.draw.circle(humo_surf, (50, 50, 50, alpha), (particula['size'], particula['size']), particula['size'])
        surface.blit(humo_surf, (x - particula['size'], y - particula['size']))
        
        # Mover humo hacia arriba
        particula['y'] -= particula['speed']
        
        # Reiniciar partícula de humo cuando desaparece
        if particula['y'] < 0:
            particula['y'] = random.randint(470, 490)
            particula['x'] = random.randint(320, 480)
            particula['size'] = random.randint(12, 25)
            particula['alpha'] = random.randint(30, 80)

def draw_smoke_particles(surface, anim):
    """Dibuja partículas de humo realistas"""
    for particula in particulas_humo:
        # Movimiento natural del humo
        x = particula['x'] + particula['drift'] * anim/10
        y = particula['y']
        
        # Dibujar partícula de humo
        humo_surf = pygame.Surface((particula['size']*2, particula['size']*2), pygame.SRCALPHA)
        alpha = max(0, particula['alpha'] - int(particula['y'] / 8))
        color_humo = (100, 100, 100, alpha)
        pygame.draw.circle(humo_surf, color_humo, (particula['size'], particula['size']), particula['size'])
        surface.blit(humo_surf, (x - particula['size'], y - particula['size']))
        
        # Mover humo hacia arriba
        particula['y'] -= particula['speed']
        particula['size'] += 0.05
        
        # Reiniciar partícula
        if particula['y'] < 200 or particula['size'] > 35:
            particula['y'] = random.randint(470, 490)
            particula['x'] = random.randint(320, 480)
            particula['size'] = random.randint(12, 18)
            particula['alpha'] = random.randint(40, 90)

def draw_led_indicators(surface, anim):
    """Dibuja indicadores LED de estado del sistema"""
    for i, led in enumerate(indicadores_led):
        # Estado parpadeante basado en la animación
        if led['estado'] == 'activo':
            brillo = 255  # Siempre encendido
        elif led['estado'] == 'calentando':
            brillo = int(128 + 127 * math.sin(anim / 15))  # Parpadeo lento
        else:  # presion
            brillo = int(128 + 127 * math.sin(anim / 8))   # Parpadeo rápido
        
        # Color del LED con brillo variable
        color_led = tuple(int(c * brillo / 255) for c in led['color'])
        
        # Dibujar LED
        pygame.draw.circle(surface, color_led, (led['x'], led['y']), 4)
        pygame.draw.circle(surface, NEGRO, (led['x'], led['y']), 4, 1)
        
        # Efecto de resplandor
        if brillo > 200:
            resplandor_surf = pygame.Surface((16, 16), pygame.SRCALPHA)
            pygame.draw.circle(resplandor_surf, (*led['color'], 50), (8, 8), 8)
            surface.blit(resplandor_surf, (led['x']-8, led['y']-8))

def draw_enhanced_water_effects(surface, anim):
    """Efectos adicionales del agua - turbulencia y reflexos"""
    # Área del agua visible
    agua_x, agua_y = 365, 375
    agua_w, agua_h = 70, 45
    
    # Reflexos en la superficie del agua
    for i in range(3):
        reflejo_x = agua_x + 15 + i * 20
        reflejo_y = agua_y + 5 * math.sin(anim/12 + i)
        reflejo_surf = pygame.Surface((8, 3), pygame.SRCALPHA)
        pygame.draw.ellipse(reflejo_surf, (255, 255, 255, 150), (0, 0, 8, 3))
        surface.blit(reflejo_surf, (reflejo_x, reflejo_y))
    
    # Turbulencia cerca de las paredes
    for i in range(agua_w//8):
        turb_x = agua_x + i * 8
        turb_y = agua_y + agua_h//2 + 3 * math.sin(anim/8 + i*0.5)
        pygame.draw.circle(surface, (150, 200, 255, 100), (turb_x, int(turb_y)), 2)

def draw_enhanced_labels(surface):
    """(Panel de especificaciones eliminado a petición del usuario)"""
    pass

def draw_boiler_details(surface):
    """Dibuja detalles profesionales de la caldera"""
    # Manómetro en la parte superior
    pygame.draw.circle(surface, GRIS_METAL, (380, 230), 15)
    pygame.draw.circle(surface, BLANCO, (380, 230), 12)
    pygame.draw.circle(surface, NEGRO, (380, 230), 15, 2)
    # Aguja del manómetro
    pygame.draw.line(surface, ROJO, (380, 230), (385, 225), 2)
    
    # Válvula de entrada (izquierda)
    pygame.draw.rect(surface, GRIS_METAL, (320, 320, 30, 15), border_radius=5)
    pygame.draw.rect(surface, NEGRO, (320, 320, 30, 15), 2, border_radius=5)
    
    # Tubería de entrada
    pygame.draw.rect(surface, GRIS_METAL, (280, 325, 40, 8), border_radius=4)
    pygame.draw.rect(surface, NEGRO, (280, 325, 40, 8), 2, border_radius=4)
    
    # Válvula de salida (derecha)
    pygame.draw.rect(surface, GRIS_METAL, (450, 280, 30, 15), border_radius=5)
    pygame.draw.rect(surface, NEGRO, (450, 280, 30, 15), 2, border_radius=5)
    
    # Tubería de salida de vapor
    pygame.draw.rect(surface, GRIS_METAL, (480, 285, 60, 8), border_radius=4)
    pygame.draw.rect(surface, NEGRO, (480, 285, 60, 8), 2, border_radius=4)
    
    # Rejillas de ventilación
    for i in range(3):
        y_pos = 350 + i * 20
        pygame.draw.rect(surface, GRIS_OSCURO, (470, y_pos, 20, 3))

def draw_labels_professional(surface):
    """Dibuja etiquetas profesionales sin superposición"""
    # Título principal
    titulo = font.render("Caldera", True, NEGRO)
    surface.blit(titulo, (W//2 - titulo.get_width()//2, 30))
    
    # Etiquetas con líneas callout
    
    # Manómetro
    label_manometro = font_tiny.render("Manómetro", True, NEGRO)
    surface.blit(label_manometro, (320, 200))
    pygame.draw.line(surface, GRIS_OSCURO, (360, 210), (380, 230), 1)
    
    # Entrada de agua
    label_entrada = font_tiny.render("Entrada de agua", True, NEGRO)
    surface.blit(label_entrada, (200, 340))
    pygame.draw.line(surface, GRIS_OSCURO, (270, 345), (320, 328), 1)
    
    # Salida de vapor
    label_salida = font_tiny.render("Salida de vapor", True, NEGRO)
    surface.blit(label_salida, (550, 270))
    pygame.draw.line(surface, GRIS_OSCURO, (540, 280), (480, 290), 1)
    
    # Nivel de agua
    label_nivel = font_tiny.render("Nivel de agua", True, NEGRO)
    surface.blit(label_nivel, (480, 350))
    pygame.draw.line(surface, GRIS_OSCURO, (470, 360), (435, 360), 1)
    
    # Zona de combustión
    label_fuego = font_tiny.render("Zona de combustión", True, NEGRO)
    surface.blit(label_fuego, (500, 480))
    pygame.draw.line(surface, GRIS_OSCURO, (490, 485), (450, 490), 1)

def draw_background(surface):
    """Dibuja fondo profesional"""
    surface.fill((245, 248, 252))  # Fondo azul muy claro
    # Línea de suelo
    pygame.draw.line(surface, GRIS_OSCURO, (0, H-80), (W, H-80), 4)
    
    # Gradiente sutil en el fondo
    for i in range(0, H-80, 2):
        alpha = int(15 * (i / (H-80)))
        color = (200, 210, 230, alpha)
        line_surf = pygame.Surface((W, 2), pygame.SRCALPHA)
        line_surf.fill(color)
        surface.blit(line_surf, (0, i))

def draw_pressure_gauge(surface, anim):
    """Dibuja un manómetro animado con aguja dinámica"""
    center_x, center_y = 420, 230
    radius = 18
    
    # Cuerpo del manómetro
    pygame.draw.circle(surface, GRIS_METAL, (center_x, center_y), radius)
    pygame.draw.circle(surface, BLANCO, (center_x, center_y), radius-3)
    pygame.draw.circle(surface, NEGRO, (center_x, center_y), radius, 2)
    
    # Marcas de escala
    for i in range(8):
        angle = math.pi * 0.75 + i * (math.pi * 1.5 / 7)
        start_x = center_x + (radius-6) * math.cos(angle)
        start_y = center_y + (radius-6) * math.sin(angle)
        end_x = center_x + (radius-3) * math.cos(angle)
        end_y = center_y + (radius-3) * math.sin(angle)
        pygame.draw.line(surface, NEGRO, (start_x, start_y), (end_x, end_y), 1)
    
    # Aguja animada (oscila entre 2-7 bar)
    pressure_value = 4.5 + 2.5 * math.sin(anim / 30)
    angle = math.pi * 0.75 + (pressure_value / 10) * (math.pi * 1.5)
    needle_x = center_x + (radius-8) * math.cos(angle)
    needle_y = center_y + (radius-8) * math.sin(angle)
    pygame.draw.line(surface, ROJO, (center_x, center_y), (needle_x, needle_y), 2)
    
    # Centro de la aguja
    pygame.draw.circle(surface, NEGRO, (center_x, center_y), 3)

def draw_temperature_display(surface, anim):
    """Dibuja display digital de temperatura"""
    temp_value = int(85 + 15 * math.sin(anim / 25))  # 85-100°C
    
    # Pantalla digital
    display_rect = pygame.Rect(460, 220, 60, 25)
    pygame.draw.rect(surface, NEGRO, display_rect, border_radius=3)
    pygame.draw.rect(surface, (0, 50, 0), (display_rect.x+2, display_rect.y+2, display_rect.w-4, display_rect.h-4))
    
    # Texto de temperatura
    temp_text = font_tiny.render(f"{temp_value}°C", True, (0, 255, 0))
    text_rect = temp_text.get_rect(center=display_rect.center)
    surface.blit(temp_text, text_rect)

def draw_pipes_system(surface):
    """Dibuja sistema completo de tuberías"""
    # Tubería principal de entrada (izquierda)
    pygame.draw.rect(surface, GRIS_METAL, (250, 322, 100, 12), border_radius=6)
    pygame.draw.rect(surface, NEGRO, (250, 322, 100, 12), 2, border_radius=6)
    
    # Válvula de entrada
    pygame.draw.circle(surface, GRIS_METAL, (335, 328), 8)
    pygame.draw.circle(surface, NEGRO, (335, 328), 8, 2)
    
    # Tubería de vapor (derecha)
    pygame.draw.rect(surface, GRIS_METAL, (450, 282, 120, 12), border_radius=6)
    pygame.draw.rect(surface, NEGRO, (450, 282, 120, 12), 2, border_radius=6)
    
    # Válvula de salida de vapor
    pygame.draw.circle(surface, GRIS_METAL, (465, 288), 8)
    pygame.draw.circle(surface, NEGRO, (465, 288), 8, 2)
    
    # Tubería vertical de retorno
    pygame.draw.rect(surface, GRIS_METAL, (570, 288, 12, 100), border_radius=6)
    pygame.draw.rect(surface, NEGRO, (570, 288, 12, 100), 2, border_radius=6)

def draw_safety_valve(surface, anim):
    """Dibuja válvula de seguridad con vapor ocasional"""
    valve_x, valve_y = 400, 210
    
    # Cuerpo de la válvula
    pygame.draw.rect(surface, GRIS_METAL, (valve_x-5, valve_y, 10, 15), border_radius=3)
    pygame.draw.rect(surface, NEGRO, (valve_x-5, valve_y, 10, 15), 1, border_radius=3)
    
    # Vapor ocasional de la válvula de seguridad
    if int(anim / 60) % 8 == 0:  # Cada 8 segundos aproximadamente
        for i in range(3):
            vapor_y = valve_y - 10 - i * 8
            vapor_size = 6 - i
            vapor_surf = pygame.Surface((vapor_size*2, vapor_size*2), pygame.SRCALPHA)
            pygame.draw.circle(vapor_surf, (255, 255, 255, 100-i*30), (vapor_size, vapor_size), vapor_size)
            surface.blit(vapor_surf, (valve_x-vapor_size, vapor_y-vapor_size))

def draw_fire_animated(surface, anim):
    """Dibuja fuego animado realista en la base"""
    for llama in llamas:
        # Oscilación de la llama
        oscilacion = 8 * math.sin(anim / 6 + llama['fase'])
        altura_actual = llama['altura'] + oscilacion
        # Color de la llama basado en intensidad
        if llama['intensidad'] > 0.9:
            color = AMARILLO
        elif llama['intensidad'] > 0.8:
            color = NARANJA
        else:
            color = ROJO_FUEGO
        # Puntos de la llama (forma orgánica)
        puntos_llama = [
            (llama['x'], llama['y']),
            (llama['x'] - llama['ancho']/2, llama['y'] - altura_actual/3),
            (llama['x'] - llama['ancho']/4 + oscilacion/2, llama['y'] - altura_actual*2/3),
            (llama['x'] + oscilacion, llama['y'] - altura_actual),
            (llama['x'] + llama['ancho']/4 + oscilacion/2, llama['y'] - altura_actual*2/3),
            (llama['x'] + llama['ancho']/2, llama['y'] - altura_actual/3),
        ]
        # Dibujar llama with transparencia
        llama_surf = pygame.Surface((llama['ancho']+20, int(altura_actual)+10), pygame.SRCALPHA)
        puntos_rel = [(p[0] - llama['x'] + 10, p[1] - llama['y'] + int(altura_actual) + 5) for p in puntos_llama]
        pygame.draw.polygon(llama_surf, (*color, 200), puntos_rel)
        surface.blit(llama_surf, (llama['x'] - 10, llama['y'] - int(altura_actual) - 5))
        # Actualizar propiedades de la llama
        llama['fase'] += 0.1
        llama['intensidad'] = 0.7 + 0.3 * math.sin(anim / 12 + llama['fase'])

# Bucle principal mejorado
while True:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            volver_rect = pygame.Rect(W//2-60, H-70, 120, 40)
            if volver_rect.collidepoint(mouse_pos):
                pygame.quit(); sys.exit()
    
    # Dibujar todos los elementos en orden
    draw_background(screen)
    
    # Base y soporte
    draw_boiler_base(screen)
    
    # Sistema de tuberías
    draw_pipes_system(screen)
    
    # Fuego animado en la base
    draw_fire_animated(screen, f_anim)
    # Humo adicional
    draw_smoke_particles(screen, f_anim)
    # Cuerpo principal de la caldera
    draw_boiler_body(screen)
    
    # Nivel de agua visible
    draw_water_level(screen, f_anim)
    
    # Efectos de agua mejorados
    draw_enhanced_water_effects(screen, f_anim)
    
    # Burbujas internas
    draw_bubbles_internal(screen, f_anim)
    
    # Detalles y accesorios
    draw_boiler_details(screen)
    
    # Instrumentación
    draw_pressure_gauge(screen, f_anim)
    draw_temperature_display(screen, f_anim)
    draw_safety_valve(screen, f_anim)
    
    # Vapor saliendo
    draw_steam(screen, f_anim)
    
    # Indicadores LED
    draw_led_indicators(screen, f_anim)
    
    # Etiquetas profesionales
    draw_labels_professional(screen)
    draw_enhanced_labels(screen)
    
    # Botón Volver centrado abajo (estandarizado)
    volver_rect = pygame.Rect(W//2-60, H-70, 120, 40)
    pygame.draw.rect(screen, AZUL_OSCURO, volver_rect, border_radius=8)
    pygame.draw.rect(screen, NEGRO, volver_rect, 2, border_radius=8)
    text = font_small.render("Volver", True, BLANCO)
    text_rect = text.get_rect(center=volver_rect.center)
    screen.blit(text, text_rect)
    
    # Incrementar animación
    f_anim += 1
    
    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
