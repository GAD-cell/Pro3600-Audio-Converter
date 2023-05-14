from moviepy.editor import *
videoclip = VideoFileClip(r"C:\Users\sinou\OneDrive\Documents\Projet_INFO\Git\Pro3600-Audio-Converter\Sequence.mp4")
audioclip = AudioFileClip(r"C:\Users\sinou\OneDrive\Documents\Projet_INFO\Git\Pro3600-Audio-Converter\Test.wav")

new_audioclip = CompositeAudioClip([audioclip])
videoclip.audio = new_audioclip
videoclip.write_videofile("new_filename.mp4")