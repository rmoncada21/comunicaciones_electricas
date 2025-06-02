# graficar.py
import numpy as np
import matplotlib.pyplot as plt
import sys

def gra_main():
    # Obtener argumentos desde la línea de comandos
    f_m = float(sys.argv[1]) if len(sys.argv) > 1 else 1000  # Frecuencia del mensaje
    f_c = float(sys.argv[2]) if len(sys.argv) > 2 else 3000  # Frecuencia de la portadora

    fs = 10000
    t = np.linspace(0, 0.01, int(fs * 0.01), endpoint=False)
    mensaje = np.sin(2 * np.pi * f_m * t)
    portadora = np.cos(2 * np.pi * f_c * t)
    modulada = mensaje * portadora

    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, modulada)
    plt.title(f"Señal DSB-SC (f_m={f_m}Hz, f_c={f_c}Hz)")

    freqs = np.fft.fftfreq(len(modulada), d=1/fs)
    espectro = np.abs(np.fft.fft(modulada)) / len(modulada)

    plt.subplot(2, 1, 2)
    plt.plot(np.fft.fftshift(freqs), np.fft.fftshift(espectro))
    plt.title("Espectro de la señal DSB-SC")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    gra_main()