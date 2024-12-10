import pyedflib
import numpy as np
import heapq
from collections import defaultdict
import os

# 创建 refs_same_codebook 文件夹（如果不存在）
os.makedirs('refs_same_codebook', exist_ok=True)

# 读取 .edf 文件的信号
def read_edf_file(filename):
    # 打开 EDF 文件
    f = pyedflib.EdfReader(filename)
    # 提取信号数量
    num_signals = f.signals_in_file
    # 读取所有通道的信号数据
    signals = []
    for i in range(num_signals):
        signals.append(f.readSignal(i))
    # 获取采样频率（假设所有通道相同）
    signal_frequency = f.getSampleFrequency(0)
    f._close()
    return signals, signal_frequency

# Huffman树
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


def huffman_encode(data, codebook):
    encoded_data = ''.join([codebook[val] for val in data])
    return encoded_data

# 保存 Huffman 编码字典到文件
def save_huffman_codebook(codebook, filename):
    with open(os.path.join('refs_same_codebook', filename), 'w') as f:
        for symbol, code in codebook.items():
            f.write(f"{symbol}: {code}\n")
    print(f"Huffman codebook saved: refs_same_codebook/{filename}")

# 保存压缩数据到二进制文件
def save_compressed_data_to_binary_file(encoded_data, filename):
    with open(os.path.join('refs_same_codebook', filename), 'wb') as f:
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            f.write(bytes([int(byte, 2)]))
    print(f"Compressed data (binary) saved: refs_same_codebook/{filename}")

# 保存差分编码起始值
def save_start_values(start_values, filename):
    with open(os.path.join('refs_same_codebook', filename), 'w') as f:
        f.write(','.join(map(str, start_values)))
    print(f"Start value saved: refs_same_codebook/{filename}")


# 压缩所有通道
def compress_all_channels_with_global_codebook(edf_filename):
    # 读取所有通道的信号数据
    signals, _ = read_edf_file(edf_filename)

    # 差分编码
    diff_signals = []
    start_values = []
    for signal_data in signals:
        start_values.append(signal_data[0])  # 记录起始值
        diff_signal = np.diff(signal_data, prepend=signal_data[0])
        diff_signals.append(diff_signal)

    # 合并所有通道的差分数据用于生成全局 Huffman 编码字典
    all_diff_data = np.concatenate(diff_signals)

    # 生成全局 Huffman 编码字典
    global_huffman_root = build_huffman_tree(all_diff_data)
    global_huffman_codebook = generate_huffman_codes(global_huffman_root)

    # 保存全局 Huffman 编码字典
    save_huffman_codebook(global_huffman_codebook, 'global_huffman_codebook.txt')

    # 压缩每个通道的信号并保存
    for i, diff_signal in enumerate(diff_signals):
        print(f"\nProcessing Channel {i + 1}/{len(diff_signals)}...")

        # Huffman 编码
        huffman_encoded_data = huffman_encode(diff_signal, global_huffman_codebook)

        # 保存压缩数据到二进制文件
        compressed_data_filename = f'compressed_data_huffman_channel_{i + 1}.bin'
        save_compressed_data_to_binary_file(huffman_encoded_data, compressed_data_filename)

    # 保存所有通道的差分起始值
    save_start_values(start_values, 'start_values.txt')

    print("\nCompression is complete on all channels!")


# 示例：压缩所有通道的信号
edf_filename = '../0. data/r01.edf'  # 替换为你的 EDF 文件路径
compress_all_channels_with_global_codebook(edf_filename)
