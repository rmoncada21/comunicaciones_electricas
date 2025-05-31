# import numpy as np
# import matplotlib.pyplot as plt
import os
import sys
import subprocess
import wave
import contextlib
import sounddevice as sd
from scipy.io import wavfile

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen


class Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="Pantalla Principal", font_size=20, pos_hint={"center_x": 0.5, "center_y": 0.5}))
        self.add_widget(layout)

        # Fondo animado
        current_dir = os.path.dirname(os.path.abspath(__file__))
        fondo_animado = Image(
            source=os.path.join(current_dir, '..', 'assets', 'giphy_plasma1.gif'),
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

    
class Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="Pantalla de Modulación SSB", font_size=20, pos_hint={"center_x": 0.5, "center_y": 0.5}))
        self.add_widget(layout)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        fondo_animado = Image(
            source=os.path.join(current_dir, '..', 'assets', 'giphy_signal1.gif'),  # Ajuste para usar ../assets'fondo_animado.gif',  # debe ser un GIF válido
            anim_delay=0.05,  # velocidad de animación
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(fondo_animado)

        ########################### Título
        label_titulo = Label(
            text="Modulación SSB (USB - LSB)",
            font_size=24,
            size_hint=(.6, .1),
            pos_hint={'center_x': .5, 'top': 1}
        )
        layout.add_widget(label_titulo)
        ############################################################################################################
        ########################### Botón regresar a pantalla 1
        # btn_regresar = Button(
        #     text='Regresar a Pantalla 1', 
        #     size_hint=(None, None), 
        #     size=(200, 50),
        #     pos_hint={'center_x': .15, 'center_y': .90}
        # )
        # btn_regresar.bind(on_press=self.regresar_a_pantalla1)
        # layout.add_widget(btn_regresar)

        ########################### Botón - Regresar a pantalla 1
        btn_regresar = Button(
            text='Regresar a Pantalla 1', 
            size_hint=(None, None), 
            size=(200, 50),
            pos_hint={'x': 0.60, 'y': .0}
        )
        btn_regresar.bind(on_press=self.regresar_a_pantalla1)
        layout.add_widget(btn_regresar)

        ########################### Botón Cargar WAV
        btn_cargar_audio = Button(
            text='Cargar Archivo WAV',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': .78}
        )
        btn_cargar_audio.bind(on_press=self.cargar_audio)
        layout.add_widget(btn_cargar_audio)

        ####################################################### CHECKPOINT
        # Escoger banda a transmitir
        # btn_tipo_modulacion = Button(
        #     text='Escoger USB o LSB',
        #     size_hint=(None, None),
        #     size=(200, 50),
        #     pos_hint={'center_x': .15, 'center_y': .48}
        # )
        # btn_tipo_modulacion.bind(on_press=self.get_tipo_mod)
        # layout.add_widget(btn_tipo_modulacion)
        
        ########################### Boton container
        self.boton_container = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': 0.60},
            spacing=10
        )

        ########################### Botón principal - Escoger modulación
        self.boton_principal = Button(
            text="Escoger tipo de modulación",
            size_hint=(None, None),
            size=(250, 50)
        )
        self.boton_principal.bind(on_press=self.toggle_botones)
        self.boton_container.add_widget(self.boton_principal)

        ########################### Botones USB escondido
        self.boton_usb = Button(
            text="USB",
            size_hint=(None, None),
            size=(200, 50),
            opacity=0,
            disabled=True
        )
        # self.boton_usb.bind(on_press=self.get_tipo_mod)
        # Obtener el botón presionado
        self.boton_usb.bind(on_press=self.seleccionar_modo)
        self.boton_container.add_widget(self.boton_usb)

        ########################### Botones LSB escondido
        self.boton_lsb = Button(
            text="LSB",
            size_hint=(None, None),
            size=(200, 50),
            opacity=0,
            disabled=True
        )
        # self.boton_lsb.bind(on_press=self.get_tipo_mod)
        # Obtener el botón presionado
        self.boton_lsb.bind(on_press=self.seleccionar_modo)
        self.boton_container.add_widget(self.boton_lsb)

        layout.add_widget(self.boton_container)

        ####################################################### CHECKPOINT

        ########################### Botón - Set frecuencia portadora
        btn_set_carrier = Button(
            text='Set frecuencia portadora',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': .48}
        )
        btn_set_carrier.bind(on_press=self.set_carrier_freq)
        layout.add_widget(btn_set_carrier)

        ########################### Botón - Set error fase
        btn_set_phase_error = Button(
            text='Set error de fase',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': .36}
        )
        btn_set_phase_error.bind(on_press=self.set_phase_error)
        layout.add_widget(btn_set_phase_error)

        ########################### Botón - Set error frecuencia
        btn_set_freq_error = Button(
            text='Set error de frecuencia',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': .24}
        )
        btn_set_freq_error.bind(on_press=self.set_freq_error)
        layout.add_widget(btn_set_freq_error)

        ########################### Botón - Iniciar modulación
        btn_init_mod = Button(
            text='Iniciar mod',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': .12}
        )
        btn_init_mod.bind(on_press=self.init_mod)
        btn_init_mod.bind(on_press=self.ir_a_mod)
        # btn_init_mod.bind(on_press=self.ir_pantalla4)
        layout.add_widget(btn_init_mod)

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
    def ir_a_mod(self, instance):
        self.manager.current = 'pantalla3_modulacion'

    ########################### Función Regresar a pantalla 1
    def regresar_a_pantalla1(self, instance):
        # Regresar a la primera pantalla
        self.manager.current = 'pantalla1'
    
    ########################### Función Salir
    def salir(self, instance):
        App.get_running_app().stop()

    # def get_tipo_mod(self, instance):
    #     return 'TODO'
    
    ########################### Función Seleccionar modo
    def seleccionar_modo(self, instance):
        self.modo_seleccionado = instance.text
        print(f"Modo guardado: {self.modo_seleccionado}")

    ########################### Función Mostrar / esconder botones USB - LSB
    def toggle_botones(self, instance):
        # Alternar visibilidad de los botones
        for btn in [self.boton_usb, self.boton_lsb]:
            if btn.opacity == 0:
                btn.opacity = 1
                btn.disabled = False
            else:
                btn.opacity = 0
                btn.disabled = True

    ########################### Función Set frecuencia portadora
    def set_carrier_freq(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text='Ingrese frecuencia de modulación (Hz):')
        layout.add_widget(label)

        self.input_freq_mod = TextInput(
            multiline=False,
            input_filter='float',
            hint_text='Ej: 1000.0'
        )
        layout.add_widget(self.input_freq_mod)

        btn_confirmar = Button(text='Confirmar', size_hint=(1, 0.3))
        layout.add_widget(btn_confirmar)

        self.popup_freq_mod = Popup(
            title='Frecuencia de Modulación',
            content=layout,
            size_hint=(None, None),
            size=(400, 250)
        )

        def confirmar_freq_mod(instance):
            try:
                frecuencia = float(self.input_freq_mod.text)
                self.popup_freq_mod.dismiss()
                popup_result = Popup(
                    title='Frecuencia Registrada',
                    content=Label(text=f'Frecuencia de modulación ingresada: {frecuencia} Hz'),
                    size_hint=(None, None),
                    size=(400, 200)
                )
                popup_result.open()

                ############################# ###########################
                # Guardar el valor o exportarlo a otra función
                self.frecuencia_modulacion = frecuencia
                # self.get_carrier(frecuencia)
                # print(f"Frecuncia desde kivy: {self.frecuencia_modulacion}");
                ############################# ###########################3

            except ValueError:
                popup_error = Popup(
                    title='Entrada inválida',
                    content=Label(text='Por favor, ingrese un número válido.'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_error.open()

        btn_confirmar.bind(on_press=confirmar_freq_mod)
        self.popup_freq_mod.open()    

    ########################### Función Set error de fase
    def set_phase_error(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text='Ingrese error de fase (en grados):')
        layout.add_widget(label)

        self.input_fase = TextInput(
            multiline=False,
            input_filter='float',
            hint_text='Ej: 45.0'
        )
        layout.add_widget(self.input_fase)

        btn_confirmar = Button(text='Confirmar', size_hint=(1, 0.3))
        layout.add_widget(btn_confirmar)

        self.popup_fase = Popup(
            title='Error de Fase',
            content=layout,
            size_hint=(None, None),
            size=(400, 250)
        )

        def confirmar_error(instance):
            try:
                error = float(self.input_fase.text)
                self.popup_fase.dismiss()
                popup_result = Popup(
                    title='Fase Registrada',
                    content=Label(text=f'Error de fase ingresado: {error} grados'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_result.open()
                
                ############################# ###########################
                # Guardar el valor o llamarlo desde otra función
                self.valor_error_fase = error
                # print(f"Error valor fase: {self.valor_error_fase}")
                # self.aplicar_error_fase(error)
                # print(f"Aplicar valor fase: {self.aplicar_valor_error_fase}")
                ############################# ###########################

            except ValueError:
                popup_error = Popup(
                    title='Entrada inválida',
                    content=Label(text='Por favor, ingrese un número válido.'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_error.open()

        btn_confirmar.bind(on_press=confirmar_error)
        self.popup_fase.open()
    
    ########################### Función Set error de frecuencia
    def set_freq_error(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text='Ingrese error de frecuencia (en Hertz/radianes):')
        layout.add_widget(label)

        self.input_fase = TextInput(
            multiline=False,
            input_filter='float',
            hint_text='Ej: 45.0'
        )
        layout.add_widget(self.input_fase)

        btn_confirmar = Button(text='Confirmar', size_hint=(1, 0.3))
        layout.add_widget(btn_confirmar)

        self.popup_fase = Popup(
            title='Error de Fase',
            content=layout,
            size_hint=(None, None),
            size=(400, 250)
        )

        def confirmar_error(instance):
            try:
                # Exxportar este error de fase 
                error_freq = float(self.input_fase.text)
                self.popup_fase.dismiss()
                popup_result = Popup(
                    title='Fase Registrada',
                    content=Label(text=f'Error de fase ingresado: {error_freq} grados'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_result.open()

                # Guardar el valor o llamarlo desde otra función
                self.valor_error_freq = error_freq
                # self.aplicar_error_fase(error_freq)

            except ValueError:
                popup_error = Popup(
                    title='Entrada inválida',
                    content=Label(text='Por favor, ingrese un número válido.'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_error.open()

        btn_confirmar.bind(on_press=confirmar_error)
        self.popup_fase.open()

    ########################### Función cargar audio
    def cargar_audio(self, instance):
        content = BoxLayout(orientation='vertical')

        filechooser = FileChooserListView(
            path=os.getcwd(),
            filters=['*.wav']
        )
        content.add_widget(filechooser)

        btn_select = Button(text='Seleccionar', size_hint=(1, 0.2))
        content.add_widget(btn_select)

        self.popup = Popup(title='Selecciona un archivo WAV', content=content,
                           size_hint=(0.8, 0.8))

        def on_select(*args):
            if filechooser.selection:
                ruta_archivo = filechooser.selection[0]
                self.pwd_archivo = ruta_archivo
                ############## Exportar ruta archivo a otro archivo ##############
                samplerate_input_signal, input_signal = wavfile.read(ruta_archivo)
                # sd.play(input_signal, samplerate_input_signal)
                self.popup.dismiss()
                self.get_wav_info(ruta_archivo)

                # Llamar al callback con la ruta del archivo seleccionado desde
                # un main u otro archivo
                # if self.on_file_selected_callback:
                #     self.on_file_selected_callback(ruta_archivo)

        btn_select.bind(on_press=on_select)
        self.popup.open()
    
    ########################### Función Obtener info del wav
    def get_wav_info(self, ruta_archivo):
        try:
            with contextlib.closing(wave.open(ruta_archivo, 'r')) as wf:
                n_channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                framerate = wf.getframerate()
                n_frames = wf.getnframes()
                duration = n_frames / float(framerate)

                info = (
                    f"Archivo: {os.path.basename(ruta_archivo)}\n"
                    f"Canales: {n_channels}\n"
                    f"Frecuencia de muestreo: {framerate} Hz\n"
                    f"Duración: {duration:.2f} segundos\n"
                    f"Profundidad de bits: {sample_width * 8} bits"
                )
        except Exception as e:
            info = f"Error al leer el archivo:\n{str(e)}"

        popup_info = Popup(
            title='Información del WAV',
            content=Label(text=info),
            size_hint=(None, None),
            size=(400, 300)
        )
        popup_info.open()

    # def get_carrier(self, carrier):
    #     return 'TODO'
    
    # def get_phase(self, instance):
    #     return 'TODO'

    ########################### Función Iniciar modulación
    def init_mod(self, instance):
        # Obtener valores digitados desde la interfaz
        print(f"Modo seleccionado: {self.modo_seleccionado}")
        print(f"Frecuencia portadora: {self.frecuencia_modulacion}")
        print(f"Error fase: {self.valor_error_fase}")
        print(f"Error frecuencia: {self.valor_error_freq}")
        print(f"Ruta de archivo: {self.pwd_archivo}")
        
        # Ejecutar el script graficar.py como un subproceso
        subprocess.Popen([sys.executable, "graficar.py", str(500), str(self.frecuencia_modulacion)])
        # gra_main()
        # return 'TODO'

class pantalla3_modulacion(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="Calculando Modulación", font_size=20, pos_hint={"center_x": 0.5, "center_y": 0.5}))
        self.add_widget(layout)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        fondo_animado = Image(
            source=os.path.join(current_dir, '..', 'assets', 'test_giphy_math2.gif'),  # Ajuste para usar ../assets'fondo_animado.gif',  # debe ser un GIF válido
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


class Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="Pantalla de Modulación ISB", font_size=20, pos_hint={"center_x": 0.5, "center_y": 0.5}))
        self.add_widget(layout)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        fondo_animado = Image(
            source=os.path.join(current_dir, '..', 'assets', 'giphy_signal4.gif'),  # Ajuste para usar ../assets'fondo_animado.gif',  # debe ser un GIF válido
            anim_delay=0.05,  # velocidad de animación
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(fondo_animado)

        ########################### Título
        label_titulo = Label(
            text="Modulación ISB",
            font_size=24,
            size_hint=(.6, .1),
            pos_hint={'center_x': .5, 'top': 1}
        )
        layout.add_widget(label_titulo)
        ############################################################################################################
        ########################### Botón - Regresar a pantalla 1
        # btn_regresar = Button(
        #     text='Regresar a Pantalla 1', 
        #     size_hint=(None, None), 
        #     size=(200, 50),
        #     pos_hint={'center_x': .15, 'center_y': .60}
        # )
        # btn_regresar.bind(on_press=self.regresar_a_pantalla1)
        # layout.add_widget(btn_regresar)
        ########################### Botón - Regresar a pantalla 1
        btn_regresar = Button(
            text='Regresar a Pantalla 1', 
            size_hint=(None, None), 
            size=(200, 50),
            pos_hint={'x': 0.60, 'y': .0}
        )
        btn_regresar.bind(on_press=self.regresar_a_pantalla1)
        layout.add_widget(btn_regresar)

        ########################### Botón - Cargar WAV
        btn_cargar_audio = Button(
            text='Cargar Archivo WAV',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': .48}
        )
        btn_cargar_audio.bind(on_press=self.cargar_audio)
        layout.add_widget(btn_cargar_audio)

        ########################### Botón - Set frecuencia portadora
        btn_set_carrier = Button(
            text='Set frecuencia portadora',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': .36}
        )
        btn_set_carrier.bind(on_press=self.set_carrier_freq)
        layout.add_widget(btn_set_carrier)

        ########################### Botón - Set error fase
        btn_set_phase_error = Button(
            text='Set error de fase',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': .24}
        )
        btn_set_phase_error.bind(on_press=self.set_phase_error)
        layout.add_widget(btn_set_phase_error)

        ########################### Botón - Set error frecuencia
        btn_set_freq_error = Button(
            text='Set error de frecuencia',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': .12}
        )
        btn_set_freq_error.bind(on_press=self.set_freq_error)
        layout.add_widget(btn_set_freq_error)
        
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

    ########################### Función Set carrier
    def set_carrier_freq(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text='Ingrese frecuencia de modulación (Hz):')
        layout.add_widget(label)

        self.input_freq_mod = TextInput(
            multiline=False,
            input_filter='float',
            hint_text='Ej: 1000.0'
        )
        layout.add_widget(self.input_freq_mod)

        btn_confirmar = Button(text='Confirmar', size_hint=(1, 0.3))
        layout.add_widget(btn_confirmar)

        self.popup_freq_mod = Popup(
            title='Frecuencia de Modulación',
            content=layout,
            size_hint=(None, None),
            size=(400, 250)
        )

        def confirmar_freq_mod(instance):
            try:
                frecuencia = float(self.input_freq_mod.text)
                self.popup_freq_mod.dismiss()
                popup_result = Popup(
                    title='Frecuencia Registrada',
                    content=Label(text=f'Frecuencia de modulación ingresada: {frecuencia} Hz'),
                    size_hint=(None, None),
                    size=(400, 200)
                )
                popup_result.open()

                # Guardar el valor o exportarlo a otra función
                # self.frecuencia_modulacion = frecuencia

            except ValueError:
                popup_error = Popup(
                    title='Entrada inválida',
                    content=Label(text='Por favor, ingrese un número válido.'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_error.open()

        btn_confirmar.bind(on_press=confirmar_freq_mod)
        self.popup_freq_mod.open()    

    ########################### Función Set error de fase
    def set_phase_error(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text='Ingrese error de fase (en grados):')
        layout.add_widget(label)

        self.input_fase = TextInput(
            multiline=False,
            input_filter='float',
            hint_text='Ej: 45.0'
        )
        layout.add_widget(self.input_fase)

        btn_confirmar = Button(text='Confirmar', size_hint=(1, 0.3))
        layout.add_widget(btn_confirmar)

        self.popup_fase = Popup(
            title='Error de Fase',
            content=layout,
            size_hint=(None, None),
            size=(400, 250)
        )

        def confirmar_error(instance):
            try:
                error = float(self.input_fase.text)
                self.popup_fase.dismiss()
                popup_result = Popup(
                    title='Fase Registrada',
                    content=Label(text=f'Error de fase ingresado: {error} grados'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_result.open()

                # Guardar el valor o llamarlo desde otra función
                # self.valor_error_fase = error
                # self.aplicar_error_fase(error)

            except ValueError:
                popup_error = Popup(
                    title='Entrada inválida',
                    content=Label(text='Por favor, ingrese un número válido.'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_error.open()

        btn_confirmar.bind(on_press=confirmar_error)
        self.popup_fase.open()
    
    ########################### Función Set error de frecuencia
    def set_freq_error(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text='Ingrese error de frecuencia (en Hertz/radianes):')
        layout.add_widget(label)

        self.input_fase = TextInput(
            multiline=False,
            input_filter='float',
            hint_text='Ej: 45.0'
        )
        layout.add_widget(self.input_fase)

        btn_confirmar = Button(text='Confirmar', size_hint=(1, 0.3))
        layout.add_widget(btn_confirmar)

        self.popup_fase = Popup(
            title='Error de Fase',
            content=layout,
            size_hint=(None, None),
            size=(400, 250)
        )

        def confirmar_error(instance):
            try:
                # Exxportar este error de fase 
                error_freq = float(self.input_fase.text)
                self.popup_fase.dismiss()
                popup_result = Popup(
                    title='Fase Registrada',
                    content=Label(text=f'Error de fase ingresado: {error_freq} grados'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_result.open()

                # Guardar el valor o llamarlo desde otra función
                # self.valor_error_fase = error_freq
                # self.aplicar_error_fase(error_freq)

            except ValueError:
                popup_error = Popup(
                    title='Entrada inválida',
                    content=Label(text='Por favor, ingrese un número válido.'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_error.open()

        btn_confirmar.bind(on_press=confirmar_error)
        self.popup_fase.open()
    
    ########################### Función Cargar Audio
    # Pasar funciones a otro archivo de procesamiento de audio (ssb_mod)
    def cargar_audio(self, instance):
        content = BoxLayout(orientation='vertical')

        filechooser = FileChooserListView(
            path=os.getcwd(),
            filters=['*.wav'],
            multiselect=True  # Permitir múltiples selecciones
        )
        content.add_widget(filechooser)

        btn_select = Button(text='Seleccionar', size_hint=(1, 0.2))
        content.add_widget(btn_select)

        self.popup = Popup(title='Selecciona dos archivos WAV', content=content,
                           size_hint=(0.8, 0.8))

        def on_select(*args):
            seleccionados = filechooser.selection
            if len(seleccionados) != 2:
                error_popup = Popup(title="Error",
                                    content=Label(text="Por favor selecciona exactamente 2 archivos WAV."),
                                    size_hint=(None, None), size=(400, 200))
                error_popup.open()
                return

            # Procesar ambos archivos
            for ruta in seleccionados:
                try:
                    samplerate, data = wavfile.read(ruta)
                    sd.play(data, samplerate)
                    self.get_wav_info(ruta)
                except Exception as e:
                    error_popup = Popup(title="Error al leer archivo",
                                        content=Label(text=str(e)),
                                        size_hint=(None, None), size=(400, 200))
                    error_popup.open()

            self.popup.dismiss()

        btn_select.bind(on_press=on_select)
        self.popup.open()

    

    ########################### Función Obtner Info del archivo wav
    # Obtener el archivo de audio WAV
    def get_wav_info(self, ruta_archivo):
        try:
            with contextlib.closing(wave.open(ruta_archivo, 'r')) as wf:
                n_channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                framerate = wf.getframerate()
                n_frames = wf.getnframes()
                duration = n_frames / float(framerate)

                info = (
                    f"Archivo: {os.path.basename(ruta_archivo)}\n"
                    f"Canales: {n_channels}\n"
                    f"Frecuencia de muestreo: {framerate} Hz\n"
                    f"Duración: {duration:.2f} segundos\n"
                    f"Profundidad de bits: {sample_width * 8} bits"
                )
        except Exception as e:
            info = f"Error al leer el archivo:\n{str(e)}"

        popup_info = Popup(
            title='Información del WAV',
            content=Label(text=info),
            size_hint=(None, None),
            size=(400, 300)
        )
        popup_info.open()

class MyApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(Screen1(name='pantalla1'))
        screen_manager.add_widget(Screen2(name='pantalla2'))
        screen_manager.add_widget(Screen3(name='pantalla3'))
        screen_manager.add_widget(pantalla3_modulacion(name='pantalla3_modulacion'))
        return screen_manager


if __name__ == '__main__':
    MyApp().run()
