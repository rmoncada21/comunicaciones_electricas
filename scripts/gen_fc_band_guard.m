%% Función - gen_fc_band_guard
% -------------------------------------------------------------------------
% Descripción:
% Esta función calcula las frecuencias de portadora (fc) necesarias para cada
% señal de mensaje dada en `vector_fm`, asegurando que se respete una banda 
% de guarda entre cada par de señales moduladas para evitar interferencias.
%
% Parámetros de entrada:
%   vector_fm    - Vector con las frecuencias de los tonos de mensaje [fm1, fm2, fm3]
%   fc           - Frecuencia de portadora base (Hz)
%   banda_guarda - Banda de guarda entre cada señal modulada (Hz)
%   ancho_banda  - Ancho de banda total asignado para el sistema (Hz)
%
% Parámetro de salida:
%   vector_fc    - Vector con las frecuencias de portadora calculadas [fc1, fc2, fc3]
%
% La función también imprime el ancho de banda total utilizado para verificar
% que esté dentro de los límites especificados.
% -------------------------------------------------------------------------

function vector_fc = gen_fc_band_guard(vector_fm, fc, banda_guarda, ancho_banda)
    % Extraer frecuencias de mensaje individuales
    fm1 = vector_fm(1);     % Frecuencia de mensaje 1
    fm2 = vector_fm(2);     % Frecuencia de mensaje 2
    fm3 = vector_fm(3);     % Frecuencia de mensaje 3
    
    % Calcular frecuencia de portadora para cada mensaje
    % -------------------------------------------------
    % fc1: frecuencia de portadora base, directamente asignada
    fc1 = fc;
    
    % fc2: frecuencia de portadora para el segundo mensaje
    % Sumamos la primera portadora (fc1) con la frecuencia de mensaje 1,
    % la banda de guarda, y la frecuencia de mensaje 2
    fc2 = fc1 + fm1 + banda_guarda + fm2;
    
    % fc3: frecuencia de portadora para el tercer mensaje
    % Sumamos la segunda portadora (fc2) con la frecuencia de mensaje 2,
    % la banda de guarda, y la frecuencia de mensaje 3
    fc3 = fc2 + fm2 + banda_guarda + fm3;

    % Calcular el ancho de banda total utilizado por las portadoras
    % -------------------------------------------------------------
    % bt: ancho de banda necesario, calculado desde la frecuencia mínima hasta la máxima
    bt = (fc3 + fm3) - (fc1 - fm1);
    
    % Mostrar el ancho de banda calculado
    disp('Ancho de banda total utilizado:');
    disp(2 * bt);  % Multiplicamos por 2 para tener el ancho de banda bilateral

    % Vector de frecuencias de portadora a retornar
    vector_fc = [fc1, fc2, fc3];
end