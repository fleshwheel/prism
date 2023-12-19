# prism

Prism is a command-line tool converting between audio and image representations of frequency intensity over time. This tool is intended for creative synesthetic research by providing a visual representation of audio represented the way humans seem to hear -- a "spectrum" of frequencies -- which also happens to be an extremely useful perspective in science and engineering.

Messing around with this code for artistic purposes is very encouraged! Some features I want to try and add are:

- mapping 24 bit integers to RGB space to increase bit depth in images!
- including phase somehow, perhaps in RGB color space?

# Issues
- Don't know how to calculate scaling factor for fft.py. For sample sizes we have:


1024 -- 155890496
512 -- 131783648
256 -- 121652056
128 -- 110638472
64 -- 97089592