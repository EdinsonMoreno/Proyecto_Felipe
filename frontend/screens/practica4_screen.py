from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from backend import practica4_caldera as caldera
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class Practica4Screen(Screen):
    temperatura_maxima = StringProperty("")
    tiempo_ebullicion = StringProperty("")
    energia_consumida = StringProperty("")
    vapor_generado = StringProperty("")
    eficiencia = StringProperty("")
    mensaje_error = StringProperty("")
    barra_temp = NumericProperty(0)

    def mostrar_error(self, mensaje):
        self.mensaje_error = mensaje
        popup = Popup(title='Error',
                      content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def simular_caldera(self, modo="resistencia"):
        try:
            # Leer inputs del usuario
            volumen = self.ids.input_volumen.text
            potencia = self.ids.input_potencia.text
            tiempo = self.ids.input_tiempo.text
            temperatura_inicial = self.ids.input_temperatura.text if 'input_temperatura' in self.ids else 25.0
            # Validar y convertir
            try:
                volumen = float(volumen)
                potencia = float(potencia)
                tiempo = float(tiempo)
                temperatura_inicial = float(temperatura_inicial)
            except ValueError:
                self.mostrar_error("Todos los valores deben ser numéricos y válidos.")
                return
            if volumen <= 0 or potencia <= 0 or tiempo <= 0:
                self.mostrar_error("Todos los valores deben ser mayores a cero.")
                return
            # Llamar backend correctamente
            resultado = caldera.calcular_resultados(
                temperatura_inicial=temperatura_inicial,
                volumen_agua=volumen/1000,  # ml a L
                energia_entrada=potencia,
                modo=modo
            )
            if resultado.get("status") == "ok":
                datos = resultado.get("data", {})
                self.temperatura_maxima = f"{datos.get('temperatura_maxima', 0):.1f} °C"
                self.tiempo_ebullicion = f"{datos.get('tiempo_hasta_ebullicion', 0):.1f} min"
                self.energia_consumida = f"{datos.get('energia_consumida', 0):.1f} Wh"
                self.vapor_generado = f"{datos.get('vapor_generado', 0):.1f} ml"
                # Eficiencia real: energía útil (evaporación) / energía suministrada total
                energia_util = float(datos.get('vapor_generado', 0)) / 1000 * 2260000  # ml a kg, L_v=2260000 J/kg
                energia_suministrada = float(potencia) * float(tiempo) * 60  # W * min a J
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
                self.mostrar_error(resultado.get("message", "Error en la simulación"))
        except Exception:
            self.temperatura_maxima = ""
            self.tiempo_ebullicion = ""
            self.energia_consumida = ""
            self.vapor_generado = ""
            self.eficiencia = ""
            self.barra_temp = 0
            self.mostrar_error("Datos inválidos")
