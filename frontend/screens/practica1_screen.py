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
        import matplotlib.pyplot as plt
        from kivy_garden.matplotlib import FigureCanvasKivyAgg
        plt.style.use("seaborn-v0_8-muted")
        valores = self.grafico_valores or [0]
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        # Barra
        axs[0, 0].bar(range(len(valores)), valores, color="#2e86de")
        axs[0, 0].set_title('Energía generada (Barra)')
        axs[0, 0].set_xlabel('Simulación')
        axs[0, 0].set_ylabel('Wh')
        axs[0, 0].grid(True)
        # Línea
        axs[0, 1].plot(valores, color="#10ac84", marker='o', label="Energía generada")
        axs[0, 1].set_title('Energía generada (Línea)')
        axs[0, 1].set_xlabel('Simulación')
        axs[0, 1].set_ylabel('Wh')
        axs[0, 1].grid(True)
        axs[0, 1].legend(loc='upper right')
        # Puntos
        axs[1, 0].scatter(range(len(valores)), valores, color="#ff9f43", label="Energía generada")
        axs[1, 0].set_title('Energía generada (Puntos)')
        axs[1, 0].set_xlabel('Simulación')
        axs[1, 0].set_ylabel('Wh')
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
        self.ids.input_radiacion.text = ""
        self.ids.input_area.text = ""
        self.ids.input_eficiencia.text = ""
        self.ids.input_consumo.text = ""
        self.ids.input_perdidas.text = ""
        self.energia_generada = ""
        self.energia_consumida = ""
        self.eficiencia = ""
        self.mensaje_error = ""

    def mostrar_animacion(self):
        from kivy.uix.widget import Widget
        from kivy.uix.popup import Popup
        from kivy.uix.button import Button
        from kivy.graphics import Ellipse, Color, Rectangle, Line, RoundedRectangle
        from kivy.clock import Clock
        import math
        class SolarRealista(Widget):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.size = (800, 500)
                with self.canvas.before:
                    Color(1, 1, 1, 1)
                    Rectangle(pos=self.pos, size=self.size)
                # Posiciones y estados
                self.sol_pos = [160, 400]
                self.rayos_ang = [i*math.pi/8 for i in range(16)]
                self.rayos_long = [60+10*math.sin(i) for i in self.rayos_ang]
                self.panel_pos = [500, 180]
                self.bateria_pos = [670, 120]
                self.bateria_nivel = 0
                self.bateria_visible = False
                self.t = 0
                with self.canvas:
                    # Panel solar con textura de celdas
                    self.panel_color = Color(0.12, 0.36, 0.7, 1)
                    self.panel = Rectangle(pos=self.panel_pos, size=(120, 60))
                    # Celdas
                    self.celdas = []
                    self.celdas_colors = []
                    for i in range(4):
                        for j in range(2):
                            c_color = Color(0.18, 0.52, 0.87, 1)
                            self.celdas_colors.append(c_color)
                            self.celdas.append(Rectangle(pos=(self.panel_pos[0]+10+25*i, self.panel_pos[1]+10+20*j), size=(20, 16)))
                    # Borde panel
                    Color(0.1, 0.1, 0.1, 1)
                    Line(rectangle=(self.panel_pos[0], self.panel_pos[1], 120, 60), width=2)
                    # Batería cilíndrica (inicialmente vacía)
                    self.bateria_color = Color(0.3, 0.3, 0.3, 1)
                    self.bateria = RoundedRectangle(pos=self.bateria_pos, size=(40, 100), radius=[20])
                    # Tapa batería
                    self.tapa_color = Color(0.5, 0.5, 0.5, 1)
                    self.tapa = Ellipse(pos=(self.bateria_pos[0], self.bateria_pos[1]+90), size=(40, 20))
                    # Nivel de carga (verde, animado)
                    self.nivel_color = Color(0.2, 0.8, 0.2, 0.85)
                    self.nivel = Rectangle(pos=(self.bateria_pos[0]+5, self.bateria_pos[1]+10), size=(30, 0))
                # Sol y halo
                with self.canvas.after:
                    # Halo
                    self.halo_color = Color(1, 1, 0.5, 0.18)
                    self.halo = Ellipse(pos=(self.sol_pos[0]-40, self.sol_pos[1]-40), size=(170, 170))
                    # Sol
                    self.sol_color = Color(1, 0.95, 0.3, 1)
                    self.sol = Ellipse(pos=self.sol_pos, size=(90, 90))
                    # Rayos
                    self.rayos = []
                    self.rayos_colors = []
                    for ang, long in zip(self.rayos_ang, self.rayos_long):
                        r_color = Color(1, 0.95, 0.3, 0.7)
                        self.rayos_colors.append(r_color)
                        x0 = self.sol_pos[0]+45
                        y0 = self.sol_pos[1]+45
                        x1 = x0 + long*math.cos(ang)
                        y1 = y0 + long*math.sin(ang)
                        self.rayos.append(Line(points=[x0, y0, x1, y1], width=3))
                self._event = Clock.schedule_interval(self.animar, 1/60)
            def animar(self, dt):
                # Sol baja y rayos giran
                if self.sol_pos[1] > 250:
                    self.sol_pos[1] -= 2.5
                    self.sol.pos = self.sol_pos
                    self.halo.pos = (self.sol_pos[0]-40, self.sol_pos[1]-40)
                    # Rayos giran
                    for i, (ang, long) in enumerate(zip(self.rayos_ang, self.rayos_long)):
                        ang2 = ang + self.t*0.7
                        x0 = self.sol_pos[0]+45
                        y0 = self.sol_pos[1]+45
                        x1 = x0 + long*math.cos(ang2)
                        y1 = y0 + long*math.sin(ang2)
                        self.rayos[i].points = [x0, y0, x1, y1]
                else:
                    # Batería se llena por bloques
                    if self.bateria_nivel < 90:
                        self.bateria_nivel += 1.5
                        self.nivel.size = (30, self.bateria_nivel)
                    # Efecto de brillo en tapa
                    self.tapa.pos = (self.bateria_pos[0], self.bateria_pos[1]+90+self.bateria_nivel/10)
                self.t += dt
                if self.t > 8:
                    if self._event:
                        self._event.cancel()
            def stop(self):
                if hasattr(self, '_event') and self._event:
                    self._event.cancel()
        content = SolarRealista()
        popup = Popup(
            title="Animación – Energía Solar (Práctica 1)",
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
