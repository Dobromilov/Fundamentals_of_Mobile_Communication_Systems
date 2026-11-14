import numpy as np
import matplotlib.pyplot as plt
import math

# Расчёт бюджета восходящего канала и MAPL_UL.
def num_1(TxPowerUE, AntGainBS, MIMO_gain, IM,
          PenetretionM, BW_UL, NF_BS, SINR_UP):

    FeederLoss = 2 + 0.4 + 0.5  # Потери в антенно-фидерном тракте, дБ
    ThermalNoise = -174 + 10 * math.log10(BW_UL)
    RxSensBS = ThermalNoise + NF_BS + SINR_UP

    MAPL_UL = TxPowerUE - FeederLoss+ AntGainBS + MIMO_gain - IM - PenetretionM- RxSensBS
    return MAPL_UL

# Расчёт бюджета нисходящего канала и MAPL_DL.
def num_2(TxPowerBS, AntGainBS, MIMO_gain, IM,
          PenetretionM, BW_DL, NF_UE, SINR_DL):

    FeederLoss = 2 + 0.4 + 0.5  # Потери в антенно-фидерном тракте, дБ
    ThermalNoise = -174 + 10 * math.log10(BW_DL)
    RxSensUE = ThermalNoise + NF_UE + SINR_DL

    MAPL_DL = TxPowerBS - FeederLoss + AntGainBS + MIMO_gain - IM - PenetretionM - RxSensUE
    return MAPL_DL

# Расчёт потерь по моделям UMiNLOS, COST 231 Hata и Walfish–Ikegami и построение графика.
def num_3(f, MAPL_UL, MAPL_DL):
    hBS = 50  # Высота антенны БС, м
    hms = 1.2  # Высота антенны телефона, м

    d_m = np.arange(1, 5001)
    d_km = d_m / 1000

    a_hms = 3.2 * math.log10(11.75 * hms)**2 - 4.97
    L_clutter = 3  # Поправка на плотную городскую застройку, дБ

    if 150 <= f < 1500:
        A = 69.55
        B = 26.16
    elif 1500 <= f <= 2000:
        A = 46.3
        B = 33.9
    else:
        raise ValueError("Частота должна быть от 150 до 2000 МГц")

    PL_FSPM = 20 * np.log10((4 * math.pi * d_m * f * 10**6) / (3 * 10**8))
    PL_UMiNLOS = 26 * math.log10(f / 1000) + 22.7 + 36.7 * np.log10(d_m)
    PL_Hata = np.zeros(len(d_m))

    for i in range(len(d_km)):
        if d_km[i] >= 1:
            s = 44.9 - 6.55 * math.log10(f)
        else:
            s = (47.88 + 13.9 * math.log10(f) - 13.9 * math.log10(hBS)) / math.log10(50)
        PL_Hata[i] = (
            A + B * math.log10(f) - 13.82 * math.log10(hBS)
            - a_hms + s * math.log10(d_km[i]) + L_clutter
        )

    plt.figure(figsize=(10, 6))
    plt.plot(d_m, PL_UMiNLOS, color="red", label="UMiNLOS")

    if 800 <= f <= 2000:
        h_roof = 20  # Средняя высота крыш, м
        w = 20  # Ширина улицы, м
        b = 50  # Расстояние между зданиями, м
        phi = 30  # Угол между улицей и направлением сигнала, °
        mask_WI = d_m >= 30
        d_WI_km = d_km[mask_WI]

        L_ori = -10 + 0.354 * phi
        L_rts = (
            -16.9 - 10 * math.log10(w) + 10 * math.log10(f)
            + 20 * math.log10(h_roof - hms) + L_ori
        )

        L_bsh = -18 * math.log10(1 + hBS - h_roof)
        kf = -4 + 0.7 * (f / 925 - 1)
        L_msd = (
            L_bsh + 54 + 18 * np.log10(d_WI_km)
            + kf * math.log10(f) - 9 * math.log10(b)
        )

        PL_WI = PL_FSPM[mask_WI] + np.maximum(0, L_rts + L_msd)
        plt.plot(d_m[mask_WI], PL_WI, color="blue", label="Walfish–Ikegami (NLOS)")

    plt.plot(d_m, PL_Hata, color="green", label="COST 231 Hata")
    plt.axhline(MAPL_UL, color="black", linestyle="--", label="MAPL UL")
    plt.axhline(MAPL_DL, color="purple", linestyle="-.", label="MAPL DL")
    plt.xlabel("Расстояние, м")
    plt.ylabel("Потери сигнала PL(d), дБ")
    plt.title("Зависимость потерь сигнала от расстояния")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    return d_m, d_km, PL_Hata, PL_UMiNLOS

