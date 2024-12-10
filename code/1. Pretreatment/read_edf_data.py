import pyedflib

def read_edf(file_path):
    f = pyedflib.EdfReader(file_path)
    n_signals = f.signals_in_file
    signal_labels = f.getSignalLabels()
    signals = []

    for i in range(n_signals):
        signals.append(f.readSignal(i))

    f.close()
    return signals, signal_labels


if __name__ == "__main__":
    file_path = '../0. data/r01.edf'
    signals, labels = read_edf(file_path)
    print(f"Loaded {len(signals)} signals with labels: {labels}")

