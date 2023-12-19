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

im = np.asarray(Image.open("out.bmp"))
mags = np.rot90(im, 3).astype(np.float32)

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
            result[sample_idx] += mag * np.sin(2 * np.pi * freq * (sample_idx / num_samples) + phases[freq_idx])

result /= np.max(abs(result.flatten()))
    
with open("final.wav", "wb") as f:
    wavfile.write(f, rate, result)

print(result.shape)
