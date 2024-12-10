import numpy as np
import pyedflib
from collections import Counter

# 加载 EDF 文件
def load_edf_signal(file_path, signal_index=0):
    with pyedflib.EdfReader(file_path) as f:
        signal = f.readSignal(signal_index)
    return signal

# 预测编码 (差分编码)
def differential_encoding(signal):
    diff_signal = np.diff(signal)
    return diff_signal

if __name__ == "__main__":
    file_path = '../0. data/r01.edf'
    signal_data = load_edf_signal(file_path, signal_index=0)  # 读取第0个频道

    # 对信号数据进行差分编码
    diff_encoded_data = differential_encoding(signal_data)

    # 打印结果
    print("Original signal (First 30):", signal_data[:30])
    print("\nDifferential encoding (First 30):", diff_encoded_data[:30])