"""
Backend para la simulación de captación de agua lluvia desde un techo hacia un tanque con sensor ultrasónico.
Módulo funcional y modular para ser invocado desde la interfaz Kivy.
Incluye manejo de errores y validación de datos para robustez y seguridad.
Ahora es determinista: los resultados dependen solo de las entradas explícitas.
"""

from typing import Dict, List

# Variables internas de simulación
_estado_captacion = {
    "intensidad_lluvia": 25.0,   # mm/h
    "area_techo": 12.0,         # m2
    "duracion": 8.5,            # min
    "volumen_captado": 0.0,     # L
    "nivel_sensor": 0.0,        # cm
    "volumen_est_medido": 0.0,  # L
    "precision_medicion": 0.0,  # %
    "tiempo_captacion": 8.5     # min
}

# Datos históricos simulados para graficar
_datos_grafico = {
    "niveles": [],
    "volumenes": [],
    "tiempos": []
}

def iniciar_captacion(intensidad_lluvia: float = 25.0, area_techo: float = 12.0, duracion: float = 8.5):
    """
    Inicializa variables de simulación para el evento de captación de agua lluvia.
    Ahora determinista: solo usa los valores de entrada o los valores por defecto.
    """
    try:
        _estado_captacion["intensidad_lluvia"] = intensidad_lluvia
        _estado_captacion["area_techo"] = area_techo
        _estado_captacion["duracion"] = duracion
        # Cálculo determinista de volumen captado
        volumen = (intensidad_lluvia / 60) * area_techo * duracion
        _estado_captacion["volumen_captado"] = volumen
        # Nivel detectado por sensor (tanque cilíndrico típico, 40 cm alto, 30 cm diámetro)
        altura_tanque = 40  # cm
        area_base = 3.1416 * (15**2)  # cm2
        volumen_sensor = volumen * 1000  # L a cm3
        nivel_sensor = min(volumen_sensor / area_base, altura_tanque)
        _estado_captacion["nivel_sensor"] = nivel_sensor
        # Volumen estimado por el sensor (sin error aleatorio)
        _estado_captacion["volumen_est_medido"] = volumen
        _estado_captacion["tiempo_captacion"] = duracion
        _estado_captacion["precision_medicion"] = calcular_precision()["data"]
        return {"status": "ok", "data": {}, "message": "Captación iniciada correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en iniciar_captacion: {str(e)}"}

def obtener_datos() -> Dict[str, object]:
    """
    Retorna un diccionario con los indicadores principales del proceso de captación y medición.
    Incluye manejo de errores y validación de datos.
    """
    try:
        datos = {
            "volumen_captado": round(_estado_captacion["volumen_captado"], 2),
            "nivel_sensor": round(_estado_captacion["nivel_sensor"], 1),
            "volumen_est_medido": round(_estado_captacion["volumen_est_medido"], 2),
            "precision_medicion": round(_estado_captacion["precision_medicion"], 1),
            "tiempo_captacion": round(_estado_captacion["tiempo_captacion"], 1)
        }
        if any(v < 0 for v in datos.values() if isinstance(v, (int, float))):
            return {"status": "error", "data": datos, "message": "Valores negativos detectados en los datos."}
        return {"status": "ok", "data": datos, "message": "Datos obtenidos correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en obtener_datos: {str(e)}"}

def calcular_precision() -> Dict[str, object]:
    """
    Calcula la precisión de la medición del sensor ultrasónico comparando volumen real y estimado.
    Determinista: no usa aleatoriedad, solo entradas explícitas o constantes.
    """
    try:
        v_real = _estado_captacion.get("volumen_captado", 12.5)
        v_sensor = _estado_captacion.get("volumen_est_medido", 12.1)
        if v_real == 0:
            return {"status": "error", "data": 0.0, "message": "Volumen real igual a cero."}
        precision = (1 - abs(v_real - v_sensor) / v_real) * 100 if v_real > 0 else 0
        precision = max(0, min(precision, 100))
        return {"status": "ok", "data": precision, "message": "Precisión calculada correctamente."}
    except Exception as e:
        return {"status": "error", "data": 0.0, "message": f"Error en calcular_precision: {str(e)}"}

def generar_datos_grafico(puntos: int = 10) -> Dict[str, object]:
    """
    Genera listas deterministas de nivel y volumen a lo largo del tiempo para graficar el comportamiento de captación.
    """
    try:
        volumen_total = _estado_captacion.get("volumen_captado", 12.5)
        nivel_max = _estado_captacion.get("nivel_sensor", 23.4)
        tiempo_total = _estado_captacion.get("tiempo_captacion", 8.5)
        if puntos <= 0 or tiempo_total <= 0:
            return {"status": "error", "data": {}, "message": "Parámetros de simulación inválidos."}
        niveles = []
        volumenes = []
        tiempos = []
        for i in range(puntos+1):
            t = i * (tiempo_total / puntos)
            v = volumen_total * (t / tiempo_total) if tiempo_total > 0 else 0
            n = nivel_max * (t / tiempo_total) if tiempo_total > 0 else 0
            niveles.append(round(n, 2))
            volumenes.append(round(v, 2))
            tiempos.append(round(t, 2))
        _datos_grafico["niveles"] = niveles
        _datos_grafico["volumenes"] = volumenes
        _datos_grafico["tiempos"] = tiempos
        return {"status": "ok", "data": {"niveles": niveles, "volumenes": volumenes, "tiempos": tiempos}, "message": "Datos de gráfico generados correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en generar_datos_grafico: {str(e)}"}
