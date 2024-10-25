import pyedflib
import numpy as np
from scipy.stats import entropy

print('1. calculate entropy edf')
# 1. 读取 .edf 文件，存储到 NumPy 数组中
# 1.1 打开 .edf 文件
file_path = '../0. data/r01.edf'
edf = pyedflib.EdfReader(file_path)

# 1.2 获取通道信息并打印所有信号的标签
n_channels = edf.signals_in_file
channel_labels = edf.getSignalLabels()
print()
print("Signal Label:", channel_labels)

# 1.3 提取第 0 个信号标签的数据，可以更改数字来替换
ecg_signal = edf.readSignal(0)

# 1.4 将信号数据转换为 numpy 数组以便后续分析
ecg_signal = np.array(ecg_signal)
print(ecg_signal)

# 1.5 获取采样频率
sampling_frequency = edf.getSampleFrequency(0)  # 通常所有通道的采样频率相同
print()
print(f"Sampling frequency: {sampling_frequency} Hz")

# 1.6 关闭 .edf 文件
edf.close()

# 2. 计算数据熵
#    此时，ecg_signal 数组已经包含了心电信号数据，直接使用如下代码计算熵值：

# 2.1 将信号归一化到 0-255 范围
ecg_normalized = np.round((ecg_signal - np.min(ecg_signal)) / (np.max(ecg_signal) - np.min(ecg_signal)) * 255)

# 2.2 计算信号分布
value, counts = np.unique(ecg_normalized, return_counts=True)

# 2.3 计算熵
signal_entropy = entropy(counts, base=2)
print()
print("--------------")
print(f"ECG数据的熵为: {signal_entropy:.2f} bits")
