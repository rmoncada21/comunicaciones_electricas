addpath("test\", "scripts\");
%savepath;
% parametrós de simulación test (proyecto)
%% Mensajes 
clear all;
test_am1 = 20; test_fm1 = 1000;
test_am2 = 15; test_fm2 = 2000;
test_am3 = 10; test_fm3 = 3000;

test_fs = 10*test_fm3;
test_ts = 1/test_fs;


%% portadoras
vector_fm = [test_fm1, test_fm2, test_fm3];
banda_guarda = 10000;
ancho_de_banda = 120000;


% amplitudes de portadoras
test_ac1 = 1;
test_ac2 = 1;
test_ac3 = 1;

% frecuencias portadoras
test_fc1 = 10*test_fm1; vector_fc = gen_fc_band_guard(vector_fm, test_fc1, banda_guarda, ancho_de_banda);
test_fc2 = vector_fc(2);
test_fc3 = vector_fc(3);

% nueva frecuencia de muestreo
test_fs = 10*test_fc3;
test_ts = 1/test_fs;

%% Modulador y demodulador FM
test_FM_mod = 110000;

test_fs = 10*test_FM_mod;
test_ts = 1/test_fs;

%% Sintonizador
test_FI = 110000; % 110e3

test_fc1_receptor = test_FI + test_fc3;
test_fc2_receptor = test_FI + test_fc2;
test_fc3_receptor = test_FI + test_fc1;

test_fs = 10*test_FI;
test_ts = 1/test_fs;
