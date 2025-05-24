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
            # Validar inputs si existen (ejemplo: volumen esperado, altura, etc.)
            # Si no hay inputs, omitir validación
            captacion.iniciar_captacion()
            resultado = captacion.obtener_datos()
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
