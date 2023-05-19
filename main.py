import tkinter as tk
import customtkinter as ct
from __Init_AC__ import*
from PIL import Image,ImageTk

class Interface():
    def __init__(self):
        self.ac = None
        self.root= ct.CTk()
        self.file = None
        self.label1 = None
        self.frame=None
        self.directory = None

    def window_init(self):
        ct.set_appearance_mode("dark")
        ct.set_default_color_theme("dark-blue")
        self.root.geometry("1100x700")
        self.frame = ct.CTkFrame(master=self.root)
        self.frame.pack(pady=20,padx=20,fill="both", expand=True)
        img= ct.CTkImage(dark_image=Image.open("./Audio_covnerter.png"),size=(961,124))

        #resized = img.resize((961,124))
        label = ct.CTkLabel(master=self.frame, text= "" ,image=img )
        label.pack(pady=12,padx=10)

        button_1 = ct.CTkButton(master=self.frame,
                                        text="Input",
                                        corner_radius=8,
                                        command=self.browser_function)
        button_1.pack(padx=20,pady=20)
        
        self.label1 = ct.CTkLabel(self.frame, text="")
        self.label1.pack(padx=20,pady=5)
        
        button_3 = ct.CTkButton(master=self.frame,
                                text="Output",
                                corner_radius=8,
                                command=self.output_function)
        button_3.pack(padx=20,pady=50)
        
        self.label2 = ct.CTkLabel(self.frame, text="")
        self.label2.pack(padx=20,pady=5)
        
        button_2 = ct.CTkButton(master=self.frame,
                                        text="Conversion",
                                        corner_radius=8,
                                        command=self.launch_function)
        button_2.pack(padx=20,pady=60)
        
        percentage = ct.CTkLabel(self.frame, text="0%")
        percentage.pack()
        progressbar = ct.CTkProgressBar(self.frame,width=400)
        progressbar.set(0)
        progressbar.pack()


        self.root.mainloop()

    def browser_function(self):
        self.file = tk.filedialog.askopenfile(mode='r', filetypes=[('mp3 files','*.mp3'),("wav files",'*.wav')])
        if self.file != None :
            self.file = self.file.name
            self.label1.configure(text=self.file)
        self.ac= Initialize(self.file)
    
    def output_function(self):
        self.directory = tk.filedialog.askdirectory()
        print(self.directory)
        if self.file != None :
            self.ac.output_path = self.directory
            self.label2.configure(text=self.directory)
    
    def launch_function(self):
        self.ac.image_generator(4000,version=2,windowing=True) 
        self.ac.images_to_video(image_folder_path="./Image_gen",extension=".png",video_name="test_interface",output_format=".mp4", audioclip=self.file)

interface = Interface()
interface.window_init()