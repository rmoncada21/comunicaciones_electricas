import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.signal import welch

class Signal_plot:
    def __init__(self):
        pass

    def graficar_senal(self, titulo, signal, fs, lim):
        N = len(signal)
        t = np.linspace(0, N / fs, N, endpoint=False)
        
        plt.figure(figsize=(10, 4))
        plt.plot(t, signal)
        # plt.title(f"Señal DSB-SC (f_m=Hz, f_c=Hz)")
        plt.title(f"Grafico temporal de la señal {titulo}")
        plt.xlabel("Tiempo [s]")
        plt.xlim(0, lim)
        plt.ylabel("Amplitud")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Graficar parte positiva
    def graficar_espectro(self, titulo, signal, samplerate):
        espectro = np.abs(np.fft.fft(signal)) / len(signal)
        freqs = np.fft.fftfreq(len(signal), d=1/samplerate)

        # Aplicar fftshift
        espectro_shifted = np.fft.fftshift(espectro)
        freqs_shifted = np.fft.fftshift(freqs)

        # Filtrar solo las frecuencias positivas
        mask = freqs_shifted >= 0
        freqs_pos = freqs_shifted[mask]
        espectro_pos = espectro_shifted[mask]

        plt.figure(figsize=(12, 4))
        plt.plot(freqs_pos, espectro_pos)
        plt.title(f"Espectro de la señal {titulo}")
        plt.xlabel("Frecuencia [Hz]")
        plt.ylabel("Magnitud")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    
    def graficar_espectro_welch(self,titulo, signal, fs, mult=3):
        nperseg = 4 * 1024
        f_fc, Pxx_fc = welch(signal, fs, nperseg=nperseg)
        # f_usb, Pxx_usb = welch(ssb_usb, fs, nperseg=nperseg)
        
        plt.figure(figsize=(12, 6))

        plt.semilogy(f_fc, Pxx_fc)
        plt.title(f"Espectro de la señal {titulo}")
        plt.xlabel("Frecuencia [Hz]")
        plt.ylabel("PSD [V²/Hz]")
        plt.xlim([0, f_fc[np.argmax(Pxx_fc)]*mult])
        plt.grid(True)
        plt.show()        
        

def main():
    # signal = float(sys.argv[1]) if len(sys.argv) > 1 else 1000
    signal = np.load(sys.argv[1])
    f_s = float(sys.argv[2]) if len(sys.argv) > 2 else 3000
    # f_c = float(sys.argv[2]) if len(sys.argv) > 2 else 3000
    modo = sys.argv[3] if len(sys.argv) > 3 else "ambos"  # "senal", "espectro", o "ambos"
    lim = float(sys.argv[4]) if len(sys.argv) > 4 else 1
    titulo = sys.argv[5] if len(sys.argv) > 5 else "Agregar titulo"
    
    # titulo_espectro = sys.argv[6] if len(sys.argv) > 6 else "Agregar titulo_espectro"

    # modulador = Signal_plot(signal, f_s)
    modulador = Signal_plot()

    if modo == "senal":
        modulador.graficar_senal(titulo, signal, f_s, lim)
    elif modo == "espectro":
        modulador.graficar_espectro_welch(titulo, signal, f_s)
    else:
        modulador.graficar_senal(titulo, signal, f_s, lim)
        modulador.graficar_espectro_welch(titulo, signal, f_s)

if __name__ == "__main__":
    main()

