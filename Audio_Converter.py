import matplotlib.pyplot as plt
import numpy as np
from math import*
import moviepy.video.io.ImageSequenceClip
from moviepy.editor import *

class AC(): #Audio Converter

    def __init__(self, FPS, FS, f) : #Résolution de l'analyse , fréquence d'échantillonage, audio pré-chargé
        self.FPS=FPS
        self.fs=FS
        self.f=f

    def normalize_f(self):
        fft=np.fft.fft(self.f,len(self.f))
        max=0
        f_abs=np.abs(fft).real
        for i in range(len(self.f)):
            if f_abs[i]>max:
                max=f_abs[i]
        self.max_f=max
    
    def normalize(self,f): #normalise les amplitudes de l'audio       
        normalized=f/self.max_f
        return(normalized)

    def FFT(self,f,windowing): #on implementera notre propre algorithme FFT plus tard
        if windowing :
            l=[]
            g=np.hanning(len(f))
            for i in range(len(f)):
                l.append(f[i]*g[i])
            fft=np.fft.fft(l,len(l))
        else :
            fft=np.fft.fft(f,len(f))
        fft=np.abs(fft).real
        return(fft)
    
    def analyze(self,windowing): #partitionne l'audio en fonction des FPS qu'on a choisit afin de faire l'analyse de fourier sur chaque portion
        FFTS=[] 
        time=len(self.f)/self.fs
        image_count=floor(time*self.FPS)

        for i in range(image_count):
            FFTS.append(self.FFT(self.f[floor(i*len(self.f)/image_count):floor((i+1)*len(self.f)/image_count)],windowing))
        #on normalise l'ensemble des valeurs
        max=np.amax(FFTS[0])
        for i in range(1,len(FFTS)):
            amax=np.amax(FFTS[i])
            if amax>max :
                max=amax
        for i in range(len(FFTS)):
            FFTS[i]=FFTS[i]/max
        return(FFTS)
    
    def visualize(self,f): #visualise le fichier audio sur une partie de la bande son
        f=self.normalize(f)
        Pxx=[i/self.fs for i in range(len(self.f))]
        fig,ax = plt.subplots()
        plt.plot(Pxx,f, linewidth=2)
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
    
    def image_generator(self,fmax,windowing): #génère une séquence d'image représentant l'évolution du spectre audio dans le temps
        FFTS=self.analyze(windowing)
        Pxx=[j*self.fs/floor(self.fs/self.FPS) for j in range(floor(self.fs/self.FPS))]
        x=[num for num in Pxx if num<=fmax]
        for i in range(len(FFTS)):
            plt.plot(x,FFTS[i][:len(x)], linewidth=2)
            plt.ylim([0,1])
            plt.ylabel('Magnitude')
            plt.xlabel('Fréquence(Hertz)')
            name="./Image_gen/"+str(i)+".png"
            plt.savefig(name)
            plt.close()

    def images_to_video(self,image_folder_path,extension, video_name, output_format, audioclip): #converti séquence image en vidéos
        images = [image_folder_path+'/'+img for img in os.listdir(image_folder_path) if img.endswith(extension)]
        movie_clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(images, self.FPS)
        movie_clip.write_videofile("./Video_gen/"+video_name+output_format)
        videoclip = VideoFileClip("./Video_gen/Sequence.mp4")
        audioclip = AudioFileClip(audioclip)
        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        videoclip.write_videofile("./Video_gen/"+video_name+"_with_sound"+output_format)
