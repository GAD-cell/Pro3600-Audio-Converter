import matplotlib.pyplot as plt
import numpy as np
from math import*
import moviepy.video.io.ImageSequenceClip
from moviepy.editor import *
import os

class AC(): #Audio Converter

    def __init__(self, FPS, FS, f,window_size) : #Résolution de l'analyse , fréquence d'échantillonage, audio pré-chargé
        self.FPS=FPS
        self.fs=FS
        self.f=f
        self.window_size = window_size
        self.notes=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    def normalize(self,f): #normalise les amplitudes de l'audio       
        for i in range(len(f)):
            if f[i]>max:
                max=f[i]      
        normalized=f/max
        return(normalized)

    def freq_to_midi(self,freq): #associe une fréquence à son nombre MIDI
        if int(freq) != 0 :
            midi=round(12*np.log2(freq/440) + 69)
            return(midi)
        return(None)
    
    def freq_to_note(self,freq): #associe une fréquence à sa note de musique
        midi=self.freq_to_midi(freq)
        if midi != None :
            note=self.notes[int(midi%12)] + str(floor(midi/12-1))
            return(note)
        return (None)
    
    def FFT(self,f,windowing): #on implementera notre propre algorithme FFT plus tard
        if windowing :
            l=[]
            g=np.hanning(len(f))
            for i in range(len(f)):
                l.append(f[i]*g[i])
            fft=np.fft.rfft(l,len(l))
        else :
            fft=np.fft.rfft(f,len(f))
        fft=np.abs(fft).real
        return(fft)
    
    def analyze_V1(self,windowing): #partitionne l'audio en fonction des FPS qu'on a choisit afin de faire l'analyse de fourier sur chaque portion
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
    
    def analyze_V2(self, windowing): #algorithme de partition par fenêtre qui se décale d'un certain offset à chaque pas
        FFTS=[] 
        time=len(self.f)/self.fs
        image_count=floor(time*self.FPS)
        window_begin=floor(self.fs*self.window_size)
        bottom=0
        top=window_begin
        while top<=len(self.f):
            FFTS.append(self.FFT(self.f[bottom:top],windowing))
            bottom+=floor(self.fs/self.FPS)
            top+=floor(self.fs/self.FPS)

        #on normalise l'ensemble des valeurs
        max=np.amax(FFTS[0])
        for i in range(1,len(FFTS)):
            amax=np.amax(FFTS[i])
            if amax>max :
                max=amax
        for i in range(len(FFTS)):
            FFTS[i]=FFTS[i]/max
        return(FFTS)
    
    def find_notes(self,fft,seuil): #trouve les notes sur le spectre audio
        FREQ=[]
        AMP={}
        for i in range(len(fft)):
            if fft[i]>seuil:
                FREQ.append(i*self.fs/floor(self.fs*self.window_size))
                AMP[i*self.fs/floor(self.fs*self.window_size)]=fft[i]
        return(FREQ,AMP)
    
    def no_redundancy(self,fft,seuil):#supprime les notes redondantes
        FREQ,AMP=self.find_notes(fft,seuil)
        notes_amp={}
        notes_freq={}
        for freq in FREQ:
            note=self.freq_to_note(freq)
            if note in notes_amp and AMP[freq]>notes_amp[note]:
                notes_amp[note]=AMP[freq]
                notes_freq[note]=freq
            elif note not in notes_amp:
                notes_amp[note]=AMP[freq]
                notes_freq[note]=freq
        return(notes_amp,notes_freq)

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
    
    def image_generator(self,fmax,version,windowing): #génère une séquence d'image représentant l'évolution du spectre audio dans le temps
        if version==1 :
            FFTS=self.analyze_V1(windowing)
            Pxx=[j*self.fs/floor(self.fs/self.FPS) for j in range(floor(self.fs/self.FPS))]
        else:
            FFTS=self.analyze_V2(windowing)
            Pxx=[j*self.fs/floor(self.fs*self.window_size) for j in range(floor(self.fs*self.window_size))]
        x=[num for num in Pxx if num<=fmax]
        
        for i in range(len(FFTS)):
            #affichage des notes
            notes_amp,notes_freq=self.no_redundancy(FFTS[i],seuil=0.2)
            print(notes_amp)
            plt.plot(x,FFTS[i][:len(x)], linewidth=2)
            for note in notes_amp:
                plt.text(x=notes_freq[note],y=notes_amp[note],s=note)
            #config de l'affichage
            plt.ylim([0,1])
            plt.xlim([10,fmax])
            plt.ylabel('Magnitude')
            plt.xlabel('Fréquence(Hertz)')
            name="./Image_gen/"+"{:03d}".format(i)+".png" #permet d'enregistrer avec un affichage de type 000 afin que les images soient dans l'ordre
            plt.savefig(name)
            plt.close()

    def images_to_video(self,image_folder_path,extension, video_name, output_format, audioclip): #converti séquence image en vidéos
        images = [image_folder_path+'/'+img for img in os.listdir(image_folder_path) if img.endswith(extension)]
        movie_clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(images, self.FPS)
        movie_clip.write_videofile("./Video_gen/"+video_name+output_format)
        videoclip = VideoFileClip("./Video_gen/"+video_name+output_format)
        audioclip = AudioFileClip(audioclip)
        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        videoclip.write_videofile("./Video_gen/"+video_name+"_with_sound"+output_format)


    