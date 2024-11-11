% Parámetros del filtro
filtro_frecuencia_intermedia= 100e3;               % Frecuencia intermedia (100 kHz)
filtro_bw = 10e3;                % Ancho de banda del filtro (20 kHz)
filtro_fs_fm = 10 * filtro_frecuencia_intermedia;          % Frecuencia de muestreo
filtro_fs_fm =fs_mux;

% Frecuencias de corte y normalización
filtro_f_low = filtro_frecuencia_intermedia - filtro_bw/2;        
filtro_f_high = filtro_frecuencia_intermedia + filtro_bw/2;       
filtro_Wn = [filtro_f_low, filtro_f_high] / ((10 * filtro_frecuencia_intermedia) / 2);

% Coeficientes del filtro Butterworth
orden = 4;
[b, a] = butter(orden, filtro_Wn, 'bandpass');

% Guarda los coeficientes en el Workspace
assignin('base', 'b', b);
assignin('base', 'a', a);
