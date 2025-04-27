%% frecuencias de auddio y video
f_audioL
f_audioR
f_video

portadora_audioL = 
portadora_audioR = 

sample_rate =


%%
% Parámetros de la señal de video
f_video = 15734; % Frecuencia central (15.734 kHz)
fs = 10e6;       % Frecuencia de muestreo (10 MHz, mayor que 2 * BW)
t = 0:1/fs:1e-3; % Tiempo para 1 ms de simulación
video_signal = sin(2 * pi * f_video * t); % Tono sinusoidal

% Visualización
plot(t, video_signal);
title('Señal de Video Simulada');
xlabel('Tiempo (s)');
ylabel('Amplitud');

%%
% Parámetros
fc = 915e6;          % Frecuencia de portadora (Hz)
fv = 2e6;            % Frecuencia del tono de video (Hz)
Fs = 100e6;          % Frecuencia de muestreo (Hz)
t = 0:1/Fs:10e-6;    % Tiempo de simulación (10 us)

% Parámetros de modulación FM
delta_f = 5e6;       % Desviación de frecuencia (Hz)
k_f = 2 * pi * delta_f;  % Sensibilidad del modulador FM

% Señal de video (tono analógico)
video_signal = sin(2*pi*fv*t); % Simula componente de video

% Señal FM
integrated_signal = cumsum(video_signal) / Fs; % Integración de la señal
fm_signal = cos(2*pi*fc*t + k_f * integrated_signal);

% Graficar resultados
subplot(2,1,1);
plot(t*1e6, video_signal);
title('Señal de video (tono de 2 MHz)');
xlabel('Tiempo [us]');
ylabel('Amplitud');

subplot(2,1,2);
plot(t*1e6, fm_signal);
title('Señal modulada en FM (portadora 915 MHz)');
xlabel('Tiempo [us]');
ylabel('Amplitud');


