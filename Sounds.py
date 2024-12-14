import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "heart": pygame.mixer.Sound("Sounds/preview.mp3"),
            "death": pygame.mixer.Sound("Sounds/mort.wav"),
            "attack": pygame.mixer.Sound("Sounds/attack_sound.wav.wav")
        }

    def play_sound(self, sound_name):
        """Joue un son spécifique s'il est chargé."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Son '{sound_name}' introuvable.")
