import pyedflib
import numpy as np
import heapq
from collections import defaultdict
import os

# 创建refs_diff_codebook文件夹（如果不存在）
os.makedirs('refs_diff_codebook', exist_ok=True)

# 读取.edf文件的信号
def read_edf_file(filename):
    # 打开EDF文件
    f = pyedflib.EdfReader(filename)

    # 提取所有信号的数量
    num_signals = f.signals_in_file

    # 获取每个信号的采样频率
    signal_frequency = f.getSampleFrequency(0)

    # 获取所有信号数据
    signal_data = []
    for i in range(num_signals):
        signal_data.append(f.readSignal(i))  # 读取每个通道的数据

    f._close()  # 关闭文件

    return signal_data, signal_frequency


# Huffman编码相关函数
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(data):
    frequency = defaultdict(int)
    for value in data:
        frequency[value] += 1

    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]


def generate_huffman_codes(root, prefix='', codebook={}):
    if root:
        if root.char is not None:
            codebook[root.char] = prefix
        generate_huffman_codes(root.left, prefix + '0', codebook)
        generate_huffman_codes(root.right, prefix + '1', codebook)
    return codebook


def huffman_encode(data):
    root = build_huffman_tree(data)
    codebook = generate_huffman_codes(root)
    encoded_data = ''.join([codebook[val] for val in data])
    return encoded_data, codebook


# 保存压缩数据到文本文件
def save_compressed_data_to_file(encoded_data, filename):
    with open(os.path.join('refs_diff_codebook', filename), 'w') as f:
        f.write(encoded_data)
    print(f"压缩数据已保存到文件: refs_diff_codebook/{filename}")


# 保存Huffman编码字典到文件
def save_huffman_codebook(codebook, filename):
    with open(os.path.join('refs_diff_codebook', filename), 'w') as f:
        for symbol, code in codebook.items():
            f.write(f"{symbol}: {code}\n")
    print(f"Huffman编码字典已保存到文件: refs_diff_codebook/{filename}")


# 保存压缩数据到二进制文件
def save_compressed_data_to_binary_file(encoded_data, filename):
    with open(os.path.join('refs_diff_codebook', filename), 'wb') as f:
        # 将每个字节写入二进制文件
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            f.write(bytes([int(byte, 2)]))
    print(f"压缩数据（以二进制格式）已保存到文件: refs_diff_codebook/{filename}")


# 示例：读取edf文件并进行处理
filename = '../0. data/r01.edf'  # 将此替换为你自己的edf文件路径

# 读取信号数据
signal_data, signal_frequency = read_edf_file(filename)
print(f"信号数据长度: {len(signal_data[0])}")

# 处理每个通道的数据
for channel_index, channel_data in enumerate(signal_data):
    print(f"正在处理第{channel_index + 1}通道数据...")

    # Huffman编码
    huffman_encoded_data, huffman_codebook = huffman_encode(channel_data)
    print(f"第{channel_index + 1}通道 Huffman 编码结果:", huffman_encoded_data[:30])  # 输出前30个字符

    # 保存每个通道的压缩数据和字典到文件
    # save_compressed_data_to_file(huffman_encoded_data, f'compressed_data_huffman_channel_{channel_index + 1}.txt')
    save_huffman_codebook(huffman_codebook, f'huffman_codebook_channel_{channel_index + 1}.txt')
    save_compressed_data_to_binary_file(huffman_encoded_data, f'compressed_data_huffman_channel_{channel_index + 1}.bin')

print("所有通道的压缩操作已完成！")