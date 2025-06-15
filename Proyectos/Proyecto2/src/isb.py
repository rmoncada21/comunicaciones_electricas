# import numpy as np
# import matplotlib.pyplot as plt
# import sounddevice as sd
# from scipy.signal import butter, filtfilt, hilbert
# # from scipy.fft import fft, fftfreq, fftshift

# class ISB:
#     def __init__(self):
#         pass

#     # Filtro pasa bajas como método interno
#     def _lowpass(self, signal, fs, cutoff=5000, order=6):
#         nyq = 0.5 * fs
#         normal_cutoff = cutoff / nyq
#         b, a = butter(order, normal_cutoff, btype='low')
#         return filtfilt(b, a, signal)

#     #################### CHECKPOINT
#     # Modulación ISB
#     # def isb_modulate(self, m1, m2, fs, fc):
#     #     N = min(len(m1), len(m2))
#     #     m1 = m1[:N]
#     #     m2 = m2[:N]
#     #     t = np.arange(N) / fs

#     #     cos_carrier = np.cos(2 * np.pi * fc * t)
#     #     sin_carrier = np.sin(2 * np.pi * fc * t)

#     #     s_isb = m1 * cos_carrier + m2 * sin_carrier
#     #     return s_isb, t, cos_carrier, sin_carrier


#     def isb_modulate(self, audio1, audio2, fs, fc, error_fase, error_frecuencia):
#         if audio1.ndim > 1:
#             audio1 = audio1[:, 0]  # tomar solo el canal izquierdo
#         if audio2.ndim > 1:
#             audio2 = audio2[:, 0]  # tomar solo el canal izquierdo
        
#         m1 = audio1.astype(np.float32)
#         m2 = audio2.astype(np.float32)
#         # m1 /= np.max(np.abs(m1))
#         # m2 /= np.max(np.abs(m2))

#         # 4. Asegurar que ambas señales tengan la misma longitud
#         N = min(len(m1), len(m2))
#         m1 = m1[:N]
#         m2 = m2[:N]
#         t = np.arange(N) / fs

#         error_fase_rad = np.deg2rad(error_fase)
#         print(f"Radianes {error_fase_rad}")
#         print(f"Error de frecuencia {fc + error_frecuencia}")
#         # 5. Modulación ISB (portadora en fase y en cuadratura)
#         # fc = 5000  # frecuencia de portadora en Hz
#         cos_carrier = np.cos(2 * np.pi * (fc + error_frecuencia) * t + error_fase_rad)
#         sin_carrier = np.sin(2 * np.pi * (fc + error_frecuencia) * t + error_fase_rad)

#         # TODO: cambiar de cuadratura a isb (ambas bandas laterales de ssb)
#         # s_isb = m1 * cos_carrier + m2 * sin_carrier  # señal modulada ISB
#         s_isb = m1 * cos_carrier - hilbert(m1) * sin_carrier + m2 * cos_carrier + hilbert(m2) * cos_carrier
#         return s_isb, t, cos_carrier, sin_carrier

#     # Demodulación ISB
#     # def isb_demodulate(self, s_isb, fs, fc, cos_carrier, sin_carrier):
#     #     y1 = 2 * s_isb * cos_carrier
#     #     y2 = 2 * s_isb * sin_carrier

#     #     m1_rec = self._lowpass(y1, fs)
#     #     m2_rec = self._lowpass(y2, fs)

#     #     return m1_rec, m2_rec

#     def isb_demodulate(self, s_isb, fs, fc, t):
        
#         cos_carrier = np.cos(2 * np.pi * fc * t)
#         sin_carrier = np.sin(2 * np.pi * fc * t)
        
#         y1 = 2 * s_isb * cos_carrier
#         y2 = 2 * s_isb * sin_carrier

#         m1_rec = self._lowpass(y1, fs)
#         m2_rec = self._lowpass(y2, fs)

#         return m1_rec, m2_rec

#     # # Opcional: reproducir audio
#     # def play_audio(self, signal, fs, label="Audio"):
#     #     print(f"Reproduciendo {label}...")
#     #     sd.play(signal / np.max(np.abs(signal)), fs)
#     #     sd.wait()

