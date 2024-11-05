%% Función - fdm
% -------------------------------------------------------------------------
% Descripción:
% La función `fdm` realiza la modulación AM de un conjunto de señales de 
% mensaje y luego multiplexa estas señales en una sola señal FDM (Frequency 
% Division Multiplexing). Se retorna la señal FDM junto con el vector de 
% señales AM moduladas para su posterior análisis o graficado.
%
% Parámetros de entrada:
%   vector_mensaje - Cell array que contiene las señales de mensaje a modular (mt1, mt2, mt3)
%   fs             - Frecuencia de muestreo (Hz)
%   vector_fc      - Vector con las frecuencias de portadora para cada señal de mensaje
%   vector_fm      - Vector con las frecuencias de cada señal de mensaje
%
% Parámetro de salida:
%   fdm_celda      - Cell array con los siguientes elementos:
%                     {1} -> fdm: Señal multiplexada en frecuencia (FDM)
%                     {2} -> am_signal_vector: Cell array con las señales 
%                           moduladas AM individuales
% -------------------------------------------------------------------------

function fdm_celda = fdm(vector_mensaje, fs, vector_fc, vector_fm)
    % Modulación AM de cada señal de mensaje con su frecuencia de portadora
    % ---------------------------------------------------------------------
    % Cada señal de mensaje es modulada en amplitud utilizando la función `modulate`
    % en MATLAB. Las señales moduladas se almacenan en un vector para referencia.
    
    am_signal1 = modulate(vector_mensaje{1}, vector_fc(1), fs, 'am');  % Señal AM para mensaje 1
    am_signal2 = modulate(vector_mensaje{2}, vector_fc(2), fs, 'am');  % Señal AM para mensaje 2
    am_signal3 = modulate(vector_mensaje{3}, vector_fc(3), fs, 'am');  % Señal AM para mensaje 3
    
    % Agrupación de las señales AM moduladas en un cell array
    am_signal_vector = {am_signal1, am_signal2, am_signal3};
    
    % Multiplexación en Frecuencia (FDM)
    % ---------------------------------------------------------------------
    % La señal FDM se obtiene sumando las señales moduladas en AM. Esto combina
    % todas las señales moduladas en una sola señal de banda ancha.
    
    fdm = am_signal1 + am_signal2 + am_signal3;  % Señal FDM multiplexada
    
    % Salida
    % ---------------------------------------------------------------------
    % fdm_celda devuelve un cell array con la señal FDM completa y el vector
    % de señales AM individuales para su posterior análisis.
    
    fdm_celda = {fdm, am_signal_vector};
end