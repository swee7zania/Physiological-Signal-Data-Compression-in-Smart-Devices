import pandas as pd
import matplotlib.pyplot as plt

# 读取Huffman编码字典
def read_huffman_codebook(filename):
    codebook = {}
    with open(filename, 'r') as f:
        for line in f:
            symbol, code = line.strip().split(': ')
            # 处理符号为浮动数值或其他类型
            try:
                symbol = float(symbol)  # 尝试解析为浮动数值
            except ValueError:
                symbol = int(symbol)  # 如果不能转换为浮动数值，则转换为整数
            codebook[code] = symbol  # 将符号和编码保存到字典中
    return codebook


# 读取压缩的二进制数据
def read_compressed_data(filename):
    with open(filename, 'rb') as f:
        binary_data = f.read()
    return ''.join(format(byte, '08b') for byte in binary_data)  # 转换为二进制字符串


# 解码Huffman编码数据
def huffman_decode(encoded_data, codebook):
    decoded_data = []
    current_code = ''
    for bit in encoded_data:
        current_code += bit
        if current_code in codebook:
            decoded_data.append(codebook[current_code])
            current_code = ''
    return decoded_data


# 读取起始值
def read_start_values(filename, index):
    with open(filename, 'r') as file:
        content = file.read().strip()
        start_values = [float(value) for value in content.split(',')]
    return start_values[index]

# 解压缩并恢复信号数据
def decompress_and_restore_signal(encoded_filename, codebook_filename, start_value_filename, start_value_index):
    # 读取Huffman编码字典
    codebook = read_huffman_codebook(codebook_filename)

    # 读取压缩的二进制数据
    compressed_data = read_compressed_data(encoded_filename)

    # 使用Huffman编码字典解码压缩的数据（差分编码后的数据）
    diff_signal = huffman_decode(compressed_data, codebook)

    # 读取起始值
    start_value = read_start_values(start_value_filename, start_value_index)

    # 根据差分数据恢复原始信号
    restored_signal = [start_value]
    for diff in diff_signal:
        restored_signal.append(restored_signal[-1] + diff)

    return restored_signal


# 绘制信号图
def plot_signal(signal_data):
    # 创建x轴坐标，这里假设每个数据点表示时间上的连续采样
    time_ms = range(len(signal_data))  # time = [0, 1, 2, ..., n-1]
    time = [t / 1000 for t in time_ms]  # 假设采样间隔为1ms，转为秒

    # 绘制信号图
    plt.figure(figsize=(10, 6))
    plt.plot(time, signal_data, marker='o', color='b', markersize=0, linewidth=1.3, label='Decoded Signal')

    # 添加标题和标签
    plt.title('Decoded Physiological Signal Diagram', fontsize=14)
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Signal value', fontsize=12)

    # 显示图例
    plt.legend()

    # 显示网格
    plt.grid(True)

    # 展示图形
    plt.show()


# 解压缩过程
encoded_filename = 'refs_same_codebook/compressed_data_huffman_channel_2.bin'  # 压缩的二进制文件
codebook_filename = 'refs_same_codebook/global_huffman_codebook.txt'  # Huffman编码字典
start_value_filename = 'refs_same_codebook/start_values.txt'  # 起始值文件
start_value_index = 1  # 起始值通道

# 解压缩并恢复信号数据
restore_signal_array = decompress_and_restore_signal(encoded_filename, codebook_filename, start_value_filename, start_value_index)
print("恢复后的信号：", restore_signal_array[:30])  # 仅打印前30个数据点

# 绘制信号图
plot_signal(restore_signal_array)
