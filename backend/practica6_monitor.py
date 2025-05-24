# Consolidación de datos de monitoreo general para Práctica 6

from backend.practica1_balance_energetico import calcular_resultados as p1_resultados
from backend.practica2_filtrado_multicapa import calcular_resultados as p2_resultados
from backend.practica3_intercambiador_calor import calcular_resultados as p3_resultados
from backend.practica4_caldera import calcular_resultados as p4_resultados
from backend.practica5_captacion_lluvia import calcular_resultados as p5_resultados

def consolidar_datos():
    """
    Llama a los métodos de resultados de cada práctica y consolida los valores clave en un solo diccionario.
    Si alguna práctica no entrega datos, se documenta el error en el campo correspondiente.
    """
    datos = {}
    errores = []
    # Práctica 1
    try:
        p1 = p1_resultados(None, None, None, None)
        d1 = p1["data"] if isinstance(p1, dict) and "data" in p1 else {}
        datos["energia_generada"] = d1.get("energia_generada")
        datos["eficiencia_panel"] = d1.get("eficiencia")
    except Exception as e:
        datos["energia_generada"] = None
        datos["eficiencia_panel"] = None
        errores.append(f"Práctica 1 no responde: {str(e)}")
    # Práctica 2
    try:
        p2 = p2_resultados(None, None, None)
        d2 = p2["data"] if isinstance(p2, dict) and "data" in p2 else {}
        datos["turbidez_final"] = d2.get("turbidez_final")
        datos["eficiencia_remocion"] = d2.get("eficiencia_remocion")
    except Exception as e:
        datos["turbidez_final"] = None
        datos["eficiencia_remocion"] = None
        errores.append(f"Práctica 2 no responde: {str(e)}")
    # Práctica 3
    try:
        p3 = p3_resultados(None, None, None, None)
        d3 = p3["data"] if isinstance(p3, dict) and "data" in p3 else {}
        datos["temperatura_final"] = d3.get("temperatura_final")
        datos["eficiencia_termica"] = d3.get("eficiencia_termica")
    except Exception as e:
        datos["temperatura_final"] = None
        datos["eficiencia_termica"] = None
        errores.append(f"Práctica 3 no responde: {str(e)}")
    # Práctica 4
    try:
        p4 = p4_resultados(None, None, None)
        d4 = p4["data"] if isinstance(p4, dict) and "data" in p4 else {}
        datos["temp_caldera"] = d4.get("temperatura_maxima")
        datos["tiempo_ebullicion"] = d4.get("tiempo_hasta_ebullicion")
    except Exception as e:
        datos["temp_caldera"] = None
        datos["tiempo_ebullicion"] = None
        errores.append(f"Práctica 4 no responde: {str(e)}")
    # Práctica 5
    try:
        p5 = p5_resultados(None, None, None)
        d5 = p5["data"] if isinstance(p5, dict) and "data" in p5 else {}
        datos["nivel_tanque"] = d5.get("nivel_sensor")
        datos["volumen_captado"] = d5.get("volumen_captado")
    except Exception as e:
        datos["nivel_tanque"] = None
        datos["volumen_captado"] = None
        errores.append(f"Práctica 5 no responde: {str(e)}")
    datos["errores"] = errores
    return datos

def simular_condiciones_climaticas(parametros):
    """
    Reenvía parámetros climáticos a los módulos correspondientes.
    parametros: dict con claves como 'radiacion', 'lluvia', 'temperatura'.
    """
    resultados = {}
    errores = []
    # Práctica 1: radiación
    try:
        from backend.practica1_balance_energetico import simular_radiacion
        resultados["practica1"] = simular_radiacion(parametros.get("radiacion", 0))
    except Exception as e:
        errores.append(f"Práctica 1: {str(e)}")
    # Práctica 5: lluvia
    try:
        from backend.practica5_captacion_lluvia import simular_lluvia
        resultados["practica5"] = simular_lluvia(parametros.get("lluvia", 0))
    except Exception as e:
        errores.append(f"Práctica 5: {str(e)}")
    # Práctica 3 y 4: temperatura ambiente
    try:
        from backend.practica3_intercambiador_calor import simular_temperatura_ambiente
        resultados["practica3"] = simular_temperatura_ambiente(parametros.get("temperatura", 0))
    except Exception as e:
        errores.append(f"Práctica 3: {str(e)}")
    try:
        from backend.practica4_caldera import simular_temperatura_ambiente
        resultados["practica4"] = simular_temperatura_ambiente(parametros.get("temperatura", 0))
    except Exception as e:
        errores.append(f"Práctica 4: {str(e)}")
    resultados["errores"] = errores
    return resultados
