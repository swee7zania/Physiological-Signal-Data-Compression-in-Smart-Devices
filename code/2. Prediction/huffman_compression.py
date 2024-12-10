import pyedflib
import numpy as np
import heapq
from collections import defaultdict
import os

# 创建 refs 文件夹（如果不存在）
os.makedirs('refs', exist_ok=True)

# 从 .edf 文件读取信号
def read_edf_signal(file_path, signal_index):
    with pyedflib.EdfReader(file_path) as edf_file:
        signal_data = edf_file.readSignal(signal_index)
    return np.array(signal_data)

# 差分编码函数
def differential_encoding(data):
    diff_encoded = np.diff(data, prepend=data[0])
    return diff_encoded

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

# 保存Huffman编码字典到文件
def save_huffman_codebook(codebook, filename):
    with open(os.path.join('refs', filename), 'w') as f:
        for symbol, code in codebook.items():
            f.write(f"{symbol}: {code}\n")
    print(f"Huffman codebook saved: refs/{filename}")

# 保存压缩数据到二进制文件
def save_compressed_data_to_binary_file(encoded_data, filename):
    with open(os.path.join('refs', filename), 'wb') as f:
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            f.write(bytes([int(byte, 2)]))
    print(f"Compressed data (binary) saved: refs/{filename}")

# 保存起始值到文件
def save_start_value(start_value, filename):
    with open(os.path.join('refs', filename), 'w') as f:
        f.write(str(start_value))
    print(f"Start value saved: refs/{filename}")


if __name__ == "__main__":
    edf_file_path = '../0. data/r01.edf'
    signal_data = read_edf_signal(edf_file_path, signal_index=0)
    print(f"Original signal data length: {len(signal_data)}")

    # 差分编码
    signal_diff = differential_encoding(signal_data)

    # Huffman编码
    huffman_encoded_data, huffman_codebook = huffman_encode(signal_diff)

    # 保存压缩后数据
    save_huffman_codebook(huffman_codebook, 'huffman_codebook.txt')
    save_compressed_data_to_binary_file(huffman_encoded_data, 'compressed_data_huffman.bin')
    save_start_value(signal_diff[0], 'start_value.txt')

    print("\nDifferential encoding (First 30):", signal_diff[:30])
    print("\nHuffman coding completed!")