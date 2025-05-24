"""
Backend para la simulación del funcionamiento de una caldera alimentada por energía solar o resistencia eléctrica.
Módulo funcional y modular para ser invocado desde la interfaz Kivy.
Incluye manejo de errores y validación de datos para robustez y seguridad.
Ahora es determinista: los resultados dependen solo de las entradas explícitas.
"""

from typing import Dict, List

# Variables internas de simulación
_estado_caldera = {
    "temperatura_inicial": 25.0,   # °C
    "temperatura_maxima": 100.0,  # °C (ebullición)
    "volumen_agua": 3.0,          # L
    "masa_agua": 3.0,             # kg
    "energia_entrada": 1000.0,    # W
    "modo": "resistencia",       # "resistencia" o "solar"
    "tiempo_hasta_ebullicion": 0, # min
    "energia_consumida": 0.0,     # Wh
    "vapor_generado": 0.0         # ml
}

# Datos históricos simulados para graficar
_datos_grafico = {
    "temperaturas": [],
    "tiempos": []
}

def iniciar_caldera(temperatura_inicial: float = 25.0, volumen_agua: float = 3.0, energia_entrada: float = 1000.0, modo: str = "resistencia"):
    """
    Inicializa variables de simulación para el proceso de calentamiento en la caldera.
    Ahora determinista: solo usa los valores de entrada o los valores por defecto.
    """
    try:
        _estado_caldera["temperatura_inicial"] = temperatura_inicial
        _estado_caldera["volumen_agua"] = volumen_agua
        _estado_caldera["masa_agua"] = volumen_agua  # 1L ~ 1kg
        _estado_caldera["energia_entrada"] = energia_entrada
        _estado_caldera["modo"] = modo if modo in ("resistencia", "solar") else "resistencia"
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
    Determinista: no usa aleatoriedad, solo entradas explícitas o constantes.
    """
    try:
        m = _estado_caldera.get("masa_agua", 3.0)  # kg
        c = 4186  # J/kg·°C
        T_ini = _estado_caldera.get("temperatura_inicial", 25.0)
        T_max = _estado_caldera.get("temperatura_maxima", 100.0)
        P = _estado_caldera.get("energia_entrada", 1000.0)  # W
        delta_T = T_max - T_ini
        energia_J = m * c * delta_T
        tiempo_s = energia_J / P if P > 0 else 1
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
        _estado_caldera["tiempo_hasta_ebullicion"] = 0
        _estado_caldera["energia_consumida"] = 0.0
        _estado_caldera["vapor_generado"] = 0.0

def generar_datos_grafico(puntos: int = 20) -> Dict[str, object]:
    """
    Genera listas deterministas de temperatura del agua a lo largo del tiempo para graficar la curva de calentamiento.
    """
    try:
        T_ini = _estado_caldera.get("temperatura_inicial", 25.0)
        T_max = _estado_caldera.get("temperatura_maxima", 100.0)
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
