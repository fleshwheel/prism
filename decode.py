import click

import numpy as np
from PIL import Image
from scipy.io import wavfile


RATE = 44_100
WINDOW_SIZE = 2048
FREQ_STEP = 100


@click.command()
@click.option("-i", "--in-file", required=True, help="Input BMP file.")
@click.option("-o", "--out-file", required=True, help="Output mono WAV file (44,100Hz).")
def decode(in_file, out_file):
    spectra = np.asarray(Image.open(in_file)).T.astype(np.float64) / 255

    length = spectra.shape[0] * WINDOW_SIZE

    T = np.linspace(0, length / RATE, spectra.shape[0] * WINDOW_SIZE)

    freqs = list(range(1, RATE // 2, FREQ_STEP))

    components = []

    for freq in freqs:
        components.append(np.sin(2 * np.pi * freq * T + np.random.random()))

    for spec_idx, spectrum in enumerate(spectra):
        for freq_idx, freq in enumerate(freqs):
            for i in range(WINDOW_SIZE):
                components[freq_idx][spec_idx * WINDOW_SIZE + i] *= spectrum[freq_idx]

    result = sum(components)
    result /= max(result.flatten())

    wavfile.write(out_file, RATE, result)

if __name__ == "__main__":
    decode()