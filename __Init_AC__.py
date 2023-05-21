#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from Audio_Converter import*
import librosa
#configure.run()
def Initialize(PATH):
    f, fs = librosa.load(PATH,sr=22050)
    ac= AC(30,fs,f-np.mean(f),window_size=0.25) #retire mean(f) pour ne pas avoir de bruit constant en fond, peut être assimilé à un offset
    tempo, beat_frames = librosa.beat.beat_track(y=f,sr=fs)
    return ac,tempo  



