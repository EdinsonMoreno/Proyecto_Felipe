"""
Backend para el análisis de balance energético del sistema fotovoltaico.
Módulo completamente funcional y modular para ser invocado desde la interfaz Kivy.
Incluye manejo de errores y validación de datos para robustez y seguridad.
Ahora es determinista: los resultados dependen solo de las entradas explícitas.
"""

from typing import Dict, List

# Variables internas de simulación (pueden ser sobrescritas por la interfaz si se desea)
_estado_simulacion = {
    "radiacion": 850.0,  # W/m² (valor fijo por defecto)
    "tension": 14.0,    # V
    "corriente": 8.0,   # A
    "tiempo": 1.0       # h
}

# Datos históricos simulados para graficar
_datos_grafico = {
    "energia_generada": [],
    "energia_consumida": []
}

def iniciar_medicion(radiacion: float = 850.0, tension: float = 14.0, corriente: float = 8.0, tiempo: float = 1.0):
    """
    Inicializa variables de simulación para la medición del sistema fotovoltaico.
    Ahora determinista: solo usa los valores de entrada o los valores por defecto.
    """
    try:
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
    Determinista: no usa aleatoriedad, solo entradas explícitas o constantes.
    """
    try:
        V = _estado_simulacion.get("tension", 14.0)
        I = _estado_simulacion.get("corriente", 8.0)
        t = _estado_simulacion.get("tiempo", 1.0)
        energia_generada = V * I * t
        # Consumo fijo: 75% de la energía generada
        energia_consumida = energia_generada * 0.75
        eficiencia = (energia_consumida / energia_generada) * 100 if energia_generada > 0 else 0
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
    Genera listas deterministas de energía generada y consumida a lo largo del tiempo para graficar.
    """
    try:
        if puntos <= 0:
            return {"status": "error", "data": {}, "message": "Parámetros de simulación inválidos."}
        energia_gen = []
        energia_con = []
        V = _estado_simulacion.get("tension", 14.0)
        I = _estado_simulacion.get("corriente", 8.0)
        for i in range(puntos):
            eg = V * I * 1.0  # 1h por punto
            ec = eg * 0.75
            energia_gen.append(round(eg, 2))
            energia_con.append(round(ec, 2))
        _datos_grafico["energia_generada"] = energia_gen
        _datos_grafico["energia_consumida"] = energia_con
        return {"status": "ok", "data": {"energia_generada": energia_gen, "energia_consumida": energia_con}, "message": "Datos de gráfico generados correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en generar_datos_grafico: {str(e)}"}
