from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from backend import practica5_captacion_lluvia as captacion
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import matplotlib.pyplot as plt
from kivy_garden.matplotlib import FigureCanvasKivyAgg

class Practica5Screen(Screen):
    volumen_captado = StringProperty("")
    nivel_sensor = StringProperty("")
    volumen_estimado = StringProperty("")
    precision = StringProperty("")
    tiempo_captacion = StringProperty("")
    mensaje_error = StringProperty("")
    grafico_valores = ListProperty([])

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
                # Guardar valor para graficar (nivel del sensor)
                valor_actual = datos.get('nivel_sensor', 0)
                self.grafico_valores.append(valor_actual)
                if len(self.grafico_valores) > 4:
                    self.grafico_valores.pop(0)
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
    def graficar_resultados(self):
        import matplotlib.pyplot as plt
        from kivy_garden.matplotlib import FigureCanvasKivyAgg
        plt.style.use("seaborn-v0_8-muted")
        valores = self.grafico_valores or [0]
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        # Barra
        axs[0, 0].bar(range(len(valores)), valores, color="#2e86de")
        axs[0, 0].set_title('Nivel del sensor (Barra)')
        axs[0, 0].set_xlabel('Simulación')
        axs[0, 0].set_ylabel('cm')
        axs[0, 0].grid(True)
        # Línea
        axs[0, 1].plot(valores, color="#10ac84", marker='o', label="Nivel del sensor")
        axs[0, 1].set_title('Nivel del sensor (Línea)')
        axs[0, 1].set_xlabel('Simulación')
        axs[0, 1].set_ylabel('cm')
        axs[0, 1].grid(True)
        axs[0, 1].legend(loc='upper right')
        # Puntos
        axs[1, 0].scatter(range(len(valores)), valores, color="#ff9f43", label="Nivel del sensor")
        axs[1, 0].set_title('Nivel del sensor (Puntos)')
        axs[1, 0].set_xlabel('Simulación')
        axs[1, 0].set_ylabel('cm')
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
        self.ids.input_intensidad.text = ""
        self.ids.input_area.text = ""
        self.ids.input_tiempo.text = ""
        self.volumen_captado = ""
        self.nivel_sensor = ""
        self.volumen_estimado = ""
        self.precision = ""
        self.tiempo_captacion = ""
        self.mensaje_error = ""
    def mostrar_animacion(self):
        from kivy.uix.widget import Widget
        from kivy.uix.popup import Popup
        from kivy.uix.button import Button
        from kivy.graphics import Ellipse, Color, Rectangle, Line
        from kivy.clock import Clock
        import random
        class CaptacionAnimada(Widget):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.size = (800, 500)
                with self.canvas.before:
                    Color(1, 1, 1, 1)
                    Rectangle(pos=self.pos, size=self.size)
                # Estado de gotas: lista de [x, y, velocidad, rebote]
                self.gotas = [[random.randint(270, 530), 340, random.uniform(2, 3.5), False] for _ in range(14)]
                self.nube_pos = (300, 340)
                self.nube_size = (200, 60)
                self.techo_pos = (260, 260)
                self.techo_size = (280, 40)
                self.tanque_pos = (370, 120)
                self.tanque_size = (60, 110)
                self.nivel = 0  # 0 a 1
                self.tiempo = 0
                with self.canvas:
                    # Nube (varias elipses)
                    Color(0.7, 0.7, 0.75, 1)
                    self.nube1 = Ellipse(pos=(self.nube_pos[0], self.nube_pos[1]), size=(80, 40))
                    self.nube2 = Ellipse(pos=(self.nube_pos[0]+40, self.nube_pos[1]+10), size=(80, 50))
                    self.nube3 = Ellipse(pos=(self.nube_pos[0]+100, self.nube_pos[1]), size=(60, 38))
                    # Techo (línea inclinada)
                    Color(0.7, 0.4, 0.2, 1)
                    self.techo = Line(points=[self.techo_pos[0], self.techo_pos[1], self.techo_pos[0]+self.techo_size[0], self.techo_pos[1]+self.techo_size[1]], width=10, cap='round')
                    # Tanque (rectángulo)
                    Color(0.2, 0.6, 0.8, 1)
                    self.tanque = Rectangle(pos=self.tanque_pos, size=self.tanque_size)
                    # Nivel de agua (rectángulo)
                    Color(0.1, 0.5, 1, 0.7)
                    self.agua = Rectangle(pos=(self.tanque_pos[0], self.tanque_pos[1]), size=(self.tanque_size[0], 0))
                    # Gotas (elipses)
                    self.gota_objs = []
                    for x, y, _, _ in self.gotas:
                        Color(0.2, 0.6, 0.9, 1)
                        self.gota_objs.append(Ellipse(pos=(x, y), size=(14, 26)))
                self._event = Clock.schedule_interval(self.animar, 1/60)
            def animar(self, dt):
                gotas_en_tanque = 0
                for i, (x, y, v, rebote) in enumerate(self.gotas):
                    # Rebote en techo
                    techo_y = self.techo_pos[1] + self.techo_size[1] * ((x-self.techo_pos[0])/self.techo_size[0])
                    if not rebote and y > techo_y:
                        y -= v
                        self.gota_objs[i].pos = (x, y)
                        self.gotas[i][1] = y
                    elif not rebote:
                        # Rebota: sube un poco y luego cae al tanque
                        self.gotas[i][3] = True
                        self.gotas[i][2] = v * 0.7
                        self.gotas[i][1] = techo_y - 10
                        self.gota_objs[i].pos = (x, techo_y - 10)
                    else:
                        # Baja directo al tanque
                        if y > self.tanque_pos[1]+self.tanque_size[1]:
                            y -= v*1.2
                            self.gota_objs[i].pos = (x, y)
                            self.gotas[i][1] = y
                        else:
                            gotas_en_tanque += 1
                            # Reiniciar gota arriba
                            self.gotas[i][1] = 340
                            self.gotas[i][3] = False
                            self.gota_objs[i].pos = (x, 340)
                # Llenar tanque según gotas que llegan
                self.nivel += gotas_en_tanque * 0.0025
                if self.nivel > 1:
                    self.nivel = 1
                # Actualizar nivel de agua
                self.agua.size = (self.tanque_size[0], self.tanque_size[1]*self.nivel)
                self.agua.pos = (self.tanque_pos[0], self.tanque_pos[1])
                self.tiempo += dt
                if self.tiempo > 12 or self.nivel >= 1:
                    if self._event:
                        self._event.cancel()
            def stop(self):
                if hasattr(self, '_event') and self._event:
                    self._event.cancel()
        # Popup con fondo blanco puro y botón cerrar
        content = CaptacionAnimada()
        popup = Popup(
            title="Animación – Práctica 5",
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
