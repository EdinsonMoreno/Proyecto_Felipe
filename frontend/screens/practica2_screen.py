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
    def mostrar_animacion(self):
        from kivy.uix.widget import Widget
        from kivy.uix.popup import Popup
        from kivy.uix.button import Button
        from kivy.graphics import Ellipse, Color, Rectangle, Line
        from kivy.clock import Clock
        import math
        class FiltradoRealista(Widget):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.size = (800, 500)
                with self.canvas.before:
                    Color(1, 1, 1, 1)
                    Rectangle(pos=self.pos, size=self.size)
                # Capas de filtro
                self.capas = [
                    {'color': (0.6,0.6,0.6,1), 'y': 340, 'label': 'Grava'},
                    {'color': (0.95,0.85,0.5,1), 'y': 260, 'label': 'Arena'},
                    {'color': (0.18,0.18,0.18,1), 'y': 180, 'label': 'Carbón'}
                ]
                self.gota_y = 400
                self.gota_color = [0.2, 0.6, 0.9, 1]
                self.gota_brillo = 1.0
                self.t = 0
                self.etapa = 0
                with self.canvas:
                    # Filtros con textura
                    self.rect_capas = []
                    for capa in self.capas:
                        Color(*capa['color'])
                        self.rect_capas.append(Rectangle(pos=(320, capa['y']), size=(160, 60)))
                        # Textura: líneas
                        for i in range(8):
                            Color(0.8,0.8,0.8,0.15)
                            Line(points=[330+i*18, capa['y'], 330+i*18, capa['y']+60], width=1)
                    # Recipiente final
                    Color(0.7, 0.9, 1, 0.4)
                    self.rec_final = Rectangle(pos=(340, 120), size=(120, 40))
                    # Gota
                    self.gota_color_instr = Color(*self.gota_color)
                    self.gota = Ellipse(pos=(380, self.gota_y), size=(40, 56))
                    # Brillo de la gota
                    self.gota_brillo_color_instr = Color(1,1,1,0.25)
                    self.gota_brillo_ellipse = Ellipse(pos=(395, self.gota_y+30), size=(15, 18))
                self._event = Clock.schedule_interval(self.animar, 1/60)
            def animar(self, dt):
                # Gota baja y cambia de color según capa
                if self.etapa < 3:
                    if self.gota_y > self.capas[self.etapa]['y']+10:
                        self.gota_y -= 2.5
                        self.gota.pos = (380, self.gota_y)
                        self.gota_brillo_ellipse.pos = (395, self.gota_y+30)
                    else:
                        # Cambia color y brillo
                        if self.etapa == 0:
                            self.gota_color = [0.3, 0.5, 0.8, 1]
                        elif self.etapa == 1:
                            self.gota_color = [0.7, 0.8, 0.9, 1]
                        elif self.etapa == 2:
                            self.gota_color = [0.8, 1, 1, 1]
                        self.gota_brillo = 0.5 + 0.2*self.etapa
                        self.etapa += 1
                else:
                    # Gota llega al recipiente y se vuelve translúcida
                    if self.gota_y > 140:
                        self.gota_y -= 2.5
                        self.gota.pos = (380, self.gota_y)
                        self.gota_brillo_ellipse.pos = (395, self.gota_y+30)
                        self.gota_color = [0.8, 1, 1, 0.7]
                    else:
                        # Rebote y reinicio
                        self.gota_y = 400
                        self.etapa = 0
                        self.gota_color = [0.2, 0.6, 0.9, 1]
                # Actualizar color y brillo
                self.gota_color_instr.rgba = self.gota_color
                self.gota_brillo_color_instr.a = self.gota_brillo
                self.t += dt
                if self.t > 12:
                    if self._event:
                        self._event.cancel()
            def stop(self):
                if hasattr(self, '_event') and self._event:
                    self._event.cancel()
        content = FiltradoRealista()
        popup = Popup(
            title="Animación – Filtrado Multicapa (Práctica 2)",
            content=content,
            background="atlas://data/images/defaulttheme/button",
            size_hint=(None, None), size=(800, 500),
            separator_color=(0, 0, 0, 1),
            title_color=(0, 0, 0, 1)
        )
        btn_cerrar = Button(text="Cerrar", size_hint=(None, None), size=(100, 40), pos_hint={"right": 1, "top": 1}, background_color=(0.93, 0.49, 0.14, 1), color=(0,0,0,1), font_size=16)
        def cerrar_popup(*a):
            content.stop()
            popup.dismiss()
        btn_cerrar.bind(on_release=cerrar_popup)
        popup._container.add_widget(btn_cerrar)
        popup.open()
