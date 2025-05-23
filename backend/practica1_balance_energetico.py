"""
Backend para el análisis de balance energético del sistema fotovoltaico.
Módulo completamente funcional y modular para ser invocado desde la interfaz Kivy.
Incluye manejo de errores y validación de datos para robustez y seguridad.
"""

import random
from typing import Dict, List

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
    Incluye validación de rangos físicos y manejo de errores.
    """
    try:
        radiacion = random.uniform(600, 1000)  # W/m²
        tension = random.uniform(12, 15)       # V
        corriente = random.uniform(5, 10)      # A
        tiempo = 1.0                           # h
        if not (0 < radiacion <= 1500 and 0 < tension <= 100 and 0 < corriente <= 100 and 0 < tiempo <= 24):
            return {"status": "error", "data": {}, "message": "Parámetros fuera de rango físico."}
        _estado_simulacion["radiacion"] = radiacion
        _estado_simulacion["tension"] = tension
        _estado_simulacion["corriente"] = corriente
        _estado_simulacion["tiempo"] = tiempo
        return {"status": "ok", "data": {}, "message": "Medición iniciada correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en iniciar_medicion: {str(e)}"}

def obtener_datos() -> Dict[str, object]:
    """
    Retorna un diccionario con los indicadores principales del balance energético.
    Incluye manejo de errores y validación de datos.
    """
    try:
        resultados = calcular_resultados()["data"]
        datos = {
            "radiacion": round(_estado_simulacion["radiacion"], 1),
            "energia_generada": round(resultados["energia_generada"], 2),
            "energia_consumida": round(resultados["energia_consumida"], 2),
            "eficiencia": round(resultados["eficiencia"], 1)
        }
        if any(v < 0 for v in datos.values() if isinstance(v, (int, float))):
            return {"status": "error", "data": datos, "message": "Valores negativos detectados en los datos."}
        return {"status": "ok", "data": datos, "message": "Datos obtenidos correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en obtener_datos: {str(e)}"}

def calcular_resultados() -> Dict[str, object]:
    """
    Calcula la energía generada, consumida y la eficiencia del sistema.
    Si falta algún dato, utiliza valores simulados razonables.
    Incluye manejo de errores y validación de datos.
    """
    try:
        V = _estado_simulacion.get("tension", 12)
        I = _estado_simulacion.get("corriente", 7)
        t = _estado_simulacion.get("tiempo", 1.0)
        try:
            energia_generada = V * I * t
        except Exception:
            energia_generada = 0.0
        energia_consumida = energia_generada * random.uniform(0.6, 0.85)
        try:
            eficiencia = (energia_consumida / energia_generada) * 100 if energia_generada > 0 else 0
        except ZeroDivisionError:
            eficiencia = 0.0
        resultados = {
            "energia_generada": energia_generada,
            "energia_consumida": energia_consumida,
            "eficiencia": eficiencia
        }
        if any(v < 0 for v in resultados.values() if isinstance(v, (int, float))):
            return {"status": "error", "data": resultados, "message": "Valores negativos detectados en los resultados."}
        return {"status": "ok", "data": resultados, "message": "Resultados calculados correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en calcular_resultados: {str(e)}"}

def generar_datos_grafico(puntos: int = 24) -> Dict[str, object]:
    """
    Genera listas simuladas de energía generada y consumida a lo largo del tiempo para graficar.
    Incluye manejo de errores y validación de datos.
    """
    try:
        if puntos <= 0:
            return {"status": "error", "data": {}, "message": "Parámetros de simulación inválidos."}
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
        return {"status": "ok", "data": {"energia_generada": energia_gen, "energia_consumida": energia_con}, "message": "Datos de gráfico generados correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en generar_datos_grafico: {str(e)}"}
