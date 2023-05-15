#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from Audio_Converter import*
import librosa
def Initialize(PATH):
    f, fs = librosa.load(PATH,sr=22050)
    tempo,beat_frames=librosa.beat.beat_track(y=f,sr=fs)
    ac= AC(30,fs,f-np.mean(f),window_size=0.25) #retire mean(f) pour ne pas avoir de bruit constant en fond, peut être assimilé à un offset
    return ac  

    #ac.image_generator(4000,version=2,windowing=True) # fmax affiché, V1 ou V2 , algo de fenêtrage ou pas
    #ac.images_to_video(image_folder_path="./Image_gen",extension=".png",video_name="Tuning_fftcalculate",output_format=".mp4", audioclip=PATH)

Initialize("C:/Users/sinou/OneDrive/Documents/Projet_INFO/Git/Pro3600-Audio-Converter/Sound/Tuning_fork.mp3")