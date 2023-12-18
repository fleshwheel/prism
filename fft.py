#!/usr/bin/python3

import sys
import numpy as np
from PIL import Image
from scipy.io import wavfile

BLOCK_SIZE = 256
assert BLOCK_SIZE % 2 == 0

def make_blocks(data):
    overlap = int(BLOCK_SIZE / 2)
    return np.array([data[i : i + BLOCK_SIZE] for i in range(0, len(data) - BLOCK_SIZE, overlap)])

with open("lall.wav", "rb") as f:
    rate, data = wavfile.read(f)
    
blocks = make_blocks(data)

window = np.hamming(BLOCK_SIZE)
freqs = np.fft.fftfreq(BLOCK_SIZE)
result = np.zeros((len(blocks), len(freqs)))
for idx, block in enumerate(blocks):
    windowed_block = np.multiply(block, window)
    w = np.fft.fft(windowed_block)
    result[idx] = abs(w)

print("first results like")
print("result[0] = ", result[0])
    
result = result / max(result.flatten())
result = (result * (2 ** 8)).astype(np.int8)

result = np.rot90(result)

print(result.shape)

im = Image.fromarray(result, mode = "L")

im.save("out.bmp")
