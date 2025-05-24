from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Importar las pantallas del frontend
from frontend.main_screen import MainScreen
from frontend.screens.practica1_screen import Practica1Screen
from frontend.screens.practica2_screen import Practica2Screen
from frontend.screens.practica3_screen import Practica3Screen
from frontend.screens.practica4_screen import Practica4Screen
from frontend.screens.practica5_screen import Practica5Screen
from frontend.screens.practica6_monitor_screen import Practica6MonitorScreen

# Cargar los archivos .kv
Builder.load_file('kv/main.kv')
Builder.load_file('kv/practica1.kv')
Builder.load_file('kv/practica2.kv')
Builder.load_file('kv/practica3.kv')
Builder.load_file('kv/practica4.kv')
Builder.load_file('kv/practica5.kv')
Builder.load_file('kv/practica6.kv')

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        sm = RootWidget()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(Practica1Screen(name='practica1'))
        sm.add_widget(Practica2Screen(name='practica2'))
        sm.add_widget(Practica3Screen(name='practica3'))
        sm.add_widget(Practica4Screen(name='practica4'))
        sm.add_widget(Practica5Screen(name='practica5'))
        sm.add_widget(Practica6MonitorScreen(name='practica6_monitor'))
        return sm

# Punto de entrada de la app
if __name__ == "__main__":
    MainApp().run()
