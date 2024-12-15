import os
import pygame
import random
from game import *
#from main import *
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
    def __init__(self, nom, x, y, vie, attaque, equipe, defense, deplacement_distance, competences, arme=None, image_id=None ,range=1, game = None):
        super().__init__(x, y, vie, attaque, equipe, arme)
        self.nom = nom
        self.defense = defense
        self.attaque = attaque
        self.deplacement_distance = deplacement_distance
        self.competences = competences
        self.image = pygame.image.load(f'image/p{image_id}.jpg')
        self.range = range
        self.game = game
        # Redimensionner l'image
        scale_factor = 0.9
        new_size = (int(CELL_SIZE * scale_factor), int(CELL_SIZE * scale_factor))
        self.image = pygame.transform.scale(self.image, new_size)

    def attaquer_avec_arme(self, cible, terrain , game = None):
        
        """
        Attaque une cible avec l'arme actuelle de l'unité.
        Dessine un laser vers les unités de l'équipe opposée dans la zone accessible.
        """
        if not self.game:
            raise ValueError(f"L'unité {self.nom} n'a pas de référence à l'objet Game.")

        # Récupérer les cellules accessibles
        accessible_cells = self.game.get_accessible_cells(self)

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
        cible.vie -= degats
        print(f"{self.nom} attaque {cible.nom} avec {self.arme.nom} pour {degats} dégâts.")

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


