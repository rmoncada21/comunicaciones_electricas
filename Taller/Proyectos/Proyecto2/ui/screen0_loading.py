import os
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image

class Screen0_loading(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # self.status_label = Label(text="Cargando...", font_size=20, pos_hint={"center_x": 0.5, "y": 0.1})
        # layout.add_widget(self.status_label)

        current_dir = os.path.dirname(__file__)
        fondo_animado = Image(
            source=os.path.join(current_dir, '..', 'assets', 'v3', 'dribble_robot0.gif'),
            anim_delay=0.05,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        layout.add_widget(fondo_animado)

        self.add_widget(layout)

        # Carga diferida mínima
        # Clock.schedule_once(self.load_screen_1n2, 7.0)
        Clock.schedule_once(self.load_screen_1, 6)
        # Clock.schedule_once(self.load_others_screen, 4.0)
        Clock.schedule_once(self.change_to_next, 16.0)

    def load_screen_1(self, dt):
        # self.status_label.text = "Cargando pantallas principales..."
        start_time = time.time()

        from ui.screen1 import Screen1
        # from ui.screen2 import Screen2
        
        sm = self.manager
        sm.add_widget(Screen1(name='pantalla1'))
        # sm.add_widget(Screen2(name='pantalla2'))

        print(f"[INFO] Pantallas 1 en {time.time() - start_time:.2f} s")

    def change_to_next(self, dt):
        self.manager.current = 'pantalla1'
