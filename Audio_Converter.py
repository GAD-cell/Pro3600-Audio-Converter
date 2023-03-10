import librosa
import matplotlib.pyplot as plt
import numpy as np
from math import*

class AC(): #Audio Converter

    def __init__(self, FPS, FS, f) : #Résolution de l'analyse , fréquence d'échantillonage, audio pré-chargé
        self.FPS=FPS
        self.fs=FS
        self.f=f #on prend la fréquence d'échantillonage de librosa pour commencer (22050 hz)

    def normalize(self,f): #normalise les amplitudes de l'audio
        max=0
        for i in range(len(f)):
            if f[i]>max:
                max=f[i]

        normalized=f/max
        return(normalized)

    def FFT(self,f): #on implementera notre propre algorithme FFT plus tard
        fft=np.fft.fft(self.f,len(self.f))
        fft=np.abs(fft).real
        fft=self.normalize(fft)
        return(fft)
    
    def visualize(self,f): #visualise le fichier audio sur une partie de la bande son
        f=self.normalize(f)
        Pxx=[i/self.fs for i in range(len(self.f))]
        fig,ax = plt.subplots()
        plt.plot(Pxx[10000:20000],f[10000:20000], linewidth=2)
        plt.ylabel('Amplitude')
        plt.xlabel('Temps(sec)')
        plt.show()
   
    def visualize_FFT(self,fft,fmax): #visualise la transormée de fourier jusqu'à fmax
        Pxx=[i*self.fs/len(self.f) for i in range(len(self.f))]
        x=[num for num in Pxx if num<=fmax]
        fig,ax = plt.subplots()
        plt.plot(x,fft[:len(x)], linewidth=2)
        plt.ylabel('Magnitude')
        plt.xlabel('Fréquence(Hertz)')
        plt.show()
    
    def analyze(self): #partitionne l'audio en fonction des FPS qu'on a choisit afin de faire l'analyse de fourier sur chaque portion
        FFTS=[] 
        time=len(self.f)/self.fs
        image_count=floor(time*self.FPS)

        for i in range(image_count):
            FFTS.append(self.FFT(self.f[floor(i*len(self.f)/image_count):floor((i+1)*len(self.f)/image_count)]))