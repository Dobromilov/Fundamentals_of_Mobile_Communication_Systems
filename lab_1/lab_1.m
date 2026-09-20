[y, Fs] = audioread("voice.wav");

if size(y, 2) == 2
    y = mean(y, 2);
end

N = length(y);
T = N / Fs;

fprintf("Количество отсчетов: %d\n", N);
fprintf("Длительность записи: %.3f с\n", T);
fprintf("Частота дискретизации из файла: %.0f Гц\n", Fs);

Fs_calc = N / T;

fprintf("Рассчитанная частота дискретизации: %.0f Гц\n", Fs_calc);


y1 = downsample(y, 10);
Fs1 = Fs / 10;

fprintf("\nНовая частота дискретизации: %.0f Гц\n", Fs1);

player1 = audioplayer(y, Fs);

disp("Воспроизведение исходного сигнала");
playblocking(player1);

pause(1);

player2 = audioplayer(y1, Fs1);

disp("Воспроизведение прореженного сигнала");
playblocking(player2);


t = (0:length(y)-1) / Fs;
t1 = (0:length(y1)-1) / Fs1;

figure;

subplot(2, 1, 1);

plot(t, y);

xlabel("Время, с");
ylabel("Амплитуда");
title("Исходный сигнал");
grid on;


subplot(2, 1, 2);

plot(t1, y1);

xlabel("Время, с");
ylabel("Амплитуда");
title("Сигнал после уменьшения частоты дискретизации в 10 раз");
grid on;


Y = fft(y);
N = length(y);

P = abs(Y) / N;

P = P(1:floor(N/2)+1);

if length(P) > 2
    P(2:end-1) = 2 * P(2:end-1);
end

f = (0:floor(N/2)) * Fs / N;


Y1 = fft(y1);
N1 = length(y1);

P1 = abs(Y1) / N1;

P1 = P1(1:floor(N1/2)+1);

if length(P1) > 2
    P1(2:end-1) = 2 * P1(2:end-1);
end

f1 = (0:floor(N1/2)) * Fs1 / N1;


figure;

plot(f, P);

hold on;

plot(f1, P1);

hold off;

xlabel("Частота, Гц");
ylabel("Амплитуда");
title("Сравнение амплитудных спектров");

xlim([0 Fs1 / 2]);

grid on;

function yq = quantize_signal(y, bits)

    levels = 2^bits;

    ymin = min(y);
    ymax = max(y);

    y_norm = (y - ymin) / (ymax - ymin);

    yq = round(y_norm * (levels - 1));

    yq = yq / (levels - 1);

    yq = yq * (ymax - ymin) + ymin;

end


y3 = quantize_signal(y, 3);
y4 = quantize_signal(y, 4);
y5 = quantize_signal(y, 5);
y6 = quantize_signal(y, 6);

error3 = mean(abs(y - y3));
error4 = mean(abs(y - y4));
error5 = mean(abs(y - y5));
error6 = mean(abs(y - y6));

fprintf("\nСредняя ошибка квантования:\n");
fprintf("3 бита: %e\n", error3);
fprintf("4 бита: %e\n", error4);
fprintf("5 бит: %e\n", error5);
fprintf("6 бит: %e\n", error6);