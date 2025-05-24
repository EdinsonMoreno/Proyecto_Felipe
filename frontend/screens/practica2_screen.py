# Pantalla práctica 2

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from backend import practica2_filtrado_multicapa as filtrado
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import matplotlib.pyplot as plt
from kivy_garden.matplotlib import FigureCanvasKivyAgg

class Practica2Screen(Screen):
    turbidez_final = StringProperty("")
    tiempo_filtrado = StringProperty("")
    eficiencia_remocion = StringProperty("")
    mensaje_error = StringProperty("")
    grafico_valores = ListProperty([])

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
            # Enviar el estado de las capas activas al backend
            resultado = filtrado.calcular_resultados(
                turbidez_inicial=turbidez,
                volumen=volumen,
                tiempo=tiempo,
                grava_activa=self.grava_activa,
                arena_activa=self.arena_activa,
                carbon_activo=self.carbon_activo
            )
            if resultado.get("status") == "ok":
                datos = resultado.get("data", {})
                self.turbidez_final = f"{datos.get('turbidez_final', 0):.2f} NTU"
                self.tiempo_filtrado = f"{datos.get('tiempo_filtrado', 0):.1f} s"
                self.eficiencia_remocion = f"{datos.get('eficiencia_remocion', 0):.1f} %"
                self.mensaje_error = ""
                # Guardar valor para graficar (turbidez final)
                valor_actual = datos.get('turbidez_final', 0)
                self.grafico_valores.append(valor_actual)
                if len(self.grafico_valores) > 4:
                    self.grafico_valores.pop(0)
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
    def graficar_resultados(self):
        import matplotlib.pyplot as plt
        from kivy_garden.matplotlib import FigureCanvasKivyAgg
        plt.style.use("seaborn-v0_8-muted")
        valores = self.grafico_valores or [0]
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        # Barra
        axs[0, 0].bar(range(len(valores)), valores, color="#2e86de")
        axs[0, 0].set_title('Turbidez final (Barra)')
        axs[0, 0].set_xlabel('Simulación')
        axs[0, 0].set_ylabel('NTU')
        axs[0, 0].grid(True)
        # Línea
        axs[0, 1].plot(valores, color="#10ac84", marker='o', label="Turbidez final")
        axs[0, 1].set_title('Turbidez final (Línea)')
        axs[0, 1].set_xlabel('Simulación')
        axs[0, 1].set_ylabel('NTU')
        axs[0, 1].grid(True)
        axs[0, 1].legend(loc='upper right')
        # Puntos
        axs[1, 0].scatter(range(len(valores)), valores, color="#ff9f43", label="Turbidez final")
        axs[1, 0].set_title('Turbidez final (Puntos)')
        axs[1, 0].set_xlabel('Simulación')
        axs[1, 0].set_ylabel('NTU')
        axs[1, 0].grid(True)
        axs[1, 0].legend(loc='upper right')
        # Circular
        colores = ["#2e86de", "#10ac84", "#ff9f43", "#f6e58d"]
        axs[1, 1].pie([valores[-1], sum(valores[:-1]) or 1],
                      labels=['Actual', 'Anteriores'], autopct='%1.1f%%', colors=colores[:2])
        axs[1, 1].set_title('Distribución actual vs anteriores')
        fig.tight_layout()
        popup = Popup(title="Gráficas de resultados",
                      content=FigureCanvasKivyAgg(fig),
                      size_hint=(None, None), size=(900, 600))
        popup.open()
    def limpiar_datos(self):
        self.grafico_valores = []
        self.ids.input_turbidez.text = ""
        self.ids.input_volumen.text = ""
        if 'input_tiempo' in self.ids:
            self.ids.input_tiempo.text = ""
        self.turbidez_final = ""
        self.tiempo_filtrado = ""
        self.eficiencia_remocion = ""
        self.mensaje_error = ""
