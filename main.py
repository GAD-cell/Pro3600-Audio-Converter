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
        self.percentage = None
        self.tempo=None

    def window_init(self):
        # Définit le mode d'apparence en mode sombre
        ct.set_appearance_mode("dark")
        # Définit le thème de couleur par défaut en bleu foncé
        ct.set_default_color_theme("dark-blue")
        # Définit la taille de la fenêtre racine
        self.root.geometry("1100x700")
        # Crée un cadre Tkinter à l'intérieur de la fenêtre racine
        self.frame = ct.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Charge une image à partir d'un fichier
        img = ct.CTkImage(dark_image=Image.open("./Audio_covnerter.png"), size=(961, 124))

        # Crée une étiquette avec l'image chargée
        label = ct.CTkLabel(master=self.frame, text="", image=img)
        label.pack(pady=12, padx=10)

        # Crée un bouton pour sélectionner le chemin d'entrée
        button_1 = ct.CTkButton(master=self.frame, text="Chemin d'entrée", corner_radius=8, command=self.browser_function)
        button_1.pack(padx=20, pady=20)

        # Crée une étiquette pour afficher le chemin d'entrée sélectionné
        self.label1 = ct.CTkLabel(self.frame, text="")
        self.label1.pack(padx=20, pady=5)

        # Crée un bouton pour sélectionner le chemin de sortie
        button_3 = ct.CTkButton(master=self.frame, text="Chemin de sortie", corner_radius=8, command=self.output_function)
        button_3.pack(padx=20, pady=50)

        # Crée une étiquette pour afficher le chemin de sortie sélectionné
        self.label2 = ct.CTkLabel(self.frame, text="")
        self.label2.pack(padx=20, pady=5)

        # Crée un bouton pour lancer la conversion
        button_2 = ct.CTkButton(master=self.frame, text="Conversion", corner_radius=8, command=self.launch_function)
        button_2.pack(padx=20, pady=60)

        # Lance la boucle principale de l'interface utilisateur
        self.root.mainloop()

    def browser_function(self):
        self.file = tk.filedialog.askopenfile(mode='r', filetypes=[('mp3 files','*.mp3'),("wav files",'*.wav')])
        if self.file != None :
            self.file = self.file.name
            self.label1.configure(text=self.file)
        self.ac, self.tempo= Initialize(self.file)
    
    def output_function(self):
        self.directory = tk.filedialog.askdirectory()
        if self.file != None :
            self.ac.output_path = self.directory
            self.label2.configure(text=self.directory)
    
    def launch_function(self):
        print("Init")
        analyse = self.ac.get_rythm(windowing=True,bpm=self.tempo)
        print("analysé")
        self.ac.get_partition(analyse)

interface = Interface()
interface.window_init()