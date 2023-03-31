from Audio_Converter import*
import librosa
PATH="./Sound/Test.wav"

f, fs = librosa.load(PATH,sr=44100)
tempo,beat_frames=librosa.beat.beat_track(y=f,sr=fs)

ac= AC(30,fs,f-np.mean(f),window_size=1) #retire mean(f) pour ne pas avoir de bruit constant en fond, peut être assimilé à un offset

ac.image_generator(4000,version=2,windowing=True) # fmax affiché, V1 ou V2 , algo de fenêtrage ou pas
ac.images_to_video(image_folder_path="./Image_gen",extension=".png",video_name="Test_superposition",output_format=".mp4", audioclip=PATH)

