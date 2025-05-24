"""
Backend para la simulación del calentamiento de agua mediante un intercambiador de calor solar térmico.
Módulo funcional y modular para ser invocado desde la interfaz Kivy.
Incluye manejo de errores y validación de datos para robustez y seguridad.
Ahora es determinista: los resultados dependen solo de las entradas explícitas.
"""

from typing import Dict, List

# Variables internas de simulación
_estado_calentamiento = {
    "temperatura_inicial": 22.0,  # °C
    "masa_agua": 10.0,           # kg
    "potencia_solar": 700.0,     # W
    "tiempo_exposicion": 35,     # minutos
    "temperatura_final": 0.0     # °C
}

# Datos históricos simulados para graficar
_datos_grafico = {
    "temperaturas": [],
    "tiempos": []
}

def iniciar_calentamiento(temperatura_inicial: float = 22.0, masa_agua: float = 10.0, potencia_solar: float = 700.0, tiempo_exposicion: int = 35):
    """
    Inicializa variables de simulación para el proceso de calentamiento de agua.
    Ahora determinista: solo usa los valores de entrada o los valores por defecto.
    """
    try:
        _estado_calentamiento["temperatura_inicial"] = temperatura_inicial
        _estado_calentamiento["masa_agua"] = masa_agua
        _estado_calentamiento["potencia_solar"] = potencia_solar
        _estado_calentamiento["tiempo_exposicion"] = tiempo_exposicion
        # Cálculo determinista de temperatura final
        delta_T = (potencia_solar * tiempo_exposicion * 60) / (masa_agua * 4186)
        _estado_calentamiento["temperatura_final"] = temperatura_inicial + delta_T
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
    Determinista: no usa aleatoriedad, solo entradas explícitas o constantes.
    """
    try:
        m = _estado_calentamiento.get("masa_agua", 10.0)
        c = 4186  # J/kg·°C (agua)
        delta_T = _estado_calentamiento.get("temperatura_final", 47.5) - _estado_calentamiento.get("temperatura_inicial", 22.0)
        P = _estado_calentamiento.get("potencia_solar", 700.0)
        t = _estado_calentamiento.get("tiempo_exposicion", 35) * 60  # s
        numerador = m * c * delta_T
        denominador = P * t
        eficiencia = (numerador / denominador) * 100 if denominador > 0 else 0
        eficiencia = max(0, min(eficiencia, 100))
        return {"status": "ok", "data": eficiencia, "message": "Eficiencia calculada correctamente."}
    except Exception as e:
        return {"status": "error", "data": 0.0, "message": f"Error en calcular_eficiencia_termica: {str(e)}"}

def generar_datos_grafico(puntos: int = 12) -> Dict[str, object]:
    """
    Genera listas deterministas de temperatura del agua a lo largo del tiempo para graficar la curva de calentamiento.
    """
    try:
        temp_ini = _estado_calentamiento.get("temperatura_inicial", 22.0)
        temp_fin = _estado_calentamiento.get("temperatura_final", 47.5)
        tiempo_total = _estado_calentamiento.get("tiempo_exposicion", 35)
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
