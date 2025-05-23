"""
Backend para la simulación del calentamiento de agua mediante un intercambiador de calor solar térmico.
Módulo funcional y modular para ser invocado desde la interfaz Kivy.
Incluye manejo de errores y validación de datos para robustez y seguridad.
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
    Incluye validación de rangos físicos y manejo de errores.
    """
    try:
        temp_ini = random.uniform(18, 25)  # °C
        masa = random.uniform(8, 15)       # kg
        potencia = random.uniform(500, 900) # W
        tiempo = random.randint(20, 60)    # minutos
        if not (0 < temp_ini < 100 and 0 < masa <= 100 and 0 < potencia <= 2000 and 0 < tiempo <= 180):
            return {"status": "error", "data": {}, "message": "Parámetros fuera de rango físico."}
        _estado_calentamiento["temperatura_inicial"] = temp_ini
        _estado_calentamiento["masa_agua"] = masa
        _estado_calentamiento["potencia_solar"] = potencia
        _estado_calentamiento["tiempo_exposicion"] = tiempo
        # Simulación de temperatura final (aumenta según potencia y tiempo)
        try:
            delta_T = (potencia * tiempo * 60) / (masa * 4186)
        except ZeroDivisionError:
            delta_T = 0.0
        _estado_calentamiento["temperatura_final"] = temp_ini + delta_T
        return {"status": "ok", "data": {}, "message": "Calentamiento iniciado correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en iniciar_calentamiento: {str(e)}"}

def obtener_datos() -> Dict[str, object]:
    """
    Retorna un diccionario con los indicadores principales del proceso de calentamiento.
    Incluye manejo de errores y validación de datos.
    """
    try:
        temp_ini = round(_estado_calentamiento["temperatura_inicial"], 1)
        temp_fin = round(_estado_calentamiento["temperatura_final"], 1)
        tiempo = _estado_calentamiento["tiempo_exposicion"]
        variacion = (temp_fin - temp_ini) / tiempo if tiempo > 0 else 0
        eficiencia = calcular_eficiencia_termica()["data"]
        datos = {
            "temperatura_inicial": temp_ini,
            "temperatura_final": temp_fin,
            "tiempo_exposicion": tiempo,
            "variacion_termica": round(variacion, 2),
            "eficiencia_termica": round(eficiencia, 1)
        }
        if any(v < 0 for v in datos.values() if isinstance(v, (int, float))):
            return {"status": "error", "data": datos, "message": "Valores negativos detectados en los datos."}
        return {"status": "ok", "data": datos, "message": "Datos obtenidos correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en obtener_datos: {str(e)}"}

def calcular_eficiencia_termica() -> Dict[str, object]:
    """
    Calcula la eficiencia térmica del sistema solar térmico.
    Si falta algún dato, utiliza valores simulados razonables.
    Fórmula: eta = (m * c * delta_T) / (P_solar * t)
    Retorna estructura controlada con manejo de errores.
    """
    try:
        m = _estado_calentamiento.get("masa_agua", 10)  # kg
        c = 4186  # J/kg·°C (agua)
        delta_T = _estado_calentamiento.get("temperatura_final", 40) - _estado_calentamiento.get("temperatura_inicial", 20)
        P = _estado_calentamiento.get("potencia_solar", 700)  # W
        t = _estado_calentamiento.get("tiempo_exposicion", 30) * 60  # s
        if P <= 0 or t <= 0 or m <= 0:
            P = 700
            t = 1800
            m = 10
        numerador = m * c * delta_T
        denominador = P * t
        try:
            eficiencia = (numerador / denominador) * 100 if denominador > 0 else 0
        except ZeroDivisionError:
            eficiencia = 0.0
        eficiencia = max(0, min(eficiencia, 100))
        return {"status": "ok", "data": eficiencia, "message": "Eficiencia calculada correctamente."}
    except Exception as e:
        return {"status": "error", "data": 0.0, "message": f"Error en calcular_eficiencia_termica: {str(e)}"}

def generar_datos_grafico(puntos: int = 12) -> Dict[str, object]:
    """
    Genera listas simuladas de temperatura del agua a lo largo del tiempo para graficar la curva de calentamiento.
    Incluye manejo de errores y validación de datos.
    """
    try:
        temp_ini = _estado_calentamiento.get("temperatura_inicial", 20)
        temp_fin = _estado_calentamiento.get("temperatura_final", 45)
        tiempo_total = _estado_calentamiento.get("tiempo_exposicion", 30)
        if puntos <= 0 or tiempo_total <= 0:
            return {"status": "error", "data": {}, "message": "Parámetros de simulación inválidos."}
        temperaturas = []
        tiempos = []
        for i in range(puntos+1):
            t = i * (tiempo_total / puntos)
            temp = temp_ini + (temp_fin - temp_ini) * (t / tiempo_total) if tiempo_total > 0 else temp_ini
            temperaturas.append(round(temp, 2))
            tiempos.append(round(t, 1))
        _datos_grafico["temperaturas"] = temperaturas
        _datos_grafico["tiempos"] = tiempos
        return {"status": "ok", "data": {"temperaturas": temperaturas, "tiempos": tiempos}, "message": "Datos de gráfico generados correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en generar_datos_grafico: {str(e)}"}
