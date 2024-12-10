import pyedflib
import numpy as np
import heapq
from collections import defaultdict
import os

os.makedirs('refs_diff_codebook', exist_ok=True)

# 从 .edf 文件读取信号
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


# 保存 Huffman 编码字典到文件
def save_huffman_codebook(codebook, filename):
    with open(os.path.join('refs_diff_codebook', filename), 'w') as f:
        for symbol, code in codebook.items():
            f.write(f"{symbol}: {code}\n")
    print(f"Huffman codebook saved: refs_diff_codebook/{filename}")


# 保存压缩数据到二进制文件
def save_compressed_data_to_binary_file(encoded_data, filename):
    with open(os.path.join('refs_diff_codebook', filename), 'wb') as f:
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            f.write(bytes([int(byte, 2)]))
    print(f"Compressed data (binary) saved: refs_diff_codebook/{filename}")


# 保存差分编码起始值
def save_start_value(start_value, filename):
    with open(os.path.join('refs_diff_codebook', filename), 'w') as f:
        f.write(str(start_value))
    print(f"Start value saved: refs_diff_codebook/{filename}")


# 压缩每个通道的信号
def compress_all_channels(edf_filename):
    # 读取 EDF 文件中的信号数据
    signals, _ = read_edf_file(edf_filename)

    for i, signal_data in enumerate(signals):
        print(f"\nProcessing Channel {i + 1}/{len(signals)}...")

        # 差分编码
        diff_signal = np.diff(signal_data, prepend=signal_data[0])

        # Huffman 编码
        huffman_encoded_data, huffman_codebook = huffman_encode(diff_signal)

        # 保存差分编码的起始值
        start_value_filename = f'start_value_channel_{i + 1}.txt'
        save_start_value(signal_data[0], start_value_filename)

        # 保存 Huffman 编码字典
        codebook_filename = f'huffman_codebook_channel_{i + 1}.txt'
        save_huffman_codebook(huffman_codebook, codebook_filename)

        # 保存压缩数据到二进制文件
        compressed_data_filename = f'compressed_data_huffman_channel_{i + 1}.bin'
        save_compressed_data_to_binary_file(huffman_encoded_data, compressed_data_filename)

        print(f"\nChannel {i + 1} compression completed!")

if __name__ == "__main__":
    edf_filename = '../0. data/r01.edf'
    compress_all_channels(edf_filename)
