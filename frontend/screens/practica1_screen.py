from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from backend import practica1_balance_energetico as be
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import matplotlib.pyplot as plt
from kivy_garden.matplotlib import FigureCanvasKivyAgg

class Practica1Screen(Screen):
    energia_generada = StringProperty("")
    energia_consumida = StringProperty("")
    eficiencia = StringProperty("")
    mensaje_error = StringProperty("")
    grafico_valores = ListProperty([])

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
                # Guardar valor para graficar (energía generada)
                valor_actual = datos.get('energia_generada', 0)
                self.grafico_valores.append(valor_actual)
                if len(self.grafico_valores) > 4:
                    self.grafico_valores.pop(0)
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

    def graficar_resultados(self):
        valores = self.grafico_valores or [0]
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        axs[0, 0].bar(range(len(valores)), valores)
        axs[0, 0].set_title('Barra')
        axs[0, 1].plot(valores)
        axs[0, 1].set_title('Línea')
        axs[1, 0].scatter(range(len(valores)), valores)
        axs[1, 0].set_title('Puntos')
        axs[1, 1].pie([valores[-1], sum(valores[:-1]) or 1],
                      labels=['Actual', 'Anteriores'], autopct='%1.1f%%')
        axs[1, 1].set_title('Circular')
        fig.tight_layout()
        popup = Popup(title="Gráficas de resultados",
                      content=FigureCanvasKivyAgg(fig),
                      size_hint=(None, None), size=(900, 600))
        popup.open()

    def limpiar_datos(self):
        self.grafico_valores = []
        self.ids.input_radiacion.text = ""
        self.ids.input_area.text = ""
        self.ids.input_eficiencia.text = ""
        self.ids.input_consumo.text = ""
        self.ids.input_perdidas.text = ""
        self.energia_generada = ""
        self.energia_consumida = ""
        self.eficiencia = ""
        self.mensaje_error = ""
