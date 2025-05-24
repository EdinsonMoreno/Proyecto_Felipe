# Pantalla práctica 3

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from backend import practica3_intercambiador_calor as intercambiador

class Practica3Screen(Screen):
    temperatura_inicial = StringProperty("")
    temperatura_final = StringProperty("")
    tiempo_exposicion = StringProperty("")
    eficiencia_termica = StringProperty("")
    mensaje_error = StringProperty("")

    def simular_intercambio(self):
        try:
            intercambiador.iniciar_calentamiento()
            resultado = intercambiador.obtener_datos()
            if resultado.get("status") == "ok":
                datos = resultado.get("data", {})
                self.temperatura_inicial = f"{datos.get('temperatura_inicial', 0):.1f} °C"
                self.temperatura_final = f"{datos.get('temperatura_final', 0):.1f} °C"
                self.tiempo_exposicion = f"{datos.get('tiempo_exposicion', 0):.1f} min"
                self.eficiencia_termica = f"{datos.get('eficiencia_termica', 0):.1f} %"
                self.mensaje_error = ""
            else:
                self.temperatura_inicial = ""
                self.temperatura_final = ""
                self.tiempo_exposicion = ""
                self.eficiencia_termica = ""
                self.mensaje_error = resultado.get("message", "Error en la simulación")
        except Exception:
            self.temperatura_inicial = ""
            self.temperatura_final = ""
            self.tiempo_exposicion = ""
            self.eficiencia_termica = ""
            self.mensaje_error = "Datos inválidos"
