import pygame

class Competence:
    def __init__(self, nom, description, effet):
        self.nom = nom
        self.description = description
        self.effet = effet

    def appliquer(self, cible):
        """Appliquer un effet à une cible."""
        self.effet(cible)


def soin_effet(cible):
    cible.health += 20
    if cible.health > 100:  # Supposons que 100 est le maximum
        cible.health = 100


def attaque_puissante_effet(cible):
    degats = 50
    cible.recevoir_degats(degats)

def feu_effet(caster, target, terrain):
    """Inflige des dégâts de zone autour de la cible."""
    damage = 30  # Dégâts de base
    x, y = target.x, target.y  # Position de la cible
    zone = [
        (x-1, y), (x+1, y), (x, y-1), (x, y+1),  # Cases adjacentes
        (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)  # Diagonales
    ]

    for u in caster.game.player_units + caster.game.enemy_units:
        if (u.x, u.y) in zone:  # Vérifie si une unité est dans la zone
            u.health -= damage
            if u.health <= 0:
                u.is_alive = False  # Gère la mort de l'unité


