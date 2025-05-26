"""
Backend para la simulación del funcionamiento de una caldera alimentada por energía solar o resistencia eléctrica.
Corrige el cálculo físico: temperatura final, tiempo hasta ebullición y vapor generado.
"""

from typing import Dict

def calcular_resultados(potencia_w, tiempo_min, volumen_agua_ml, temperatura_inicial_c=25.0) -> Dict[str, object]:
    """
    Calcula la temperatura final, tiempo hasta ebullición y vapor generado para una caldera eléctrica.
    Parámetros:
        potencia_w: Potencia de la resistencia (W)
        tiempo_min: Tiempo de operación (minutos)
        volumen_agua_ml: Volumen de agua (ml)
        temperatura_inicial_c: Temperatura inicial del agua (°C)
    Retorna:
        Dict con temperatura final, tiempo hasta ebullición, energía consumida y vapor generado.
    """
    try:
        # Validación y conversión de entradas
        try:
            potencia_w = float(potencia_w)
        except Exception:
            potencia_w = 1000.0
        try:
            tiempo_min = float(tiempo_min)
        except Exception:
            tiempo_min = 10.0
        try:
            volumen_agua_ml = float(volumen_agua_ml)
        except Exception:
            volumen_agua_ml = 3000.0
        try:
            temperatura_inicial_c = float(temperatura_inicial_c)
        except Exception:
            temperatura_inicial_c = 25.0

        # Constantes físicas
        c = 4186  # J/(kg·°C)
        L_v = 2260000  # Calor de vaporización J/kg
        temperatura_ebullicion = 100.0
        masa_agua_kg = volumen_agua_ml / 1000.0  # 1 ml = 0.001 kg
        
        # Energía entregada por la resistencia
        tiempo_s = tiempo_min * 60
        energia_entregada_J = potencia_w * tiempo_s

        # Energía necesaria para llegar a ebullición
        delta_T_ebullicion = temperatura_ebullicion - temperatura_inicial_c
        energia_necesaria_ebullicion = masa_agua_kg * c * delta_T_ebullicion

        if energia_entregada_J >= energia_necesaria_ebullicion:
            # El agua llega a ebullición
            temperatura_final = temperatura_ebullicion
            # Tiempo real hasta ebullición
            tiempo_ebullicion_s = energia_necesaria_ebullicion / potencia_w
            tiempo_ebullicion_min = tiempo_ebullicion_s / 60
            # Energía sobrante para vaporizar agua
            energia_restante = energia_entregada_J - energia_necesaria_ebullicion
            masa_vapor_kg = energia_restante / L_v if energia_restante > 0 else 0
            vapor_ml = max(0, masa_vapor_kg * 1000)
        else:
            # El agua no llega a ebullición
            temperatura_final = temperatura_inicial_c + energia_entregada_J / (masa_agua_kg * c)
            temperatura_final = min(temperatura_final, temperatura_ebullicion)
            tiempo_ebullicion_min = None
            vapor_ml = 0

        # Energía consumida en Wh
        energia_consumida_Wh = energia_entregada_J / 3600

        datos = {
            "temperatura_final": round(temperatura_final, 2),
            "tiempo_hasta_ebullicion": round(tiempo_ebullicion_min, 1) if tiempo_ebullicion_min is not None else None,
            "energia_consumida": round(energia_consumida_Wh, 2),
            "vapor_generado": round(vapor_ml, 1)
        }
        return {"status": "ok", "data": datos, "message": "Cálculo físico correcto."}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Error en el cálculo: {str(e)}"}
