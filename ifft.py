#!/usr/bin/python3

import sys
import numpy as np
from PIL import Image
from scipy.io import wavfile

rate = 44100
BLOCK_SIZE = 256
assert BLOCK_SIZE % 2 == 0

im = np.asarray(Image.open("out.bmp"))
im = np.rot90(im, 3).astype(np.float32) / (2 ** 8)

print("shape of u")
print(im.shape)

import matplotlib.pyplot as plt

magnitudes = np.zeros((im.shape[0] * int(BLOCK_SIZE / 2), BLOCK_SIZE))

for (line_idx, line) in enumerate(im):
    for idx in range(int(BLOCK_SIZE / 2)):
        magnitudes[line_idx * int(BLOCK_SIZE / 2) + idx] = line

magnitudes = magnitudes * 1_552_737.0

freqs = np.fft.fftfreq(BLOCK_SIZE, 1 / rate)


print("freqs are")
print(freqs)


num_samples = len(magnitudes)
final_length = num_samples / rate # final length in seconds

full_spectrum = np.array([[np.sin(f * t * 2 * np.pi) for f in freqs] for t in np.linspace(0, final_length, num_samples)])
result = np.zeros(im.shape[0] * int(BLOCK_SIZE / 2)).astype(np.float32)

with open("344.wav", "wb") as f:
    data = full_spectrum[:,2]
    wavfile.write(f, rate, data)

import matplotlib.pyplot as plt

#plt.plot(full_spectrum[:,1])
#plt.plot(full_spectrum[:,2])
#plt.show()

print("setting this many")

#magnitudes = np.zeros(magnitudes.shape)
#for row in magnitudes:
#    row[1] = 1000

for i in range(len(result)):
    result[i] = np.dot(full_spectrum[i], magnitudes[i])

result /= np.max(result, axis=0)
    
with open("translated.wav", "wb") as f:
    wavfile.write(f, rate, result)

print(result.shape)
