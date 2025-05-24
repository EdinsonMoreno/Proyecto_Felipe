# Pantalla práctica 2

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty
from backend import practica2_filtrado_multicapa as filtrado

class Practica2Screen(Screen):
    turbidez_final = StringProperty("")
    tiempo_filtrado = StringProperty("")
    eficiencia_remocion = StringProperty("")
    mensaje_error = StringProperty("")

    grava_activa = BooleanProperty(True)
    arena_activa = BooleanProperty(True)
    carbon_activo = BooleanProperty(True)

    def simular_filtrado(self):
        try:
            filtrado.iniciar_filtrado()
            resultado = filtrado.obtener_datos()
            if resultado.get("status") == "ok":
                datos = resultado.get("data", {})
                self.turbidez_final = f"{datos.get('turbidez_final', 0):.2f} NTU"
                self.tiempo_filtrado = f"{datos.get('tiempo_filtrado', 0):.1f} s"
                self.eficiencia_remocion = f"{datos.get('eficiencia_remocion', 0):.1f} %"
                self.mensaje_error = ""
            else:
                self.turbidez_final = ""
                self.tiempo_filtrado = ""
                self.eficiencia_remocion = ""
                self.mensaje_error = resultado.get("message", "Error en la simulación")
        except Exception:
            self.turbidez_final = ""
            self.tiempo_filtrado = ""
            self.eficiencia_remocion = ""
            self.mensaje_error = "Datos inválidos"
