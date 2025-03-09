function senal_filtrada = filtroPasoBanda(signal, frecuencia_intermedia, f_central, fs)
    % Filtro Paso Banda
    % Crea un filtro paso banda Butterworth para aislar un tono en la FI.
    %
    % Entradas:
    %   f_central   - Frecuencia central del tono a filtrar (en Hz)
    %   ancho_banda - Ancho de banda del filtro (en Hz)
    %   fs          - Frecuencia de muestreo de la señal (en Hz)
    %
    % Salidas:
    %   b, a - Coeficientes del filtro paso banda

    % Calcular las frecuencias de corte del filtro paso banda
    ancho_banda = 10e3;
    f1 = (frecuencia_intermedia) - ancho_banda / 2;
    f2 = (frecuencia_intermedia) + ancho_banda / 2;

    % Convertir las frecuencias de corte a frecuencias normalizadas (0 a 1)
    Wn = [f1 f2] / (fs / 2);

    % Orden del filtro (ajusta si es necesario)
    orden = 4;

    % Diseño del filtro Butterworth paso banda
    [b, a] = butter(orden, Wn, 'bandpass');
    senal_filtrada = filter(b, a, signal);
end