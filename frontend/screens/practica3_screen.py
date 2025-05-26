# Pantalla práctica 3

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from backend import practica3_intercambiador_calor as intercambiador
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import matplotlib.pyplot as plt
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import subprocess
import os
import sys

class Practica3Screen(Screen):
    temperatura_inicial = StringProperty("")
    temperatura_final = StringProperty("")
    tiempo_exposicion = StringProperty("")
    eficiencia_termica = StringProperty("")
    mensaje_error = StringProperty("")
    grafico_valores = ListProperty([])

    def mostrar_error(self, mensaje):
        self.mensaje_error = mensaje
        popup = Popup(title='Error',
                      content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def simular_intercambio(self):
        try:
            try:
                tcaliente = float(self.ids.input_tcaliente.text)
                caudal_caliente = float(self.ids.input_caudal_caliente.text)  # L/min
                tfrio = float(self.ids.input_tfrio.text)
                caudal_frio = float(self.ids.input_caudal_frio.text)  # L/min
                tiempo = float(self.ids.input_tiempo.text)  # min
            except ValueError:
                self.mostrar_error("Todos los valores deben ser numéricos y válidos.")
                return
            if tcaliente < 0 or caudal_caliente <= 0 or tfrio < 0 or caudal_frio <= 0 or tiempo <= 0:
                self.mostrar_error("Todos los valores deben ser mayores a cero (excepto temperaturas, que pueden ser >= 0).")
                return
            # Calcular masa de agua calentada (kg)
            masa_agua = caudal_frio * tiempo  # L/min * min = L ≈ kg (fluido frío)
            # Potencia solar estimada: Q = m*c*ΔT/t, c=4186 J/kgK, ΔT = tcaliente-tfrio, t=tiempo*60s
            delta_T = tcaliente - tfrio
            energia_absorbida = masa_agua * 4186 * delta_T  # J
            energia_suministrada = energia_absorbida / 0.7 if delta_T > 0 else 1  # Supón eficiencia realista < 1
            potencia_solar = energia_suministrada / (tiempo * 60) if tiempo > 0 else 1
            resultado = intercambiador.calcular_resultados(
                temperatura_inicial=tfrio,
                masa_agua=masa_agua,
                potencia_solar=potencia_solar,
                tiempo_exposicion=tiempo,
                tcaliente=tcaliente,
                caudal_caliente=caudal_caliente,
                caudal_frio=caudal_frio
            )
            if resultado.get("status") == "ok":
                datos = resultado.get("data", {})
                self.temperatura_inicial = f"{datos.get('temperatura_inicial', 0):.1f} °C"
                self.temperatura_final = f"{datos.get('temperatura_final', 0):.1f} °C"
                self.tiempo_exposicion = f"{datos.get('tiempo_exposicion', 0):.1f} min"
                self.eficiencia_termica = f"{datos.get('eficiencia_termica', 0):.1f} %"
                self.mensaje_error = ""
                # Guardar valor para graficar (temperatura final)
                valor_actual = datos.get('temperatura_final', 0)
                self.grafico_valores.append(valor_actual)
                if len(self.grafico_valores) > 4:
                    self.grafico_valores.pop(0)
            else:
                self.temperatura_inicial = ""
                self.temperatura_final = ""
                self.tiempo_exposicion = ""
                self.eficiencia_termica = ""
                self.mostrar_error(resultado.get("message", "Error en la simulación"))
        except Exception:
            self.temperatura_inicial = ""
            self.temperatura_final = ""
            self.tiempo_exposicion = ""
            self.eficiencia_termica = ""
            self.mostrar_error("Datos inválidos")
    def graficar_resultados(self):
        import matplotlib.pyplot as plt
        from kivy_garden.matplotlib import FigureCanvasKivyAgg
        plt.style.use("seaborn-v0_8-muted")
        valores = self.grafico_valores or [0]
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        # Barra
        axs[0, 0].bar(range(len(valores)), valores, color="#2e86de")
        axs[0, 0].set_title('Temperatura final (Barra)')
        axs[0, 0].set_xlabel('Simulación')
        axs[0, 0].set_ylabel('°C')
        axs[0, 0].grid(True)
        # Línea
        axs[0, 1].plot(valores, color="#10ac84", marker='o', label="Temperatura final")
        axs[0, 1].set_title('Temperatura final (Línea)')
        axs[0, 1].set_xlabel('Simulación')
        axs[0, 1].set_ylabel('°C')
        axs[0, 1].grid(True)
        axs[0, 1].legend(loc='upper right')
        # Puntos
        axs[1, 0].scatter(range(len(valores)), valores, color="#ff9f43", label="Temperatura final")
        axs[1, 0].set_title('Temperatura final (Puntos)')
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
        self.ids.input_tcaliente.text = ""
        self.ids.input_caudal_caliente.text = ""
        self.ids.input_tfrio.text = ""
        self.ids.input_caudal_frio.text = ""
        self.ids.input_tiempo.text = ""
        self.temperatura_inicial = ""
        self.temperatura_final = ""
        self.tiempo_exposicion = ""
        self.eficiencia_termica = ""
        self.mensaje_error = ""
    def mostrar_animacion(self):
        # Detectar si estamos en un ejecutable PyInstaller
        if getattr(sys, 'frozen', False):
            exe_path = os.path.join(os.path.dirname(sys.executable), 'animacion_practica3_pygame.exe')
            if os.path.exists(exe_path):
                os.startfile(exe_path)
            else:
                from kivy.uix.popup import Popup
                from kivy.uix.label import Label
                Popup(title='Error', content=Label(text='No se encontró animacion_practica3_pygame.exe'), size_hint=(None, None), size=(400, 200)).open()
        else:
            # Ejecutar la animación sin mostrar la consola en Windows
            if sys.platform == 'win32':
                CREATE_NO_WINDOW = 0x08000000
                subprocess.Popen([sys.executable, 'animacion_practica3_pygame.py'], creationflags=CREATE_NO_WINDOW)
            else:
                subprocess.Popen([sys.executable, 'animacion_practica3_pygame.py'])
