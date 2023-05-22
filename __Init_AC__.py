#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from Audio_Converter import*
import librosa
#configure.run()
def Initialize(PATH):
    f, fs = librosa.load(PATH,sr=44000)
    ac= AC(60,fs,f-np.mean(f),window_size=0.5) #retire mean(f) pour ne pas avoir de bruit constant en fond, peut être assimilé à un offset
    tempo, beat_frames = librosa.beat.beat_track(y=f,sr=fs)
    return ac,tempo  

#PATH='C:/Users/sinou/OneDrive/Documents/Projet_INFO/Sound/FJ.mp3'
#f, fs = librosa.load(PATH,sr=22050)
#ac= AC(30,fs,f-np.mean(f),window_size=0.25) #retire mean(f) pour ne pas avoir de bruit constant en fond, peut être assimilé à un offset
#tempo, beat_frames = librosa.beat.beat_track(y=f,sr=fs)
#ac.image_generator(4000,version=2,windowing=True)
#ac.images_to_video(image_folder_path="./Image_gen",extension=".png",video_name="test_FJ",output_format=".mp4", audioclip=PATH)