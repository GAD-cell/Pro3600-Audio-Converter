# Pro3600-Audio-Converter

--Instructions :

    L'algorithme sera codé en programmation orienté objet
    On a donc un premier ficher Audio_Converter qui contient la class AC
    cette classe contiendra toutes les fonctions de notre algorithme de conversion

    Le deuxième est __Init_AC__ et il permet d'initialiser le programme, cela nous permettra notamment de faire tout les tests

    Les fichiers .wav et .mp3 servent à faire des tests sur les fonctions

--Etat actuel du programme : 

    Le programme est capable d'identifier les fréquences d'un fichier audio de longueurs quelconques et avec des notes superposées grâce à l'algorithme FFT.
    Il peut générer une séquence d'image représentant l'évolution temporel du spectre audio.
    Les images générées sont stockées dans le dossier Image_gen et sont numérotées dans l'ordre chronologique.
    Les images sont converties en fichier vidéo .mp4 avec le son correspondant afin de s'assurer de la cohérence des piques avec le son.

--Evolution à venir :

    création d'un tableau de conversion entre fréquence et notes de musique.
    Implémenter l'algorithme FFT

--Notes et améliorations :
    
    Amélioration notable : les valeurs étaient normalisées sur chaque portion temporel de l'audio. La normalisation n'était donc pas représentative sur la séquence totale de l'audio lorsqu'on tout était mis à bout.
    La solution a donc été de normaliser les valeurs uniquement après que l'entièreté des transformées de fourier ait été effectué sur toutes les séquences temporelles de l'audio
    L'audio étant coupé en séquence de 1/FPS secondes, il y avait un fort étalement des fréquences sur le spectre. Il a donc fallu procéder à un fenêtrage en utilisant la fonction Hann. Cela a nettement amélioré la précision du spectre.
    Il a fallu aussi soustraire la moyenne du signal temporel au signal d'entrée afin de s'assurer qu'aucun 'offset' n'était envoyé lors de l'execution de l'algo FFT.
