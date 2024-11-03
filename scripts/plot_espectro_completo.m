function plot_espectro_completo(signal, fc, fs, titulo)
    % Calcular el tamaño de la señal
    N = length(signal);
    
    % Generar vector de frecuencias
    f = (-N/2:N/2-1) * (fs / N);  % Obtener frecuencias tanto positivas como negativas
    
    % Calcular la Transformada Rápida de Fourier (FFT)
    fft_signal = fft(signal);  % Transformada de Fourier
    pos_fft_signal = abs(fft_signal);  % Magnitud de la FFT
    fft_normalizada = 2 * (pos_fft_signal / N);  % Normalizar la FFT (considerando la conservación de la energía)
    
    % Reorganizar la FFT para centrarla en 0
    fft_shifted = fftshift(fft_normalizada);  % Desplazar la FFT para centrar en 0
    
    % Visualización del espectro
    figure;
    plot(f, fft_shifted, 'LineWidth', 1.5);  % Graficar con línea gruesa para mayor claridad
    
    % Personalización de la gráfica
    title(['Espectro de la Señal ', titulo, ' a frecuencia modulada ', num2str(fc)], ...
          'FontSize', 14, 'FontWeight', 'bold');  % Título de la gráfica
    xlabel('Frecuencia (Hz)', 'FontSize', 12);   % Etiqueta para el eje X
    ylabel(['|', titulo, '(f)|'], 'FontSize', 12);  % Etiqueta para el eje Y
    xlim([-fs/2, fs/2]);  % Limitar el espectro para mostrar ambas partes
    grid on;  % Activar cuadrícula para facilitar la lectura
end
