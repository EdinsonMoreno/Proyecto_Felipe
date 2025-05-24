from kivy.uix.screenmanager import Screen
from backend.practica6_monitor import consolidar_datos, simular_condiciones_climaticas
from kivy.uix.popup import Popup
from matplotlib import pyplot as plt
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class Practica6MonitorScreen(Screen):
    def on_pre_enter(self):
        self.actualizar_datos()

    def actualizar_datos(self):
        datos = consolidar_datos()
        self.ids.lbl_energia.text = str(datos.get("energia_generada")) if datos.get("energia_generada") is not None else "Dato no disponible"
        self.ids.lbl_eficiencia.text = str(datos.get("eficiencia_panel")) if datos.get("eficiencia_panel") is not None else "Dato no disponible"
        self.ids.lbl_turbidez.text = str(datos.get("turbidez_final")) if datos.get("turbidez_final") is not None else "Dato no disponible"
        self.ids.lbl_tempfinal.text = str(datos.get("temperatura_final")) if datos.get("temperatura_final") is not None else "Dato no disponible"
        self.ids.lbl_nivel.text = str(datos.get("nivel_tanque")) if datos.get("nivel_tanque") is not None else "Dato no disponible"
        self.ids.lbl_alertas.text = "\n".join(datos.get("errores", []))

    def simular_clima(self):
        radiacion = float(self.ids.input_radiacion.text or 0)
        lluvia = float(self.ids.input_lluvia.text or 0)
        temperatura = float(self.ids.input_temperatura.text or 0)
        simular_condiciones_climaticas({
            "radiacion": radiacion,
            "lluvia": lluvia,
            "temperatura": temperatura
        })
        self.actualizar_datos()

    def mostrar_grafica_practica1(self):
        from matplotlib import pyplot as plt
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
        from kivy.uix.popup import Popup
        try:
            valor = float(self.ids.lbl_energia.text)
        except Exception:
            valor = 0
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        axs[0, 0].bar(['Valor'], [valor], color='#10ac84')
        axs[0, 0].set_title('Barra')
        axs[0, 1].plot([0, 1], [0, valor], color='#10ac84')
        axs[0, 1].set_title('Línea')
        axs[1, 0].scatter([1], [valor], color='#10ac84', s=100)
        axs[1, 0].set_title('Punto')
        axs[1, 1].pie([valor, max(1, 100-valor)], labels=['Generada', 'Resto'], autopct='%1.1f%%', colors=['#10ac84', '#dfe6e9'])
        axs[1, 1].set_title('Circular')
        fig.tight_layout()
        popup = Popup(title='Gráficas de Energía Generada',
                      content=FigureCanvasKivyAgg(fig),
                      size_hint=(None, None), size=(900, 600))
        popup.open()

    def mostrar_grafica_eficiencia(self):
        from matplotlib import pyplot as plt
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
        from kivy.uix.popup import Popup
        try:
            valor = float(self.ids.lbl_eficiencia.text)
        except Exception:
            valor = 0
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        axs[0, 0].bar(['Valor'], [valor], color='#2e86de')
        axs[0, 0].set_title('Barra')
        axs[0, 1].plot([0, 1], [0, valor], color='#2e86de')
        axs[0, 1].set_title('Línea')
        axs[1, 0].scatter([1], [valor], color='#2e86de', s=100)
        axs[1, 0].set_title('Punto')
        axs[1, 1].pie([valor, max(1, 100-valor)], labels=['Eficiencia', 'Resto'], autopct='%1.1f%%', colors=['#2e86de', '#dfe6e9'])
        axs[1, 1].set_title('Circular')
        fig.tight_layout()
        popup = Popup(title='Gráficas de Eficiencia Panel',
                      content=FigureCanvasKivyAgg(fig),
                      size_hint=(None, None), size=(900, 600))
        popup.open()

    def mostrar_grafica_practica2(self):
        from matplotlib import pyplot as plt
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
        from kivy.uix.popup import Popup
        try:
            valor = float(self.ids.lbl_turbidez.text)
        except Exception:
            valor = 0
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        axs[0, 0].bar(['Valor'], [valor], color='#ff7f50')
        axs[0, 0].set_title('Barra')
        axs[0, 1].plot([0, 1], [0, valor], color='#ff7f50')
        axs[0, 1].set_title('Línea')
        axs[1, 0].scatter([1], [valor], color='#ff7f50', s=100)
        axs[1, 0].set_title('Punto')
        axs[1, 1].pie([valor, max(1, 100-valor)], labels=['Turbidez', 'Resto'], autopct='%1.1f%%', colors=['#ff7f50', '#dfe6e9'])
        axs[1, 1].set_title('Circular')
        fig.tight_layout()
        popup = Popup(title='Gráficas de Turbidez Final',
                      content=FigureCanvasKivyAgg(fig),
                      size_hint=(None, None), size=(900, 600))
        popup.open()

    def mostrar_grafica_practica3(self):
        from matplotlib import pyplot as plt
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
        from kivy.uix.popup import Popup
        try:
            valor = float(self.ids.lbl_tempfinal.text)
        except Exception:
            valor = 0
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        axs[0, 0].bar(['Valor'], [valor], color='#ffa801')
        axs[0, 0].set_title('Barra')
        axs[0, 1].plot([0, 1], [0, valor], color='#ffa801')
        axs[0, 1].set_title('Línea')
        axs[1, 0].scatter([1], [valor], color='#ffa801', s=100)
        axs[1, 0].set_title('Punto')
        axs[1, 1].pie([valor, max(1, 100-valor)], labels=['Temperatura', 'Resto'], autopct='%1.1f%%', colors=['#ffa801', '#dfe6e9'])
        axs[1, 1].set_title('Circular')
        fig.tight_layout()
        popup = Popup(title='Gráficas de Temperatura Final',
                      content=FigureCanvasKivyAgg(fig),
                      size_hint=(None, None), size=(900, 600))
        popup.open()

    def mostrar_grafica_practica5(self):
        from matplotlib import pyplot as plt
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
        from kivy.uix.popup import Popup
        try:
            valor = float(self.ids.lbl_nivel.text)
        except Exception:
            valor = 0
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        axs[0, 0].bar(['Valor'], [valor], color='#48dbfb')
        axs[0, 0].set_title('Barra')
        axs[0, 1].plot([0, 1], [0, valor], color='#48dbfb')
        axs[0, 1].set_title('Línea')
        axs[1, 0].scatter([1], [valor], color='#48dbfb', s=100)
        axs[1, 0].set_title('Punto')
        axs[1, 1].pie([valor, max(1, 100-valor)], labels=['Nivel', 'Resto'], autopct='%1.1f%%', colors=['#48dbfb', '#dfe6e9'])
        axs[1, 1].set_title('Circular')
        fig.tight_layout()
        popup = Popup(title='Gráficas de Nivel Tanque',
                      content=FigureCanvasKivyAgg(fig),
                      size_hint=(None, None), size=(900, 600))
        popup.open()

    def mostrar_grafica_climatica(self):
        from matplotlib import pyplot as plt
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
        from kivy.uix.popup import Popup
        try:
            radiacion = float(self.ids.input_radiacion.text)
        except:
            radiacion = 0
        try:
            lluvia = float(self.ids.input_lluvia.text)
        except:
            lluvia = 0
        try:
            temperatura = float(self.ids.input_temperatura.text)
        except:
            temperatura = 0
        fig, ax = plt.subplots()
        categorias = ['Radiación', 'Lluvia', 'Temperatura']
        valores = [radiacion, lluvia, temperatura]
        colores = ['#1f77b4', '#2ca02c', '#ff7f0e']
        ax.bar(categorias, valores, color=colores)
        ax.set_ylabel("Valor")
        ax.set_title("Condiciones climáticas simuladas")
        popup = Popup(title="Gráfica de Condiciones Climáticas",
                      content=FigureCanvasKivyAgg(fig),
                      size_hint=(None, None), size=(600, 400))
        popup.open()
