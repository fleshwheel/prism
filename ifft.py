#!/usr/bin/python3

from tqdm import tqdm
import sys
import random
import numpy as np
from PIL import Image
from scipy.io import wavfile

rate = 44100
BLOCK_SIZE = 512
WINDOW_SIZE = BLOCK_SIZE//2
assert BLOCK_SIZE % 2 == 0

im = np.asarray(Image.open("amen.bmp"))
print(im.shape)

mags = np.zeros((im.shape[0], im.shape[1])).astype(np.float32)

for i in range(im.shape[0]):
    for j in range(im.shape[1]):
        if im[i][j][0] > 0:
            mags[i][j] = im[i][j][0]
        if im[i][j][2] < 0:
            mags[i][j] = -im[i][j][2]

print("mags shape is")
print(mags.shape)

mags = mags / (2 ** 8) # scale to 0-1
mags = np.power(mags * 16 - 8, 10)

freqs = np.fft.fftfreq(BLOCK_SIZE, 1 / rate)[:WINDOW_SIZE]

num_samples = len(mags) * WINDOW_SIZE
final_length = num_samples / rate # final length in seconds

result = np.zeros(num_samples).astype(np.float32)

phases = [random.uniform(0,2*np.pi) for j in range(len(freqs))]

print(mags)

for (window_idx, window_start) in tqdm(list(enumerate(range(0, num_samples, WINDOW_SIZE)))):
    
    for tic in range(0, WINDOW_SIZE):
        sample_idx = window_start + tic
        
        for (freq_idx, freq) in enumerate(freqs):
            mag = mags[window_idx][freq_idx]      
            result[sample_idx] += mag * np.sin(2.0 * np.pi * (sample_idx / num_samples) * freq + phases[freq_idx])

result /= np.max(abs(result.flatten()))
    
with open("amen-recovered.wav", "wb") as f:
    wavfile.write(f, rate, result)

from scipy.signal import spectrogram

f, t, Sxx = spectrogram(result, rate)
import matplotlib.pyplot as plt
plt.imshow(Sxx)
plt.show()

print(result.shape)
