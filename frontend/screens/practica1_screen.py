from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from backend import practica1_balance_energetico as be
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class Practica1Screen(Screen):
    energia_generada = StringProperty("")
    energia_consumida = StringProperty("")
    eficiencia = StringProperty("")
    mensaje_error = StringProperty("")

    def mostrar_error(self, mensaje):
        self.mensaje_error = mensaje
        popup = Popup(title='Error',
                      content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def simular_balance(self):
        try:
            try:
                radiacion = float(self.ids.input_radiacion.text)
                area = float(self.ids.input_area.text)
                eficiencia = float(self.ids.input_eficiencia.text) / 100.0  # % a fracción
                consumo = float(self.ids.input_consumo.text)
                perdidas = float(self.ids.input_perdidas.text) / 100.0  # % a fracción
            except ValueError:
                self.mostrar_error("Todos los valores deben ser numéricos y válidos.")
                return
            if radiacion <= 0 or area <= 0 or eficiencia <= 0 or consumo < 0 or perdidas < 0:
                self.mostrar_error("Todos los valores deben ser mayores a cero (excepto consumo y pérdidas, que pueden ser cero).")
                return
            # Cálculo de parámetros para el backend
            # Suponemos 1 día de operación
            tiempo = 24  # horas
            # Potencia generada por el panel (W) = radiación * área * eficiencia
            potencia_panel = radiacion * area * eficiencia
            # Energía generada (Wh) = potencia * tiempo
            energia_generada = potencia_panel * tiempo
            # Tensión y corriente ficticias para el backend (ajustar si se requiere realismo)
            tension = 12.0
            corriente = energia_generada / (tension * tiempo) if tension * tiempo > 0 else 1.0
            # Llamar backend con los parámetros calculados
            resultado = be.calcular_resultados(
                radiacion=radiacion,
                tension=tension,
                corriente=corriente,
                tiempo=tiempo,
                consumo=consumo,
                perdidas=perdidas
            )
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
                self.mostrar_error(resultado.get("message", "Error en la simulación"))
        except Exception:
            self.energia_generada = ""
            self.energia_consumida = ""
            self.eficiencia = ""
            self.mostrar_error("Datos inválidos")
