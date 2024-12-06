import pygame 

class Arme:
    """Classe pour représenter une arme."""
    def __init__(self, nom, degats, vitesse, effet):
        self.nom = nom
        self.degats = degats
        self.vitesse = vitesse
        self.effet = effet  # Une fonction représentant l'effet de l'arme

    def utiliser(self, utilisateur, cible, terrain=None):
        """Utilise l'arme sur une cible."""
        if self.effet:
            self.effet(utilisateur, cible, terrain)


# Effets des armes
def epee_effet(utilisateur, cible, terrain=None):
    """Effet de l'épée : inflige des dégâts directs."""
    print(f"{utilisateur.nom} utilise une ÉPÉE sur {cible.nom}!")
    cible.recevoir_degats(30)

def arc_effet(utilisateur, cible, terrain=None):
    """Effet de l'arc : inflige des dégâts à distance."""
    print(f"{utilisateur.nom} utilise un ARC sur {cible.nom}!")
    if abs(utilisateur.x - cible.x) <= 3 and abs(utilisateur.y - cible.y) <= 3:  # Portée de 3 cases
        cible.recevoir_degats(20)

def lance_effet(utilisateur, cible, terrain=None):
    """Effet de la lance : inflige des dégâts à la cible et la repousse."""
    print(f"{utilisateur.nom} utilise une LANCE sur {cible.nom}!")
    cible.recevoir_degats(25)
    # Repousser la cible d'une case si possible
    dx = cible.x - utilisateur.x
    dy = cible.y - utilisateur.y
    if dx != 0: dx = dx // abs(dx)
    if dy != 0: dy = dy // abs(dy)
    cible.move(dx, dy, terrain)

def bombe_effet(utilisateur, cible, terrain=None):
    """Effet de la bombe : inflige des dégâts de zone."""
    print(f"{utilisateur.nom} utilise une BOMBE sur {cible.nom}!")
    zone = [
        (cible.x-1, cible.y), (cible.x+1, cible.y),
        (cible.x, cible.y-1), (cible.x, cible.y+1),
        (cible.x, cible.y)  # Inclure la case de la cible
    ]
    for u in utilisateur.game.player_units + utilisateur.game.enemy_units:
        if (u.x, u.y) in zone:
            u.recevoir_degats(40)


epee = Arme("Épée", degats=30, vitesse=5, effet=epee_effet)
arc = Arme("Arc", degats=20, vitesse=10, effet=arc_effet)
lance = Arme("Lance", degats=25, vitesse=8, effet=lance_effet)
bombe = Arme("Bombe", degats=40, vitesse=3, effet=bombe_effet)
