import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# User input for the bitstream
bitstream = input("Enter the bitstream (e.g., 1011001): ")
bitstream = [int(b) for b in bitstream]

# Time settings
bit_duration = 1  # Time duration for each bit
t = np.arange(0, len(bitstream) * bit_duration, 0.01)

# Encoding Methods

# 1. Unipolar NRZ: High for 1, Low (0) for 0
def unipolar_nrz(bits):
    return np.repeat(bits, 100)

# 2. Unipolar RZ: High for half the bit duration, Low for the other half
def unipolar_rz(bits):
    signal = []
    for bit in bits:
        signal.extend([bit] * 50 + [0] * 50)  # High for 50% of time, then zero
    return signal

# 3. Polar NRZ-L: +1 for 1, -1 for 0 (no return to zero)
def polar_nrz_l(bits):
    return np.repeat([1 if bit == 1 else -1 for bit in bits], 100)

# 4. Polar NRZ-I: Toggle on '1', hold value on '0'
def polar_nrz_i(bits):
    signal = []
    last = -1
    for bit in bits:
        if bit == 1:
            last = -last
        signal.append(last)
    return np.repeat(signal, 100)

# 5. Polar RZ: +1 for 1, -1 for 0, but returns to 0 in the second half
def polar_rz(bits):
    signal = []
    for bit in bits:
        if bit == 1:
            signal.extend([1]*50 + [0]*50)
        else:
            signal.extend([-1]*50 + [0]*50)
    return signal

# 6. Manchester IEEE: 1 is high-to-low transition, 0 is low-to-high
def manchester_ieee(bits):
    signal = []
    for bit in bits:
        if bit == 1:
            signal.extend([-1]*50 + [1]*50)  # Low to High transition for 1
        else:
            signal.extend([1]*50 + [-1]*50)  # High to Low transition for 0
    return signal

# 7. Differential Manchester: Transitions at start of every bit, with transition in middle only for 0
def differential_manchester(bits):
    signal = []
    last = -1
    for bit in bits:
        if bit == 1:
            signal.extend([last]*50 + [-last]*50)  # No middle transition for '1'
        else:
            last = -last
            signal.extend([last]*50 + [-last]*50)  # Middle transition for '0'
    return signal

# Function to plot signal and PSD
def plot_signal_and_psd(signal, title):
    plt.figure(figsize=(12, 5))

    # Plot signal
    plt.subplot(1, 2, 1)
    plt.plot(t[:len(signal)], signal)
    plt.title(f'{title} Encoding')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.grid()

    # Calculate and plot Power Spectral Density (PSD)
    f, psd = welch(signal, fs=100, nperseg=256)
    plt.subplot(1, 2, 2)
    plt.semilogy(f, psd)
    plt.title(f'PSD of {title}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')
    plt.grid()

    plt.tight_layout()
    plt.show()

# List of encoding methods
encoding_methods = [
    ('Unipolar NRZ', unipolar_nrz),
    ('Unipolar RZ', unipolar_rz),
    ('Polar NRZ-L', polar_nrz_l),
    ('Polar NRZ-I', polar_nrz_i),
    ('Polar RZ', polar_rz),
    ('Manchester IEEE', manchester_ieee),
    ('Differential Manchester', differential_manchester)
]

# Loop through each encoding, plot signal and PSD
for title, encoding_fn in encoding_methods:
    signal = encoding_fn(bitstream)
    plot_signal_and_psd(signal, title)
