%% Función - plot_espectro
% -------------------------------------------------------------------------
% Descripción:
% La función `plot_espectro` calcula y grafica el espectro de una señal
% utilizando la Transformada Rápida de Fourier (FFT). La gráfica muestra
% la magnitud de la señal en función de la frecuencia, permitiendo analizar
% las componentes espectrales de la señal.
%
% Parámetros de entrada:
%   signal - Vector que representa la señal cuya transformada se quiere calcular
%   fc     - Frecuencia de portadora (Hz) para referencia en la gráfica
%   fs     - Frecuencia de muestreo (Hz), utilizada para calcular las frecuencias
%   titulo  - Título adicional para la gráfica, que se incluirá en la leyenda
%
% Salida:
%   No tiene salida, pero genera una gráfica del espectro de la señal.
% -------------------------------------------------------------------------

function plot_espectro(signal, fc, fs, titulo)
    % Calcular el tamaño de la señal
    N = length(signal);
    
    % Generar vector de frecuencias
    f = (0:N-1) * (fs / N);  % Obtener la parte positiva de las frecuencias
    
    % Calcular la Transformada Rápida de Fourier (FFT)
    fft_signal = fft(signal);  % Transformada de Fourier
    pos_fft_signal = abs(fft_signal);  % Magnitud de la FFT
    fft_normalizada = 2 * (pos_fft_signal / N);  % Normalizar la FFT (considerando la conservación de la energía)
    
    % Visualización del espectro
    figure;
    plot(f, fft_normalizada, 'LineWidth', 1.5);  % Graficar con línea gruesa para mayor claridad
    
    % Personalización de la gráfica
    title(['Espectro de la Señal ', titulo, ' a frecuencia modulada ', num2str(fc)], ...
          'FontSize', 14, 'FontWeight', 'bold');  % Título de la gráfica
    xlabel('Frecuencia (Hz)', 'FontSize', 12);   % Etiqueta para el eje X
    ylabel(['|', titulo, '(f)|'], 'FontSize', 12);  % Etiqueta para el eje Y
    xlim([0, 2 * fc]);  % Limitar el espectro para centrarse en la portadora y las bandas laterales
    grid on;  % Activar cuadrícula para facilitar la lectura
end