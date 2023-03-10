import librosa
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from scipy.signal import find_peaks

# Load data and sampling frequency from the data file
data, sampling_frequency = librosa.load('.\Test.mp3')

# Get some useful statistics
T = 1/sampling_frequency # Sampling period
N = len(data) # Signal length in samples
t = N / sampling_frequency # Signal length in seconds
print(N)
Y_k = np.fft.fft(data)[0:int(N/2)]/N # FFT
Y_k[1:] = 2*Y_k[1:] # Single-sided spectrum
Pxx = np.abs(Y_k) # Power spectrum

f = sampling_frequency * np.arange((N/2)) / N; # frequencies

# plotting
fig,ax = plt.subplots()
plt.plot(f[0:5000], Pxx[0:5000], linewidth=2)
plt.ylabel('Amplitude')
plt.xlabel('Frequency [Hz]')
plt.show()

auto = sm.tsa.acf(data, nlags=2000)
peaks = find_peaks(auto)[0] # Find peaks of the autocorrelation
lag = peaks[0] # Choose the first peak as our pitch component lag
pitch = sampling_frequency / lag # Transform lag into frequency
print(pitch)