import pyedflib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# 创建refs文件夹（如果不存在）
os.makedirs('refs', exist_ok=True)

# 保存恢复后的数据到Excel文件
def save_data_to_excel(data, filename):
    # 将数据转为DataFrame，假设每个信号是一个单独的行
    df = pd.DataFrame(data, columns=["Decoded Signal"])

    # 保存为Excel文件
    df.to_excel(os.path.join('refs', filename), index=False)
    print(f"数据已保存到Excel文件: refs/{filename}")

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

# 保存数据到Excel文件
save_data_to_excel(signal_data, 'original_data.xlsx')
# 打印读取到的信号数据（前10个数据点作为示例）
print("该通道的信号数据（前10个数据点）:", signal_data[:10])
