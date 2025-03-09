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
    
    return s_t #note que s_t es una unica señal utilizando un unico array, NO una lista

def canal(s_t):
    
    #Note que los parámetros mu (media) y sigma (desviacion) del ruido blanco Gaussiano deben cambiarse segun especificaciones
    mu=0;
    sigma=0.001;
    
    #Su codigo para el canal va aca. 
    
    s_t_prima=s_t #eliminar cuando se tenga solucion propuesta
    
    return s_t_prima


def receptor(s_t_prima,f_rf):
    
    # Note que f_rf es la frecuencia utilizada para la seleccionar la señal que se desea demodular
    
    #Su codigo para el receptor va aca  
       
    
    m_t_reconstruida=s_t_prima #eliminar cuando se tenga solucion propuesta
    
    #note que en el caso de multiples señales
    
    return m_t_reconstruida



## Inicio de ejecucion ##
#Se da con ejemplo de tono, pasandolo por todo el sistema sin ningun cambio

#leer tono desde archivo
samplerate_tono, tono = wavfile.read("datos/tono.wav")

#oir tono rescatado. Esta funcion sirve tambien como transductor de salida 
#Note la importancia de la frecuencia de muestreo (samplerate), la cual es diferente a la frecuencia fm del tono.
sd.play(tono, samplerate_tono)

#Sobremuestreo para evitar problemas de aliasing (de necesitarse)
resampling_factor = 4
samples_new = len(tono) * resampling_factor
samplerate_resampled = samplerate * resampling_factor
print('Cambiando frecuencia de muestreo de '+str(samplerate)+' a '+str(samplerate_resampled))
data_resampled=signal.resample(tono, samples_new).astype(np.int16)
new_length=data_resampled.shape[0] / samplerate_resampled
time_resampled = np.linspace(0., new_length, data_resampled.shape[0])


#agregar el tono a la lista X_t requerida por el transmisor
x_t=[]  #solo para ejemplo, crear lista con el mismo tono 3 veces
x_t.append(tono)
x_t.append(tono)
x_t.append(tono)
print("Se envia una lista con "+str(len(x_t))+" señales")


#llamar funcion de transmisor
s_t=transmisor(x_t)


#llamar funcion que modela el canal
s_t_prima=canal(s_t)

#llamar funcion de receptor
m_t_reconstruida=receptor(s_t_prima)


