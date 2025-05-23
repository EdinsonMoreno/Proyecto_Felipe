"""
Backend para la simulación del proceso de filtrado multicapa del agua.
Módulo funcional y modular para ser invocado desde la interfaz Kivy.
"""

import random
from typing import Dict, List

# Variables internas de simulación
_estado_filtrado = {
    "turbidez_inicial": 0.0,  # NTU
    "turbidez_final": 0.0,    # NTU
    "volumen": 0.0,           # L
    "tiempo": 0               # segundos
}

# Datos históricos simulados para graficar
_datos_grafico = {
    "turbidez": [],
    "tiempos": []
}

def iniciar_filtrado():
    """
    Inicializa variables de simulación para el proceso de filtrado multicapa.
    Simula valores razonables de turbidez inicial, volumen y tiempo de proceso.
    """
    _estado_filtrado["turbidez_inicial"] = random.uniform(80, 200)  # NTU
    _estado_filtrado["volumen"] = random.uniform(8, 15)             # L
    # Simulación de tiempo de filtrado (segundos)
    _estado_filtrado["tiempo"] = random.randint(60, 150)
    # Simulación de reducción de turbidez a través de las capas
    turbidez = _estado_filtrado["turbidez_inicial"]
    for capa in [0.5, 0.3, 0.2]:  # Eficiencia relativa de cada capa
        turbidez = turbidez * (1 - capa)
    _estado_filtrado["turbidez_final"] = max(turbidez, 1.0)

def obtener_datos() -> Dict[str, float]:
    """
    Retorna un diccionario con los indicadores principales del proceso de filtrado.
    """
    eficiencia = calcular_eficiencia()
    return {
        "tiempo_filtrado": _estado_filtrado["tiempo"],
        "turbidez_inicial": round(_estado_filtrado["turbidez_inicial"], 1),
        "turbidez_final": round(_estado_filtrado["turbidez_final"], 1),
        "volumen_filtrado": round(_estado_filtrado["volumen"], 1),
        "eficiencia_remocion": round(eficiencia, 1)
    }

def calcular_eficiencia() -> float:
    """
    Calcula la eficiencia de remoción de sólidos en el filtrado multicapa.
    Si falta algún dato, utiliza valores simulados razonables.
    """
    tin = _estado_filtrado.get("turbidez_inicial", 100)
    tf = _estado_filtrado.get("turbidez_final", 10)
    if tin == 0:
        # Si no hay dato, se asume un valor típico
        tin = 100.0
    eficiencia = ((tin - tf) / tin) * 100 if tin > 0 else 0
    return eficiencia

def generar_datos_grafico(puntos: int = 5) -> Dict[str, List[float]]:
    """
    Genera listas simuladas de turbidez a lo largo de las etapas de filtrado para graficar.
    :param puntos: Número de etapas/capas (por defecto 5)
    :return: Diccionario con listas de turbidez y tiempos
    """
    turbidez = _estado_filtrado.get("turbidez_inicial", 100)
    turbidez_list = [turbidez]
    tiempos = [0]
    capas = [0.5, 0.3, 0.2, 0.1, 0.05][:puntos-1]  # Eficiencia relativa por capa
    for i, capa in enumerate(capas):
        turbidez = turbidez * (1 - capa)
        turbidez_list.append(round(turbidez, 2))
        tiempos.append((i+1) * (_estado_filtrado.get("tiempo", 100) // puntos))
    _datos_grafico["turbidez"] = turbidez_list
    _datos_grafico["tiempos"] = tiempos
    return {
        "turbidez": turbidez_list,
        "tiempos": tiempos
    }
