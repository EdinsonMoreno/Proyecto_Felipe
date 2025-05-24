"""
Backend para la simulación del proceso de filtrado multicapa del agua.
Módulo funcional y modular para ser invocado desde la interfaz Kivy.
Incluye manejo de errores y validación de datos para robustez y seguridad.
Ahora es determinista: los resultados dependen solo de las entradas explícitas.
"""

from typing import Dict, List

# Variables internas de simulación
_estado_filtrado = {
    "turbidez_inicial": 120.0,  # NTU
    "turbidez_final": 8.5,     # NTU
    "volumen": 10.0,           # L
    "tiempo": 95               # segundos
}

# Datos históricos simulados para graficar
_datos_grafico = {
    "turbidez": [],
    "tiempos": []
}

def iniciar_filtrado(turbidez_inicial: float = 120.0, volumen: float = 10.0, tiempo: int = 95):
    """
    Inicializa variables de simulación para el proceso de filtrado multicapa.
    Ahora determinista: solo usa los valores de entrada o los valores por defecto.
    """
    try:
        _estado_filtrado["turbidez_inicial"] = turbidez_inicial
        _estado_filtrado["volumen"] = volumen
        _estado_filtrado["tiempo"] = tiempo
        # Cálculo determinista de turbidez final (reducción fija)
        _estado_filtrado["turbidez_final"] = max(turbidez_inicial * 0.07, 1.0)
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
    Determinista: no usa aleatoriedad, solo entradas explícitas o constantes.
    """
    try:
        tin = _estado_filtrado.get("turbidez_inicial", 120.0)
        tf = _estado_filtrado.get("turbidez_final", 8.5)
        if tin == 0:
            return {"status": "error", "data": 0.0, "message": "Turbidez inicial igual a cero."}
        eficiencia = ((tin - tf) / tin) * 100 if tin > 0 else 0
        eficiencia = max(0, min(eficiencia, 100))
        return {"status": "ok", "data": eficiencia, "message": "Eficiencia calculada correctamente."}
    except Exception as e:
        return {"status": "error", "data": 0.0, "message": f"Error en calcular_eficiencia: {str(e)}"}

def generar_datos_grafico(puntos: int = 5) -> Dict[str, object]:
    """
    Genera listas deterministas de turbidez a lo largo de las etapas de filtrado para graficar.
    """
    try:
        turbidez = _estado_filtrado.get("turbidez_inicial", 120.0)
        turbidez_list = [turbidez]
        tiempos = [0]
        if puntos <= 0:
            return {"status": "error", "data": {}, "message": "Parámetros de simulación inválidos."}
        for i in range(1, puntos):
            turbidez = turbidez * 0.5 if i == 1 else turbidez * 0.4 if i == 2 else turbidez * 0.25
            turbidez_list.append(round(turbidez, 2))
            tiempos.append(i * (_estado_filtrado.get("tiempo", 95) // puntos))
        _datos_grafico["turbidez"] = turbidez_list
        _datos_grafico["tiempos"] = tiempos
        return {"status": "ok", "data": {"turbidez": turbidez_list, "tiempos": tiempos}, "message": "Datos de gráfico generados correctamente."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en generar_datos_grafico: {str(e)}"}
