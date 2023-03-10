from Audio_Converter import*
import librosa
PATH="./Test.wav"

f, fs = librosa.load(PATH)
ac= AC(30,fs,f)

ac.analyze()

