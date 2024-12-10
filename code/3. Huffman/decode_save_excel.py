import pandas as pd
import os

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


# 解压缩并恢复信号数据
def decompress_and_restore_signal(encoded_filename, codebook_filename):
    # 读取Huffman编码字典
    codebook = read_huffman_codebook(codebook_filename)

    # 读取压缩的二进制数据
    compressed_data = read_compressed_data(encoded_filename)

    # 使用Huffman编码字典解码压缩的数据
    decoded_signal = huffman_decode(compressed_data, codebook)

    return decoded_signal


# 保存恢复后的数据到Excel文件
def save_data_to_excel(data, filename):
    # 将数据转为DataFrame，假设每个信号是一个单独的行
    df = pd.DataFrame(data, columns=["Decoded Signal"])

    # 保存为Excel文件
    df.to_excel(os.path.join('refs', filename), index=False)
    print(f"数据已保存到Excel文件: refs/{filename}")


# 解压缩过程
encoded_filename = 'refs/compressed_data_huffman.bin'  # 压缩的二进制文件
codebook_filename = 'refs/huffman_codebook.txt'  # Huffman编码字典

restore_signal_array = decompress_and_restore_signal(encoded_filename, codebook_filename)
print("恢复后的信号：", restore_signal_array)
# 保存数据到Excel文件
save_data_to_excel(restore_signal_array, 'restored_data.xlsx')