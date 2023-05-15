import tkinter as tk
import customtkinter as ct
from __Init_AC__ import*

class Interface():
    def __init__(self):
        self.ac = None
        self.root= ct.CTk()
        self.file = None
    def window_init(self):
        ct.set_appearance_mode("dark")
        ct.set_default_color_theme("dark-blue")
        self.root.geometry("1000x700")
        frame = ct.CTkFrame(master=self.root)
        frame.pack(pady=20,padx=60,fill="both", expand=True)
        label = ct.CTkLabel(master=frame, text= "Audio Converter" )
        label.pack(pady=12,padx=10)

        button_1 = ct.CTkButton(master=frame,
                                        text="Browse",
                                        corner_radius=8,
                                        command=self.browser_function)
        button_1.pack(padx=20,pady=20)

        button_2 = ct.CTkButton(master=frame,
                                        text="Conversion",
                                        corner_radius=8,
                                        command=self.launch_function)
        button_2.pack(padx=20,pady=100)
        self.root.mainloop()

    def browser_function(self):
        self.file = tk.filedialog.askopenfile(mode='r', filetypes=[('mp3 files','*.mp3'),("wav files",'*.wav')]).name
        try :
            self.ac = Initialize(self.file)
        except AttributeError : 
            pass

    def launch_function(self):
        self.ac.image_generator(4000,version=2,windowing=True) 
        self.ac.images_to_video(image_folder_path="./Image_gen",extension=".png",video_name="test_interface",output_format=".mp4", audioclip=self.file)

interface = Interface()
interface.window_init()