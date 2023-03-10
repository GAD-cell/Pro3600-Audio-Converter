from Audio_Converter import*
import librosa
PATH="./Sound/Test.wav"

f, fs = librosa.load(PATH,sr=44100)
ac= AC(15,fs,f)

ac.image_generator(1000)

ac.images_to_video("./Image_gen",".png","Sequence",".mp4", PATH)