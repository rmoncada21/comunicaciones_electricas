# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 11:06:24 2022

Plantilla para Proyecto. 
Curso Comunicaciones Electricas 1. 
Sistema de transmisión y recepción analógica

@author: lcabrera
"""

#importar bibliotecas utiles. De no tenerse alguna (import not found) se debe instalar, generalmente con pip
import scipy.signal
from scipy.io import wavfile 
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

#definicion de 3 bloques principales: TX, canal y RX

def transmisor(x_t):
    
    #x_t debe ser una lista con multiples array (caso de 3 señales) o una sola(caso del tono)
       
    #Su codigo para el transmisor va aca
    
    s_t=x_t[0] #eliminar cuando se tenga solucion propuesta
    sample=x_t[1]
    
    am = dsb_sc(s_t, sample)
    
    return am #note que s_t es una unica señal utilizando un unico array, NO una lista


def receptor(s_t_prima,f_rf):
    
    # Note que f_rf es la frecuencia utilizada para la seleccionar la señal que se desea demodular
    
    #Su codigo para el receptor va aca  
       
    
    m_t_reconstruida=s_t_prima #eliminar cuando se tenga solucion propuesta
    
    #note que en el caso de multiples señales
    
    return m_t_reconstruida

def canal(s_t, samplerate):
    
    #Note que los parámetros mu (media) y sigma (desviacion) del ruido blanco Gaussiano deben cambiarse segun especificaciones
    
    mu=0;
    sigma=0.1 + np.std(s_t)
    
    #Su codigo para el canal va aca. 

    canal_noise = np.random.normal(mu, sigma, s_t.shape[0])
    plot_time_signal("Ruido de canal",canal_noise, samplerate)
    s_t_prima= canal_noise + s_t 
    
    
    #s_t_prima=s_t #eliminar cuando se tenga solucion propuesta
    
    return  s_t_prima


def frecuencia_moduladora(signal, samplerate_signal):
    fft_signal = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal))
    
    frecuencia_pico = np.argmax(np.abs(fft_signal))
    frecuencia_fm = freqs[frecuencia_pico]
    
    return abs(frecuencia_fm * samplerate_signal)


def dsb_sc(signal, samplerate_signal):
    
    fm = frecuencia_moduladora(signal, samplerate_signal)
    fc = 10 * fm

    time = np.linspace(0., signal.shape[0] / samplerate_signal, signal.shape[0])

    # print("time")
    # print(time)

    carrier  = np.cos(2*np.pi*fc*time)
    plot_time_signal("Portadora", carrier, samplerate_signal)

    am_dsbsc = carrier *signal
    plot_time_signal("DSB-SC", am_dsbsc, samplerate_signal)
    # plt.plot(time,am_dsbsc)
    # #plt.plot(time,data)
    # plt.title("Cruce")
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")

    return am_dsbsc


# Grafica la señal con respecto al tiempo
def plot_time_signal(titulo_grafico, signal, samplerate_signal):

    plt.figure()
    #time_signal = np.linspace(0., 1000 / samplerate_signal, 1000) #shape entrega una tupla
    time_signal = np.linspace(0., signal.shape[0] / samplerate_signal, signal.shape[0]) #shape entrega una tupla
    
    plt.plot(time_signal,signal) 
    plt.xlim([0, 0.01]) #mostrar solo parte de la onda
    plt.title(titulo_grafico)
    #plt.show()

    return 0


# Grafica la señal con respecto a la frecuencia
def plot_psd_signal(titulo_grafico, signal, fs):

    (f, S)= scipy.signal.welch(signal, fs, nperseg=4*1024)
    plt.figure()
    plt.semilogy(f, S)
    plt.xlim([0, fs/10])
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    plt.title(titulo_grafico)
    #plt.show()

    return 0
    

## Inicio de ejecucion ##
#Se da con ejemplo de tono, pasandolo por todo el sistema sin ningun cambio

#leer tono desde archivo
#Audio_name = "datos/vowel_1.wav"
Audio_name = "datos/tono.wav"
samplerate_input_signal, input_signal = wavfile.read(Audio_name)

#oir tono rescatado. Esta funcion sirve tambien como transductor de salida 
#Note la importancia de la frecuencia de muestreo (samplerate), la cual es diferente a la frecuencia fm del tono.
sd.play(input_signal, samplerate_input_signal)

#graficar tono
# plt.plot(np.linspace(0., tono.shape[0] / samplerate_input_signal, tono.shape[0]),tono)
# plt.xlim([0, 0.01]) #mostrar solo parte de la onda



#agregar el tono a la lista X_t requerida por el transmisor
x_t=[]  #solo para ejemplo, crear lista con el mismo tono 3 veces
x_t.append(input_signal)
x_t.append(samplerate_input_signal)
x_t.append(input_signal)
x_t.append(input_signal)
print("Se envia una lista con "+str(len(x_t))+" señales")


#llamar funcion de transmisor


s_t=transmisor(x_t)
#s_t=dsb_sc(x_t[0])

plot_time_signal(Audio_name, s_t, samplerate_input_signal)


#llamar funcion que modela el canal
s_t_prima = canal(s_t, samplerate_input_signal)
plot_time_signal("Señal ruidosa", s_t_prima, samplerate_input_signal)

#llamar funcion de receptor
m_t_reconstruida = receptor(s_t_prima, samplerate_input_signal)


# mostrar las graficas
plt.show()

#graficar señal recibida
# plt.plot(np.linspace(0., m_t_reconstruida.shape[0] / samplerate_input_signal, m_t_reconstruida.shape[0]),m_t_reconstruida)
# plt.xlim([0, 0.01]) #mostrar solo parte de la onda









#print(frecuencia_moduladora(input_signal, samplerate_input_signal))