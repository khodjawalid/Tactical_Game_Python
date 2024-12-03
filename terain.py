import pygame
import random
import numpy as np
from unit import *
from game import *

# Charger les images (icônes)
icon_feu = pygame.image.load("Herbe.png")
icon_eau = pygame.image.load("eau.png")
icon_obstacle = pygame.image.load("obstacle.jpg")


icon_feu = pygame.transform.scale(icon_feu, (50, 50))
icon_eau = pygame.transform.scale(icon_eau, (50, 50))
icon_obstacle = pygame.transform.scale(icon_obstacle, (50, 50))

class Case:
    def __init__(self, type_case, x, y, effet=None):
        self.type_case = type_case
        self.x = x
        self.y = y
        self.effet = effet

    def afficher(self, screen):
        """Calculer la position sur la grille et afficher l'icône associée."""
        position = (self.x * 50, self.y * 50)

        if self.type_case == 1:
            screen.blit(icon_obstacle, position)
        else :
            pass

class Terrain:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur  # Largeur de la grille
        self.hauteur = hauteur  # Hauteur de la grille
        self.cases = []  # Initialisation de la liste des cases

    def generer(self):
        """Génère la grille avec des cases de types aléatoires."""
        
        for x in range(self.largeur):
            ligne = []
            for y in range(self.hauteur):
                case_type = random.choices(['traversable', 'obstacle', 'eau', 'feu'], weights=[0.7,0.1,0.1,0.1], k=1)[0]

                # Créer une nouvelle case avec le type sélectionné
                nouvelle_case = Case(case_type, x, y)
                ligne.append(nouvelle_case)  # Ajout de la case à la ligne

            self.cases.append(ligne)  # Ajout de la ligne au terrain

    def generer_grille(self):

        grille = np.zeros((self.hauteur,self.largeur))
        
        for x in range(self.largeur):
            ligne = []
            for y in range(self.hauteur):

                if (x in range(5, 10) and y in range(3, 6)) or (x in range(7, 9) and y in range(9, 12)):
                    case_type = 1  # Obstacle
                else :  # Ajouter un peu de hasard
                    case_type = 0  # Obstacle ponctuel

                    # Créer une nouvelle case avec le type sélectionné
                nouvelle_case = Case(case_type, x, y)
                ligne.append(nouvelle_case)  # Ajout de la case à la ligne
            self.cases.append(ligne)




    def afficher_grille(self, screen):
        """Affiche toutes les cases de la grille sur l'écran."""
        for ligne in self.cases:
            for case in ligne:
                case.afficher(screen)


