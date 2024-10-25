import pyedflib
import numpy as np
import matplotlib.pyplot as plt

print('0. convert edf to img')
# 打开 .edf 文件
file_path = '../0. data/r01.edf'
edf_file = pyedflib.EdfReader(file_path)

# 选择第 0 个信号标签的信号
ecg_signal = edf_file.readSignal(0)

# 获取采样率，用于确定时间轴
sampling_rate = edf_file.getSampleFrequency(0)
time = np.arange(0, len(ecg_signal)) / sampling_rate

# 绘制心电图信号
plt.figure(figsize=(10, 4))
plt.plot(time, ecg_signal)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.savefig('../ecg_image.png')  # 保存为PNG图像
plt.show()

edf_file.close()