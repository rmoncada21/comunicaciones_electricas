# kivy_inter.py

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout

import wave
import contextlib
import os
import sounddevice as sd
from scipy.io import wavfile

# from src import ssb

class HoverButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_color = self.background_color[:]
        self.hover_color = (0.3, 0.8, 1, 1)  # Azul claro
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return  # No está montado aún

        if self.collide_point(*self.to_widget(*pos)):
            self.background_color = self.hover_color
        else:
            self.background_color = self.default_color

class MyApp(App):
    
    def __init__(self, on_file_selected_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.on_file_selected_callback = on_file_selected_callback  # Método de callback

    def build(self):
        root = FloatLayout()

        # Obtener ruta absoluta a la imagen dentro de la carpeta 'assets'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, '..', 'assets', 'red.jpg')  # Ajuste para usar ../assets

        # Imagen de fondo
        fondo = Image(source=img_path, allow_stretch=True, keep_ratio=False)
        fondo.disabled = True
        root.add_widget(fondo)

        # Etiqueta
        label = Label(
            text="Modulación SSB PYTHON",
            font_size=24,
            size_hint=(.6, .1),
            pos_hint={'center_x': .5, 'top': 1}
        )
        root.add_widget(label)

        # Botón 1 Saludar
        btn_saludar = HoverButton(
            text='Saludar',
            size_hint=(.3, .1),
            pos_hint={'center_x': .5, 'center_y': .6}
        )
        btn_saludar.bind(on_press=self.saludar)
        root.add_widget(btn_saludar)

        # Botón 2 Salir
        btn_salir = HoverButton(
            text='Salir',
            size_hint=(.3, .1),
            pos_hint={'center_x': .5, 'center_y': .48}
        )
        btn_salir.bind(on_press=self.salir)
        root.add_widget(btn_salir)

        # Botón 3 Cargar WAV
        btn_cargar_audio = HoverButton(
            text='Cargar Archivo WAV',
            size_hint=(.3, .1),
            pos_hint={'center_x': .5, 'center_y': .36}
        )
        btn_cargar_audio.bind(on_press=self.cargar_audio)
        root.add_widget(btn_cargar_audio)

        return root

    # Funciones de la clase MyAPP
    def saludar(self, instance):
        popup = Popup(title='Saludo',
                      content=Label(text='¡Hola desde Kivy!'),
                      size_hint=(None, None), size=(300, 200))
        popup.open()

    def salir(self, instance):
        App.get_running_app().stop()
    
    
    # Pasar funciones a otro archivo de procesamiento de audio (ssb_mod)
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
                
                ############## Exportar ruta archivo a otro archivo ##############
                samplerate_input_signal, input_signal = wavfile.read(ruta_archivo)
                sd.play(input_signal, samplerate_input_signal)
                self.popup.dismiss()
                self.get_wav_info(ruta_archivo)

                # Llamar al callback con la ruta del archivo seleccionado desde
                # un main u otro archivo
                # if self.on_file_selected_callback:
                #     self.on_file_selected_callback(ruta_archivo)

        btn_select.bind(on_press=on_select)
        self.popup.open()
    
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
