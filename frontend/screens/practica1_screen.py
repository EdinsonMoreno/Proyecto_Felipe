from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from backend import practica1_balance_energetico as be

class Practica1Screen(Screen):
    energia_generada = StringProperty("")
    energia_consumida = StringProperty("")
    eficiencia = StringProperty("")
    mensaje_error = StringProperty("")

    def simular_balance(self):
        try:
            be.iniciar_medicion()
            resultado = be.obtener_datos()
            if resultado.get("status") == "ok":
                datos = resultado.get("data", {})
                self.energia_generada = f"{datos.get('energia_generada', 0):.2f} Wh"
                self.energia_consumida = f"{datos.get('energia_consumida', 0):.2f} Wh"
                self.eficiencia = f"{datos.get('eficiencia', 0):.1f} %"
                self.mensaje_error = ""
            else:
                self.energia_generada = ""
                self.energia_consumida = ""
                self.eficiencia = ""
                self.mensaje_error = resultado.get("message", "Error en la simulación")
        except Exception:
            self.energia_generada = ""
            self.energia_consumida = ""
            self.eficiencia = ""
            self.mensaje_error = "Datos inválidos"
