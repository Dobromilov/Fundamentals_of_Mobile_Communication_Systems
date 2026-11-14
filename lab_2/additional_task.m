% Чувствительность приёмников UL и DL
% в зависимости от полосы и температуры

k = 1.380649e-23;

% Исходные параметры приёмников
NF_BS = 2.4;
NF_UE = 6;
SINR_UP = 4;
SINR_DL = 2;

% Диапазоны для построения графиков
BW_MHz = 1:0.5:40;
T_C = -40:2:60;

% Все сочетания полосы и температуры
[BW_grid, T_grid] = meshgrid(BW_MHz, T_C);

% Перевод в единицы для формулы kTB
BW_Hz = BW_grid * 10^6;
T_K = T_grid + 273.15;

% Тепловой шум в ваттах
% .* означает поэлементное умножение матриц
ThermalNoise_W = k .* T_K .* BW_Hz;

% Перевод теплового шума в дБм
ThermalNoise_dBm = 10 * log10(ThermalNoise_W) + 30;

% UL: принимает базовая станция
RxSens_UL = ThermalNoise_dBm + NF_BS + SINR_UP;

% DL: принимает телефон
RxSens_DL = ThermalNoise_dBm + NF_UE + SINR_DL;

% Контрольные точки для исходных полос при 20 градусах
T_example_C = 20;
T_example_K = T_example_C + 273.15;

BW_UL = 10 * 10^6;
BW_DL = 20 * 10^6;

RxSens_UL_example = 10 * log10(k * T_example_K * BW_UL) + 30 + NF_BS + SINR_UP;
RxSens_DL_example = 10 * log10(k * T_example_K * BW_DL) + 30 + NF_UE + SINR_DL;

% Одинаковые шкалы для сравнения двух графиков
all_values = [RxSens_UL(:); RxSens_DL(:)];
limits = [floor(min(all_values)), ceil(max(all_values))];

figure('Color', 'w', 'Position', [100, 100, 1300, 550]);

% Первый график: UL
subplot(1, 2, 1);

surf(BW_grid, T_grid, RxSens_UL, 'EdgeColor', 'none');
hold on;

plot3(BW_UL / 10^6, T_example_C, RxSens_UL_example, ...
      'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 8);

xlabel('Ширина полосы, МГц');
ylabel('Температура, °C');
zlabel('Чувствительность, дБм');
title('UL: приёмник базовой станции');

colorbar;
caxis(limits);
zlim(limits);
grid on;
view(45, 25);

% Второй график: DL
subplot(1, 2, 2);

surf(BW_grid, T_grid, RxSens_DL, 'EdgeColor', 'none');
hold on;

plot3(BW_DL / 10^6, T_example_C, RxSens_DL_example, ...
      'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 8);

xlabel('Ширина полосы, МГц');
ylabel('Температура, °C');
zlabel('Чувствительность, дБм');
title('DL: приёмник пользовательского устройства');

colorbar;
caxis(limits);
zlim(limits);
grid on;
view(45, 25);

colormap(parula);
rotate3d on;

% Вывод контрольных значений
fprintf('\nЧувствительность при температуре %.1f °C:\n', T_example_C);
fprintf('UL, полоса 10 МГц: %.2f дБм\n', RxSens_UL_example);
fprintf('DL, полоса 20 МГц: %.2f дБм\n', RxSens_DL_example);