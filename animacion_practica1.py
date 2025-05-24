from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty

class AnimacionEnergiaWidget(Widget):
    carga_bateria = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tiempo = 0
        Clock.schedule_interval(self.animar, 0.1)

    def animar(self, dt):
        if self.carga_bateria < 80:
            self.carga_bateria += 4
        else:
            Clock.unschedule(self.animar)

class PruebaApp(App):
    def build(self):
        Builder.load_file("animacion_practica1.kv")
        return AnchorLayout(anchor_x='center', anchor_y='center', children=[AnimacionEnergiaWidget()])

    def abrir_animacion(self):
        popup = Popup(
            title="Animación – Energía Solar (Práctica 1)",
            content=AnchorLayout(anchor_x='center', anchor_y='center', children=[AnimacionEnergiaWidget()]),
            size_hint=(None, None), size=(800, 500),
            separator_color=(0.1, 0.1, 0.1, 1),
            title_color=(0, 0, 0, 1),
        )
        popup.open()

if __name__ == "__main__":
    PruebaApp().run()
