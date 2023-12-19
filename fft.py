#!/usr/bin/python3

import sys
import numpy as np
from PIL import Image
from scipy.io import wavfile
import scipy.signal as signal

BLOCK_SIZE = 512
assert BLOCK_SIZE % 2 == 0

def make_blocks(data):
    overlap = BLOCK_SIZE // 2
    return np.array([data[i : i + BLOCK_SIZE] for i in range(0, len(data) - BLOCK_SIZE, overlap)])

with open("tomato.wav", "rb") as f:
    rate, data = wavfile.read(f)
    
if data.dtype == np.int32:
    data = data.astype(np.float32) / (2 ** 31)

data = data / (max(abs(data.flatten())))

data = data * 8192


    
#left, right = list(zip(*data))    
#data = np.array(left)
    
blocks = make_blocks(data)

window = np.hamming(BLOCK_SIZE)
freqs = np.fft.fftfreq(BLOCK_SIZE, 1 / rate)
print(freqs[:len(freqs) // 2])
result = np.zeros((len(blocks), len(freqs) // 2)).astype(np.float32)
for idx, block in enumerate(blocks):
    windowed_block = np.multiply(block, window)
    w = np.fft.fft(windowed_block)
    for i, val in enumerate(w):
        if val == 0:
            w[i] = 1e-12
    result[idx] = np.log10(abs(w))[:len(freqs) // 2][::-1]

print("max is", max(result.flatten()))
print("min is", min(result.flatten()))

# normalizing ?? need 2 figure out how to calc factor
result = result / max(abs(result.flatten()))
result = np.clip(result, 1e-12, None)

spectrogram = Image.new("RGB", result.shape)

pixels = spectrogram.load()

for row_idx in range(result.shape[0]):
    for col_idx in range(result.shape[1]):
        value = result[row_idx][col_idx]
        magnitude = (abs(value) * (2 ** 8)).astype(np.uint8)
        if value >= 0:
            pixels[row_idx, col_idx] = (magnitude, magnitude, 0)
        else:
            pixels[row_idx, col_idx] = (0, magnitude, magnitude)


import matplotlib.pyplot as plt

plt.imshow(result)
plt.show()

spectrogram.show()
spectrogram.save("0.bmp")
print(result)
