clear; clc; close all;

frequencies = [
    440.000, 523.251, 587.330, 587.330, ...
    587.330, 659.255, 698.456, 698.456, ...
    698.456, 783.991, 659.255, 659.255, ...
    587.330, 523.251, 523.251, 587.330, ...
    ...
    440.000, 523.251, 587.330, 587.330, ...
    587.330, 659.255, 698.456, 698.456, ...
    698.456, 783.991, 659.255, 659.255, ...
    587.330, 523.251, 523.251, 587.330, ...
    ...
    440.000, 523.251, 587.330, 587.330, ...
    587.330, 698.456, 783.991, 783.991, ...
    783.991, 880.000, 932.328, 932.328, ...
    880.000, 783.991, 880.000, 1174.659
];

fs = 44100;          
noteDuration = 0.3;  
amplitude = 0.25;    

N = round(noteDuration * fs); 
t = (0:N-1) / fs;  
numNotes = numel(frequencies);

audio = zeros(1, numNotes * N);
phase = 0;

for k = 1:numNotes
    f = frequencies(k);
    phaseStep = 2*pi*f/fs;

    signal = amplitude * sin(phase + phaseStep*(0:N-1));

    indices = (k-1)*N + (1:N);
    audio(indices) = signal;

    phase = mod(phase + phaseStep*N, 2*pi);
end

time = (0:length(audio)-1) / fs;

figure('Color', 'w');

subplot(2, 1, 1);
plot(time, audio);
xlabel('Время, с');
ylabel('Амплитуда');
title('Звуковой сигнал всей мелодии');
grid on;
xlim([0, length(audio)/fs]);

sound(audio, fs);