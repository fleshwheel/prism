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

with open("final.wav", "rb") as f:
    rate, data = wavfile.read(f)
    
if data.dtype == np.int32:
    data = data.astype(np.float32) / (2 ** 31)

data = data / (max(abs(data.flatten())))

print(data.dtype)
print(data)
    
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
    result[idx] = np.log10(abs(w))[:len(freqs) // 2]

print("max is", max(result.flatten()))
print("min is", min(result.flatten()))
    
    
import matplotlib.pyplot as plt
plt.imshow(result)
plt.show()
    
# normalizing ?? need 2 figure out how to calc factor
print(result)
result = result / 32 # -1 to 1 now
result = (result * (2 ** 31)).astype(np.int32)

print(result)

result = np.rot90(result)

print(max(result.flatten()))
print(result.shape)

im = Image.fromarray(result, mode = "I")

im.save("test.png")
