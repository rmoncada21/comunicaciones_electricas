import os
import sys
import subprocess

import soundfile as sf
# import src.SSB as ssb
import numpy as np
from src.SSB import SSB

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

class Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="Pantalla de Modulación SSB", font_size=20, pos_hint={"center_x": 0.5, "center_y": 0.5}))
        self.add_widget(layout)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        fondo_animado = Image(
            # source=os.path.join(current_dir, '..', 'assets', 'v3','giphy_signal5.gif'),  # Ajuste para usar ../assets', 'v3'fondo_animado.gif',  # debe ser un GIF válido
            source=os.path.join(current_dir, '..', 'assets', 'v3', 'dribble_robot7a.gif'), 
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
            pos_hint={'center_x': .15, 'center_y': .84}
        )
        btn_cargar_audio.bind(on_press=self.cargar_audio)
        layout.add_widget(btn_cargar_audio)

        ########################### Boton container - SSB SC o FC
        self.boton_container0 = BoxLayout(
            # orientation='horizontal',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': 0.72},
            spacing=10
        )

        ########################### Botón principal - Escoger modulación
        self.boton_principal0 = Button(
            text="Escoger SSB SC o FC",
            size_hint=(None, None),
            size=(200, 50)
        )
        self.boton_principal0.bind(on_press=self.toggle_botones0)
        self.boton_container0.add_widget(self.boton_principal0)

        ########################### Botones SC escondido
        self.boton_ssb_sc = Button(
            text="SC",
            size_hint=(None, None),
            size=(200, 50),
            opacity=0,
            disabled=True
        )
        # self.boton_ssb_sc.bind(on_press=self.get_tipo_mod)
        # Obtener el botón presionado
        self.boton_ssb_sc.bind(on_press=self.set_ssb_tipo)
        self.boton_container0.add_widget(self.boton_ssb_sc)

        ########################### Botones LSB escondido
        self.boton_ssb_fc = Button(
            text="LSB",
            size_hint=(None, None),
            size=(200, 50),
            opacity=0,
            disabled=True
        )
        # self.boton_ssb_fc.bind(on_press=self.get_tipo_mod)
        # Obtener el botón presionado
        self.boton_ssb_fc.bind(on_press=self.set_ssb_tipo)
        self.boton_container0.add_widget(self.boton_ssb_fc)

        layout.add_widget(self.boton_container0)
        ####################################################### CHECKPOINT
        ########################### Boton container
        self.boton_container = BoxLayout(
            # orientation='horizontal',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': .15, 'center_y': 0.60},
            spacing=10
        )

        ########################### Botón principal - Escoger modulación
        self.boton_principal = Button(
            text="Escoger Banda lateral",
            size_hint=(None, None),
            size=(200, 50)
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
        self.boton_usb.bind(on_press=self.set_banda_lateral)
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
        self.boton_lsb.bind(on_press=self.set_banda_lateral)
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
        Clock.schedule_once(self.load_screen2_modulation, 0)
        layout.add_widget(btn_salir)
    ############################################################################################################
    def load_screen2_modulation(self, dt):
        # self.status_label.text = "Cargando pantallas secundarias..."
        from ui.screen2_modulation import Screen2_modulation
        sm = self.manager
        sm.add_widget(Screen2_modulation(name='Screen2_modulation'))
        # print(f"[INFO] Pantallas 2_modulation y 3 cargadas en {time.time() - start_time:.2f} s")
        # self.status_label.text = "¡Listo!"

    ########################### Función para esperar 5 segundos
    def iniciar_mod_con_delay(self, instance):
        # self.init_mod(instance)  # Ejecuta primero
        Clock.schedule_once(lambda dt: self.init_mod(instance), 5)  # Espera 3 segundos y ejecuta
    
    ########################### Función para ir a pantalla3_modulación
    def ir_a_mod(self, instance):
        self.manager.current = 'Screen2_modulation'

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

    ########################### Función Set frecuencia portadora
    # def set_carrier_freq(self, instance):
    #     layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

    #     label = Label(text='Ingrese frecuencia de modulación (Hz):')
    #     layout.add_widget(label)

    #     self.input_freq_mod = TextInput(
    #         multiline=False,
    #         input_filter='float',
    #         hint_text='Ej: 1000.0'
    #     )
    #     layout.add_widget(self.input_freq_mod)

    #     btn_confirmar = Button(text='Confirmar', size_hint=(1, 0.3))
    #     layout.add_widget(btn_confirmar)

    #     self.popup_freq_mod = Popup(
    #         title='Frecuencia de Modulación',
    #         content=layout,
    #         size_hint=(None, None),
    #         size=(400, 250)
    #     )

    #     def confirmar_carrier_freq(instance):
    #         try:
    #             frecuencia_carrier = float(self.input_freq_mod.text)
    #             self.popup_freq_mod.dismiss()
    #             popup_result = Popup(
    #                 title='Frecuencia Registrada',
    #                 content=Label(text=f'Frecuencia de carrier ingresada: {frecuencia_carrier} Hz'),
    #                 size_hint=(None, None),
    #                 size=(400, 200)
    #             )
    #             popup_result.open()

    #             ############################# ###########################
    #             # Guardar el valor o exportarlo a otra función
    #             self.frecuencia_carrier = frecuencia_carrier
    #             # self.get_carrier(frecuencia)
    #             # print(f"Frecuncia desde kivy: {self.frecuencia_carrier}");
    #             ############################# ###########################3

    #         except ValueError:
    #             popup_error = Popup(
    #                 title='Entrada inválida',
    #                 content=Label(text='Por favor, ingrese un número válido.'),
    #                 size_hint=(None, None),
    #                 size=(350, 200)
    #             )
    #             popup_error.open()

    #     btn_confirmar.bind(on_press=confirmar_carrier_freq)
    #     self.popup_freq_mod.open()

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
    

    ########################### Función Set error de fase
    # def set_phase_error(self, instance):
    #     layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

    #     label = Label(text='Ingrese error de fase (en grados):')
    #     layout.add_widget(label)

    #     self.input_fase = TextInput(
    #         multiline=False,
    #         input_filter='float',
    #         hint_text='Ej: 45.0'
    #     )
    #     layout.add_widget(self.input_fase)

    #     btn_confirmar = Button(text='Confirmar', size_hint=(1, 0.3))
    #     layout.add_widget(btn_confirmar)

    #     self.popup_fase = Popup(
    #         title='Error de Fase',
    #         content=layout,
    #         size_hint=(None, None),
    #         size=(400, 250)
    #     )

    #     def confirmar_error(instance):
    #         try:
    #             error = float(self.input_fase.text)
    #             self.popup_fase.dismiss()
    #             popup_result = Popup(
    #                 title='Fase Registrada',
    #                 content=Label(text=f'Error de fase ingresado: {error} grados'),
    #                 size_hint=(None, None),
    #                 size=(350, 200)
    #             )
    #             popup_result.open()
                
    #             ############################# ###########################
    #             # Guardar el valor o llamarlo desde otra función
    #             self.valor_error_fase = error
    #             # print(f"Error valor fase: {self.valor_error_fase}")
    #             # self.aplicar_error_fase(error)
    #             # print(f"Aplicar valor fase: {self.aplicar_valor_error_fase}")
    #             ############################# ###########################

    #         except ValueError:
    #             popup_error = Popup(
    #                 title='Entrada inválida',
    #                 content=Label(text='Por favor, ingrese un número válido.'),
    #                 size_hint=(None, None),
    #                 size=(350, 200)
    #             )
    #             popup_error.open()

    #     btn_confirmar.bind(on_press=confirmar_error)
    #     self.popup_fase.open()
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

    
    ########################### Función Set error de frecuencia
    # def set_freq_error(self, instance):
    #     layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

    #     label = Label(text='Ingrese error de frecuencia (en Hertz/radianes):')
    #     layout.add_widget(label)

    #     self.input_fase = TextInput(
    #         multiline=False,
    #         input_filter='float',
    #         hint_text='Ej: 45.0'
    #     )
    #     layout.add_widget(self.input_fase)

    #     btn_confirmar = Button(text='Confirmar', size_hint=(1, 0.3))
    #     layout.add_widget(btn_confirmar)

    #     self.popup_fase = Popup(
    #         title='Error de Fase',
    #         content=layout,
    #         size_hint=(None, None),
    #         size=(400, 250)
    #     )

    #     def confirmar_error(instance):
    #         try:
    #             # Exxportar este error de fase 
    #             error_freq = float(self.input_fase.text)
    #             self.popup_fase.dismiss()
    #             popup_result = Popup(
    #                 title='Fase Registrada',
    #                 content=Label(text=f'Error de fase ingresado: {error_freq} grados'),
    #                 size_hint=(None, None),
    #                 size=(350, 200)
    #             )
    #             popup_result.open()

    #             # Guardar el valor o llamarlo desde otra función
    #             self.valor_error_freq = error_freq
    #             # self.aplicar_error_fase(error_freq)

    #         except ValueError:
    #             popup_error = Popup(
    #                 title='Entrada inválida',
    #                 content=Label(text='Por favor, ingrese un número válido.'),
    #                 size_hint=(None, None),
    #                 size=(350, 200)
    #             )
    #             popup_error.open()

    #     btn_confirmar.bind(on_press=confirmar_error)
    #     self.popup_fase.open()

    def set_freq_error(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text='Ingrese error de frecuencia (en Hertz) [±25%×fc]:')
        layout.add_widget(label)

        self.input_freq = TextInput(
            multiline=False,
            input_filter='float',
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
                # samplerate_input_signal, input_signal = wavfile.read(ruta_archivo)
                data, samplerate = sf.read(ruta_archivo)
                # sd.play(input_signal, samplerate_input_signal)
                self.popup.dismiss()
                self.get_wav_info(ruta_archivo)

        btn_select.bind(on_press=on_select)
        self.popup.open()
    
    # Usando librería soundfile
    def get_wav_info(self, ruta_archivo):
        try:
            with sf.SoundFile(ruta_archivo) as f:
                data_audio = f.read(dtype='float32')
                n_channels = f.channels
                samplerate = f.samplerate
                n_frames = len(f)
                duration = n_frames / samplerate
                subtype = f.subtype  # Por ejemplo: 'PCM_16'
                
                self.audio_data = data_audio
                self.audio_n_canales = n_channels
                self.audio_samplerate = samplerate

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

    ########################### Función Iniciar modulación
    def init_mod(self, instance):
        # Obtener valores digitados desde la interfaz
        print(f"Longitud de data {len(self.audio_data)}")
        print(f"SSB tipo SC or FC: {self.ssb_tipo}")
        print(f"Banda lateral: {self.banda_lateral}")
        print(f"Frecuencia portadora: {self.frecuencia_carrier}")
        print(f"Error fase: {self.valor_error_fase}")
        print(f"Error frecuencia: {self.valor_error_freq}")
        print(f"Ruta de archivo: {self.pwd_archivo}")

        print(f'Numero de canales: {self.audio_n_canales}') # Mono (1) o estéreo (2)
        print(f'Frecuencia de muestreo: {self.audio_samplerate}')

        ssb = SSB()
        usb, lsb = ssb.ssb_mono_mod(self.audio_data, self.audio_samplerate, self.frecuencia_carrier, "sc", "usb")

        np.save("signal_mod.npy", usb)  # Guarda en disco

        # Grafica en el tiempo
        subprocess.Popen([
                    sys.executable, "src/script_plot.py",
                    "signal.npy",
                    str(self.audio_samplerate),
                    "senal"  # espectro, "senal", o "ambos"
                ])
        
        # Grafica en el espectro
        subprocess.Popen([
                    sys.executable, "src/script_plot.py",
                    "signal.npy",
                    str(self.audio_samplerate),
                    "espectro"  # espectro, "senal", o "ambos"
                ])
        
        banda_demod = ssb.ssb_mono_demod("usb", usb, self.frecuencia_carrier, self.audio_samplerate)
        np.save("signal_demod.npy", usb)  # Guarda en disco
        subprocess.Popen([
                    sys.executable, "src/script_plot.py",
                    "signal.npy",
                    str(self.audio_samplerate),
                    "senal"  # espectro, "senal", o "ambos"
                ])