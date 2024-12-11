import pygame

class Competence:
    def __init__(self, nom, description, effet):
        self.nom = nom
        self.description = description
        self.effet = effet

    def appliquer(self, cible):
        """Appliquer un effet à une cible."""
        self.effet(cible)

def bouclier_effet(cible):
    cible.reduction_degats = 0.5  # Réduction de 50 % des dégâts
    cible.duree_bouclier = 1  # Bouclier actif pour 1 tour
    print(f"{cible.nom} active un bouclier protecteur (50% de réduction des dégâts).")


# Effet : Poison
def poison_effet(cible):
    cible.est_poisonne = True
    cible.poison_duree = 3  # Effet du poison pendant 3 tours
    cible.poison_degat_par_tour = 10
    print(f"{cible.nom} est empoisonné ! Dégâts : 10 par tour pendant 3 tours.")

def glace_eclatante_effet(cible):
    """Immobilise la cible pendant 2 tours et inflige 20 points de dégâts."""
    cible.vie -= 20  # Inflige des dégâts
    cible.est_glace = True  # Ajoute un statut pour l'immobilisation
    cible.glace_duree = 2  # Immobilisation pendant 2 tours
    print(f"{cible.nom} est frappé par Glace Éclatante ! Dégâts : 20. Immobilisé pour 2 tours.")


def soin_effet(cible):
    cible.vie += 20
    if cible.vie > 100:  # Supposons que 100 est le maximum
        cible.vie = 100

