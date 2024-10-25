import numpy as np
import pyedflib
import pywt


def compress_ecg(input_file, output_file, wavelet='db1', threshold=0.1):
    edf = pyedflib.EdfReader(input_file)

    n_channels = edf.signals_in_file
    compressed_signals = []

    for i in range(n_channels):
        signal = edf.readSignal(i)

        coeffs = pywt.wavedec(signal, wavelet)

        for j in range(1, len(coeffs)):
            magnitude = np.abs(coeffs[j])
            if np.any(magnitude):
                coeffs[j] = pywt.threshold(coeffs[j], threshold * max(magnitude))
            else:
                coeffs[j] = np.zeros_like(coeffs[j])

        compressed_signal = pywt.waverec(coeffs, wavelet)
        compressed_signals.append(compressed_signal[:len(signal)])

    with pyedflib.EdfWriter(output_file, n_channels, file_type=pyedflib.FILETYPE_EDFPLUS) as writer:
        for i in range(n_channels):
            signal_header = edf.getSignalHeader(i)
            writer.setSignalHeader(i, signal_header)
            print(f"Writing channel {i}: {signal_header}")  # 打印信号头信息
            writer.writePhysicalSamples(compressed_signals[i])

    edf.close()

# 示例用法
input_file = '../0. data/r01.edf'  # 输入的 .edf 文件
output_file = '../compressed_output.edf'  # 输出的压缩 .edf 文件
compress_ecg(input_file, output_file)
