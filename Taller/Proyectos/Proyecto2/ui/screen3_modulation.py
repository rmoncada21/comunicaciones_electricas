import os  # Para manejo de rutas y directorios
import subprocess
import sys
import numpy as np
import sounddevice as sd
# Kivy core
from kivy.app import App  # Para manejar la aplicación y cerrar con stop()
from kivy.uix.screenmanager import Screen  # Para heredar la pantalla
from kivy.uix.label import Label  # Para mostrar texto
from kivy.uix.button import Button  # Para crear botones
from kivy.uix.image import Image  # Para mostrar imágenes (y GIFs animados)
from kivy.uix.floatlayout import FloatLayout  # Para el layout base que usas


class Screen3_modulation(Screen):
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
            keep_ratio=False
        )
        layout.add_widget(fondo_animado)

        ########################### Título
        titulo_boton = Button(
            text="Calculando Modulación - Espere un momento",
            font_size=24,
            size_hint=(.7, .1),
            pos_hint={'center_x': .5, 'top': 1},
            disabled=False  # Desactiva la funcionalidad
        )
        layout.add_widget(titulo_boton)

        ############################################################################################################

        btn_reproducir_mensaje = Button(
            text='Reproducir Mensaje',
            size_hint=(None, None),
            size=(215, 50),
            pos_hint={'center_x': .15, 'center_y': .84}
        )
        btn_reproducir_mensaje.bind(on_press=self.reproducir_mensaje)
        layout.add_widget(btn_reproducir_mensaje)

        # Reproducir modulacion ssb
        btn_reproducir_modulacion = Button(
            text='Rep. Mensaje modulado ISB',
            size_hint=(None, None),
            size=(215, 50),
            pos_hint={'center_x': .15, 'center_y': .72}
        )
        btn_reproducir_modulacion.bind(on_press=self.reproducir_modulacion)
        layout.add_widget(btn_reproducir_modulacion)

        # Reproducir demodulacion ssb
        btn_reproducir_demodulacion = Button(
            text='Rep. Mensaje demod 1 ISB',
            size_hint=(None, None),
            size=(215, 50),
            pos_hint={'center_x': .15, 'center_y': .60}
        )
        btn_reproducir_demodulacion.bind(on_press=self.reproducir_demodulacion)
        layout.add_widget(btn_reproducir_demodulacion)

        # Reproducir demodulacion ssb
        btn_reproducir_demodulacion = Button(
            text='Rep. Mensaje demod 2 ISB',
            size_hint=(None, None),
            size=(215, 50),
            pos_hint={'center_x': .15, 'center_y': .48}
        )
        btn_reproducir_demodulacion.bind(on_press=self.reproducir_demodulacion2)
        layout.add_widget(btn_reproducir_demodulacion)

        # TODO: Todos los Graficos o por separado
        btn_mostrar_graficos = Button(
            text='Mostrar Gráficos',
            size_hint=(None, None),
            size=(215, 50),
            pos_hint={'center_x': .15, 'center_y': .36}
        )
        btn_mostrar_graficos.bind(on_press=self.mostrar_graficos)
        layout.add_widget(btn_mostrar_graficos)
        
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
    
    # TODO: botones para reproducir sonidos
    ########################### Función Reproducir mensaje
    def reproducir_mensaje(self, instance):
        signal_data = np.load("output/isb_mensaje_data1.npy")
        signal_samplerate = np.load("output/isb_mensaje_samplerate.npy").item()
        sd.play(signal_data, signal_samplerate)
        pass

    def reproducir_modulacion(self, instance):
        signal_data = np.load("output/isb_modulada.npy")
        signal_samplerate = np.load("output/isb_mensaje_samplerate.npy").item()
        sd.play(signal_data, signal_samplerate)
        pass

    def reproducir_demodulacion(self, instance):
        signal_data = np.load("output/isb_demodulada1.npy")
        signal_samplerate = np.load("output/isb_mensaje_samplerate.npy").item()
        sd.play(signal_data, signal_samplerate)
        pass

    def reproducir_demodulacion2(self, instance):
        signal_data = np.load("output/isb_demodulada2.npy")
        signal_samplerate = np.load("output/isb_mensaje_samplerate.npy").item()
        sd.play(signal_data, signal_samplerate)
        pass
    
    # def mostrar_graficos(self, instance):
    #     print(f"Longitud de data {len(self.manager.audio_data)}")
    #     print(f"SSB tipo SC or FC: {self.manager.ssb_tipo}")
    #     print(f"Banda lateral: {self.manager.banda_lateral}")
    #     print(f"Frecuencia portadora: {self.manager.frecuencia_carrier}")
    #     print(f"Error fase: {self.manager.valor_error_fase}")
    #     print(f"Error frecuencia: {self.manager.valor_error_freq}")
    #     print(f"Ruta de archivo: {self.manager.pwd_archivo}")
    #     print(f'Numero de canales: {self.manager.audio_n_canales}') # Mono (1) o estéreo (2)
    #     print(f'Frecuencia de muestreo: {self.manager.audio_samplerate}')

    #     if self.manager.audio_filename == "tono.wav":
    #         plot_time = 0.05
    #     else:
    #         plot_time = self.manager.audio_duration

    #     subprocess.Popen([
    #                 sys.executable, "src/signal_plot.py",
    #                 "output/ssb_mensaje_data.npy",
    #                 str(self.manager.audio_samplerate),
    #                 "ambos",  # espectro, "senal", o "ambos"
    #                 # "0.05",
    #                 str(plot_time),
    #                 f"de información {str(self.manager.audio_filename)}" #titulo
    #             ])
        
    #     subprocess.Popen([
    #                 sys.executable, "src/signal_plot.py",
    #                 "output/ssb_banda_lateral_mod.npy",
    #                 str(self.manager.audio_samplerate),
    #                 "ambos",  # espectro, "senal", o "ambos"
    #                 # "0.05",
    #                 str(plot_time),
    #                 f"MODULADA SSB {str(self.manager.ssb_tipo)} {str(self.manager.banda_lateral)} {str(self.manager.audio_filename)}" #titulo
    #             ])
        
    #     subprocess.Popen([
    #                 sys.executable, "src/signal_plot.py",
    #                 "output/ssb_banda_lateral_demod.npy",
    #                 str(self.manager.audio_samplerate),
    #                 "ambos",  # espectro, "senal", o "ambos"
    #                 # "0.05",
    #                 str(plot_time),
    #                 f"DEMODULADA SSB {str(self.manager.ssb_tipo)} {str(self.manager.banda_lateral)} {str(self.manager.audio_filename)}" #titulo
    #             ])
    def mostrar_graficos(self, instance):
        print(f"Archivo 1: {self.manager.audio_filename_1}")
        print(f"Archivo 2: {self.manager.audio_filename_2}")
        print(f"Frecuencia portadora: {self.manager.frecuencia_carrier}")
        print(f'Canales archivo 1: {self.manager.audio_n_canales_1}')
        print(f'Canales archivo 2: {self.manager.audio_n_canales_2}')
        print(f'Frecuencia de muestreo (común): {self.manager.audio_samplerate_1}')
    
        # Asumimos que la duración de la señal más larga es la que se grafica
        plot_time = max(self.manager.audio_duration_1, self.manager.audio_duration_2)
    
        #### Señal de información 1
        subprocess.Popen([
            sys.executable, "src/signal_plot.py",
            "output/isb_mensaje_data1.npy",
            str(self.manager.audio_samplerate_1),
            "senal",
            str(plot_time),
            f"Señal de información 1: {self.manager.audio_filename_1}"
        ])
    
        #### Señal de información 2
        subprocess.Popen([
            sys.executable, "src/signal_plot.py",
            "output/isb_mensaje_data2.npy",
            str(self.manager.audio_samplerate_2),
            "senal",
            str(plot_time),
            f"Señal de información 2: {self.manager.audio_filename_2}"
        ])
    
        #### Señal modulada ISB
        subprocess.Popen([
            sys.executable, "src/signal_plot.py",
            "output/isb_modulada.npy",
            str(self.manager.audio_samplerate_1),
            "ambos",
            str(plot_time),
            "Señal ISB Modulada"
        ])
    
        #### Señal demodulada 1
        subprocess.Popen([
            sys.executable, "src/signal_plot.py",
            "output/isb_demodulada1.npy",
            str(self.manager.audio_samplerate_1),
            "ambos",
            str(plot_time),
            "Señal ISB Demodulada 1"
        ])

        #### Señal demodulada 2
        subprocess.Popen([
            sys.executable, "src/signal_plot.py",
            "output/isb_demodulada2.npy",
            str(self.manager.audio_samplerate_2),
            "ambos",
            str(plot_time),
            "Señal ISB Demodulada 2"
        ])


        # pass
    ########################### Función Regresar a pantalla 1
    def regresar_a_pantalla1(self, instance):
        # Regresar a la primera pantalla
        # print(f"Mensaje interpantalla {self.manager.ssb_tipo}")
        self.manager.current = 'pantalla1'

    ########################### Función Salir
    def salir(self, instance):
        App.get_running_app().stop()