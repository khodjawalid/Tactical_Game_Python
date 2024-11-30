import pygame
import random
from unit import *
from game import *

# Charger les images (icônes)
icon_feu = pygame.image.load("feu.png")
icon_eau = pygame.image.load("eau.png")
icon_obstacle = pygame.image.load("obstacle.png")

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

        if self.type_case == 'obstacle':
            screen.blit(icon_obstacle, position)
        elif self.type_case == 'eau':
            screen.blit(icon_eau, position)
        elif self.type_case == 'feu':
            screen.blit(icon_feu, position)

class Terrain:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur  # Largeur de la grille
        self.hauteur = hauteur  # Hauteur de la grille
        self.cases = []  # Initialisation de la liste des cases

    def generer_grille(self):
        """Génère la grille avec des cases de types aléatoires."""
        for x in range(self.largeur):
            ligne = []
            for y in range(self.hauteur):
                case_type = random.choice(['traversable', 'obstacle', 'eau', 'feu'])
                
               
                if random.random() < 0.05:  # 
                    case_type = 'obstacle'
                elif random.random() < 0.05:  
                    case_type = 'eau'
                elif random.random() < 0.05:  
                    case_type = 'feu'
                else:
                    case_type = 'traversable'  

                # Créer une nouvelle case avec le type sélectionné
                nouvelle_case = Case(case_type, x, y)
                ligne.append(nouvelle_case)  # Ajout de la case à la ligne

            self.cases.append(ligne)  # Ajout de la ligne au terrain

    def afficher_grille(self, screen):
        """Affiche toutes les cases de la grille sur l'écran."""
        for ligne in self.cases:
            for case in ligne:
                case.afficher(screen)

