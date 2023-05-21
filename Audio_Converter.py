#!/usr/bin/env python
# -*- coding: utf-8 -*- clear
import matplotlib.pyplot as plt
import numpy as np
from math import*
import moviepy.video.io.ImageSequenceClip
from moviepy.editor import *
import os
from music21 import*

class AC(): #Audio Converter

    def __init__(self, FPS, FS, f,window_size) :     #Résolution de l'analyse , fréquence d'échantillonage, audio pré-chargé
        self.FPS=FPS
        self.fs=FS
        self.f=f
        self.window_size = window_size               #définition de la taille de la fenêtre utilisée pour l'analyse
        self.notes=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"] #définit une liste de notes avec les noms des notes de la gamme chromatique occidentale standard
        self.output_path = None
        self.compteur = 0
        self.chiffrage=[3,4]
    
    def progress(self):
        time=len(self.f)/self.fs
        return self.compteur/round(self.FPS*time)
    
    def normalize(self,f):           #normalise les amplitudes de l'audio en divisant chaque amplitude par la valeur maximale de l'audio     
        for i in range(len(f)):      #recherche de la valeur maximale de f
            if f[i]>max:
                max=f[i]      
        normalized=f/max             #normalise chaque amplitude en la divisant par la valeur maximale.
        return(normalized)           #permet de normaliser les amplitudes de l'audio afin que la plus grande amplitude soit de 1.0 et les autres amplitudes soient proportionnelles à celle-ci
    
    def remove(self,x,L):
        S=[]
        for y in L :
            if y!= x :
                S.append(y)
        return S

    def freq_to_midi(self,freq):                     #associe une fréquence à son nombre MIDI
        if int(freq) != 0 :
            midi=round(12*np.log2(freq/440) + 69)    #La formule de conversion utilise une opération de logarithme et une constante de référence de 440 Hz pour la note A4.
            return(midi)
        return(None)
    
    def freq_to_note(self,freq):     #associe une fréquence à sa note de musique à l'aide d'une méthode de calcul standardisée
        midi=self.freq_to_midi(freq)
        if midi != None :
            note=self.notes[int(midi%12)] + str(floor(midi/12-1))  
            return(note)
        return (None)
    
    def round_rythm(self,duration):
        power=round(np.log2(duration))
        new_duration=2**(power)
        return new_duration



    
    def FFT(self,f,windowing):           #on implementera notre propre algorithme FFT plus tard
        if windowing :                   #la fonction de fenêtrage est appliquée au signal et le signal fenêtré est stocké dans la liste l
            l=[]
            g=np.hanning(len(f))         #utilise la fenêtre de Hanning pour appliquer une pondération sur les échantillons de l'audio pré-chargé
            for i in range(len(f)):      #parcourt tous les échantillons de l'audio pré-chargé, multiplie chacun par la valeur de la fenêtre à son indice, et stocke les résultats dans une nouvelle liste l
                l.append(f[i]*g[i])
            fft=np.fft.rfft(l,len(l))
        else :
            fft=np.fft.rfft(f,len(f))    #FFT calculée sur la liste l en utilisant la fonction np.fft.rfft qui calcule la transformée de Fourier rapide réelle
        fft=np.abs(fft).real    
        return(fft)
    
    def analyze_V1(self,windowing):         #partitionne l'audio en fonction des FPS qu'on a choisit afin de faire l'analyse de fourier sur chaque portion
        FFTS=[] 
        time=len(self.f)/self.fs            #En divisant la longueur totale de l'audio par sa fréquence d'échantillonnage, on obtient la durée totale en secondes
        image_count=floor(time*self.FPS)    #calcule le nombre d'images ou de portions que l'on doit diviser l'audio en fonction de la fréquence de rafraîchissement par seconde (FPS) que l'on a choisi

        for i in range(image_count):
            FFTS.append(self.FFT(self.f[floor(i*len(self.f)/image_count):floor((i+1)*len(self.f)/image_count)],windowing))  #our chaque segment, on utilise la fonction FFT pour calculer la transformée de Fourier de ce segment
        #on normalise l'ensemble des valeurs en divisant chaque amplitude par la valeur maximale de l'audio
        max=np.amax(FFTS[0])
        for i in range(1,len(FFTS)):   
            amax=np.amax(FFTS[i])
            if amax>max :
                max=amax
        for i in range(len(FFTS)):
            FFTS[i]=FFTS[i]/max
        return(FFTS)
    
    def analyze_V2(self, windowing):                    #algorithme de partition par fenêtre qui se décale d'un certain offset à chaque pas
        FFTS=[] 
        time=len(self.f)/self.fs
        image_count=floor(time*self.FPS)
        window_begin=floor(self.fs*self.window_size)    #détermine la taille de la fenêtre en nombre d'échantillons, en multipliant la fréquence d'échantillonnage (self.fs) par la taille de la fenêtre (self.window_size)
        bottom=0                                        #indique le début de la fenêtre courante, qui correspond au premier échantillon de la fenêtre précédente, décalée d'un certain offset
        top=window_begin                                #ndique la fin de la fenêtre courante, qui correspond au dernier échantillon de la fenêtre précédente, décalée du même offset
        while top<=len(self.f):
            FFTS.append(self.FFT(self.f[bottom:top],windowing))     #stocke ensuite chaque transformée de Fourier dans une liste appelée FFTS
            bottom+=floor(self.fs/self.FPS)
            top+=floor(self.fs/self.FPS)
            self.compteur +=1


        #on normalise l'ensemble des valeurs
        max=np.amax(FFTS[0])
        for i in range(1,len(FFTS)):
            amax=np.amax(FFTS[i])
            if amax>max :
                max=amax
        for i in range(len(FFTS)):
            FFTS[i]=FFTS[i]/max
        return(FFTS)
    
    def find_notes(self,fft,seuil):  #trouve les notes sur le spectre audio
        FREQ=[]                      #initialiser une liste vide (FREQ) pour y stocker les fréquences trouvées
        AMP={}                       #dictionnaire vide qui associera à chaque fréquence trouvée son amplitude correspondante
        for i in range(len(fft)):
            if fft[i]>seuil:
                FREQ.append(i*self.fs/floor(self.fs*self.window_size))
                AMP[i*self.fs/floor(self.fs*self.window_size)]=fft[i]       #stocke l'amplitude correspondante à cette fréquence dans le dictionnaire
        return(FREQ,AMP)
    
    def no_redundancy(self,fft,seuil):          #supprime les notes redondantes
        FREQ,AMP=self.find_notes(fft,seuil)     #extraire les fréquences et amplitudes de toutes les notes dont l'amplitude est supérieure au seuil donné
        notes_amp={}
        notes_freq={}
        for freq in FREQ:                       #parcourt ces notes une par une et vérifie si elle est déjà présente dans les dictionnaires 
            note=self.freq_to_note(freq)
            if note in notes_amp and AMP[freq]>notes_amp[note]:     #compare l'amplitude de la note actuelle avec celle déjà présente et la remplace si l'ancienne est plus petite
                notes_amp[note]=AMP[freq]
                notes_freq[note]=freq
            elif note not in notes_amp:         #Si la note n'est pas encore présente, elle l'ajoute aux dictionnaires avec son amplitude et sa fréquence
                notes_amp[note]=AMP[freq]
                notes_freq[note]=freq
        return(notes_amp,notes_freq)
    
    def no_harmonics(self,fft, seuil):#On enlève les harmoniques de chaque note utile
        L= []
        (notes_amp,notes_freq) = self.no_redundancy(fft,seuil)
        for note_f,amp_f in notes_amp.items():#On crée une liste de toutes les notes
            L.append(note_f)
            #print(note_f)
        for i in range (len(L)) :#On cherche les harmoniques de la i-ème note de la liste
            for j in range(i+1,len(L)):
                if L[j][0] == L[i][0] and len(L[j])==len(L[i]):#On compare la lettre de la i-ème note avec celle de la j-ème (ex A3 est une harmmonique de A1)
                    if len(L[j])==3:
                            n= int(L[j][2])-int(L[i][2])
                    else : 
                            n= int(L[j][1])-int(L[i][1])            
                    if notes_amp[L[j]]-0.10*notes_amp[L[j]] < (1/(n+1))*notes_amp[L[i]]: #On vérifie que la potentielle harmonique n'est pas une note utile en comparant son amplitude (marge d'erreur d'amplitude calculé de 10l;m!:,n%)                                           avec l'amplitude théorique qu'aurait une harmonique
                        del notes_amp[L[j]] #On enlève les harmoniques des dictionnaires et de L
                        del notes_freq[L[j]]
                        self.remove(L[j],L)
        return(notes_amp, notes_freq)
    
    def get_rythm(self, windowing, bpm):
        séquence = []  # Liste pour stocker la séquence de rythme
        FFTS = self.analyze_V2(windowing)  # Analyse des FFTs

        # Traitement des FFTs
        for i in range(len(FFTS)):
            FFTS[i] = self.no_harmonics(FFTS[i], seuil=0.2)[0]

        compteur = 0

        # Parcours des FFTs pour construire la séquence de rythme
        for i in range(len(FFTS)):
            séquence.append([])

            if i < len(FFTS) and len(FFTS[i]) == 0:
                # FFT vide, donc occurrence de pause
                occurence = 1
                compteur = i + 1

                # Recherche de la durée de la pause (occurence consécutive de FFTs vides)
                while len(FFTS[compteur]) == 0:
                    occurence = occurence + 1
                    del FFTS[compteur]

                    if compteur == len(FFTS):
                        break

                temps = occurence * (1 / self.FPS)
                rythme = self.round_rythm((temps / (60 / bpm)) * (4 / self.chiffrage[1]))
                séquence[i].append([rythme])
            else:
                if i < len(FFTS):
                    for note, amp in FFTS[i].items():
                        occurence = 1
                        compteur = i + 1

                        # Recherche des occurrences consécutives de la même note
                        while note in FFTS[compteur].keys() and i < len(FFTS):
                            if len(FFTS[compteur]) == 1:
                                del FFTS[compteur]
                            else:
                                del FFTS[compteur][note]
                                compteur += 1
                            occurence = occurence + 1

                        temps = occurence * (1 / self.FPS)
                        rythme = self.round_rythm((temps / (60 / bpm)) * (4 / self.chiffrage[1]))
                        séquence[i].append([note, rythme])

        cleaned_sequence = []

        # Nettoyage de la séquence de rythme: on enlève les séquences vides, les notes de trop faibles durées et les silences en début de partition
        detecteur = 0
        for i in range(len(séquence)):
            if len(séquence[i]) != 0:
                for j in range(len(séquence[i])):
                    if len(séquence[i][j]) > 1 and séquence[i][j][1] < 1 / 16:
                        del séquence[i][j]
            if detecteur == 0:
                if len(séquence[i]) != 0 and len(séquence[i][0]) == 2 
                    detecteur = 1
            if len(séquence[i]) != 0 and detecteur == 1 :
                cleaned_sequence.append(séquence[i])
        print(cleaned_sequence)
        return cleaned_sequence

    def get_partition(self, f):
        s = stream.Stream()  # Crée un objet Stream pour stocker la partition musicale

        for i in range(len(f)):
            if len(f[i]) == 1:
                if len(f[i][0]) == 1:
                    # Pause
                    n = note.Rest()
                    n.quarterLength = f[i][0][0]
                else:
                    # Note unique
                    n = note.Note(f[i][0][0])
                    n.quarterLength = f[i][0][1]
            else:
                # Accord
                accord = []
                for j in range(len(f[i])):
                    m = note.Note(f[i][j][0])
                    m.quarterLength = f[i][0][1]
                    accord.append(m)
                n = chord.Chord(accord)

            s.append(n)  # Ajoute la note ou l'accord à la partition musicaleS
            s.write('xml', fp=self.output_path + '/my_melody.xml')


    def visualize(self,f):      #visualise le fichier audio sur une partie de la bande son
        f=self.normalize(f) 
        Pxx=[i/self.fs for i in range(len(self.f))]     #contient les valeurs du temps en secondes
        fig,ax = plt.subplots()                         #utilisé pour tracer des graphiques à l'intérieur de la figure
        plt.plot(Pxx,f, linewidth=2)                    #trace la courbe du signal audio f par rapport à Pxx
        plt.ylabel('Amplitude')
        plt.xlabel('Temps(sec)')
        plt.show()              #affiche le tracé
   
    def visualize_FFT(self,fft,fmax): #visualise la transormée de fourier jusqu'à fmax
        Pxx=[i*self.fs/len(self.f) for i in range(len(self.f))]     #créer une liste Pxx contenant les fréquences correspondant à chaque point de la FFT (en Hz)
        x=[num for num in Pxx if num<=fmax]                         #crée une nouvelle liste x qui ne contient que les fréquences inférieures ou égales à fmax
        fig,ax = plt.subplots()
        plt.plot(x,fft[:len(x)], linewidth=2)                       #trace la FFT en fonction de la fréquence sur l'axe des abscisses et de la magnitude sur l'axe des ordonnées 
        plt.ylabel('Magnitude')
        plt.xlabel('Fréquence(Hertz)')
        plt.show()
    
    def image_generator(self,fmax,version,windowing):    #génère une séquence d'image représentant l'évolution du spectre audio dans le temps
        if version==1 :
            FFTS=self.analyze_V1(windowing)
            Pxx=[j*self.fs/floor(self.fs/self.FPS) for j in range(floor(self.fs/self.FPS))]     #représente les fréquences à chaque point de l'axe horizontal, en fonction de la méthode d'analyse utilisée et de la fréquence d'échantillonnage fs de l'audio
        else:
            FFTS=self.analyze_V2(windowing)
            Pxx=[j*self.fs/floor(self.fs*self.window_size) for j in range(floor(self.fs*self.window_size))]
        x=[num for num in Pxx if num<=fmax]
        
        for i in range(len(FFTS)):
            #affichage des notes
            notes_amp,notes_freq=self.no_harmonics(FFTS[i],seuil=0.2)      #supprimer les redondances
            plt.plot(x,FFTS[i][:len(x)], linewidth=2)                       #affiche ensuite le spectre audio avec plt.plot et les notes identifiées avec plt.text
            for note in notes_amp:
                plt.text(x=notes_freq[note],y=notes_amp[note],s=note)
            #config de l'affichage
            plt.ylim([0,1])          #afficher les fréquences 
            plt.xlim([10,fmax])      #afficher magnitudes
            plt.ylabel('Magnitude')
            plt.xlabel('Fréquence(Hertz)')
            name="./Image_gen/"+"{:03d}".format(i)+".png"       #permet d'enregistrer avec un affichage de type 000 afin que les images soient dans l'ordre
            plt.savefig(name)                                   #enregistre chaque image générée avec un nom de fichier correspondant à son numéro dans la séquence
            plt.close()

    def images_to_video(self,image_folder_path,extension, video_name, output_format, audioclip): #convertit séquence image en vidéos
        images = [image_folder_path+'/'+img for img in os.listdir(image_folder_path) if img.endswith(extension)]    #on commence par récupérer tous les fichiers images présents dans le dossier spécifié par image_folder_path et ayant l'extension spécifiée par extension
        movie_clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(images, self.FPS)                         #on crée un objet ImageSequenceClip de la bibliothèque MoviePy à partir de ces images avec une fréquence d'images de self.FPS
        movie_clip.write_videofile("./Video_gen/"+video_name+output_format)                                         #on écrit ensuite cette séquence d'images dans un fichier vidéo dans le dossier "./Video_gen/" sous le nom spécifié par video_name et avec le format spécifié par output_format
        videoclip = VideoFileClip("./Video_gen/"+video_name+output_format)                                          #on charge ensuite l'audio du fichier spécifié
        audioclip = AudioFileClip(audioclip)
        new_audioclip = CompositeAudioClip([audioclip])      #on crée un objet CompositeAudioClip avec cet audio chargé
        videoclip.audio = new_audioclip                      #on associe finalement l'objet CompositeAudioClip à la vidéo créée précédemment à l'aide de videoclip.audio
        videoclip.write_videofile(self.output_path + video_name +"_with_sound"+output_format)                            #on écrit ensuite cette nouvelle vidéo, avec l'audio intégré, dans un fichier dans le dossier "./Video_gen/" sous le nom et le format spécifiés


    
