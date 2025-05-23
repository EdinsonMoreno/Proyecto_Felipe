"""
Backend para la simulación del calentamiento de agua mediante un intercambiador de calor solar térmico.
Módulo funcional y modular para ser invocado desde la interfaz Kivy.
"""

import random
from typing import Dict, List

# Variables internas de simulación
_estado_calentamiento = {
    "temperatura_inicial": 0.0,  # °C
    "temperatura_final": 0.0,    # °C
    "tiempo_exposicion": 0,      # minutos
    "masa_agua": 0.0,            # kg
    "potencia_solar": 0.0        # W
}

# Datos históricos simulados para graficar
_datos_grafico = {
    "temperaturas": [],
    "tiempos": []
}

def iniciar_calentamiento():
    """
    Inicializa variables de simulación para el proceso de calentamiento de agua.
    Simula temperatura inicial, masa de agua, potencia solar y tiempo de exposición.
    """
    _estado_calentamiento["temperatura_inicial"] = random.uniform(18, 25)  # °C
    _estado_calentamiento["masa_agua"] = random.uniform(8, 15)             # kg (volumen típico de tanque pequeño)
    _estado_calentamiento["potencia_solar"] = random.uniform(500, 900)     # W (potencia solar incidente)
    _estado_calentamiento["tiempo_exposicion"] = random.randint(20, 60)    # minutos
    # Simulación de temperatura final (aumenta según potencia y tiempo)
    delta_T = (_estado_calentamiento["potencia_solar"] * _estado_calentamiento["tiempo_exposicion"] * 60) / (_estado_calentamiento["masa_agua"] * 4186)
    _estado_calentamiento["temperatura_final"] = _estado_calentamiento["temperatura_inicial"] + delta_T

def obtener_datos() -> Dict[str, float]:
    """
    Retorna un diccionario con los indicadores principales del proceso de calentamiento.
    """
    temp_ini = round(_estado_calentamiento["temperatura_inicial"], 1)
    temp_fin = round(_estado_calentamiento["temperatura_final"], 1)
    tiempo = _estado_calentamiento["tiempo_exposicion"]
    variacion = (temp_fin - temp_ini) / tiempo if tiempo > 0 else 0
    eficiencia = calcular_eficiencia_termica()
    return {
        "temperatura_inicial": temp_ini,
        "temperatura_final": temp_fin,
        "tiempo_exposicion": tiempo,
        "variacion_termica": round(variacion, 2),
        "eficiencia_termica": round(eficiencia, 1)
    }

def calcular_eficiencia_termica() -> float:
    """
    Calcula la eficiencia térmica del sistema solar térmico.
    Si falta algún dato, utiliza valores simulados razonables.
    Fórmula: eta = (m * c * delta_T) / (P_solar * t)
    """
    m = _estado_calentamiento.get("masa_agua", 10)  # kg
    c = 4186  # J/kg·°C (agua)
    delta_T = _estado_calentamiento.get("temperatura_final", 40) - _estado_calentamiento.get("temperatura_inicial", 20)
    P = _estado_calentamiento.get("potencia_solar", 700)  # W
    t = _estado_calentamiento.get("tiempo_exposicion", 30) * 60  # s
    if P <= 0 or t <= 0 or m <= 0:
        # Si falta algún dato, se asumen valores típicos
        P = 700
        t = 1800
        m = 10
    numerador = m * c * delta_T
    denominador = P * t
    eficiencia = (numerador / denominador) * 100 if denominador > 0 else 0
    return max(0, min(eficiencia, 100))

def generar_datos_grafico(puntos: int = 12) -> Dict[str, List[float]]:
    """
    Genera listas simuladas de temperatura del agua a lo largo del tiempo para graficar la curva de calentamiento.
    :param puntos: Número de intervalos simulados (por defecto 12)
    :return: Diccionario con listas de temperaturas y tiempos
    """
    temp_ini = _estado_calentamiento.get("temperatura_inicial", 20)
    temp_fin = _estado_calentamiento.get("temperatura_final", 45)
    tiempo_total = _estado_calentamiento.get("tiempo_exposicion", 30)
    temperaturas = []
    tiempos = []
    for i in range(puntos+1):
        t = i * (tiempo_total / puntos)
        # Interpolación lineal para simular el aumento de temperatura
        temp = temp_ini + (temp_fin - temp_ini) * (t / tiempo_total) if tiempo_total > 0 else temp_ini
        temperaturas.append(round(temp, 2))
        tiempos.append(round(t, 1))
    _datos_grafico["temperaturas"] = temperaturas
    _datos_grafico["tiempos"] = tiempos
    return {
        "temperaturas": temperaturas,
        "tiempos": tiempos
    }
