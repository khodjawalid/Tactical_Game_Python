import pygame
import random
import numpy as np
from unit import *
from game import *
#from main import *



# Constantes
GRID_SIZE = 8
CELL_SIZE = 40
NUM_ROWS = 18
NUM_COLUMNS = 37
WIDTH = NUM_COLUMNS* CELL_SIZE
HEIGHT = NUM_ROWS * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
Select_color = (75,0,130)  #Couleur à afficher derriere le joueur selectionné à choisir lus tard 



# Charger les images (icônes)
icon_obstacle = pygame.image.load("image/obstacle.jpg")
icon_herbe = pygame.image.load("image/Herbe.png")
icon_health = pygame.image.load("image/health.png")
icon_protection = pygame.image.load("image/protection.png")  # Ajoutez une icône pour la protection
icon_trou = pygame.image.load("image/Trou.png")  # Ajoutez une icône pour la protection


NUM_COLUMNS = 37
NUM_ROWS = 18

CELL_SIZE = 40

#Redimenssionner les images  
icon_obstacle = pygame.transform.scale(icon_obstacle, (CELL_SIZE, CELL_SIZE))
icon_herbe = pygame.transform.scale(icon_herbe, (CELL_SIZE, CELL_SIZE))
icon_health = pygame.transform.scale(icon_health, (CELL_SIZE, CELL_SIZE))
icon_protection = pygame.transform.scale(icon_protection, (CELL_SIZE, CELL_SIZE))
icon_trou = pygame.transform.scale(icon_trou, (CELL_SIZE, CELL_SIZE))

            # screen.blit(icon_desert, position)

class Case:
    """
    Classe représentant une case dans la grille.
    Attributs :
    - type_case (int) : Type de la case (0 = vide, 1 = obstacle, 2 = herbe, 3 = santé, 4 = protection, 5 = trou).
    - x (int) : Position x de la case dans la grille.
    - y (int) : Position y de la case dans la grille.
    - effet (callable, optionnel) : Effet spécial appliqué à la case.
    Méthodes :
    - afficher(screen) : Affiche la case sur l'écran.
    """
    def __init__(self, type_case, x, y, effet=None):
        self.type_case = type_case
        self.x = x
        self.y = y
        self.effet = effet

    def afficher(self, screen):
        """
        Affiche la case sur l'écran avec l'icône correspondante.
        Entrées :
        - screen (pygame.Surface) : Surface de l'écran où afficher la case.
        Sorties :
        - Affiche l'icône correspondant au type de case à sa position.
        """
        position = (self.x * CELL_SIZE, self.y * CELL_SIZE)

        if self.type_case == 1:
            screen.blit(icon_obstacle, position)
        elif self.type_case == 2 :
            screen.blit(icon_herbe, position)
        elif self.type_case == 3 :
            screen.blit(icon_health, position)
        elif self.type_case == 4:  # Protection
            screen.blit(icon_protection, position)
        elif self.type_case == 5:  # Protection
            screen.blit(icon_trou, position)
class Terrain:
    """
    Classe représentant le terrain de jeu.
    Attributs :
    - largeur (int) : Nombre de colonnes dans la grille.
    - hauteur (int) : Nombre de lignes dans la grille.
    - cases (list) : Liste contenant toutes les cases de la grille.
    - obstacles, herbes, health, trous, protection (list) : Positions des cases spécifiques.
    Méthodes :
    - generer_grille() : Génère aléatoirement la grille avec différents types de cases.
    - melanger() : Change l'emplacement des herbes aléatoirement.
    - delete_after_use(x, y) : Supprime une case spéciale après son utilisation.
    - afficher_grille(screen) : Affiche la grille entière sur l'écran.
    """
    def __init__(self, largeur, hauteur):
        self.largeur = largeur  # Largeur de la grille
        self.hauteur = hauteur  # Hauteur de la grille
        self.cases = []  # Initialisation de la liste des cases
        self.obstacles = [] 
        self.herbes = [] 
        self.health = []
        self.trous = []
        self.protection = []


    def generer_grille(self):
        """
        Génère une grille aléatoire avec des cases spéciales comme obstacles, herbes, santé, etc.
        Entrées :
        - Aucune.
        Sorties :
        - Met à jour l'attribut self.cases avec les cases générées.
        """
        grille = np.zeros((self.hauteur,self.largeur)) #grille vide 

        #Positionnnement des obstacles 
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
        

        liste_protection = [[10, 4], [10, 10], [12, 5], [27,3],[15,15], [15,5], [23,7], [30,8],[17,0]]
        liste_trous = [[5,4],[5,12], [15,7],[31,5],[30,13]]

        #Afin de ne pas avoir de l'herbe sur les joueurs au début 
        liste_interdite_herbe = [[0,i] for i in range(NUM_ROWS)]+[[NUM_COLUMNS-1 , j] for j in range(NUM_ROWS)] 
    
        for x in range(self.largeur):
            ligne = []
            for y in range(self.hauteur):

                if [x,y] in liste_obstacles :
                    case_type = 1  # Obstacle
                 
                elif random.random() < 0.03: #Probabilité d'avoir du herbe de 3%
                    case_type = 2 #herbe
                    self.herbes.append([x,y])
                elif random.random() < 0.08 and 7 <= x <= NUM_COLUMNS-10 and 7 <= y <= NUM_ROWS-7 and [x,y] not in liste_obstacles+liste_protection+liste_trous+self.herbes : #mettre balises au milieu de la carte seulement
                    case_type = 3  #health
                    self.health.append([x,y])
                elif [x, y] in liste_protection:  # Ajout des cases fixes de protection
                    case_type = 4 #protection 
                    self.protection.append([x,y])
                elif [x, y] in liste_trous:  # Ajout des cases fixes de protection
                    case_type = 5 #trou 
                    self.trous.append([x,y])
                else : 
                    case_type = 0 
                # Créer une nouvelle case avec le type sélectionné
                nouvelle_case = Case(case_type, x, y)
                ligne.append(nouvelle_case)  # Ajout de la case à la ligne
            self.cases.append(ligne)

        self.obstacles= liste_obstacles
    

    def melanger(self):
        """
        Mélange les positions des cases d'herbe en les réinitialisant.
        Entrées :
        - Aucune.
        Sorties :
        - Met à jour l'attribut self.herbes avec les nouvelles positions.
        """
        nouvelle_liste = []
        # Suppression des anciennes herbes
        for i in self.herbes:
            self.cases[i[0]][i[1]] = Case(0, i[0], i[1])

        for x in range(self.largeur):
            for y in range(self.hauteur):
                # Ignorer les cases d'obstacles ou de santé
                if [x, y] in self.obstacles + self.health + self.trous :
                    continue
                # Générer une nouvelle herbe avec une probabilité de 5%
                if random.random() < 0.03:
                    self.cases[x][y] = Case(2, x, y)
                    nouvelle_liste.append([x, y])

        self.herbes = nouvelle_liste

    def delete_after_use(self,x,y):
        """Fonction qui suprime les  balises aprés leurs utilisation"""
        """
        Supprime une case spéciale après utilisation.
        Entrées :
        - x (int) : Position x de la case.
        - y (int) : Position y de la case.
        Sorties :
        - Remplace la case par une case vide (type 0).
        """
        self.cases[x][y] = Case(0,x,y)


    def afficher_grille(self, screen):
        """
        Affiche la grille entière sur l'écran.
        Entrées :
        - screen (pygame.Surface) : Surface de l'écran où afficher la grille.
        Sorties :
        - Affiche toutes les cases sur l'écran.
        """
        for ligne in self.cases:
            for case in ligne:
                case.afficher(screen)
