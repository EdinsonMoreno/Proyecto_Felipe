from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from backend import practica1_balance_energetico as be
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import matplotlib.pyplot as plt
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import subprocess
import os
import sys

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
                eficiencia_panel = float(self.ids.input_eficiencia.text)  # %
                consumo = float(self.ids.input_consumo.text)
                perdidas = float(self.ids.input_perdidas.text)  # %
            except ValueError:
                self.mostrar_error("Todos los valores deben ser numéricos y válidos.")
                return
            if radiacion <= 0 or area <= 0 or eficiencia_panel <= 0 or consumo < 0 or perdidas < 0:
                self.mostrar_error("Todos los valores deben ser mayores a cero (excepto consumo y pérdidas, que pueden ser cero).")
                return
            # Llamar backend con los parámetros físicos correctos
            resultado = be.calcular_resultados(
                radiacion=radiacion,
                area=area,
                eficiencia_panel=eficiencia_panel,
                horas_sol_pico=5,  # valor típico, o permitir input si se desea
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

    def graficar_animacion(self):
        # Mostrar solo las gráficas de Matplotlib, no la animación
        import matplotlib.pyplot as plt
        from kivy_garden.matplotlib import FigureCanvasKivyAgg
        from kivy.uix.popup import Popup
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
                      size_hint=(None, None), size=(900, 600),
                      background_color=(1, 1, 1, 1))
        popup.open()

    def mostrar_animacion(self):
        # Detectar si estamos en un ejecutable PyInstaller
        if getattr(sys, 'frozen', False):
            exe_path = os.path.join(os.path.dirname(sys.executable), 'animacion_practica1_pygame.exe')
            if os.path.exists(exe_path):
                os.startfile(exe_path)
            else:
                from kivy.uix.popup import Popup
                from kivy.uix.label import Label
                Popup(title='Error', content=Label(text='No se encontró animacion_practica1_pygame.exe'), size_hint=(None, None), size=(400, 200)).open()
        else:
            # Ejecutar la animación sin mostrar la consola en Windows
            if sys.platform == 'win32':
                CREATE_NO_WINDOW = 0x08000000
                subprocess.Popen([sys.executable, 'animacion_practica1_pygame.py'], creationflags=CREATE_NO_WINDOW)
            else:
                subprocess.Popen([sys.executable, 'animacion_practica1_pygame.py'])
