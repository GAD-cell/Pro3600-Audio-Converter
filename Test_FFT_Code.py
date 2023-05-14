# Importation des bibliothèques nécessaires
import numpy as np
from math import floor
from Audio_Converter import*

# Définition d'une fonction "test_algo" qui prend en entrée un taux d'échantillonnage
def test_algo(sampling_rate):
    # Initialisation d'un objet AC avec des paramètres spécifiques
    ac = AC(30,FS=sampling_rate,f=None,window_size=1)
    
    # Création d'une séquence de temps échantillonnée à la fréquence donnée
    time = np.arange(0, 1, 1/sampling_rate)
    
    # Création d'une liste de notes de musique
    notes=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    # Initialisation du taux d'erreur à 0
    error_rate=0
    
    # Boucle sur toutes les notes de musique de 21 à 108
    for i in range(21,109):
        # Boucle sur toutes les notes de musique de i à 108
        for j in range(i,109):
            # Création de deux signaux sinusoïdaux correspondant à chaque note de musique
            signal1 = np.sin(2*np.pi*440*2**((i-69)/12)*time)
            signal2 = np.sin(2*np.pi*440*2**((j-69)/12)*time)
            
            # Superposition des deux signaux pour créer un signal combiné
            signal = signal1 + signal2
            
            # Analyse du signal combiné avec l'objet AC créé précédemment
            ac.f=signal
            FFTS = ac.analyze_V2(windowing=True)
            
            # Boucle sur chaque FFT généré pour trouver la note de musique détectée
            for k in range(len(FFTS)):
                notes_amp,notes_freq=ac.no_redundancy(FFTS[k],seuil=0.8)
                for notes_found in notes_amp :
                    # Création de deux notes de musique à partir des fréquences des signaux sinusoïdaux
                    note1=notes[int(i%12)] + str(floor(i/12-1))
                    note2=notes[int(j%12)] + str(floor(j/12-1))
                    
                    # Vérification si la note détectée ne correspond pas aux deux notes créées précédemment
                    if notes_found != note1 and notes_found != note2 :
                        # Si la note détectée ne correspond à aucune des deux notes créées précédemment, incrémentation du taux d'erreur
                        error_rate +=1
    
    # Calcul du taux d'erreur en pourcentage
    error_rate=(error_rate/3828)*100
    
    # Affichage du taux d'erreur
    print("taux d'erreur:" + str(error_rate) + "%" )


test_algo(sampling_rate=22050)                    
