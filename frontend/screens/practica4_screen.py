from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, ListProperty
from backend import practica4_caldera as caldera
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import matplotlib.pyplot as plt
from kivy_garden.matplotlib import FigureCanvasKivyAgg

class Practica4Screen(Screen):
    temperatura_maxima = StringProperty("")
    tiempo_ebullicion = StringProperty("")
    energia_consumida = StringProperty("")
    vapor_generado = StringProperty("")
    eficiencia = StringProperty("")
    mensaje_error = StringProperty("")
    barra_temp = NumericProperty(0)
    grafico_valores = ListProperty([])

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
                # Guardar valor para graficar (temperatura máxima)
                valor_actual = datos.get('temperatura_maxima', 0)
                self.grafico_valores.append(valor_actual)
                if len(self.grafico_valores) > 4:
                    self.grafico_valores.pop(0)
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
    def graficar_resultados(self):
        import matplotlib.pyplot as plt
        from kivy_garden.matplotlib import FigureCanvasKivyAgg
        plt.style.use("seaborn-v0_8-muted")
        valores = self.grafico_valores or [0]
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        # Barra
        axs[0, 0].bar(range(len(valores)), valores, color="#2e86de")
        axs[0, 0].set_title('Temperatura máxima (Barra)')
        axs[0, 0].set_xlabel('Simulación')
        axs[0, 0].set_ylabel('°C')
        axs[0, 0].grid(True)
        # Línea
        axs[0, 1].plot(valores, color="#10ac84", marker='o', label="Temperatura máxima")
        axs[0, 1].set_title('Temperatura máxima (Línea)')
        axs[0, 1].set_xlabel('Simulación')
        axs[0, 1].set_ylabel('°C')
        axs[0, 1].grid(True)
        axs[0, 1].legend(loc='upper right')
        # Puntos
        axs[1, 0].scatter(range(len(valores)), valores, color="#ff9f43", label="Temperatura máxima")
        axs[1, 0].set_title('Temperatura máxima (Puntos)')
        axs[1, 0].set_xlabel('Simulación')
        axs[1, 0].set_ylabel('°C')
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
        self.ids.input_volumen.text = ""
        self.ids.input_potencia.text = ""
        self.ids.input_tiempo.text = ""
        if 'input_temperatura' in self.ids:
            self.ids.input_temperatura.text = ""
        self.temperatura_maxima = ""
        self.tiempo_ebullicion = ""
        self.energia_consumida = ""
        self.vapor_generado = ""
        self.eficiencia = ""
        self.barra_temp = 0
        self.mensaje_error = ""
    def mostrar_animacion(self):
        from kivy.uix.widget import Widget
        from kivy.uix.popup import Popup
        from kivy.uix.button import Button
        from kivy.graphics import Rectangle, Color, Line, Ellipse
        from kivy.clock import Clock
        class CalderaAnimada(Widget):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.size = (800, 500)
                with self.canvas.before:
                    Color(1, 1, 1, 1)
                    Rectangle(pos=self.pos, size=self.size)
                self.n_burbujas = 8
                self.burbujas = []
                self.vapor = []
                self.t = 0
                # Elementos
                with self.canvas:
                    # Tanque
                    Color(0.2, 0.6, 0.8, 1)
                    self.tanque = Rectangle(pos=(320, 140), size=(160, 120))
                    # Agua (nivel sube y color cambia)
                    Color(0.1, 0.5, 1, 0.7)
                    self.agua = Rectangle(pos=(320, 140), size=(160, 80))
                    # Vapor (líneas curvas)
                    for i in range(3):
                        Color(0.8, 0.8, 0.8, 0.7)
                        self.vapor.append(Line(points=[360+60*i, 260, 360+60*i, 380], width=2))
                    # Burbujas
                    for i in range(self.n_burbujas):
                        Color(1,1,1,0.7)
                        self.burbujas.append(Ellipse(pos=(340+18*i, 150), size=(16,16)))
                self._event = Clock.schedule_interval(self.animar, 1/60)
            def animar(self, dt):
                # Animar burbujas
                for i, burbuja in enumerate(self.burbujas):
                    x, y = burbuja.pos
                    y += 1.5 + i*0.1
                    if y > 220:
                        y = 150
                    burbuja.pos = (x, y)
                # Animar vapor (ondulaciones)
                for i, linea in enumerate(self.vapor):
                    p = linea.points
                    p[1] = 260 + 10 * (self.t + i)
                    p[3] = 380 + 10 * (self.t + i)
                    linea.points = p
                # Subir nivel de agua y cambiar color
                nivel = min(80 + self.t*3, 120)
                self.agua.size = (160, nivel)
                if nivel > 100:
                    self.agua.rgb = (1, 0.7, 0.2)
                self.t += dt
                if self.t > 10:
                    if self._event:
                        self._event.cancel()
            def stop(self):
                if hasattr(self, '_event') and self._event:
                    self._event.cancel()
        content = CalderaAnimada()
        popup = Popup(
            title="Animación – Práctica 4",
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
