function filtered_signal = filter_passband(signal, fintermedia, band_width)
    % Parámetros del filtro
    fi = fintermedia;               % Frecuencia intermedia (100 kHz)
    bw = band_width;                % Ancho de banda del filtro (20 kHz, ajustable)
    fs_fm = 10 * fi;          % Frecuencia de muestreo (usada en fs_fm)

    % Cálculo de las frecuencias de corte
    f_low = (fi - bw/2)+2e3;        % Frecuencia de corte baja
    f_high = (fi + bw/2)-2e3;       % Frecuencia de corte alta
    Wn = [f_low, f_high] / (fs_fm / 2);  % Normalización de frecuencia de corte

    % Diseño del filtro Butterworth paso banda de orden 4
    orden = 4;
    [b, a] = butter(orden, Wn, 'bandpass');

    % Aplicar el filtro a la señal modulada AM (ejemplo con `am`)
    filtered_signal = filter(b, a, signal);
end