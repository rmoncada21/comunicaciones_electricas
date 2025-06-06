import numpy as np
import matplotlib.pyplot as plt
import sys

class signal_plot:
    # def __init__(self, f_m=1000, f_c=3000, fs=10000, dur=0.01):
    def __init__(self, signal, fs, dur=0.01):
        # self.f_m = f_m
        # self.f_c = f_c
        self.fs = fs
        self.dur = dur

        # # Crear señales al instanciar
        # self.t = np.linspace(0, self.dur, int(self.fs * self.dur), endpoint=False)
        N = len(signal)
        self.t = np.linspace(0, N / fs, N, endpoint=False)
        # self.mensaje = np.sin(2 * np.pi * self.f_m * self.t)
        # self.portadora = np.cos(2 * np.pi * self.f_c * self.t)
        # self.modulada = self.mensaje * self.portadora
        self.modulada = signal

    def graficar_senal(self):
        plt.figure(figsize=(10, 4))
        plt.plot(self.t, self.modulada)
        plt.title(f"Señal DSB-SC (f_m=Hz, f_c=Hz)")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Amplitud")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def graficar_espectro(self):
        espectro = np.abs(np.fft.fft(self.modulada)) / len(self.modulada)
        freqs = np.fft.fftfreq(len(self.modulada), d=1/self.fs)

        plt.figure(figsize=(10, 4))
        plt.plot(np.fft.fftshift(freqs), np.fft.fftshift(espectro))
        plt.title("Espectro de la señal DSB-SC")
        plt.xlabel("Frecuencia [Hz]")
        plt.ylabel("Magnitud")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def main():
    # signal = float(sys.argv[1]) if len(sys.argv) > 1 else 1000
    signal = np.load(sys.argv[1])
    f_s = float(sys.argv[2]) if len(sys.argv) > 2 else 3000
    # f_c = float(sys.argv[2]) if len(sys.argv) > 2 else 3000
    modo = sys.argv[3] if len(sys.argv) > 3 else "ambos"  # "senal", "espectro", o "ambos"

    modulador = signal_plot(signal, f_s)

    if modo == "senal":
        modulador.graficar_senal()
    elif modo == "espectro":
        modulador.graficar_espectro()
    else:
        modulador.graficar_senal()
        modulador.graficar_espectro()


if __name__ == "__main__":
    main()

