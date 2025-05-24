from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from backend import practica4_caldera as caldera

class Practica4Screen(Screen):
    temperatura_maxima = StringProperty("")
    tiempo_ebullicion = StringProperty("")
    energia_consumida = StringProperty("")
    vapor_generado = StringProperty("")
    eficiencia = StringProperty("")
    mensaje_error = StringProperty("")
    barra_temp = NumericProperty(0)

    def simular_caldera(self, modo="resistencia"):
        try:
            # Leer inputs del usuario
            volumen = self.ids.input_volumen.text
            potencia = self.ids.input_potencia.text
            tiempo = self.ids.input_tiempo.text
            # Validar y convertir
            volumen = float(volumen) if volumen else 0
            potencia = float(potencia) if potencia else 0
            tiempo = float(tiempo) if tiempo else 0
            # Llamar backend con parámetros (ajustar backend si es necesario)
            caldera.iniciar_caldera(modo)
            # Sobrescribir valores simulados con los del usuario si son válidos
            if volumen > 0:
                caldera._estado_caldera["volumen_agua"] = volumen / 1000  # ml a L
                caldera._estado_caldera["masa_agua"] = volumen / 1000
            if potencia > 0:
                caldera._estado_caldera["energia_entrada"] = potencia
            if tiempo > 0:
                # No se usa directamente, pero podría influir en la eficiencia
                pass
            caldera.calcular_resultados()
            resultado = caldera.obtener_datos()
            if resultado.get("status") == "ok":
                datos = resultado.get("data", {})
                self.temperatura_maxima = f"{datos.get('temperatura_maxima', 0):.1f} °C"
                self.tiempo_ebullicion = f"{datos.get('tiempo_hasta_ebullicion', 0):.1f} min"
                self.energia_consumida = f"{datos.get('energia_consumida', 0):.1f} Wh"
                self.vapor_generado = f"{datos.get('vapor_generado', 0):.1f} ml"
                # Eficiencia simple: energía útil/energía suministrada
                energia_util = float(datos.get('vapor_generado', 0)) * 2260 / 1000  # ml a kg, L_v=2260 kJ/kg
                energia_suministrada = float(datos.get('energia_consumida', 0)) * 3600  # Wh a J
                self.eficiencia = f"{(energia_util/energia_suministrada*100):.1f} %" if energia_suministrada > 0 else "0 %"
                # Barra de temperatura
                temp = float(datos.get('temperatura_maxima', 0))
                self.barra_temp = min(max((temp-20)/80, 0), 1)  # Normalizar 20-100°C
                self.mensaje_error = ""
            else:
                self.temperatura_maxima = ""
                self.tiempo_ebullicion = ""
                self.energia_consumida = ""
                self.vapor_generado = ""
                self.eficiencia = ""
                self.barra_temp = 0
                self.mensaje_error = resultado.get("message", "Error en la simulación")
        except Exception:
            self.temperatura_maxima = ""
            self.tiempo_ebullicion = ""
            self.energia_consumida = ""
            self.vapor_generado = ""
            self.eficiencia = ""
            self.barra_temp = 0
            self.mensaje_error = "Datos inválidos"
