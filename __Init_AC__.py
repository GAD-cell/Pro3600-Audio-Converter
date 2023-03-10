from Audio_Converter import*
import librosa
PATH="./Sound/Tuning_fork.mp3"

f, fs = librosa.load(PATH)
ac= AC(30,fs,f)

#ac.image_generator(1000)

ac.images_to_video("./Image_gen",".png","Sequence",".mp4", PATH)