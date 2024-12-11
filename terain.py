import pygame
import random
import numpy as np
from unit import *
from game import *
from main import *

# Charger les images (icônes)

icon_obstacle = pygame.image.load("image/obstacle.jpg")
# icon_obstacle = pygame.image.load("image/ob.webp")
icon_herbe = pygame.image.load("image/Herbe.png")
icon_desert = pygame.image.load("image/carte.png")
icon_health = pygame.image.load("image/health.png")

NUM_COLUMNS = 37
NUM_ROWS = 37

CELL_SIZE = 40

icon_obstacle = pygame.transform.scale(icon_obstacle, (CELL_SIZE, CELL_SIZE))
icon_herbe = pygame.transform.scale(icon_herbe, (CELL_SIZE, CELL_SIZE))
icon_desert = pygame.transform.scale(icon_desert, (CELL_SIZE, CELL_SIZE))
icon_health = pygame.transform.scale(icon_health, (CELL_SIZE, CELL_SIZE))
class Case:
    def __init__(self, type_case, x, y, effet=None):
        self.type_case = type_case
        self.x = x
        self.y = y
        self.effet = effet

    def afficher(self, screen):
        """Calculer la position sur la grille et afficher l'icône associée."""
        position = (self.x * CELL_SIZE, self.y * CELL_SIZE)

        if self.type_case == 1:
            screen.blit(icon_obstacle, position)
        elif self.type_case == 2 :
            screen.blit(icon_herbe, position)
        elif self.type_case == 3 :
            screen.blit(icon_health, position)
        
            # screen.blit(icon_desert, position)


class Terrain:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur  # Largeur de la grille
        self.hauteur = hauteur  # Hauteur de la grille
        self.cases = []  # Initialisation de la liste des cases
        self.obstacles = [] 
        self.herbes = [] 
        self.health = []

    def generer_grille(self):

        grille = np.zeros((self.hauteur,self.largeur))
        liste_obstacles = [
        # Structure coté gauche 
        [5,2], [6,2], [7,2], [8,2], [8,3], 
        [3,4], [3,5], [4,5], [5,5], [6,5],  
        [3,8], [3,9], [3,10], [3,11], 
        [3,14], [3,15], [4,15], [5,15], [6,15], [7,15],  
        #Z descedant
        [6,8], [7,8], [7,9], [8,9], [8,10], [9,10], [9,11],[10,11], [10,12], [11,12], [11,13], [12,13], [12,14], [13,14], [13,15],  
        #Ligne horizontale basse 
        [17,14], [18,14], [19,14], [20,14], [21,14], [22,14], [23,14], [24,14], [25,14],[16,14],  
        #Structure coté droit 
        [30, 15], [31, 15], [32, 15], [33, 15], [33, 14],  
        [31,12], [30,12], [29,12], [28,12], [28,13],  
        [33, 9], [33, 8], [33, 7], [33, 6], [33, 6],  
        [33, 3], [33, 2], [32, 2], [31, 2], [30, 2], [29, 2],
        #Milieu en haut 
        [13, 2], [14, 2], [15, 2], [16, 2], [17, 2], [18, 2], [12, 2] ,
        [22, 2], [23, 2], [24, 2], [25, 2], [26, 2], [25, 3],[25,4],[25,5], 
        #Milieu
        [12, 6], [12, 7], [12, 8], [12, 9], [12, 5],  
        [25, 11], [25, 10], [25, 9], [25, 8], [24,11],[23,11],[22,11],[21,11],
        [17, 11], [16, 11], [15, 11], [18,11], 
        #centre 
        [19,6], [18,6], [19,7], [18,7],
        ]
        
        liste_interdite = [[0,i] for i in range(NUM_ROWS)]+[[NUM_COLUMNS-1 , j] for j in range(NUM_ROWS)]
        for x in range(self.largeur):
            ligne = []
            for y in range(self.hauteur):

                if [x,y] in liste_obstacles :
                    case_type = 1  # Obstacle
                 
                elif random.random() < 0.01: #Probabilité d'avoir du herbe de 5%
                    case_type = 2
                elif random.random() < 0.01 and [x,y] not in liste_interdite :
                    case_type = 3  
                    self.health.append([x,y])
                else : 
                    case_type = 0 
                

                    # Créer une nouvelle case avec le type sélectionné
                nouvelle_case = Case(case_type, x, y)
                ligne.append(nouvelle_case)  # Ajout de la case à la ligne
            self.cases.append(ligne)
        self.obstacles= liste_obstacles
    

    def melanger(self):
        """Change l'emplacement des herbes après chaque tour."""
        nouvelle_liste = []

        # Suppression des anciennes herbes
        for i in self.herbes:
            self.cases[i[0]][i[1]] = Case(0, i[0], i[1])

        for x in range(self.largeur):
            for y in range(self.hauteur):
                # Ignorer les cases d'obstacles ou de santé
                if [x, y] in self.obstacles + self.health:
                    continue
                # Générer une nouvelle herbe avec une probabilité de 5%
                if random.random() < 0.05:
                    self.cases[x][y] = Case(2, x, y)
                    nouvelle_liste.append([x, y])

        self.herbes = nouvelle_liste
        print(f"Les herbes ont été mélangées. Nouvelle liste : {self.herbes}")



    def afficher_grille(self, screen):
        """Affiche toutes les cases de la grille sur l'écran."""
        for ligne in self.cases:
            for case in ligne:
                case.afficher(screen)


