import os
import subprocess
import sys

import soundfile as sf
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import butter, filtfilt, hilbert

# from src.script_plot import ModuladorDSBSC

class SSB:
    # constructor
    def __init__(self):
        pass

    # def ssb_mono_mod(self, audio_data, audio_samplerate, SC_or_FC="SC", usb_or_lsb="USB", frecuencia_carrier=1000, error_fase=0, error_frecuencia=0):
    def ssb_mono_mod(self, audio_data, audio_samplerate, SC_or_FC, USB_or_LSB, frecuencia_carrier, error_fase, error_frecuencia):
        # sd.play(audio_data, audio_samplerate)
        # sd.wait()
        # print(f"{error_fase}")
        # Generar vector tiempo
        N = len(audio_data)
        # print(f"{N}")
        time = np.linspace(0, N / audio_samplerate, N, endpoint=False)
        # print(f"Longitud de time: {len(time)}")

        analytic_signal = hilbert(audio_data)
        mensaje = np.real(analytic_signal)
        mensaje_hat = np.imag(analytic_signal)

        # Convertir error de fase en radianes
        error_fase_rad = np.deg2rad(error_fase)  # convierte a radianes
        # print(f"{error_fase}")
        # print(f"{error_fase_rad}")

        if SC_or_FC == "FC":
            full_carrier = np.cos(2 * np.pi * (frecuencia_carrier + error_frecuencia) * time + error_fase_rad)
        else:
            full_carrier = 0

        # Carriers
        cos_carrier = np.cos(2 * np.pi * (frecuencia_carrier + error_frecuencia) * time + error_fase_rad)
        sin_carrier = np.sin(2 * np.pi * (frecuencia_carrier + error_frecuencia) * time + error_fase_rad)
        
        # print(f"{full_carrier}")
        # print(f"{-cos_carrier}")
        # print(f"{-sin_carrier}")
        # print(f"{cos_carrier}")
        # print(f"{sin_carrier}")

        # --- Generar bandas laterales ---
        usb = full_carrier + mensaje * cos_carrier - mensaje_hat * sin_carrier  # USB
        lsb = full_carrier + mensaje * cos_carrier + mensaje_hat * sin_carrier  # LSB

        if USB_or_LSB == "USB":
            return usb
        else:
            return lsb
    

    # def ssb_mono_demod(self, nombre_banda, banda_lateral, frecuencia_carrier, sample_rate):
    def ssb_mono_demod_sc(self, banda_lateral, frecuencia_carrier, sample_rate):
        # --- Filtro pasa bajas ---
        def lowpass(signal, fs, cutoff=5000, order=6):  # cutoff según el ancho de banda del audio
            nyq = fs / 2
            b, a = butter(order, cutoff / nyq, btype='low')
            return filtfilt(b, a, signal)

        N = len(banda_lateral)
        # print(f"{N}")
        time = np.linspace(0, N / sample_rate, N, endpoint=False)

        # --- Demodulación coherente USB ---
        oscilador_local = np.cos(2 * np.pi * frecuencia_carrier * time)

        banda_lateral = banda_lateral * 2 * oscilador_local  # recuperar m(t)
        banda_lateral_filtered = lowpass(banda_lateral, sample_rate)

        # --- Demodulación coherente LSB ---
        # demod_lsb = lsb * 2 * np.cos(2 * np.pi * fc * t)
        # demod_lsb_filtered = lowpass(demod_lsb, fs)

        # --- Reproducción de audio demodulado ---
        # print(f"Reproduciendo audio demodulado desde {nombre_banda}")
        # sd.play(banda_lateral_filtered / np.max(np.abs(banda_lateral_filtered)), sample_rate)
        # sd.wait()

        # print("Reproduciendo audio demodulado desde LSB...")
        # sd.play(demod_lsb_filtered / np.max(np.abs(demod_lsb_filtered)), fs)
        # sd.wait()
        
        # normalizar
        # banda_lateral_filtered = banda_lateral_filtered / np.max(np.abs(banda_lateral_filtered))

        return banda_lateral_filtered

    # TODO def ssb_mono_demod_fc
    def ssb_mono_demod_fc(self, banda_lateral, frecuencia_carrier, sample_rate, USB_or_LSB="USB"):
        
        def lowpass(signal, fs, cutoff=5000, order=6):
            nyq = fs / 2
            b, a = butter(order, cutoff / nyq, btype='low')
            return filtfilt(b, a, signal)

        N = len(banda_lateral)
        time = np.linspace(0, N / sample_rate, N, endpoint=False)

        # Portadora local coherente
        if USB_or_LSB == "USB":
            portadora_local = np.cos(2 * np.pi * frecuencia_carrier * time)
        else:  # LSB
            portadora_local = np.cos(2 * np.pi * frecuencia_carrier * time)
            # Alternativamente se puede usar sin() si la modulación fue con sin()

        # Multiplicación coherente
        producto = 2 * banda_lateral * portadora_local

        # Filtro pasa bajas para recuperar m(t)
        senal_demodulada = lowpass(producto, sample_rate)

        return senal_demodulada
