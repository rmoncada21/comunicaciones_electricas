%% Función - plot_tiempo
% -------------------------------------------------------------------------
% Descripción:
% La función `plot_tiempo` grafica una señal en el dominio del tiempo.
% Crea una nueva figura y muestra la señal `signal` en función del vector 
% de tiempo `tiempo`, añadiendo etiquetas y título a la gráfica para una 
% mejor interpretación visual.
%
% Parámetros de entrada:
%   signal - Vector con la señal a graficar (ej. señal de mensaje o señal modulada)
%   tiempo - Vector de tiempo correspondiente a la señal (eje X)
%   titulo - Título de la gráfica, proporcionado como cadena de texto
% -------------------------------------------------------------------------

function plot_tiempo(signal, tiempo, titulo)
    % Crear nueva figura para la gráfica
    figure;
    
    % Graficar señal en función del tiempo
    plot(tiempo, signal, 'LineWidth', 1.5);  % Línea más gruesa para mayor claridad
    
    % Personalización de la gráfica
    title(titulo, 'FontSize', 14, 'FontWeight', 'bold');   % Título de la gráfica
    xlabel('Tiempo (s)', 'FontSize', 12);                  % Etiqueta para el eje X
    ylabel('Amplitud', 'FontSize', 12);                    % Etiqueta para el eje Y
    grid on;                                               % Activar cuadrícula para facilitar la lectura
end