"""
Backend para el análisis de balance energético del sistema fotovoltaico.
Módulo completamente funcional y modular para ser invocado desde la interfaz Kivy.
"""

import random
from typing import Dict, List

# Si en el futuro se implementan funciones en utils, importar aquí:
# from utils.sensores import simular_radiacion, simular_tension, simular_corriente
# from utils.helpers import alguna_funcion_util

# Variables internas de simulación (pueden ser sobrescritas por la interfaz si se desea)
_estado_simulacion = {
    "radiacion": 0.0,  # W/m²
    "tension": 0.0,    # V
    "corriente": 0.0,  # A
    "tiempo": 1.0      # h (puede ser modificado para simulaciones más largas)
}

# Datos históricos simulados para graficar
_datos_grafico = {
    "energia_generada": [],
    "energia_consumida": []
}

def iniciar_medicion():
    """
    Inicializa variables de simulación para la medición del sistema fotovoltaico.
    Simula valores razonables de radiación solar, tensión y corriente.
    """
    _estado_simulacion["radiacion"] = random.uniform(600, 1000)  # W/m²
    _estado_simulacion["tension"] = random.uniform(12, 15)       # V
    _estado_simulacion["corriente"] = random.uniform(5, 10)      # A
    _estado_simulacion["tiempo"] = 1.0                           # h

def obtener_datos() -> Dict[str, float]:
    """
    Retorna un diccionario con los indicadores principales del balance energético.
    """
    resultados = calcular_resultados()
    return {
        "radiacion": round(_estado_simulacion["radiacion"], 1),
        "energia_generada": round(resultados["energia_generada"], 2),
        "energia_consumida": round(resultados["energia_consumida"], 2),
        "eficiencia": round(resultados["eficiencia"], 1)
    }

def calcular_resultados() -> Dict[str, float]:
    """
    Calcula la energía generada, consumida y la eficiencia del sistema.
    Si falta algún dato, utiliza valores simulados razonables.
    """
    V = _estado_simulacion.get("tension", 12)
    I = _estado_simulacion.get("corriente", 7)
    t = _estado_simulacion.get("tiempo", 1.0)
    # Energía generada (Wh)
    energia_generada = V * I * t
    # Simulación de cargas conectadas (puede ser ajustado por la interfaz)
    energia_consumida = energia_generada * random.uniform(0.6, 0.85)
    # Eficiencia (%)
    eficiencia = (energia_consumida / energia_generada) * 100 if energia_generada > 0 else 0
    return {
        "energia_generada": energia_generada,
        "energia_consumida": energia_consumida,
        "eficiencia": eficiencia
    }

def generar_datos_grafico(puntos: int = 24) -> Dict[str, List[float]]:
    """
    Genera listas simuladas de energía generada y consumida a lo largo del tiempo para graficar.
    :param puntos: Número de puntos simulados (por defecto 24, uno por hora)
    :return: Diccionario con listas de energía generada y consumida
    """
    energia_gen = []
    energia_con = []
    for _ in range(puntos):
        V = random.uniform(12, 15)
        I = random.uniform(5, 10)
        t = 1.0
        eg = V * I * t
        ec = eg * random.uniform(0.6, 0.85)
        energia_gen.append(round(eg, 2))
        energia_con.append(round(ec, 2))
    _datos_grafico["energia_generada"] = energia_gen
    _datos_grafico["energia_consumida"] = energia_con
    return {
        "energia_generada": energia_gen,
        "energia_consumida": energia_con
    }
