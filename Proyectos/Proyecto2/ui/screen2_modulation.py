import os  # Para manejo de rutas y directorios

# Kivy core
from kivy.app import App  # Para manejar la aplicación y cerrar con stop()
from kivy.uix.screenmanager import Screen  # Para heredar la pantalla
from kivy.uix.label import Label  # Para mostrar texto
from kivy.uix.button import Button  # Para crear botones
from kivy.uix.image import Image  # Para mostrar imágenes (y GIFs animados)
from kivy.uix.floatlayout import FloatLayout  # Para el layout base que usas

class Screen2_modulation(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="Calculando Modulación", font_size=20, pos_hint={"center_x": 0.5, "center_y": 0.5}))
        self.add_widget(layout)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        fondo_animado = Image(
            source=os.path.join(current_dir, '..', 'assets', 'v3', 'dribble_robotWork.gif'),  # Ajuste para usar ../assets', 'v3'fondo_animado.gif',  # debe ser un GIF válido
            anim_delay=0.05,  # velocidad de animación
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(fondo_animado)

        ########################### Título
        # label_titulo = Label(
        #     text="Calculando Modulación - Espere un momento",
        #     font_size=24,
        #     size_hint=(.6, .1),
        #     pos_hint={'center_x': .5, 'top': 1}
        # )
        # layout.add_widget(label_titulo)
        titulo_boton = Button(
            text="Calculando Modulación - Espere un momento",
            font_size=24,
            size_hint=(.7, .1),
            pos_hint={'center_x': .5, 'top': 1},
            # background_normal='',  # Esto asegura que el fondo se muestre
            # background_color=(0.26, 0.52, 0.96, 1),  # Color típico de botón
            disabled=False  # Desactiva la funcionalidad
        )
        layout.add_widget(titulo_boton)

        ############################################################################################################
        ########################### Botón - Regresar a pantalla 1
        btn_regresar = Button(
            text='Regresar a Pantalla 1', 
            size_hint=(None, None), 
            size=(200, 50),
            pos_hint={'x': 0.60, 'y': .0}
        )
        btn_regresar.bind(on_press=self.regresar_a_pantalla1)
        layout.add_widget(btn_regresar)

        ########################### Botón - Salir
        btn_salir = Button(
            text='Salir',
            size_hint=(None, None),
            size=(75, 50),
            pos_hint={'x': 0.85, 'y': 0}
        )
        btn_salir.bind(on_press=self.salir)
        layout.add_widget(btn_salir)
        ############################################################################################################
    
    ########################### Función Regresar a pantalla 1
    def regresar_a_pantalla1(self, instance):
        # Regresar a la primera pantalla
        self.manager.current = 'pantalla1'

    ########################### Función Salir
    def salir(self, instance):
        App.get_running_app().stop()