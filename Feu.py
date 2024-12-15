
import pygame
from game import *
from unit import * 
from terain import *


class Arme:
    """
    Classe pour représenter une arme.
    Attributs :
    - nom (str) : Nom de l'arme.
    - degats (int) : Quantité de dégâts infligés par l'arme.
    - deplacement_distance (int) : Distance maximale de déplacement associée à l'arme.
    - effet (callable) : Fonction représentant l'effet spécifique de l'arme.
    """
    def __init__(self, nom, degats, deplacement_distance, effet):
        self.nom = nom
        self.degats = degats
        self.deplacement_distance = deplacement_distance
        self.effet = effet 

    def utiliser(self, utilisateur, cible, terrain=None):
        """
        Utilise l'arme sur une cible.
        Entrées :
        - utilisateur (Unit) : L'unité qui utilise l'arme.
        - cible (Unit) : La cible de l'arme.
        - terrain (Terrain, optionnel) : Terrain où l'effet est appliqué.
        Sorties :
        - Applique l'effet de l'arme sur la cible si un effet est défini.
        """
        if self.effet:
            self.effet(utilisateur, cible, terrain)


# Effets des armes
def epee_effet(utilisateur, cible, terrain=None):
    """
    Effet de l'épée : inflige des dégâts directs.
    Entrées :
    - utilisateur (Unit) : L'unité utilisant l'épée.
    - cible (Unit) : La cible de l'épée.
    - terrain (Terrain, optionnel) : Terrain où l'effet est appliqué.
    Sorties :
    - Réduit les points de vie de la cible de 30.
    """
    print(f"{utilisateur.nom} utilise une ÉPÉE sur {cible.nom}!")
    cible.recevoir_degats(30, terrain)


def arc_effet(utilisateur, cible, terrain=None):
    """
    Effet de l'arc : inflige des dégâts à distance.
    Entrées :
    - utilisateur (Unit) : L'unité utilisant l'arc.
    - cible (Unit) : La cible de l'arc.
    - terrain (Terrain, optionnel) : Terrain où l'effet est appliqué.
    Sorties :
    - Réduit les points de vie de la cible de 20.
    """
    print(f"{utilisateur.nom} utilise un ARC sur {cible.nom}!")  # Portée de 3 cases
    cible.recevoir_degats(20 , terrain)


def lance_effet(utilisateur, cible, terrain=None):
    """
    Effet de la lance : inflige des dégâts et repousse la cible.
    Entrées :
    - utilisateur (Unit) : L'unité utilisant la lance.
    - cible (Unit) : La cible de la lance.
    - terrain (Terrain, optionnel) : Terrain où l'effet est appliqué.
    Sorties :
    - Réduit les points de vie de la cible de 25.
    - Déplace la cible d'une case dans la direction opposée à l'attaquant si possible.
    """
    print(f"{utilisateur.nom} utilise une LANCE sur {cible.nom}!")
    cible.recevoir_degats(25 , terrain)
    # Repousser la cible d'une case si possible
    dx = cible.x - utilisateur.x
    dy = cible.y - utilisateur.y
    if dx != 0: dx = dx // abs(dx)
    if dy != 0: dy = dy // abs(dy)
    cible.move(dx, dy, terrain)

def bombe_effet(utilisateur, cible, terrain=None, game_instance=None):
    """
    Effet de la bombe : inflige des dégâts de zone.
    Entrées :
    - utilisateur (Unit) : L'unité utilisant la bombe.
    - cible (Unit) : La cible principale de la bombe.
    - terrain (Terrain, optionnel) : Terrain où l'effet est appliqué.
    - game_instance (Game, optionnel) : Instance du jeu pour récupérer toutes les unités.
    Sorties :
    - Réduit les points de vie des unités dans une zone définie autour de la cible de 40.
    """
    print(f"{utilisateur.nom} utilise une BOMBE sur {cible.nom}!")

    # Définir la zone d'effet autour de la cible
    zone = [[(cible.x + i - 1, cible.y + j - 1) for j in range(3)] for i in range(3)]

    # Vérifier si une instance de jeu est fournie
    if game_instance is None:
        print("Erreur : Instance de jeu non spécifiée.")
        return

    # Récupérer toutes les unités à partir de l'instance de jeu
    toutes_unites = game_instance.get_all_units()
    liste_unites = []

    # Applique les dégâts à toutes les unités dans la zone
    for u in toutes_unites:
        if (u.x, u.y) in zone:
            liste_unites.append([u.x,u.y])
            print(f"{u.nom} est dans la zone d'effet de la bombe !")
            u.recevoir_degats(40, terrain)
    return liste_unites



# Exemple d'armes disponibles

epee = Arme("Épée", degats=30, deplacement_distance=5, effet=epee_effet)
arc = Arme("Arc", degats=20, deplacement_distance=10, effet=arc_effet)
lance = Arme("Lance", degats=25, deplacement_distance=8, effet=lance_effet)
bombe = Arme("Bombe", degats=40, deplacement_distance=3, effet=bombe_effet )
