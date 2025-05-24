from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from backend import practica5_captacion_lluvia as captacion
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class Practica5Screen(Screen):
    volumen_captado = StringProperty("")
    nivel_sensor = StringProperty("")
    volumen_estimado = StringProperty("")
    precision = StringProperty("")
    tiempo_captacion = StringProperty("")
    mensaje_error = StringProperty("")

    def mostrar_error(self, mensaje):
        self.mensaje_error = mensaje
        popup = Popup(title='Error',
                      content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def simular_captacion(self):
        try:
            try:
                intensidad_lluvia = float(self.ids.input_intensidad.text)
                area_techo = float(self.ids.input_area.text)
                duracion = float(self.ids.input_tiempo.text)  # Corregido aquí
            except (ValueError, AttributeError):
                self.mostrar_error("Todos los valores deben ser numéricos y válidos.")
                return
            if intensidad_lluvia <= 0 or area_techo <= 0 or duracion <= 0:
                self.mostrar_error("Todos los valores deben ser mayores a cero.")
                return
            resultado = captacion.calcular_resultados(
                intensidad_lluvia=intensidad_lluvia,
                area_techo=area_techo,
                duracion=duracion
            )
            if resultado.get("status") == "ok":
                datos = resultado.get("data", {})
                self.volumen_captado = f"{datos.get('volumen_captado', 0):.2f} L"
                self.nivel_sensor = f"{datos.get('nivel_sensor', 0):.1f} cm"
                self.volumen_estimado = f"{datos.get('volumen_est_medido', 0):.2f} L"
                self.precision = f"{datos.get('precision_medicion', 0):.1f} %"
                self.tiempo_captacion = f"{datos.get('tiempo_captacion', 0):.1f} min"
                self.mensaje_error = ""
            else:
                self.volumen_captado = ""
                self.nivel_sensor = ""
                self.volumen_estimado = ""
                self.precision = ""
                self.tiempo_captacion = ""
                self.mostrar_error(resultado.get("message", "Error en la simulación"))
        except Exception:
            self.volumen_captado = ""
            self.nivel_sensor = ""
            self.volumen_estimado = ""
            self.precision = ""
            self.tiempo_captacion = ""
            self.mostrar_error("Datos inválidos")
