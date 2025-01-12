import os
import pygame
import random
from game import *
import numpy as np

from Feu import *
from IA import *

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

        

class Type_Unite :
    """
    Classe représentant une unité spécialisée héritant de Unit.
    Attributs supplémentaires :
    - nom (str) : Nom de l'unité.
    - defense (int) : Points de défense de l'unité.
    - deplacement_distance (int) : Distance maximale de déplacement.
    - competences (list) : Liste des compétences de l'unité.
    - image (pygame.Surface) : Image associée à l'unité.
    - range (int) : Portée de l'unité.
    """
    def __init__(self, nom, x, y, vie, attaque, equipe, defense, deplacement_distance, competences, arme=None, image_id=None ,range=1, game = None, reduction_degats = 0):
        self.x=x
        self.y=y
        self.vie = vie
        self.equipe = equipe  # 'player' ou 'enemy'
        self.is_selected = False
        self.arme = arme
        self.game = game  # Arme associée à l'unité (par défaut aucune)

        self.nom = nom
        self.defense = defense
        self.attaque = attaque
        self.deplacement_distance = deplacement_distance
        self.competences = competences
        self.image = pygame.image.load(f'image/p{image_id}.jpg')
        self.range = range
        self.reduction_degats = reduction_degats

        # Redimensionner l'image
        scale_factor = 0.9
        new_size = (int(CELL_SIZE * scale_factor), int(CELL_SIZE * scale_factor))
        self.image = pygame.transform.scale(self.image, new_size)


    def attack(self, target, terrain=None):
        """
        Redéfinition de l'attaque.
        Entrées :
        - target (Unit) : Cible de l'attaque.
        - terrain (Terrain, optionnel) : Terrain où l'attaque se déroule.
        """
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.vie -= self.attaque

    def recevoir_degats(self, degats, terrain):
        """
        Redéfinition pour recevoir des dégâts.
        Entrées :
        - degats (int) : Quantité de dégâts reçus.
        - terrain (Terrain) : Terrain actuel de l'unité.
        """
        self.health -= degats
        if self.health < 0:
            self.health = 0


    def attaquer_avec_arme(self, cible, terrain , game = None):
        
        """
        Attaque une cible avec l'arme actuelle.
        Entrées :
        - cible (Unit) : Cible de l'attaque.
        - terrain (Terrain) : Terrain de l'attaque.
        - game (Game, optionnel) : Référence au jeu.
        """

        if not self.game:
            raise ValueError(f"L'unité {self.nom} n'a pas de référence à l'objet Game.")

        # Récupérer les cellules accessibles
        accessible_cells = self.game.get_attaque_accessible_cells(self)

        # Filtrer les unités accessibles selon l'équipe
        if self.equipe == "player":
            targets = [unit for unit in self.game.enemy_units if (unit.x, unit.y) in accessible_cells]
            color = (0, 255, 0)  # Vert pour le joueur
        else:  # Ennemi qui attaque
            targets = [unit for unit in self.game.player_units if (unit.x, unit.y) in accessible_cells]
            color = (255, 0, 0)  # Rouge pour l'ennemi

        # Dessiner le laser vers les cibles
        self.game.draw_laser(self, targets, color)

        # Appliquer les dégâts uniquement à la cible attaquée
        degats = self.arme.degats

        if self.arme.nom == "Bombe" :
            # Définir la zone d'effet autour de la cible
            zone = [[(cible.x + i - 1, cible.y + j - 1) for j in range(3)] for i in range(3)]
            # Récupérer toutes les unités à partir de l'instance de jeu
            toutes_unites = game.get_all_units()
            liste_unites = []
            # Applique les dégâts à toutes les unités dans la zone
            for u in toutes_unites:
                if (u.x, u.y) in zone[0]+zone[1]+zone[2]:
                    print("efffet bombe",u.x,u.y)
                    liste_unites.append([u.x,u.y])
                    print(f"{u.nom} est dans la zone d'effet de la bombe !")
                    cible.vie -= degats*(1-cible.reduction_degats)


        else : 
            cible.vie -= degats*(1-cible.reduction_degats)
            print(f"{self.nom} attaque {cible.nom} avec {self.arme.nom} pour {degats*(1-cible.reduction_degats)} dégâts.")

        # Vérifier si la cible est éliminée
        if cible.vie <= 0:
            print(f"{cible.nom} est éliminé !")
            if cible in self.game.player_units:
                self.game.player_units.remove(cible)
            elif cible in self.game.enemy_units:
                self.game.enemy_units.remove(cible)


    
    def move(self, dx, dy, terrain,players):
        """
        Déplace l'unité d'une case en fonction de sa capacité de déplacement.
        Entrées :
        - dx (int) : Décalage horizontal du déplacement.
        - dy (int) : Décalage vertical du déplacement.
        - terrain (Terrain) : Terrain sur lequel se déplace l'unité.
        - players (list[Type_Unite]) : Liste des unités de l'équipe actuelle (joueurs).
        Sorties :
        - (bool) : True si le déplacement a réussi, False sinon.
        """

        # Calculer la nouvelle position
        new_x = self.x + dx
        new_y = self.y + dy

        player_x = [p.x for p in players]
        player_y = [p.y for p in players] 

        player_coordinates = [[x,y] for x,y in zip(player_x,player_y)]

        # Vérifier si la position est valide
        if 0 <= new_x < NUM_COLUMNS and 0 <= new_y < NUM_ROWS -1:
            target_case = terrain.cases[new_x][new_y]

            # Si la case est un obstacle, l'unité ne peut pas avancer
            if target_case.type_case == 1 or [new_x,new_y] in player_coordinates :
                print(f"L'unité {self.nom} ne peut pas avancer : obstacle détecté ou la case contient un joueur.")
                return False
            
            elif target_case.type_case == 2:  # Herbe
                self.x = new_x #Faire le deplacement avant l'animation
                self.y = new_y
                print(f"L'unité {self.nom} traverse une case d'herbe et perd 10 points de vie.")
                self.vie -= 10
                self.game.animate_effect(new_x, new_y, "leaf")  # Animation pour herbe
                terrain.delete_after_use(new_x,new_y)
                return True
            
            elif target_case.type_case == 3:  # Cœur
                self.x = new_x
                self.y = new_y
                print(f"L'unité {self.nom} récupère de la vie en passant sur une case de santé.")
                self.vie = min(100, self.vie + 20)
                self.game.animate_effect(new_x, new_y, "heart")  # Animation pour cœur
                self.game.sound_manager.play_sound("heart")
                terrain.delete_after_use(new_x,new_y)
                return True
            
            elif target_case.type_case == 4:  # Protection
                self.x = new_x
                self.y = new_y
                print(f"L'unité {self.nom} est protégée par une case de protection.")
                self.game.animate_effect(new_x, new_y, "star")  # Animation pour protection
                return True
            
            elif target_case.type_case == 5:  # Trous
                cases_valides = [(i, j) for i in range(len(terrain.cases)) for j in range(len(terrain.cases[0])-2) if [i,j] not in terrain.obstacles+terrain.protection+player_coordinates+terrain.health+terrain.trous ] 
                case_tiree = random.choice(cases_valides)  #tirage
                self.vie -= 10
                self.x = case_tiree[0]
                self.y = case_tiree[1]
                print(f"L'unité {self.nom} est déplacé vers une case aléatoire.")
                return True

            self.x = new_x
            self.y = new_y
            return True

        print(f"L'unité {self.nom} ne peut pas se déplacer en dehors des limites.")
        return False


        

    def update_health(self, surface, terrain):
        """
        Met à jour l'affichage de la barre de vie de l'unité.
        Entrées :
        - surface (pygame.Surface) : Surface de jeu où afficher la barre de vie.
        - terrain (Terrain) : Terrain où l'unité se trouve.
        Sorties :
        - Affiche la barre de vie sur la surface spécifiée.
        """
        bar_width = 40
        bar_height = 4
        bar_position = (self.x * CELL_SIZE, self.y * CELL_SIZE, bar_width, bar_height)
        health_width = bar_width * (self.vie / 100)

        # Couleur de la barre de vie
        if terrain.cases[self.x][self.y].type_case == 4:  # Sur une case de protection
            bar_color = (0, 255, 255)  # Cyan pour indiquer la protection
        elif self.equipe == "player":
            bar_color = (0, 255, 0)  # Vert pour le joueur
        else:
            bar_color = (255, 0, 0)  # Rouge pour l'ennemi

        pygame.draw.rect(surface, (128, 128, 128), bar_position)  # Fond gris
        pygame.draw.rect(surface, bar_color, (bar_position[0], bar_position[1], health_width, bar_height))



    def utiliser_competence(self, index, cible):
        """
        Utilise une compétence sur une cible.
        Entrées :
        - index (int) : Indice de la compétence dans la liste des compétences.
        - cible (Type_Unite) : Cible de la compétence.
        Sorties :
        - Applique l'effet de la compétence si l'indice est valide.
        """
        if 0 <= index < len(self.competences):
            self.competences[index].appliquer(cible)

    def draw(self, screen):
        """
        Affiche l'unité sur l'écran avec ses caractéristiques visuelles.
        Entrées :
        - screen (pygame.Surface) : Surface où afficher l'unité.
        Sorties :
        - Affiche l'unité avec une couleur de sélection si elle est sélectionnée.
        """
        if self.is_selected:
            pygame.draw.rect(screen, Select_color, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        #Affichage du personnage au milieu de la cellule
        scale_factor = 0.9
        offset = int(CELL_SIZE * (1 - scale_factor) / 2)
        # Ajustement pour centrer l'image
        position = (self.x * CELL_SIZE + offset, self.y * CELL_SIZE + offset)
        screen.blit(self.image, position)
        

    def __str__(self):
        """
        Retourne une description textuelle de l'unité.
        Sorties :
        - (str) : Description de l'unité avec ses attributs principaux.
        """
        competences_str = [competence.nom for competence in self.competences]
        return (f"Unité({self.nom}, {self.x}, {self.y}, Vie: {self.vie}, Attaque: {self.attaque}, "
                f"Défense: {self.defense}, Vitesse: {self.deplacement_distance}, "
                f"Compétences: {competences_str})")


