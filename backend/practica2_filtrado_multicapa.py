"""
Backend para la simulación del proceso de filtrado multicapa del agua.
Módulo funcional y modular para ser invocado desde la interfaz Kivy.
Incluye manejo de errores y validación de datos para robustez y seguridad.
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
    Incluye validación de rangos físicos y manejo de errores.
    """
    try:
        turbidez_ini = random.uniform(80, 200)  # NTU
        volumen = random.uniform(8, 15)         # L
        tiempo = random.randint(60, 150)        # s
        if not (0 < turbidez_ini <= 1000 and 0 < volumen <= 100 and 0 < tiempo <= 3600):
            return {"status": "error", "data": {}, "message": "Parámetros fuera de rango físico."}
        _estado_filtrado["turbidez_inicial"] = turbidez_ini
        _estado_filtrado["volumen"] = volumen
        _estado_filtrado["tiempo"] = tiempo
        # Simulación de reducción de turbidez a través de las capas
        turbidez = turbidez_ini
        for capa in [0.5, 0.3, 0.2]:
            turbidez = turbidez * (1 - capa)
        _estado_filtrado["turbidez_final"] = max(turbidez, 1.0)
        return {"status": "ok", "data": {}, "message": "Filtrado iniciado correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en iniciar_filtrado: {str(e)}"}

def obtener_datos() -> Dict[str, object]:
    """
    Retorna un diccionario con los indicadores principales del proceso de filtrado.
    Incluye manejo de errores y validación de datos.
    """
    try:
        eficiencia = calcular_eficiencia()["data"]
        datos = {
            "tiempo_filtrado": _estado_filtrado["tiempo"],
            "turbidez_inicial": round(_estado_filtrado["turbidez_inicial"], 1),
            "turbidez_final": round(_estado_filtrado["turbidez_final"], 1),
            "volumen_filtrado": round(_estado_filtrado["volumen"], 1),
            "eficiencia_remocion": round(eficiencia, 1)
        }
        if any(v < 0 for v in datos.values() if isinstance(v, (int, float))):
            return {"status": "error", "data": datos, "message": "Valores negativos detectados en los datos."}
        return {"status": "ok", "data": datos, "message": "Datos obtenidos correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en obtener_datos: {str(e)}"}

def calcular_eficiencia() -> Dict[str, object]:
    """
    Calcula la eficiencia de remoción de sólidos en el filtrado multicapa.
    Si falta algún dato, utiliza valores simulados razonables.
    Retorna estructura controlada con manejo de errores.
    """
    try:
        tin = _estado_filtrado.get("turbidez_inicial", 100)
        tf = _estado_filtrado.get("turbidez_final", 10)
        if tin == 0:
            return {"status": "error", "data": 0.0, "message": "Turbidez inicial igual a cero."}
        eficiencia = ((tin - tf) / tin) * 100 if tin > 0 else 0
        eficiencia = max(0, min(eficiencia, 100))
        return {"status": "ok", "data": eficiencia, "message": "Eficiencia calculada correctamente."}
    except Exception as e:
        return {"status": "error", "data": 0.0, "message": f"Error en calcular_eficiencia: {str(e)}"}

def generar_datos_grafico(puntos: int = 5) -> Dict[str, object]:
    """
    Genera listas simuladas de turbidez a lo largo de las etapas de filtrado para graficar.
    Incluye manejo de errores y validación de datos.
    """
    try:
        turbidez = _estado_filtrado.get("turbidez_inicial", 100)
        turbidez_list = [turbidez]
        tiempos = [0]
        capas = [0.5, 0.3, 0.2, 0.1, 0.05][:puntos-1]
        if puntos <= 0:
            return {"status": "error", "data": {}, "message": "Parámetros de simulación inválidos."}
        for i, capa in enumerate(capas):
            turbidez = turbidez * (1 - capa)
            turbidez_list.append(round(turbidez, 2))
            tiempos.append((i+1) * (_estado_filtrado.get("tiempo", 100) // puntos))
        _datos_grafico["turbidez"] = turbidez_list
        _datos_grafico["tiempos"] = tiempos
        return {"status": "ok", "data": {"turbidez": turbidez_list, "tiempos": tiempos}, "message": "Datos de gráfico generados correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en generar_datos_grafico: {str(e)}"}
