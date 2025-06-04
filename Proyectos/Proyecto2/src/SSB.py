import os
import subprocess
import sys

import soundfile as sf
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import butter, filtfilt, hilbert

# from src.script_plot import ModuladorDSBSC

# frecuencia de portadora ?
# error de frecuencia ?
# error de fase ?
# archivo ?

class SSB:
    # constructor
    def __init__(self):
        pass

    def ssb_mono_mod(self, audio_data, audio_samplerate, frecuencia_carrier, sc_or_fc, nombre_banda):
        sd.play(audio_data, audio_samplerate)
        sd.wait()

        N = len(audio_data)
        print(f"{N}")
        time = np.linspace(0, N / audio_samplerate, N, endpoint=False)
        print(f"Longitud de time: {len(time)}")

        analytic_signal = hilbert(audio_data)
        mensaje = np.real(analytic_signal)
        mensaje_hat = np.imag(analytic_signal)

        # Carriers
        cos_carrier = np.cos(2 * np.pi * frecuencia_carrier * time)
        sin_carrier = np.sin(2 * np.pi * frecuencia_carrier * time)

        # --- Generar bandas laterales ---
        usb = mensaje * cos_carrier - mensaje_hat * sin_carrier  # USB
        lsb = mensaje * cos_carrier + mensaje_hat * sin_carrier  # LSB

        # --- Reproducción de señales moduladas ---
        print("Reproduciendo USB ")
        # sd.play(usb / np.max(np.abs(usb)), samplerate=audio_samplerate)
        sd.play(usb, audio_samplerate)
        sd.wait()

        print("Reproduciendo LSB ")
        # sd.play(lsb / np.max(np.abs(lsb)), samplerate=audio_samplerate)
        sd.play(lsb, audio_samplerate)
        sd.wait()

        # subprocess.Popen([
        #     sys.executable, "script_plot.py",
        #     str(500),
        #     str(frecuencia_carrier),
        #     "espectro"  # o "senal", o "ambos"
        # ])
        
        return usb, lsb
    
    def ssb_mono_demod(self, nombre_banda, banda_lateral, frecuencia_carrier, sample_rate):
        
        # --- Filtro pasa bajas ---
        def lowpass(signal, fs, cutoff=4000, order=6):  # cutoff según el ancho de banda del audio
            nyq = fs / 2
            b, a = butter(order, cutoff / nyq, btype='low')
            return filtfilt(b, a, signal)

        N = len(banda_lateral)
        # print(f"{N}")
        time = np.linspace(0, N / sample_rate, N, endpoint=False)

        # --- Demodulación coherente USB ---
        banda_lateral = banda_lateral * 2 * np.cos(2 * np.pi * frecuencia_carrier * time)  # recuperar m(t)
        banda_lateral_filtered = lowpass(banda_lateral, sample_rate)

        # --- Demodulación coherente LSB ---
        # demod_lsb = lsb * 2 * np.cos(2 * np.pi * fc * t)
        # demod_lsb_filtered = lowpass(demod_lsb, fs)

        # --- Reproducción de audio demodulado ---
        print(f"Reproduciendo audio demodulado desde {nombre_banda}")
        sd.play(banda_lateral_filtered / np.max(np.abs(banda_lateral_filtered)), sample_rate)
        sd.wait()

        # print("Reproduciendo audio demodulado desde LSB...")
        # sd.play(demod_lsb_filtered / np.max(np.abs(demod_lsb_filtered)), fs)
        # sd.wait()

        return banda_lateral_filtered
