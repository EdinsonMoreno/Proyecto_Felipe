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
        from kivy.graphics import Ellipse, Color, Rectangle, Line
        from kivy.clock import Clock
        class SolarAnimada(Widget):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.size = (800, 500)
                with self.canvas.before:
                    Color(1, 1, 1, 1)
                    Rectangle(pos=self.pos, size=self.size)
                self.sol_pos = [100, 400]
                self.panel_pos = [500, 180]
                self.bateria_pos = [650, 120]
                self.bateria_visible = False
                self.bateria_nivel = 0
                with self.canvas:
                    # Panel inclinado
                    Color(0.18, 0.52, 0.87, 1)
                    self.panel = Rectangle(pos=self.panel_pos, size=(120, 40))
                    # Sol
                    Color(1, 1, 0, 1)
                    self.sol = Ellipse(pos=self.sol_pos, size=(90, 90))
                    # Halo
                    Color(1, 1, 0, 0.2)
                    self.halo = Ellipse(pos=(self.sol_pos[0]-20, self.sol_pos[1]-20), size=(130, 130))
                    # Batería (inicialmente invisible)
                    self.bateria = Rectangle(pos=self.bateria_pos, size=(40, 100))
                    # Barras de carga
                    self.barras = [Rectangle(pos=(self.bateria_pos[0]+5, self.bateria_pos[1]+10+20*i), size=(30, 16)) for i in range(4)]
                self.t = 0
                self._event = Clock.schedule_interval(self.animar, 1/60)
            def animar(self, dt):
                # Sol baja hacia el panel
                if self.sol_pos[1] > 220:
                    self.sol_pos[1] -= 3
                    self.sol.pos = self.sol_pos
                    self.halo.pos = (self.sol_pos[0]-20, self.sol_pos[1]-20)
                else:
                    # Mostrar batería y llenarla por segmentos
                    self.bateria_visible = True
                    if self.bateria_nivel < 4 and self.t > 1.5:
                        self.bateria_nivel = min(4, int((self.t-1.5)//0.7)+1)
                    # Dibujar barras de carga
                    for i, barra in enumerate(self.barras):
                        if i < self.bateria_nivel:
                            barra.size = (30, 16)
                            barra.pos = (self.bateria_pos[0]+5, self.bateria_pos[1]+10+20*i)
                            Color(0.2, 0.8, 0.2, 1)
                        else:
                            barra.size = (0, 0)
                    # Batería contorno
                    Color(0.1, 0.1, 0.1, 1)
                    Line(rectangle=(self.bateria_pos[0], self.bateria_pos[1], 40, 100), width=2)
                self.t += dt
                if self.t > 7:
                    if self._event:
                        self._event.cancel()
            def stop(self):
                if hasattr(self, '_event') and self._event:
                    self._event.cancel()
        content = SolarAnimada()
        popup = Popup(
            title="Animación – Práctica 1",
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
