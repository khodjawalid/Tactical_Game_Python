import pygame

class Competence:
    """
    Classe représentant une compétence spéciale utilisée par une unité.
    Attributs :
    - nom (str) : Nom de la compétence.
    - description (str) : Description de l'effet de la compétence.
    - effet (callable) : Fonction définissant l'effet de la compétence.
    """
    def __init__(self, nom, description, effet):
        self.nom = nom
        self.description = description
        self.effet = effet

    def appliquer(self, cible):
        """Appliquer un effet à une cible."""
        self.effet(cible)


def bouclier_effet(cible):
    """
    Effet : Active un bouclier protecteur qui réduit les dégâts subis de 50 % pendant 1 tour.
    Entrées :
    - cible (Type_Unite) : L'unité qui bénéficie du bouclier.
    Sorties :
    - Modifie les attributs de la cible pour inclure une réduction de dégâts et une durée de 1 tour.
    """
    cible.reduction_degats = 1  
    cible.duree_bouclier = 1  
    print(f"{cible.nom} active un bouclier protecteur (50% de réduction des dégâts).")


def poison_effet(cible):
    """
    Effet : Applique un poison à la cible qui inflige des dégâts sur plusieurs tours.
    Entrées :
    - cible (Type_Unite) : L'unité empoisonnée.
    Sorties :
    - Modifie les attributs de la cible pour indiquer qu'elle est empoisonnée.
    - Ajoute une durée de poison (3 tours) et des dégâts infligés par tour (10).
    """
    cible.est_poisonne = True
    cible.poison_duree = 3  
    cible.poison_degat_par_tour = 10
    print(f"{cible.nom} est empoisonné ! Dégâts : 10 par tour pendant 3 tours.")



def glace_eclatante_effet(cible):
    """Immobilise la cible pendant 2 tours et inflige 20 points de dégâts."""
    """
    Effet : Immobilise la cible pendant 2 tours et inflige 20 points de dégâts.
    Entrées :
    - cible (Type_Unite) : L'unité ciblée par l'effet.
    Sorties :
    - Réduit les points de vie de la cible de 20.
    - Immobilise la cible pour 2 tours en modifiant ses attributs.
    """
    cible.vie -= 20  # Inflige des dégâts
    cible.est_glace = True  # Ajoute un statut pour l'immobilisation
    cible.glace_duree = 2  # Immobilisation pendant 2 tours
    print(f"{cible.nom} est frappé par Glace Éclatante ! Dégâts : 20. Immobilisé pour 2 tours.")


def soin_effet(cible):
    """
    Effet : Soigne la cible en augmentant ses points de vie.
    Entrées :
    - cible (Type_Unite) : L'unité à soigner.
    Sorties :
    - Augmente les points de vie de la cible de 20, jusqu'à un maximum de 100.
    """
    cible.vie += 20
    if cible.vie > 100:  # Supposons que 100 est le maximum
        cible.vie = 100

