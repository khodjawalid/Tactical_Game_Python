
import pygame
from game import *
from unit import * 
from terain import *


class Arme:
    """Classe pour représenter une arme."""
    def __init__(self, nom, degats, deplacement_distance, effet):
        self.nom = nom
        self.degats = degats
        self.deplacement_distance = deplacement_distance
        self.effet = effet  # Une fonction représentant l'effet de l'arme

    def utiliser(self, utilisateur, cible, terrain=None):
        """Utilise l'arme sur une cible."""
        if self.effet:
            self.effet(utilisateur, cible, terrain)


# Effets des armes
def epee_effet(utilisateur, cible, terrain=None):
    """Effet de l'épée : inflige des dégâts directs."""
    print(f"{utilisateur.nom} utilise une ÉPÉE sur {cible.nom}!")
    cible.recevoir_degats(30, terrain)

def arc_effet(utilisateur, cible, terrain=None):
    """Effet de l'arc : inflige des dégâts à distance."""
    print(f"{utilisateur.nom} utilise un ARC sur {cible.nom}!")  # Portée de 3 cases
    cible.recevoir_degats(20 , terrain)

def lance_effet(utilisateur, cible, terrain=None):
    """Effet de la lance : inflige des dégâts à la cible et la repousse."""
    print(f"{utilisateur.nom} utilise une LANCE sur {cible.nom}!")
    cible.recevoir_degats(25 , terrain)
    # Repousser la cible d'une case si possible
    dx = cible.x - utilisateur.x
    dy = cible.y - utilisateur.y
    if dx != 0: dx = dx // abs(dx)
    if dy != 0: dy = dy // abs(dy)
    cible.move(dx, dy, terrain)

def bombe_effet(utilisateur, cible, terrain=None, game_instance=None):
    """Effet simplifié de la bombe : inflige des dégâts de zone."""
    print(f"{utilisateur.nom} utilise une BOMBE sur {cible.nom}!")

    # Définir la zone d'effet autour de la cible
    zone = [
        (cible.x-1, cible.y), (cible.x+1, cible.y),
        (cible.x, cible.y-1), (cible.x, cible.y+1),
        (cible.x, cible.y)  # Inclure la case de la cible elle-même
    ]

    # Vérifier si une instance de jeu est fournie
    if game_instance is None:
        print("Erreur : Instance de jeu non spécifiée.")
        return

    # Récupérer toutes les unités à partir de l'instance de jeu
    toutes_unites = game_instance.get_all_units()

    # Applique les dégâts à toutes les unités dans la zone
    for u in toutes_unites:
        if (u.x, u.y) in zone:
            print(f"{u.nom} est dans la zone d'effet de la bombe !")
            u.recevoir_degats(40, terrain)

# Exemple d'utilisation



epee = Arme("Épée", degats=30, deplacement_distance=5, effet=epee_effet)
arc = Arme("Arc", degats=20, deplacement_distance=10, effet=arc_effet)
lance = Arme("Lance", degats=25, deplacement_distance=8, effet=lance_effet)
bombe = Arme("Bombe", degats=40, deplacement_distance=3, effet=bombe_effet )
