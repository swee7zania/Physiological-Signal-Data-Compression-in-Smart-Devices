import pyedflib
import numpy as np
import matplotlib.pyplot as plt

# 读取 .edf 文件
file_path = "../0. data/r01.edf"  # 修改为你的 .edf 文件路径
edf_file = pyedflib.EdfReader(file_path)

# 获取所有信号的通道名
channel_names = edf_file.getSignalLabels()
print("信号通道名:", channel_names)

# 假设我们选择第一个通道的信号数据
channel_index = 0  # 选择第一个通道（可以根据需要更改索引）

# 读取该通道的信号数据
signal_data = edf_file.readSignal(channel_index)

# 创建时间轴，假设采样率是相同的
sampling_rate = edf_file.getSampleFrequency(channel_index)
time = np.arange(len(signal_data)) / sampling_rate  # 时间单位是秒

# 绘制该通道的信号图
plt.figure(figsize=(10, 6))
plt.plot(time, signal_data, label=channel_names[channel_index])

# 设置标题和坐标轴标签
plt.title(f"Signal Channel: {channel_names[channel_index]} diagram", fontsize=14)
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Signal value', fontsize=12)

# 显示图例
plt.legend()

# 显示网格
plt.grid(True)

# 展示图形
plt.show()

# 关闭文件
edf_file.close()
