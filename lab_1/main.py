import math
import matplotlib.pyplot as plt
import sys

freq = 8
k = 64  # минимальная частота дискретизации: 2 * 32 Гц
freq_new = freq
k_new = k*4  # частота дискретизации, увеличенная в четыре раза

def dft(signal):
    # Прямое ДПФ: перевод отсчётов сигнала в частотный спектр.
    N = len(signal)
    result = []
    for k in range(N):
        s = 0
        for n in range(N):
            angle = -2 * math.pi * k * n / N
            s += signal[n] * complex(
                math.cos(angle),
                math.sin(angle)
            )
        result.append(s)
    return result

def restored_dft(spectrum):
    # Обратное ДПФ: восстановление отсчётов по спектру.
    N = len(spectrum)
    restored_sample = [0] * N
    for n in range(N):
        s = 0
        for m in range(N):
            angle = 2 * math.pi * m * n / N
            s += spectrum[m] * complex(
                math.cos(angle),
                math.sin(angle)
            )
        restored_sample[n] = (s / N).real
    return restored_sample

def f(t, frequency):
    # Вариант 9: сумма косинусов с частотами f и 4f.
    return (
        math.cos(2 * math.pi * frequency * t)
        + math.cos(2 * math.pi * frequency * 4 * t)
    )

def main():
    # Формируем отсчёты сигнала длительностью одну секунду.
    t = [i / k for i in range(k)]
    samples = [f(i, freq) for i in t]
    print("Исходные семплы")
    for i in range(len(samples)):
        print(i, samples[i])

    spectrum = dft(samples)
    # print("Спектр исходного сигнала")
    # for i in range(len(spectrum)):
    #     print(i, spectrum[i])
    
    restored_sample = restored_dft(spectrum)

    t_new = [i / k_new for i in range(k_new)]
    samples_new = [f(i, freq_new) for i in t_new]

    # print("\nНовые семплы")
    # for i in range(len(samples_new)):
    #     print(i, samples_new[i])

    spectrum_new = dft(samples_new)

    # print("\nСпектр нового сигнала")
    # for i in range(len(spectrum_new)):
    #     print(i, spectrum_new[i])

    restored_sample_new = restored_dft(spectrum_new)

    print("размер семплов: ", sys.getsizeof(samples))
    print("размер спектра: ", sys.getsizeof(spectrum))

    print("размер семплов new: ", sys.getsizeof(samples_new))
    print("размер спектра new: ", sys.getsizeof(spectrum_new))

    # Оставляем положительную половину спектра для построения графика.
    N = len(spectrum)
    frequencies = [i * k / N for i in range(N // 2 + 1)]
    amplitudes = [abs(spectrum[i]) for i in range(N // 2 + 1)]

    N_new = len(spectrum_new)
    frequencies_new = [i * k_new / N_new for i in range(N_new // 2 + 1)]
    amplitudes_new = [abs(spectrum_new[i]) for i in range(N_new // 2 + 1)]

    fig1, ax1 = plt.subplots(3, 1, figsize=(10, 8))

    ax1[0].plot(t, samples)
    ax1[0].set_title("Исходный сигнал, freq = 8 Гц")
    ax1[0].set_xlabel("Время, с")
    ax1[0].set_ylabel("Амплитуда")
    ax1[0].grid()

    ax1[1].plot(t, restored_sample)
    ax1[1].set_title("Восстановленный сигнал")
    ax1[1].set_xlabel("Время, с")
    ax1[1].set_ylabel("Амплитуда")
    ax1[1].grid()

    ax1[2].stem(frequencies, amplitudes)
    ax1[2].set_title("Спектр сигнала")
    ax1[2].set_xlabel("Частота, Гц")
    ax1[2].set_ylabel("Амплитуда")
    ax1[2].grid()

    fig1.tight_layout()

    fig2, ax2 = plt.subplots(3, 1, figsize=(10, 8))

    ax2[0].plot(t_new, samples_new)
    ax2[0].set_title("Исходный сигнал, freq = 32 Гц")
    ax2[0].set_xlabel("Время, с")
    ax2[0].set_ylabel("Амплитуда")
    ax2[0].grid()

    ax2[1].plot(t_new, restored_sample_new)
    ax2[1].set_title("Восстановленный сигнал")
    ax2[1].set_xlabel("Время, с")
    ax2[1].set_ylabel("Амплитуда")
    ax2[1].grid()

    ax2[2].stem(frequencies_new, amplitudes_new)
    ax2[2].set_title("Спектр сигнала")
    ax2[2].set_xlabel("Частота, Гц")
    ax2[2].set_ylabel("Амплитуда")
    ax2[2].grid()

    fig2.tight_layout()

    plt.show()

if __name__ == "__main__":
    main()