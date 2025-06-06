from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from backend import practica5_captacion_lluvia as captacion
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import matplotlib.pyplot as plt
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import subprocess

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
                duracion = float(self.ids.input_tiempo.text)
            except (ValueError, AttributeError):
                self.mostrar_error("Todos los valores deben ser numéricos y válidos.")
                return
            if intensidad_lluvia <= 0 or area_techo <= 0 or duracion <= 0:
                self.mostrar_error("Todos los valores deben ser mayores a cero.")
                return
            datos = captacion.calcular_resultados(
                intensidad_lluvia=intensidad_lluvia,
                area_techo=area_techo,
                duracion=duracion
            )
            if datos.get("status") == "ok":
                d = datos.get("data", {})
                self.volumen_captado = f"{d.get('volumen_captado', 0):.2f} L"
                self.nivel_sensor = f"{d.get('nivel_tanque', 0):.1f} cm"
                self.volumen_estimado = f"{d.get('volumen_estimado_sensor', 0):.2f} L"
                self.precision = f"{d.get('precision_sensor', 0):.1f} %"
                self.tiempo_captacion = f"{d.get('tiempo_captacion', 0):.1f} min"
                self.mensaje_error = ""
                valor_actual = d.get('nivel_tanque', 0)
                self.grafico_valores.append(valor_actual)
                if len(self.grafico_valores) > 4:
                    self.grafico_valores.pop(0)
            else:
                self.volumen_captado = ""
                self.nivel_sensor = ""
                self.volumen_estimado = ""
                self.precision = ""
                self.tiempo_captacion = ""
                self.mostrar_error(datos.get("message", "Error en la simulación"))
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
        axs[0, 0].set_title('Nivel del tanque (Barra)')
        axs[0, 0].set_xlabel('Simulación')
        axs[0, 0].set_ylabel('cm')
        axs[0, 0].grid(True)
        # Línea
        axs[0, 1].plot(valores, color="#10ac84", marker='o', label="Nivel del tanque")
        axs[0, 1].set_title('Nivel del tanque (Línea)')
        axs[0, 1].set_xlabel('Simulación')
        axs[0, 1].set_ylabel('cm')
        axs[0, 1].grid(True)
        axs[0, 1].legend(loc='upper right')
        # Puntos
        axs[1, 0].scatter(range(len(valores)), valores, color="#ff9f43", label="Nivel del tanque")
        axs[1, 0].set_title('Nivel del tanque (Puntos)')
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
        import os, sys, subprocess
        if getattr(sys, 'frozen', False):
            exe_path = os.path.join(os.path.dirname(sys.executable), 'animacion_practica5_pygame.exe')
            if os.path.exists(exe_path):
                os.startfile(exe_path)
            else:
                from kivy.uix.popup import Popup
                from kivy.uix.label import Label
                Popup(title='Error', content=Label(text='No se encontró animacion_practica5_pygame.exe'), size_hint=(None, None), size=(400, 200)).open()
        else:
            if sys.platform == 'win32':
                CREATE_NO_WINDOW = 0x08000000
                subprocess.Popen([sys.executable, 'animacion_practica5_pygame.py'], creationflags=CREATE_NO_WINDOW)
            else:
                subprocess.Popen([sys.executable, 'animacion_practica5_pygame.py'])
