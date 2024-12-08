import os
import pygame
import random
from game import *
from main import *
from Feu import *

# Constantes
GRID_SIZE = 8
CELL_SIZE = 40
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
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

    def recevoir_degats(self, degats):
        """Réduit les points de vie de l'unité en fonction des dégâts."""
        self.vie -= degats
        if self.vie < 0:
            self.vie = 0
        print(f"L'unité {self.equipe} reçoit {degats} dégâts. Vie restante : {self.vie}.")




class Type_Unite(Unit):
    def __init__(self, nom, x, y, vie, attaque, equipe, defense, deplacement_distance, competences, arme=None, image_id=None):
        super().__init__(x, y, vie, attaque, equipe, arme)
        self.nom = nom
        self.defense = defense
        self.deplacement_distance = deplacement_distance
        self.competences = competences
        self.image = pygame.image.load(f'image/p{image_id}.jpg')

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
        if 0 <= new_x < len(terrain.cases) and 0 <= new_y < len(terrain.cases[0]):
            target_case = terrain.cases[new_x][new_y]

            # Si la case est un obstacle, l'unité ne peut pas avancer
            if target_case.type_case == 'obstacle':
                return False

            # Si l'unité passe sur de l'eau ou du feu, elle meurt
            if target_case.type_case == 'eau' or target_case.type_case == 'feu':
                self.vie = 0
                pygame.quit()
                exit()  # L'unité meurt

            # Si tout est valide, on déplace l'unité d'une case
            self.x = new_x
            self.y = new_y
            return True
        else:
            return False  # Si la case cible est en dehors des limites
    

        

    def update_health(self, surface):
        bar_width = 40
        bar_height = 4
        bar_position = (self.x * CELL_SIZE, self.y * CELL_SIZE , bar_width, bar_height)
        health_width = bar_width * (self.vie / 100)

        if self.equipe == "player":
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



class Competence:
    def __init__(self, nom, description, effet):
        self.nom = nom
        self.description = description
        self.effet = effet

    def appliquer(self, cible):
        """Appliquer un effet à une cible."""
        self.effet(cible)


def soin_effet(cible):
    cible.vie += 20
    if cible.vie > 100:  # Supposons que 100 est le maximum
        cible.vie = 100


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
            u.vie -= damage
            if u.vie <= 0:
                u.is_alive = False  # Gère la mort de l'unité




