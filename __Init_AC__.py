from Audio_Converter import*
import librosa
PATH="./Sound/Test.wav"

f, fs = librosa.load(PATH,sr=22050)
ac= AC(30,fs,f-np.mean(f),window_size=0.25) #retire mean(f) pour ne pas avoir de bruit constant en fond, peut être assimilé à un offset

ac.image_generator(1000,Version=1,windowing=True) # famx affiché, V1 ou V2 , algo de fenêtrage ou pas

ac.images_to_video(Emplacement_image="./Image_gen",format_entree=".png",Nom_video="Sequence",format_sortie=".mp4", chemin_audio=PATH)

