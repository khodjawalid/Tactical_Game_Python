import pygame
import random

# Constantes
GRID_SIZE = 8
CELL_SIZE = 50
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, attack_power, team):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False

    def move(self, dx, dy, terrain):
        """Déplace l'unité de dx, dy en fonction des indices de la grille (1 case par direction)."""
        new_x = self.x + dx
        new_y = self.y + dy
    
    # Vérifier si les indices sont valides et dans les limites de la grille
        if 0 <= new_x < len(terrain.cases) and 0 <= new_y < len(terrain.cases[0]):
            target_case = terrain.cases[new_x][new_y]  # Récupère la case cible
        
        # Si l'unité rencontre un obstacle, elle ne peut pas avancer
            if target_case.type_case == 'obstacle':
                return False
        
        # Si l'unité passe sur de l'eau ou du feu, elle meurt
            if target_case.type_case == 'eau' or target_case.type_case == 'feu':
                self.health = 0 
                pygame.quit()
                exit() # L'unité meurt
                
        
        # Si aucune condition n'est remplie, l'unité peut se déplacer
            self.x = new_x
            self.y = new_y
            return True
    
    # Si les indices sont hors limites, l'unité ne peut pas se déplacer
        return False



       

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
    # Définir la couleur en fonction de l'équipe
        color = BLUE if self.team == 'player' else RED

    # Dessiner un carré vert si l'unité est sélectionnée
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Dessiner un cercle représentant l'unité
    # On place le cercle au centre de la case, avec un rayon proportionnel à la taille de la cellule
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)



    # def draw(self, screen):
    #     """Affiche l'unité sur l'écran."""
    #     color = BLUE if self.team == 'player' else RED
    #     if self.is_selected:
    #         pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
    #                          self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    #     pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
    #                        2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
