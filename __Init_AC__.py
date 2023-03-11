from Audio_Converter import*
import librosa
PATH="./Sound/Tuning_fork.mp3"

f, fs = librosa.load(PATH,sr=22050)
ac= AC(30,fs,f-np.mean(f),window_size=0.25) #retire mean(f) pour ne pas avoir de bruit constant en fond, peut être assimilé à un offset

ac.image_generator(1000,windowing=False)

ac.images_to_video("./Image_gen",".png","Sequence",".mp4", PATH)
