import os

# Kivy core
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.clock import Clock

class Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="Pantalla Principal", font_size=20, pos_hint={"center_x": 0.5, "center_y": 0.5}))
        self.add_widget(layout)

        Clock.schedule_once(self.load_screen_2, 0)
        Clock.schedule_once(self.load_screen_3, 0)

        # Fondo animado
        current_dir = os.path.dirname(os.path.abspath(__file__))
        fondo_animado = Image(
            source=os.path.join(current_dir, '..', 'assets', 'v3', 'dribble_robot00ax4.gif'),
            anim_delay=0.05,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        layout.add_widget(fondo_animado)

        # Título
        label_titulo = Label(
            text="Modulación Analógica PYTHON",
            font_size=24,
            size_hint=(.6, .1),
            pos_hint={'center_x': .5, 'top': 1}
        )
        layout.add_widget(label_titulo)

        ############################################################################################################
        # Contenedor para el botón principal y los desplegables
        self.boton_container = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(700, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            spacing=10
        )

        # Botón principal
        self.boton_principal = Button(
            text="Escoger tipo de modulación",
            size_hint=(None, None),
            size=(250, 50)
        )
        self.boton_principal.bind(on_press=self.toggle_botones)
        self.boton_container.add_widget(self.boton_principal)

        # Botones adicionales
        self.boton_ssb = Button(
            text="SSB",
            size_hint=(None, None),
            size=(200, 50),
            opacity=0,
            disabled=True
        )
        self.boton_ssb.bind(on_press=self.ir_a_ssb)
        # Obtener el botón presionado
        # self.boton_ssb.bind(on_press=self.seleccionar_modo)
        self.boton_container.add_widget(self.boton_ssb)

        self.boton_isb = Button(
            text="ISB",
            size_hint=(None, None),
            size=(200, 50),
            opacity=0,
            disabled=True
        )
        self.boton_isb.bind(on_press=self.ir_a_isb)
        # Obtener el botón presionado
        # self.boton_isb.bind(on_press=self.seleccionar_modo)
        self.boton_container.add_widget(self.boton_isb)

        layout.add_widget(self.boton_container)

        btn_salir = Button(
            text='Salir',
            size_hint=(None, None),
            size=(75, 50),
            pos_hint={'x': 0.9, 'y': 0}
        )
        btn_salir.bind(on_press=self.salir)
        layout.add_widget(btn_salir)
        
    
        # self.add_widget(layout)
        ############################################################################################################
    def load_screen_2(self, dt):
        # self.status_label.text = "Cargando pantallas principales..."

        # from ui.screen1 import Screen1
        from ui.screen2 import Screen2

        sm = self.manager
        sm.add_widget(Screen2(name='pantalla2'))
    
    def load_screen_3(self, dt):
        # self.status_label.text = "Cargando pantallas principales..."

        # from ui.screen1 import Screen1
        from ui.screen3 import Screen3

        sm = self.manager
        sm.add_widget(Screen3(name='pantalla3'))

    # Función para mostrar o encontrar los botones
    def toggle_botones(self, instance):
        # Alternar visibilidad de los botones
        for btn in [self.boton_ssb, self.boton_isb]:
            if btn.opacity == 0:
                btn.opacity = 1
                btn.disabled = False
            else:
                btn.opacity = 0
                btn.disabled = True

    # Ir a pantalla2 - Modulación SSB
    def ir_a_ssb(self, instance):
        self.manager.current = 'pantalla2'
    
    # Ir a pantalla3 - Modulación ISB
    def ir_a_isb(self, instance):
        self.manager.current = 'pantalla3'
    
    # Salir del programa
    def salir(self, instance):
        App.get_running_app().stop()
    
    # def seleccionar_modo(self, instance):
    #     self.modo_seleccionado = instance.text
    #     print(f"Modo guardado: {self.modo_seleccionado}")