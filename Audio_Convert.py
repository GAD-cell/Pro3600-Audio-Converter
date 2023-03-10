import librosa
import matplotlib.pyplot as plt
import numpy as np
from math import*

class AC(): #Audio Converter

    def __init__(self, FPS, FS, PATH) : #Résolution de l'analyse , fréquence d'échantillonage, chemin du fichier audio
        self.FPS=FPS
        self.FS=FS
        self.f, self.fs= librosa.load(PATH) #audio chargé

    def normalize(self): #normalise les amplitudes de l'audio
        max=0
        for i in range(len(self.f)):
            if self.f[i]>max:
                max=self.f[i]

        normalized=self.f/max
        return(normalized)

    def visualize(self): #visualise le fichier audio sur une partie de la bande son
        f=self.normalize()
        Pxx=[i/self.fs for i in range(len(self.f))]
        fig,ax = plt.subplots()
        plt.plot(Pxx[10000:20000],f[10000:20000], linewidth=2)
        plt.ylabel('Amplitude')
        plt.xlabel('Temps(sec)')
        plt.show()
    
    def analyze(self):

    


