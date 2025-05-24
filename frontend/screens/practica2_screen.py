# Pantalla práctica 2

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty
from backend import practica2_filtrado_multicapa as filtrado
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class Practica2Screen(Screen):
    turbidez_final = StringProperty("")
    tiempo_filtrado = StringProperty("")
    eficiencia_remocion = StringProperty("")
    mensaje_error = StringProperty("")

    grava_activa = BooleanProperty(True)
    arena_activa = BooleanProperty(True)
    carbon_activo = BooleanProperty(True)

    def mostrar_error(self, mensaje):
        self.mensaje_error = mensaje
        popup = Popup(title='Error',
                      content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def simular_filtrado(self):
        try:
            try:
                turbidez = float(self.ids.input_turbidez.text)
                volumen = float(self.ids.input_volumen.text)
                tiempo = float(self.ids.input_tiempo.text) if 'input_tiempo' in self.ids else 95
            except ValueError:
                self.mostrar_error("Todos los valores deben ser numéricos y válidos.")
                return
            if turbidez < 0 or volumen <= 0 or tiempo <= 0:
                self.mostrar_error("La turbidez debe ser >= 0 y el volumen y tiempo > 0.")
                return
            resultado = filtrado.calcular_resultados(
                turbidez_inicial=turbidez,
                volumen=volumen,
                tiempo=tiempo
            )
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
                self.mostrar_error(resultado.get("message", "Error en la simulación"))
        except Exception:
            self.turbidez_final = ""
            self.tiempo_filtrado = ""
            self.eficiencia_remocion = ""
            self.mostrar_error("Datos inválidos")
