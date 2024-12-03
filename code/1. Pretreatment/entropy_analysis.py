import numpy as np
from collections import Counter
from preprocess_signal import normalize_signal
from read_edf_data import read_edf


def calculate_entropy(signal):
    # 将信号量化为 0-255 的整数值
    quantized_signal = (signal * 255).astype(int)
    total_length = len(quantized_signal)
    frequencies = Counter(quantized_signal)

    # 计算熵
    entropy = -sum((count / total_length) * np.log2(count / total_length)
                   for count in frequencies.values())
    return entropy


if __name__ == "__main__":
    file_path = '../0. data/r01.edf'
    signals, labels = read_edf(file_path)

    for i, signal in enumerate(signals):
        normalized_signal = normalize_signal(signal)
        entropy = calculate_entropy(normalized_signal)
        print(f"Signal {labels[i]}: Entropy = {entropy:.2f} bits per symbol")
