#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from Audio_Converter import*
import librosa
#configure.run()
def Initialize(PATH):
    f, fs = librosa.load(PATH,sr=22050)
    ac= AC(30,fs,f-np.mean(f),window_size=0.25) #retire mean(f) pour ne pas avoir de bruit constant en fond, peut être assimilé à un offset
    return ac  

PATH= "C:/Users/sinou/OneDrive/Documents/Projet_INFO/Sound/melody_simple.mp3"
f, fs = librosa.load(PATH,sr=22050)
ac= AC(30,fs,f-np.mean(f),window_size=0.25)
print("Init")
analyse = ac.get_rythm(windowing=True,bpm=60)
print("analysé")
ac.get_partition(analyse)