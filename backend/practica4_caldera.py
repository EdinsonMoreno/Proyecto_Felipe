"""
Backend para la simulación del funcionamiento de una caldera alimentada por energía solar o resistencia eléctrica.
Módulo funcional y modular para ser invocado desde la interfaz Kivy.
Incluye manejo de errores y validación de datos para robustez y seguridad.
"""

import random
from typing import Dict, List

# Variables internas de simulación
_estado_caldera = {
    "temperatura_inicial": 0.0,   # °C
    "temperatura_maxima": 100.0, # °C (ebullición)
    "volumen_agua": 0.0,         # L
    "masa_agua": 0.0,            # kg
    "energia_entrada": 0.0,      # W
    "modo": "resistencia",      # "resistencia" o "solar"
    "tiempo_hasta_ebullicion": 0,# min
    "energia_consumida": 0.0,    # Wh
    "vapor_generado": 0.0        # ml
}

# Datos históricos simulados para graficar
_datos_grafico = {
    "temperaturas": [],
    "tiempos": []
}

def iniciar_caldera(modo: str = "resistencia"):
    """
    Inicializa variables de simulación para el proceso de calentamiento en la caldera.
    :param modo: 'resistencia' o 'solar'
    Incluye validación de rangos físicos y manejo de errores.
    """
    try:
        temp_ini = random.uniform(18, 30)  # °C
        volumen = random.uniform(2, 5)     # L
        if not (0 < temp_ini < 100 and 0 < volumen <= 10):
            return {"status": "error", "data": {}, "message": "Parámetros fuera de rango físico."}
        _estado_caldera["temperatura_inicial"] = temp_ini
        _estado_caldera["volumen_agua"] = volumen
        _estado_caldera["masa_agua"] = volumen  # 1L ~ 1kg
        if modo not in ("resistencia", "solar"):
            modo = "resistencia"
        _estado_caldera["modo"] = modo
        _estado_caldera["energia_entrada"] = 1500 if modo == "resistencia" else 800  # W
        calcular_resultados()
        return {"status": "ok", "data": {}, "message": "Caldera iniciada correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en iniciar_caldera: {str(e)}"}

def obtener_datos() -> Dict[str, object]:
    """
    Retorna un diccionario con los indicadores principales del proceso de calentamiento y ebullición.
    Incluye manejo de errores y validación de datos.
    """
    try:
        datos = {
            "temperatura_maxima": _estado_caldera["temperatura_maxima"],
            "tiempo_hasta_ebullicion": _estado_caldera["tiempo_hasta_ebullicion"],
            "energia_consumida": round(_estado_caldera["energia_consumida"], 1),
            "vapor_generado": round(_estado_caldera["vapor_generado"], 1)
        }
        if any(v < 0 for v in datos.values() if isinstance(v, (int, float))):
            return {"status": "error", "data": datos, "message": "Valores negativos detectados en los datos."}
        return {"status": "ok", "data": datos, "message": "Datos obtenidos correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en obtener_datos: {str(e)}"}

def calcular_resultados():
    """
    Calcula el tiempo estimado hasta ebullición, energía consumida y vapor generado.
    Incluye manejo de errores y validación de datos.
    """
    try:
        m = _estado_caldera.get("masa_agua", 3)  # kg
        c = 4186  # J/kg·°C
        T_ini = _estado_caldera.get("temperatura_inicial", 20)
        T_max = _estado_caldera.get("temperatura_maxima", 100)
        P = _estado_caldera.get("energia_entrada", 1000)  # W
        delta_T = T_max - T_ini
        if m <= 0 or P <= 0 or delta_T <= 0:
            m = 3
            P = 1000
            delta_T = 80
        energia_J = m * c * delta_T
        try:
            tiempo_s = energia_J / P if P > 0 else 1
        except ZeroDivisionError:
            tiempo_s = 1
        tiempo_min = tiempo_s / 60
        energia_Wh = energia_J / 3600
        L_v = 2260000  # J/kg
        energia_restante = max(0, P * 300 - energia_J)  # 5 min extra de calentamiento
        vapor_kg = energia_restante / L_v if energia_restante > 0 else 0
        vapor_ml = vapor_kg * 1000
        _estado_caldera["tiempo_hasta_ebullicion"] = int(round(tiempo_min))
        _estado_caldera["energia_consumida"] = energia_Wh
        _estado_caldera["vapor_generado"] = vapor_ml
    except Exception as e:
        # Si ocurre un error, se dejan los valores en cero y se puede notificar a la interfaz
        _estado_caldera["tiempo_hasta_ebullicion"] = 0
        _estado_caldera["energia_consumida"] = 0.0
        _estado_caldera["vapor_generado"] = 0.0
        # TODO: Notificar a la interfaz si se requiere manejo especial

def generar_datos_grafico(puntos: int = 20) -> Dict[str, object]:
    """
    Genera listas simuladas de temperatura del agua a lo largo del tiempo para graficar la curva de calentamiento.
    Incluye manejo de errores y validación de datos.
    """
    try:
        T_ini = _estado_caldera.get("temperatura_inicial", 20)
        T_max = _estado_caldera.get("temperatura_maxima", 100)
        tiempo_total = _estado_caldera.get("tiempo_hasta_ebullicion", 25)
        if puntos <= 0 or tiempo_total <= 0:
            return {"status": "error", "data": {}, "message": "Parámetros de simulación inválidos."}
        temperaturas = []
        tiempos = []
        for i in range(puntos+1):
            t = i * (tiempo_total / puntos)
            temp = T_ini + (T_max - T_ini) * (t / tiempo_total) if tiempo_total > 0 else T_ini
            temperaturas.append(round(temp, 2))
            tiempos.append(round(t, 1))
        _datos_grafico["temperaturas"] = temperaturas
        _datos_grafico["tiempos"] = tiempos
        return {"status": "ok", "data": {"temperaturas": temperaturas, "tiempos": tiempos}, "message": "Datos de gráfico generados correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en generar_datos_grafico: {str(e)}"}
