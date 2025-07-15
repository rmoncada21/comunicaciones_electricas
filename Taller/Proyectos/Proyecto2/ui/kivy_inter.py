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
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

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

        # Obtener ruta absoluta a la imagen dentro de la carpeta 'assets','v1'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, '..', 'assets','v1', 'red.jpg')  # Ajuste para usar ../assets','v1
        
        fondo_animado = Image(
            source=os.path.join(current_dir, '..', 'assets','v1', 'giphy_plasma1.gif'),  # Ajuste para usar ../assets','v1'fondo_animado.gif',  # debe ser un GIF válido
            anim_delay=0.05,  # velocidad de animación
            allow_stretch=True,
            keep_ratio=True
        )
        root.add_widget(fondo_animado)

        # # Imagen de fondo
        # fondo = Image(source=img_path, allow_stretch=True, keep_ratio=False)
        # fondo.disabled = True
        # root.add_widget(fondo)

        # Etiqueta - Titulo del programa
        label = Label(
            text="Modulación SSB PYTHON",
            font_size=24,
            size_hint=(.6, .1),
            pos_hint={'center_x': .5, 'top': 1}
        )
        root.add_widget(label)

        # Botón 1 Saludar
        # btn_saludar = HoverButton(
        #     text='Saludar',
        #     size_hint=(.3, .1),
        #     pos_hint={'center_x': .5, 'center_y': .6}
        # )
        # btn_saludar.bind(on_press=self.saludar)
        # root.add_widget(btn_saludar)
        
        # Botón 1 Cargar WAV
        btn_cargar_audio = HoverButton(
            text='Cargar Archivo WAV',
            size_hint=(.3, .1),
            pos_hint={'center_x': .5, 'center_y': .60}
        )
        btn_cargar_audio.bind(on_press=self.cargar_audio)
        root.add_widget(btn_cargar_audio)

        # Botón 2 Obtener Frecuencia de Portadora
        btn_freq_modulacion = HoverButton(
            text='Obtener Frecuencia de Modulación',
            size_hint=(.3, .1),
            pos_hint={'center_x': .5, 'center_y': .48}
        )
        btn_freq_modulacion.bind(on_press=self.get_freq_portadora)
        root.add_widget(btn_freq_modulacion)

        # Botón 3 Tipo de modulación SSB o ISB
        btn_tipo_modulacion = HoverButton(
            text='Digitar el tipo de modulación',
            size_hint=(.3, .1),
            pos_hint={'center_x': .5, 'center_y': .36}
        )
        btn_tipo_modulacion.bind(on_press=self.get_tipo_mod)
        root.add_widget(btn_tipo_modulacion)

        # Boton 4 error de fase
        btn_error_fase = HoverButton(
            text='Elección de error  de fase',
            size_hint=(.3, .1),
            pos_hint={'center_x': .5, 'center_y': .24}
        )
        btn_error_fase.bind(on_press=self.get_error_fase)
        root.add_widget(btn_error_fase)

        # Boton 5 error de frecuencia
        btn_error_freq = HoverButton(
            text='Elección de error  de frecuencia',
            size_hint=(.3, .1),
            pos_hint={'center_x': .5, 'center_y': .12}
        )
        btn_error_freq.bind(on_press=self.get_error_frecuencia)
        root.add_widget(btn_error_freq)

        # Botón 6 Salir
        btn_salir = HoverButton(
            text='Salir',
            size_hint=(.3, .1),
            pos_hint={'center_x': .5, 'center_y': .12}
        )
        btn_salir.bind(on_press=self.salir)
        root.add_widget(btn_salir)

        return root

    # def saludar(self, instance):
    #     popup = Popup(title='Saludo',
    #                   content=Label(text='¡Hola desde Kivy!'),
    #                   size_hint=(None, None), size=(300, 200))
    #     popup.open()

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

    def get_freq_portadora(self, instance):
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

    def get_tipo_mod(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text='Seleccione el tipo de modulación:')
        layout.add_widget(label)

        # Botón para SSB
        btn_ssb = Button(text='SSB')
        layout.add_widget(btn_ssb)

        # Botón para ISB
        btn_isb = Button(text='ISB')
        layout.add_widget(btn_isb)

        popup_modulacion = Popup(
            title='Tipo de Modulación',
            content=layout,
            size_hint=(None, None),
            size=(300, 250)
        )

        def elegir_ssb(instance):
            popup_modulacion.dismiss()
            popup_result = Popup(
                title='Modulación seleccionada',
                content=Label(text='Modulación SSB seleccionada'),
                size_hint=(None, None),
                size=(300, 200)
            )
            popup_result.open()

        def elegir_isb(instance):
            popup_modulacion.dismiss()
            popup_result = Popup(
                title='Modulación seleccionada',
                content=Label(text='Modulación ISB seleccionada'),
                size_hint=(None, None),
                size=(300, 200)
            )
            popup_result.open()

        btn_ssb.bind(on_press=elegir_ssb)
        btn_isb.bind(on_press=elegir_isb)

        popup_modulacion.open()


    def get_error_fase(self, instance):
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

    def get_error_frecuencia(self, instance):
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

if __name__ == '__main__':
    MyApp().run()