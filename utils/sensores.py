"""
Simulación de sensores para prácticas educativas.
"""
import random

def simular_radiacion() -> float:
    """
    Simula la medición de radiación solar en W/m².
    """
    return random.uniform(600, 1000)

def simular_tension() -> float:
    """
    Simula la medición de tensión del sistema en voltios.
    """
    return random.uniform(12, 15)

def simular_corriente() -> float:
    """
    Simula la medición de corriente del sistema en amperios.
    """
    return random.uniform(5, 10)
