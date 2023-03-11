from Audio_Converter import*
import librosa
import numpy as np
PATH="./Sound/Test.wav"

f, fs = librosa.load(PATH,sr=44100)
ac= AC(15,fs,f-np.mean(f)) #retire mean(f) pour ne pas avoir de bruit constant en fond, peut être assimilé à un offset

ac.image_generator(4000,windowing=True)

ac.images_to_video("./Image_gen",".png","Sequence",".mp4", PATH)



