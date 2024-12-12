import os
import pygame
import random
from game import *
from main import *
from Feu import *
from IA import *

# Constantes
GRID_SIZE = 8
CELL_SIZE = 40
# WIDTH = GRID_SIZE * CELL_SIZE
# HEIGHT = GRID_SIZE * CELL_SIZE
WIDTH = NUM_COLUMNS* CELL_SIZE
HEIGHT = NUM_ROWS * CELL_SIZE

FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
Select_color = (75,0,130)  #Couleur à afficher derriere le joueur selectionné à choisir lus tard 


class Unit:
    def __init__(self, x, y, vie, attack_power, equipe, arme=None, game = None ):
        self.x = x
        self.y = y
        self.vie = vie
        self.attack_power = attack_power
        self.equipe = equipe  # 'player' ou 'enemy'
        self.is_selected = False
        self.arme = arme 
        self .game = game  # Arme associée à l'unité (par défaut aucune)

    def attack(self, target, terrain=None):
        """Attaque une unité cible avec ou sans arme."""
        if self.arme:
            print(f"{self.equipe} utilise {self.arme.nom} contre {target.equipe}!")
            self.arme.utiliser(self, target, terrain)  # Utilisation de l'arme
        else:
            # Attaque par défaut (sans arme)
            if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
                target.recevoir_degats(self.attack_power)

    def recevoir_degats(self, degats, terrain):
        """Réduit les points de vie de l'unité en fonction des dégâts, sauf si elle est sur une case de protection."""
        current_case = terrain.cases[self.x][self.y]
        if current_case.type_case == 4:  # Case de protection
            print(f"{self.nom} est sur une case de protection. Aucun dégât reçu.")
            return  # Aucun changement de vie

        # Réduction normale des points de vie
        self.vie -= degats
        if self.vie < 0:
            self.vie = 0
        print(f"L'unité {self.nom} reçoit {degats} dégâts. Vie restante : {self.vie}.")




class Type_Unite(Unit):
    def __init__(self, nom, x, y, vie, attaque, equipe, defense, deplacement_distance, competences, arme=None, image_id=None ,range=1):
        super().__init__(x, y, vie, attaque, equipe, arme)
        self.nom = nom
        self.defense = defense
        self.attaque = attaque
        self.deplacement_distance = deplacement_distance
        self.competences = competences
        self.image = pygame.image.load(f'image/p{image_id}.jpg')
        self.range = range
        # Redimensionner l'image
        scale_factor = 0.9
        new_size = (int(CELL_SIZE * scale_factor), int(CELL_SIZE * scale_factor))
        self.image = pygame.transform.scale(self.image, new_size)

    def attaquer_avec_arme(self, cible, terrain=None):
        """Attaque une cible en utilisant l'arme équipée."""
        super().attack(cible, terrain)  # Appel de la méthode `attack` de `Unit`


    
    def move(self, dx, dy, terrain):
        """Déplace l'unité d'une case en fonction de sa capacité de déplacement."""
        # Calculer la nouvelle position
        new_x = self.x + dx
        new_y = self.y + dy

        # Vérifier si la position est valide
        if 0 <= new_x < NUM_COLUMNS and 0 <= new_y < NUM_ROWS - 1:
            target_case = terrain.cases[new_x][new_y]

            # Si la case est un obstacle, l'unité ne peut pas avancer
            if target_case.type_case == 1:
                print(f"L'unité {self.nom} ne peut pas avancer : obstacle détecté.")
                return False
            elif target_case.type_case == 2:  # Herbe
                print(f"L'unité {self.nom} traverse une case d'herbe et perd 10 points de vie.")
                self.vie -= 10
            elif target_case.type_case == 3:  # Santé
                print(f"L'unité {self.nom} récupère de la vie en passant sur une case de santé.")
                self.vie = min(100, self.vie + 20)  # Augmente la vie (par exemple, +20)
                # Supprimer le cœur
                target_case.type_case = 0
                terrain.health.remove([new_x, new_y])  # Mise à jour de la liste des cœurs

            # Déplacer l'unité
            self.x = new_x
            self.y = new_y
            return True

        print(f"L'unité {self.nom} ne peut pas se déplacer en dehors des limites.")
        return False

        

    def update_health(self, surface, terrain):
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
        """Utiliser une compétence sur une cible."""
        if 0 <= index < len(self.competences):
            self.competences[index].appliquer(cible)

    def draw(self, screen):
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
        competences_str = [competence.nom for competence in self.competences]
        return (f"Unité({self.nom}, {self.x}, {self.y}, Vie: {self.vie}, Attaque: {self.attaque}, "
                f"Défense: {self.defense}, Vitesse: {self.deplacement_distance}, "
                f"Compétences: {competences_str})")


