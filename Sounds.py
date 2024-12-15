import pygame

class SoundManager:
    """
    Gestionnaire de sons pour jouer des effets sonores spécifiques dans le jeu.
    Attributs :
    - sounds (dict) : Dictionnaire associant des noms de sons à des objets pygame.mixer.Sound.
    """
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "heart": pygame.mixer.Sound("Sounds/preview.mp3"),
            "death": pygame.mixer.Sound("Sounds/mort.wav"),
            "attack": pygame.mixer.Sound("Sounds/attack_sound.wav.wav")
        }

    def play_sound(self, sound_name):
        """
        Joue un son spécifique s'il est chargé dans le gestionnaire.
        Entrées :
        - sound_name (str) : Nom du son à jouer (doit correspondre à une clé dans le dictionnaire `sounds`).
        Sorties :
        - Joue le son correspondant si trouvé.
        - Affiche un message d'erreur dans la console si le son n'existe pas dans `sounds`.
        """
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Son '{sound_name}' introuvable.")
