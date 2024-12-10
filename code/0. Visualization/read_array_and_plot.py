import pyedflib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 读取 .edf 文件
file_path = "../0. data/r01.edf"  # 修改为你的 .edf 文件路径
edf_file = pyedflib.EdfReader(file_path)

# 获取所有信号的通道名
channel_names = edf_file.getSignalLabels()
print("信号通道名:", channel_names)

# 假设我们选择第一个通道的信号数据
channel_index = 0  # 选择第一个通道（你可以根据需要更改索引）

# 读取该通道的信号数据
signal_data = edf_file.readSignal(channel_index)

# 打印读取到的信号数据（前10个数据点作为示例）
print("该通道的信号数据（前10个数据点）:", signal_data[:10])

# 将信号数据存储为数组
signal_array = np.array(signal_data)

# 创建x轴坐标，这里假设每个数据点表示时间上的连续采样
time_ms = np.arange(len(signal_array))  # time = [0, 1, 2, ..., 9]
time = time_ms / 1000

# 绘制信号图
plt.figure(figsize=(10, 6))
plt.plot(time, signal_array, marker='o', color='b', markersize=0,linewidth=1.3, label='Signal')

# 添加标题和标签
plt.title('Physiological signal diagram', fontsize=14)
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Signal value', fontsize=12)

# 显示图例
plt.legend()

# 显示网格
plt.grid(True)

# 展示图形
plt.show()