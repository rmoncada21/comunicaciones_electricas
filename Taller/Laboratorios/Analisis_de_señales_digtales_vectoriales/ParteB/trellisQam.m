% Efecto Rate 2/3 Convolutional Code in AWGN
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Limpio la terminal y variables
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc;
close all;
clear all;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Adquisicion de variables
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
disp('Modulacion QAM M-ary')
M = input('Digite el orden de la modulación: '); % Orden de modulación
k = log2(M); % Número de bits por símbolo

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Creación de rate 2/3 convolutional
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
trellis = poly2trellis([5 4], [23 35 0; 0 5 13]); 
traceBack = 16;
codeRate = 2/3;

% Codificador y decodificador convolucional
convEncoder = comm.ConvolutionalEncoder('TrellisStructure',trellis);
vitDecoder = comm.ViterbiDecoder('TrellisStructure',trellis, ...
    'InputFormat','Hard','TracebackDepth',traceBack);

% Objeto para calcular tasa de error
errorRate = comm.ErrorRate('ReceiveDelay', 2*traceBack);

% Vector Eb/No en dB
ebnoVec = 0:2:10;
errorStats = zeros(length(ebnoVec), 3);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Simulación
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for m = 1:length(ebnoVec)
    snr = ebnoVec(m) + 10*log10(k * codeRate);
    
    while errorStats(m,2) <= 100 && errorStats(m,3) <= 1e7
        % Generar bits aleatorios
        dataIn = randi([0 1], 10000, 1);

        % Codificar con convolucional
        dataEnc = convEncoder(dataIn);

        % Asegurar que dataEnc sea múltiplo de k
        dataEnc = dataEnc(1:(floor(length(dataEnc)/k)*k));

        % Convertir bits a símbolos
        dataEncSym = bi2de(reshape(dataEnc, [], k), 'left-msb');

        % Modulación QAM
        txSig = qammod(dataEncSym, M, 'UnitAveragePower', true);

        % Canal AWGN
        rxSig = awgn(txSig, snr, 'measured');

        % Demodulación QAM
        demodSym = qamdemod(rxSig, M, 'UnitAveragePower', true);

        % Convertir símbolos a bits
        demodBits = de2bi(demodSym, k, 'left-msb');
        demodSig = reshape(demodBits, [], 1);

        % Decodificación Viterbi
        dataOut = vitDecoder(demodSig);

        % Calcular errores
        errorStats(m,:) = errorRate(dataIn, dataOut);
    end

    reset(errorRate)
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Cálculo de BER teórico para comparación
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
berUncoded = berawgn(ebnoVec', 'qam', M);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Gráfica de resultados
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
semilogy(ebnoVec, [errorStats(:,1) berUncoded], 'o-')
grid on
legend('Codificado', 'No Codificado')
xlabel('Eb/No (dB)')
ylabel('Bit Error Rate')
title(['BER para QAM-' num2str(M) ' con y sin codificación convolucional Rate 2/3'])