#     # # Opcional: visualizar espectro
#     # def plot_spectrum(self, signal, fs, title="Espectro"):
#     #     N = len(signal)
#     #     freqs = fftshift(fftfreq(N, 1 / fs))
#     #     spectrum = fftshift(np.abs(fft(signal))) / N
#     #     plt.figure(figsize=(10, 4))
#     #     plt.plot(freqs, spectrum)
#     #     plt.title(title)
#     #     plt.xlabel("Frecuencia [Hz]")
#     #     plt.ylabel("Magnitud")
#     #     plt.grid(True)
#     #     plt.tight_layout()
#     #     plt.show()

#     # # Graficar señales en el tiempo
#     # def plot_time(self, t, m1_rec, m2_rec):
#     #     plt.figure(figsize=(12, 6))
#     #     plt.subplot(2, 1, 1)
#     #     plt.plot(t, m1_rec)
#     #     plt.title("Señal m1 recuperada")
#     #     plt.xlabel("Tiempo [s]")
#     #     plt.ylabel("Amplitud")

#     #     plt.subplot(2, 1, 2)
#     #     plt.plot(t, m2_rec)
#     #     plt.title("Señal m2 recuperada")
#     #     plt.xlabel("Tiempo [s]")
#     #     plt.ylabel("Amplitud")

#     #     plt.tight_layout()
#     #     plt.show()



import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.signal import butter, filtfilt, hilbert


class ISB:
    def __init__(self):
        pass

    # Filtro pasa bajas como método interno
    def _lowpass(self, signal, fs, cutoff=5000, order=6):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low')
        return filtfilt(b, a, signal)

    # Modulación ISB correcta: USB para m1, LSB para m2
    def isb_modulate(self, audio1, audio2, fs, fc, error_fase=0, error_frecuencia=0):
        if audio1.ndim > 1:
            audio1 = audio1[:, 0]
        if audio2.ndim > 1:
            audio2 = audio2[:, 0]

        m1 = audio1.astype(np.float32)
        m2 = audio2.astype(np.float32)

        # Asegurar misma longitud
        N = min(len(m1), len(m2))
        m1 = m1[:N]
        m2 = m2[:N]
        t = np.arange(N) / fs

        # Preparar errores
        error_fase_rad = np.deg2rad(error_fase)
        fc_err = fc + error_frecuencia

        # Señales analíticas
        m1_analytic = hilbert(m1)
        m2_analytic = hilbert(m2)

        # Lado superior: m1(t)
        usb = np.real(m1_analytic * np.exp(1j * (2 * np.pi * fc_err * t + error_fase_rad)))

        # Lado inferior: m2(t)
        lsb = np.real(m2_analytic * np.exp(-1j * (2 * np.pi * fc_err * t + error_fase_rad)))

        s_isb = usb + lsb

        # Portadoras también pueden ser devueltas si lo necesitas para debug
        cos_carrier = np.cos(2 * np.pi * fc_err * t + error_fase_rad)
        sin_carrier = np.sin(2 * np.pi * fc_err * t + error_fase_rad)

        return s_isb, t, cos_carrier, sin_carrier

    # Demodulación coherente ISB
    def isb_demodulate(self, s_isb, fs, fc, t):
        # Portadoras ideales (sin errores para este caso)
        cos_carrier = np.cos(2 * np.pi * fc * t)
        sin_carrier = np.sin(2 * np.pi * fc * t)

        # Multiplicación sincrónica
        I = 2 * s_isb * cos_carrier
        Q = 2 * s_isb * sin_carrier

        # Filtrado pasa bajas
        I_filtered = self._lowpass(I, fs)
        Q_filtered = self._lowpass(Q, fs)

        # Señales analíticas recuperadas
        I_hilbert = np.imag(hilbert(I_filtered))
        Q_hilbert = np.imag(hilbert(Q_filtered))

        # Recuperación aproximada de m1 y m2
        m1_rec = 0.5 * (I_filtered + Q_hilbert)
        m2_rec = 0.5 * (I_filtered - Q_hilbert)

        return m1_rec, m2_rec
