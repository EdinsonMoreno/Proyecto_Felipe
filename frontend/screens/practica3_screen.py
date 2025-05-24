# Pantalla práctica 3

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from backend import practica3_intercambiador_calor as intercambiador
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class Practica3Screen(Screen):
    temperatura_inicial = StringProperty("")
    temperatura_final = StringProperty("")
    tiempo_exposicion = StringProperty("")
    eficiencia_termica = StringProperty("")
    mensaje_error = StringProperty("")

    def mostrar_error(self, mensaje):
        self.mensaje_error = mensaje
        popup = Popup(title='Error',
                      content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def simular_intercambio(self):
        try:
            try:
                temperatura_inicial = float(self.ids.input_tcaliente.text)
                masa_agua = float(self.ids.input_caudal_caliente.text)
                potencia_solar = float(self.ids.input_tfrio.text)
                tiempo_exposicion = float(self.ids.input_tiempo.text)
            except ValueError:
                self.mostrar_error("Todos los valores deben ser numéricos y válidos.")
                return
            if temperatura_inicial < 0 or masa_agua <= 0 or potencia_solar < 0 or tiempo_exposicion <= 0:
                self.mostrar_error("Todos los valores deben ser mayores a cero (excepto temperaturas, que pueden ser >= 0).")
                return
            resultado = intercambiador.calcular_resultados(
                temperatura_inicial=temperatura_inicial,
                masa_agua=masa_agua,
                potencia_solar=potencia_solar,
                tiempo_exposicion=tiempo_exposicion
            )
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
                self.mostrar_error(resultado.get("message", "Error en la simulación"))
        except Exception:
            self.temperatura_inicial = ""
            self.temperatura_final = ""
            self.tiempo_exposicion = ""
            self.eficiencia_termica = ""
            self.mostrar_error("Datos inválidos")
