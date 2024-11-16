addpath("scripts\");
%% parametros para simulación
%% clear all;
%% Archivo: test_am_mod
fm_test_mod_am = 1000;
fc_test_mod_am = 10*fm_test_mod_am;

fs_test_mod_am = 10 * fc_test_mod_am;
ts_test_mod_am = 1/fs_test_mod_am;

%% Archivo: test_mux_FM_mod_demod
% Multiplexación de tres señales moduladas en am

fm1_mux = 1000;
fm2_mux = 2000;
fm3_mux = 3000;

fc1_mux = 10*fm1_mux;
fc2_mux = 10*fm2_mux;
fc3_mux = 10*fm3_mux;

fs_mux = 10 * fc3_mux;
ts_mux = 1/fs_mux;

%% Archivo: test_FM
% Modulación - Demodulación Fm 
fc_mod_fm = 110e3;
fs_mux = 10 * fc_mod_fm;
ts_mux = 1/fs_mux;

%% Archivo: test_receptor
% Multiplexación de tres señales moduladas en am

fm1_mux = 1e3;
fm2_mux = 2e3;
fm3_mux = 3e3;

f_mensaje = [fm1_mux, fm2_mux, fm3_mux];
banda_guarda = 10e3;
fc1_mux = 10*fm1_mux;
%fc2_mux = 10*fm2_mux;
%fc3_mux = 10*fm3_mux;

f_portadoras = gen_fc_band_guard(f_mensaje, fc1_mux, banda_guarda, 120e3);

fc1_mux = f_portadoras(1)
fc2_mux = f_portadoras(2)
fc3_mux = f_portadoras(3)


fs_mux = 10 * fc3_mux;
ts_mux = 1/fs_mux;

% Frecuencias para portadoras para el receptor
% frecuencia_intermedia = 10.7e6;
frecuencia_intermedia = 110e3;
fs_mux = 10 * frecuencia_intermedia;
% ts_mux = 1/fs_mux;

fc1_receptor = frecuencia_intermedia + fc3_mux;
fc2_receptor = frecuencia_intermedia + fc2_mux;
fc3_receptor = frecuencia_intermedia + fc1_mux;
fc_receptores = [fc1_receptor, fc2_receptor, fc3_receptor]

fprintf('fc1_receptor: %.3e\n', fc1_receptor);
fprintf('fc2_receptor: %.3e\n', fc2_receptor);
fprintf('fc3_receptor: %.3e\n', fc3_receptor);

%% Filtro