# Расчёт радиусов по MAPL, площадей покрытия и количества БС.
def num_4(d_m, d_km, PL_Hata, PL_UMiNLOS, MAPL_UL, MAPL_DL,
          N_sectors, area_macro, area_micro):

    idx_UL = np.argmin(np.abs(PL_Hata - MAPL_UL))
    idx_DL = np.argmin(np.abs(PL_Hata - MAPL_DL))

    idx_micro_UL = np.argmin(np.abs(PL_UMiNLOS - MAPL_UL))
    idx_micro_DL = np.argmin(np.abs(PL_UMiNLOS - MAPL_DL))

    for PL in (PL_Hata, PL_UMiNLOS):
        for MAPL in (MAPL_UL, MAPL_DL):
            if not PL.min() <= MAPL <= PL.max():
                raise ValueError("Пересечение с MAPL вне диапазона графика. Измени диапазон d_m в num_3().")

    d_UL = d_km[idx_UL]
    d_DL = d_km[idx_DL]
    R_macro = min(d_UL, d_DL)

    d_micro_UL_m = d_m[idx_micro_UL]
    d_micro_DL_m = d_m[idx_micro_DL]

    R_micro_km = min(d_micro_UL_m, d_micro_DL_m) / 1000

    if N_sectors == 3:
        k = 1.95
    elif N_sectors == 2:
        k = 1.73
    elif N_sectors == 6:
        k = 2.6
    else:
        raise ValueError("Число секторов должно быть 2, 3 или 6")

    Area_Site = k * R_macro**2
    Area_Site_micro = k * R_micro_km**2

    Num_BS_macro = math.ceil(area_macro / Area_Site)
    Num_BS_micro = math.ceil(area_micro / Area_Site_micro)

    print("\nРадиус соты и расчёт БС — МАКРО")
    print(f"Радиус в UL: {d_UL * 1000:.1f} м")
    print(f"Радиус в DL: {d_DL * 1000:.1f} м")
    print(f"Итоговый радиус: {R_macro:.3f} км")
    print(f"Площадь одного сайта: {Area_Site:.4f} кв. км")
    print(f"Количество БС для территории {area_macro} кв. км: {Num_BS_macro}")

    print("\nРадиус соты и расчёт БС — МИКРО")
    print(f"Радиус в UL: {d_micro_UL_m:.1f} м")
    print(f"Радиус в DL: {d_micro_DL_m:.1f} м")
    print(f"Итоговый радиус: {R_micro_km:.3f} км")
    print(f"Площадь одного сайта: {Area_Site_micro:.4f} кв. км")
    print(f"Количество БС для территории {area_micro} кв. км: {Num_BS_micro}")

    return Num_BS_macro, Num_BS_micro

# Задание исходных данных и запуск расчётов.
def main():
    TxPowerBS=46
    N_sectors=3
    TxPowerUE=24
    AntGainBS=21
    PenetretionM=15
    IM=1
    f=1800  # Несущая частота, МГц
    BW_UL=10**7  # Полоса UL, Гц
    BW_DL=2*10**7  # Полоса DL, Гц
    NF_BS=2.4
    NF_UE=6
    SINR_DL=2
    SINR_UP=4
    area_macro=100  # Площадь для макросот, км²
    area_micro=4  # Площадь для микросот, км²
    MIMO_gain=3

    MAPL_UL = num_1(TxPowerUE, AntGainBS, MIMO_gain, IM, PenetretionM, BW_UL, NF_BS, SINR_UP)
    print(f"MAPL_UL = {MAPL_UL:.1f} дБ")

    MAPL_DL = num_2(TxPowerBS, AntGainBS, MIMO_gain, IM, PenetretionM, BW_DL, NF_UE, SINR_DL)
    print(f"MAPL_DL = {MAPL_DL:.1f} дБ")

    d_m, d_km, PL_Hata, PL_UMiNLOS = num_3(f, MAPL_UL, MAPL_DL)

    Num_BS_macro, Num_BS_micro = num_4(d_m, d_km, PL_Hata, PL_UMiNLOS, MAPL_UL, MAPL_DL, N_sectors, area_macro, area_micro)
    plt.show()

if __name__ == "__main__":
    main()