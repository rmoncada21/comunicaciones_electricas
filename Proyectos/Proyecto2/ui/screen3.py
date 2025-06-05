# Librerías estándar
import os  # Para trabajar con rutas de archivos y carpetas

# Kivy core
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView

# Para trabajar con audio (lectura de WAV)
import soundfile as sf  # Librería recomendada para leer archivos WAV de forma más robusta

# import sounddevice as sd 
# import wave
# import contextlib

class Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="Pantalla de Modulación ISB", font_size=20, pos_hint={"center_x": 0.5, "center_y": 0.5}))
        self.add_widget(layout)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        fondo_animado = Image(
            source=os.path.join(current_dir, '..', 'assets', 'v3', 'dribble_robot6a.gif'),  # Ajuste para usar ../assets', 'v3'fondo_animado.gif',  # debe ser un GIF válido
            anim_delay=0.05,  # velocidad de animación
            allow_stretch=True,
            keep_ratio=False
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
    # def cargar_audio(self, instance):
    #     content = BoxLayout(orientation='vertical')

    #     filechooser = FileChooserListView(
    #         path=os.getcwd(),
    #         filters=['*.wav'],
    #         multiselect=True  # Permitir múltiples selecciones
    #     )
    #     content.add_widget(filechooser)

    #     btn_select = Button(text='Seleccionar', size_hint=(1, 0.2))
    #     content.add_widget(btn_select)

    #     self.popup = Popup(title='Selecciona dos archivos WAV', content=content,
    #                        size_hint=(0.8, 0.8))

    #     def on_select(*args):
    #         seleccionados = filechooser.selection
    #         if len(seleccionados) != 2:
    #             error_popup = Popup(title="Error",
    #                                 content=Label(text="Por favor selecciona exactamente 2 archivos WAV."),
    #                                 size_hint=(None, None), size=(400, 200))
    #             error_popup.open()
    #             return

    #         # Procesar ambos archivos
    #         for ruta in seleccionados:
    #             try:
    #                 # samplerate, data = wavfile.read(ruta)
    #                 data, samplerate = sf.read(ruta)
    #                 data, samplerate = sf.read(ruta)
    #                 sd.play(data, samplerate)
    #                 self.get_wav_info(ruta)
    #             except Exception as e:
    #                 error_popup = Popup(title="Error al leer archivo",
    #                                     content=Label(text=str(e)),
    #                                     size_hint=(None, None), size=(400, 200))
    #                 error_popup.open()

    #         self.popup.dismiss()

    #     btn_select.bind(on_press=on_select)
    #     self.popup.open()

    # Mejora en la cargar_audio: Se seleccionar dos archivos pero uno a la vez
    def cargar_audio(self, instance):
        self.archivos_seleccionados = []

        def seleccionar_archivo(etapa=1):
            content = BoxLayout(orientation='vertical')

            filechooser = FileChooserListView(
                path=os.getcwd(),
                filters=['*.wav'],
                multiselect=False  # Solo un archivo a la vez
            )
            content.add_widget(filechooser)

            btn_select = Button(text=f'Seleccionar archivo {etapa}', size_hint=(1, 0.2))
            content.add_widget(btn_select)

            popup = Popup(title=f'Selecciona archivo WAV {etapa}', content=content,
                          size_hint=(0.8, 0.8))

            def on_select(*args):
                seleccionados = filechooser.selection
                if len(seleccionados) != 1:
                    error_popup = Popup(title="Error",
                                        content=Label(text="Por favor selecciona un archivo WAV."),
                                        size_hint=(None, None), size=(400, 200))
                    error_popup.open()
                    return

                self.archivos_seleccionados.append(seleccionados[0])
                print(f"Archivos Screen 2:{self.archivos_seleccionados}")
                popup.dismiss()

                if etapa == 1:
                    # Pedir el segundo archivo
                    seleccionar_archivo(etapa=2)
                else:
                    # Ya se tienen dos archivos para procesarlos
                    for ruta in self.archivos_seleccionados:
                        try:
                            # data, samplerate = sf.read(ruta)
                            # sd.play(data, samplerate)
                            self.get_wav_info(ruta)
                        except Exception as e:
                            error_popup = Popup(title="Error al leer archivo",
                                                content=Label(text=str(e)),
                                                size_hint=(None, None), size=(400, 200))
                            error_popup.open()

            btn_select.bind(on_press=on_select)
            popup.open()
        
        seleccionar_archivo()


    ########################### Función Obtner Info del archivo wav
    # Obtener el archivo de audio WAV
    # usando libreria wave
    # def get_wav_info(self, ruta_archivo):
    #     try:
    #         with contextlib.closing(wave.open(ruta_archivo, 'r')) as wf:
    #             n_channels = wf.getnchannels()
    #             sample_width = wf.getsampwidth()
    #             framerate = wf.getframerate()
    #             n_frames = wf.getnframes()
    #             duration = n_frames / float(framerate)

    #             info = (
    #                 f"Archivo: {os.path.basename(ruta_archivo)}\n"
    #                 f"Canales: {n_channels}\n"
    #                 f"Frecuencia de muestreo: {framerate} Hz\n"
    #                 f"Duración: {duration:.2f} segundos\n"
    #                 f"Profundidad de bits: {sample_width * 8} bits"
    #             )
    #     except Exception as e:
    #         info = f"Error al leer el archivo:\n{str(e)}"

    #     popup_info = Popup(
    #         title='Información del WAV',
    #         content=Label(text=info),
    #         size_hint=(None, None),
    #         size=(400, 300)
    #     )
    #     popup_info.open()

    # usando libreria soundfile
    def get_wav_info(self, ruta_archivo):
        try:
            with sf.SoundFile(ruta_archivo) as f:
                n_channels = f.channels
                samplerate = f.samplerate
                n_frames = len(f)
                duration = n_frames / samplerate
                subtype = f.subtype  # Por ejemplo: 'PCM_16'

                info = (
                    f"Archivo: {os.path.basename(ruta_archivo)}\n"
                    f"Canales: {n_channels}\n"
                    f"Frecuencia de muestreo: {samplerate} Hz\n"
                    f"Duración: {duration:.2f} segundos\n"
                    f"Formato: {subtype}"
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