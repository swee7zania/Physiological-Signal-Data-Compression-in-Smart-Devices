import numpy as np

def snr_db_to_linear(snr_db):
    """将 SNR 从 dB 转为线性值"""
    return 10**(snr_db / 10)

def shannon_capacity(bandwidth_hz, snr_db):
    """根据香农定理计算信道容量"""
    snr_linear = snr_db_to_linear(snr_db)
    capacity = bandwidth_hz * np.log2(1 + snr_linear)  # 单位 bps
    return capacity

def required_bandwidth(data_rate_bps, snr_db):
    """根据目标数据速率和 SNR 计算所需带宽"""
    snr_linear = snr_db_to_linear(snr_db)
    bandwidth = data_rate_bps / np.log2(1 + snr_linear)  # 单位 Hz
    return bandwidth

if __name__ == "__main__":
    # 设定参数
    bandwidth_hz = 2e6  # 带宽 2 MHz
    snr_db = 20         # 信噪比 20 dB
    data_rate_bps = 250e3  # 目标数据速率 250 kbps

    # 计算信道容量
    capacity = shannon_capacity(bandwidth_hz, snr_db)
    print(f"Channel Capacity: {capacity / 1e6:.2f} Mbps")

    # 计算所需带宽
    required_bw = required_bandwidth(data_rate_bps, snr_db)
    print(f"Required Bandwidth for {data_rate_bps / 1e3:.1f} kbps: {required_bw / 1e6:.2f} MHz")
