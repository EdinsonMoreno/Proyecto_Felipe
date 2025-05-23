# Pantalla práctica 2

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty
from backend import practica2_filtrado_multicapa as filtrado

class Practica2Screen(Screen):
    turbidez_final = StringProperty("")
    tiempo_filtrado = StringProperty("")
    eficiencia = StringProperty("")
    mensaje_error = StringProperty("")

    grava_activa = BooleanProperty(True)
    arena_activa = BooleanProperty(True)
    carbon_activo = BooleanProperty(True)

    def simular_filtrado(self):
        try:
            turbidez_inicial = float(self.ids.input_turbidez.text)
            volumen = float(self.ids.input_volumen.text)
            capas = []
            if self.grava_activa:
                capas.append("grava")
            if self.arena_activa:
                capas.append("arena")
            if self.carbon_activo:
                capas.append("carbon")

            filtrado.iniciar_filtrado(turbidez_inicial, volumen, capas)
            resultado = filtrado.obtener_datos()
            if resultado.get("status") == "ok":
                datos = resultado.get("data", {})
                self.turbidez_final = f"{datos.get('turbidez_final', 0):.2f} NTU"
                self.tiempo_filtrado = f"{datos.get('tiempo_filtrado', 0):.1f} min"
                self.eficiencia = f"{datos.get('eficiencia', 0):.1f} %"
                self.mensaje_error = ""
            else:
                self.turbidez_final = ""
                self.tiempo_filtrado = ""
                self.eficiencia = ""
                self.mensaje_error = resultado.get("message", "Error en la simulación")
        except Exception:
            self.turbidez_final = ""
            self.tiempo_filtrado = ""
            self.eficiencia = ""
            self.mensaje_error = "Datos inválidos"
