%% modulacion fm

% Características 
%
% fmax  - frecuencia max permitida para las señales de audios
% fs    - Frecuencia de muestro
% T     - Periodo de la señal
% t     - vector de tiempo
% deltaf- Un valor típico para Δf en sistemas de FM es entre 5 y 10 veces la máxima frecuencia de la señal de mensaje.
% 
% características del tono
% Am1   - amplitud del tono
% fm1   - frecuencia del tono
%
% características de la portadora
% Ac   - amplitud de la portadora
% fc   - frecuencia de la portadora


fmax = 15e3;
fs = 3*fmax;
T = 0.1; % 100 ms
t = 0:1/fs:T;
% deltaf = 75e3;

% simular tono
Am1 = 10;
fm1 = 3e3;
tono1 = Am1 * cos(2*pi*fm1*t);

% simular portadora
Ac = 1;
fc = 110e6;
deltaf = 5*15e3;
kf = deltaf/Am1; % sensibilidad del modulador de frecuencia - cambiar para los demas mensajes

% obtener la modulacion fm: Ac*cos[2pifc+2pif*integral(mt)dt]
% obtener la integral del mensaje
signal_integral = cumtrapz(tono1);

% obtenr la señal modulada
% portadora = cos(2*pi*fc*t);
fm_signal = Ac*cos(2*pi*fc+2*pi*kf*signal_integral);
% fm_signal = tono1 .* portadora;

figure;
plot(t, signal_integral);

% graficar el especto de la señal
% Espectro de la señal FM
N = length(fm_signal);
f = linspace(-fs/2, fs/2, N);
fm_signal_fft = fftshift(fft(fm_signal));

figure;
plot(f, abs(fm_signal_fft));
title('Espectro de la Señal FM');
xlabel('Frecuencia (Hz)');
ylabel('Magnitud');
axis([-200e3 200e3 0 max(abs(fm_signal_fft))]);
grid on;

disp('done');