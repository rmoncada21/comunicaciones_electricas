import os
import sys
import subprocess

import soundfile as sf
# import src.SSB as ssb
import numpy as np
# from src.ssb import SSB
from src.isb import ISB
import sounddevice as sd

# Kivy core
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.clock import Clock

class Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="Pantalla de Modulación ISB", font_size=20, pos_hint={"center_x": 0.5, "center_y": 0.5}))
        self.add_widget(layout)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        fondo_animado = Image(
            # source=os.path.join(current_dir, '..', 'assets', 'v3','giphy_signal5.gif'),  # Ajuste para usar ../assets', 'v3'fondo_animado.gif',  # debe ser un GIF válido
            source=os.path.join(current_dir, '..', 'assets', 'v3', 'dribble_robot6a.gif'), 
            anim_delay=0.05,  # velocidad de animación
            allow_stretch=True,
            keep_ratio=False
        )
        layout.add_widget(fondo_animado)

        ########################### Título
        label_titulo = Label(
            text="Modulación ISB (estereo)",
            font_size=24,
            size_hint=(.6, .1),
            pos_hint={'center_x': .5, 'top': 1}
        )
        layout.add_widget(label_titulo)
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

        ########################### Botón Cargar WAV
        btn_cargar_audio = Button(
            text='Cargar Archivo WAV',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': 0.60}
        )
        btn_cargar_audio.bind(on_press=self.cargar_audio)
        layout.add_widget(btn_cargar_audio)

        ########################### Boton container - SSB SC o FC
        # self.boton_container0 = BoxLayout(
        #     # orientation='horizontal',
        #     size_hint=(None, None),
        #     size=(200, 50),
        #     pos_hint={'center_x': .15, 'center_y': 0.60},
        #     spacing=10
        # )

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
        btn_init_mod.bind(on_press=self.ir_a_mod)
        btn_init_mod.bind(on_press=self.iniciar_mod_con_delay)
        # btn_init_mod.bind(on_press=self.init_mod)
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
        Clock.schedule_once(self.load_screen3_modulation, 0)
        layout.add_widget(btn_salir)

    ############################################################################################################
    def load_screen3_modulation(self, dt):
        # self.status_label.text = "Cargando pantallas secundarias..."
        from ui.screen3_modulation import Screen3_modulation
        sm = self.manager
        sm.add_widget(Screen3_modulation(name='Screen3_modulation'))
        # print(f"[INFO] Pantallas 2_modulation y 3 cargadas en {time.time() - start_time:.2f} s")
        # self.status_label.text = "¡Listo!"

    ########################### Función para esperar 5 segundos
    def iniciar_mod_con_delay(self, instance):
        # self.init_mod(instance)  # Ejecuta primero
        Clock.schedule_once(lambda dt: self.init_mod(instance), 5)  # Espera 3 segundos y ejecuta
    
    ########################### Función para ir a pantalla3_modulación
    def ir_a_mod(self, instance):
        self.manager.current = 'Screen3_modulation'

    ########################### Función Regresar a pantalla 1
    def regresar_a_pantalla1(self, instance):
        # Regresar a la primera pantalla
        self.manager.current = 'pantalla1'
    
    ########################### Función Salir
    def salir(self, instance):
        App.get_running_app().stop()
    
    ########################### Función Seleccionar tipo SSB SC o FC
    def set_ssb_tipo(self, instance):
        self.ssb_tipo = instance.text
        print(f"SSB SC o FC: {self.ssb_tipo}")

    ########################### Función Seleccionar banda lateral
    def set_banda_lateral(self, instance):
        self.banda_lateral = instance.text
        print(f"Banda lateral seleccionada: {self.banda_lateral}")

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
    
    ########################### Función Mostrar / esconder botones USB - LSB
    def toggle_botones0(self, instance):
        # Alternar visibilidad de los botones
        for btn in [self.boton_ssb_sc, self.boton_ssb_fc]:
            if btn.opacity == 0:
                btn.opacity = 1
                btn.disabled = False
            else:
                btn.opacity = 0
                btn.disabled = True

    def set_carrier_freq(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text='Ingrese frecuencia de portadora (Hz) - FcMax=500MHz: ')
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

        def confirmar_carrier_freq(instance):
            try:
                frecuencia_carrier = float(self.input_freq_mod.text)

                # Validación de rango: mayor a 0 y menor o igual a 500 MHz
                if not (0 < frecuencia_carrier <= 500_000_000):
                    popup_rango = Popup(
                        title='Valor fuera de rango',
                        content=Label(text='Ingrese una frecuencia entre 1 Hz y 500 MHz.'),
                        size_hint=(None, None),
                        size=(350, 200)
                    )
                    popup_rango.open()
                    return

                self.popup_freq_mod.dismiss()
                popup_result = Popup(
                    title='Frecuencia Registrada',
                    content=Label(text=f'Frecuencia de portadora ingresada: {frecuencia_carrier} Hz'),
                    size_hint=(None, None),
                    size=(400, 200)
                )
                popup_result.open()

                # Guardar el valor
                self.frecuencia_carrier = frecuencia_carrier

            except ValueError:
                popup_error = Popup(
                    title='Entrada inválida',
                    content=Label(text='Por favor, ingrese un número válido.'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_error.open()

        btn_confirmar.bind(on_press=confirmar_carrier_freq)
        self.popup_freq_mod.open()
    
    def set_phase_error(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text='Ingrese error de fase (en grados) entre [0, 180]:')
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

                # Validación de rango
                if not (0 <= error <= 180):
                    popup_rango = Popup(
                        title='Valor fuera de rango',
                        content=Label(text='Por favor ingrese un valor entre 0 y 180 grados.'),
                        size_hint=(None, None),
                        size=(350, 200)
                    )
                    popup_rango.open()
                    return

                self.popup_fase.dismiss()
                popup_result = Popup(
                    title='Fase Registrada',
                    content=Label(text=f'Error de fase ingresado: {error} grados'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_result.open()

                # Guardar el valor
                self.valor_error_fase = error

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

    def set_freq_error(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text='Ingrese error de frecuencia (en Hertz) [±25%×fc]:')
        layout.add_widget(label)

        self.input_freq = TextInput(
            multiline=False,
            input_filter='float', # CORREGIR
            hint_text='Ej: 45.0'
        )
        layout.add_widget(self.input_freq)

        btn_confirmar = Button(text='Confirmar', size_hint=(1, 0.3))
        layout.add_widget(btn_confirmar)

        self.popup_freq = Popup(
            title='Error de Frecuencia',
            content=layout,
            size_hint=(None, None),
            size=(400, 250)
        )

        def confirmar_error(instance):
            try:
                error_freq = float(self.input_freq.text)
                limite = (25 / 100) * self.frecuencia_carrier
                print(f"Error ingresado: {error_freq}, Límite: ±{limite}")  # debug

                if not (-limite <= error_freq <= limite):
                    popup_rango = Popup(
                        title='Valor fuera de rango',
                        content=Label(text=f'El error debe estar entre ±25%×fc: ±{limite:.2f} Hz'),
                        size_hint=(None, None),
                        size=(370, 200)
                    )
                    popup_rango.open()
                    return

                self.popup_freq.dismiss()
                popup_result = Popup(
                    title='Frecuencia Registrada',
                    content=Label(text=f'Error de frecuencia ingresado: {error_freq} Hz'),
                    size_hint=(None, None),
                    size=(400, 200)
                )
                popup_result.open()

                self.valor_error_freq = error_freq  # guardar el valor

            except ValueError:
                popup_error = Popup(
                    title='Entrada inválida',
                    content=Label(text='Por favor, ingrese un número válido.'),
                    size_hint=(None, None),
                    size=(350, 200)
                )
                popup_error.open()

        btn_confirmar.bind(on_press=confirmar_error)
        self.popup_freq.open()


    ########################### Función cargar audio
    # def cargar_audio(self, instance):
    #     content = BoxLayout(orientation='vertical')

    #     filechooser = FileChooserListView(
    #         path=os.getcwd(),
    #         filters=['*.wav']
    #     )
    #     content.add_widget(filechooser)

    #     btn_select = Button(text='Seleccionar', size_hint=(1, 0.2))
    #     content.add_widget(btn_select)

    #     self.popup = Popup(title='Selecciona un archivo WAV', content=content,
    #                        size_hint=(0.8, 0.8))

    #     def on_select(*args):
    #         if filechooser.selection:
    #             ruta_archivo = filechooser.selection[0]
    #             self.pwd_archivo = ruta_archivo
    #             ############## Exportar ruta archivo a otro archivo ##############
    #             # samplerate_input_signal, input_signal = wavfile.read(ruta_archivo)
    #             data, samplerate = sf.read(ruta_archivo)
    #             # sd.play(input_signal, samplerate_input_signal)
    #             self.popup.dismiss()
    #             self.get_wav_info(ruta_archivo)

    #     btn_select.bind(on_press=on_select)
    #     self.popup.open()

    def cargar_audio(self, instance):
        self.archivos_seleccionados = []

        def seleccionar_archivo(etapa=1):
            content = BoxLayout(orientation='vertical')

            filechooser = FileChooserListView(
                path=os.getcwd(),
                filters=['*.wav'],
                multiselect=False
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
                print(f"Archivo {etapa} seleccionado: {seleccionados[0]}")
                popup.dismiss()

                if etapa == 1:
                    seleccionar_archivo(etapa=2)
                else:
                    # Ya se tienen dos archivos para procesarlos
                    for i, ruta in enumerate(self.archivos_seleccionados):
                        try:
                            self.get_wav_info(ruta, indice=i+1)
                        except Exception as e:
                            error_popup = Popup(title="Error al leer archivo",
                                                content=Label(text=str(e)),
                                                size_hint=(None, None), size=(400, 200))
                            error_popup.open()

            btn_select.bind(on_press=on_select)
            popup.open()

        seleccionar_archivo()

    
    # Usando librería soundfile
    def get_wav_info(self, ruta_archivo, indice=1):
        try:
            with sf.SoundFile(ruta_archivo) as f:
                audio_filename = os.path.basename(ruta_archivo)
                data_audio = f.read(dtype='float32')
                n_channels = f.channels
                samplerate = f.samplerate
                n_frames = len(f)
                duration = n_frames / samplerate
                subtype = f.subtype

                # Guardar en variables distintas dependiendo del índice
                if indice == 1:
                    self.audio_duration_1 = duration
                    self.audio_filename_1 = audio_filename
                    self.audio_data_1 = data_audio
                    self.audio_n_canales_1 = n_channels
                    self.audio_samplerate_1 = samplerate
                elif indice == 2:
                    self.audio_duration_2 = duration
                    self.audio_filename_2 = audio_filename
                    self.audio_data_2 = data_audio
                    self.audio_n_canales_2 = n_channels
                    self.audio_samplerate_2 = samplerate

                info = (
                    f"Archivo: {audio_filename}\n"
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


    ########################### Función Iniciar modulación
    def init_mod(self, instance):
        ########## COMPARTIR INFORMACIÓN ENTRE PANTALLAS ##########

        # Archivo 1
        self.manager.audio_filename_1 = self.audio_filename_1
        self.manager.audio_data_1 = self.audio_data_1
        self.manager.audio_duration_1 = self.audio_duration_1
        self.manager.audio_n_canales_1 = self.audio_n_canales_1
        self.manager.audio_samplerate_1 = self.audio_samplerate_1

        # Archivo 2
        self.manager.audio_filename_2 = self.audio_filename_2
        self.manager.audio_data_2 = self.audio_data_2
        self.manager.audio_duration_2 = self.audio_duration_2
        self.manager.audio_n_canales_2 = self.audio_n_canales_2
        self.manager.audio_samplerate_2 = self.audio_samplerate_2

        ########## OBTENER SEÑALES DE ENTRADA ##########
        mensaje_data_1 = self.audio_data_1
        mensaje_data_2 = self.audio_data_2
        mensaje_samplerate = self.audio_samplerate_1  # Asumimos que ambos tienen el mismo fs

        ########## GUARDAR SEÑALES ORIGINALES ##########
        np.save("output/isb_mensaje_data1.npy", mensaje_data_1)
        np.save("output/isb_mensaje_data2.npy", mensaje_data_2)
        np.save("output/isb_mensaje_samplerate.npy", mensaje_samplerate)

        ########## MODULACIÓN ISB ##########
        self.manager.frecuencia_carrier = self.frecuencia_carrier
        error_fase =  self.valor_error_fase
        error_frecuencia = self.valor_error_freq
        fc = self.frecuencia_carrier
        isb = ISB()

        isb_modulada, t, cos_carrier, sin_carrier = isb.isb_modulate(
            mensaje_data_1, mensaje_data_2, mensaje_samplerate, fc, error_fase, error_frecuencia
        )
        np.save("output/isb_modulada.npy", isb_modulada)
        np.save("output/isb_t.npy", t)

        ########## DEMODULACIÓN ISB ##########
        m1_rec, m2_rec = isb.isb_demodulate(isb_modulada, mensaje_samplerate, fc, t)
        np.save("output/isb_demodulada1.npy", m1_rec)
        np.save("output/isb_demodulada2.npy", m2_rec)

        print("ISB Modulación y demodulación completadas.")
