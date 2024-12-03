import matplotlib.pyplot as plt
import numpy as np
from read_edf_data import read_edf


def normalize_signal(signal):
    signal = np.array(signal)
    normalized = (signal - np.min(signal)) / (np.max(signal) - np.min(signal))  # 标准化公式
    return normalized


def plot_signal(signal, label):
    plt.figure(figsize=(10, 4))
    plt.plot(signal)
    plt.title(f"Signal: {label}")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()


if __name__ == "__main__":
    file_path = '../0. data/r01.edf'
    signals, labels = read_edf(file_path)

    for i, signal in enumerate(signals):
        # 对信号进行标准化
        normalized_signal = normalize_signal(signal)

        # 打印标准化后的信号前 10 个数据点
        print(f"Original Signal (First 10 Points): {signal[:10]}")
        print(f"Normalized Signal (First 10 Points): {normalized_signal[:10]}")

        # 绘制标准化后的信号波形
        plot_signal(normalized_signal, labels[i])
