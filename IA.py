from game import *

import pygame

from game import *

from Feu import *
from Sounds import *


class EnemyAI:
    def __init__(self, game):
        self.game = game
        self.current_enemy_index = 0  # Index pour suivre quelle unité ennemie agit
        self.sound_manager = SoundManager()

    def play_turn(self):
        """
        L'ennemi effectue une seule action par tour : attaquer ou se déplacer.
        """
        if not self.game.enemy_units:  # Si aucune unité ennemie n'est disponible
            return False  # Aucun tour joué

        # Récupérer l'unité ennemie qui doit jouer ce tour
        enemy = self.game.enemy_units[self.current_enemy_index]
        has_acted = False

        # Affichage des cases accessibles
        accessible_cells = self.game.get_accessible_cells(enemy)
        self.game.draw_accessible_cells(accessible_cells)
        pygame.display.flip()  # Met à jour l'écran pour afficher les cases accessibles

        # Vérifier si une attaque est possible
        for player in self.game.player_units:
            if abs(enemy.x - player.x) <= enemy.deplacement_distance and abs(enemy.y - player.y) <= enemy.deplacement_distance:
                # Lancer l'attaque
                self.sound_manager.play_sound("attack")
                self.attack_with_laser(enemy, player)
                has_acted = True
                break

        # Si aucune attaque n'a été effectuée, essayer de se déplacer
        if not has_acted:
            target = self.find_closest_unit(enemy, self.game.player_units)
            if target:
                self.move_towards(enemy, target, accessible_cells)
                has_acted = True

        # Passer à l'unité ennemie suivante
        self.current_enemy_index = (self.current_enemy_index + 1) % len(self.game.enemy_units)
        return has_acted

    def attack_with_laser(self, enemy, target):
        """
        Dessine un laser et effectue une attaque contre la cible.
        """
        # Afficher le laser
        self.game.draw_laser(enemy, [target], (255, 0, 0))  # Rouge pour l'ennemi
        self.game.animate_attack_effect(target.x, target.y)

        # Appliquer les dégâts
        damage = enemy.arme.degats
        target.vie -= damage
        print(f"{enemy.nom} attaque {target.nom} pour {damage} dégâts !")

        # Vérifier si la cible est éliminée
        if target.vie <= 0:
            self.game.player_units.remove(target)
            print(f"{target.nom} est éliminé !")

    def find_closest_unit(self, enemy, player_units):
        """
        Trouve l'unité alliée la plus proche d'une unité ennemie.
        """
        closest_unit = None
        min_distance = float('inf')

        for player_unit in player_units:
            distance = abs(enemy.x - player_unit.x) + abs(enemy.y - player_unit.y)
            if distance < min_distance:
                min_distance = distance
                closest_unit = player_unit

        return closest_unit

    def move_towards(self, enemy, target, accessible_cells):
        """
        Déplace l'unité ennemie vers une unité cible tout en évitant les herbes.
        """
        best_cell = None
        min_distance = float('inf')

        for cell in accessible_cells:
            x, y = cell
            if any(u.x == x and u.y == y for u in self.game.player_units):
                continue  # Éviter les cases occupées par des joueurs
            if self.game.terrain.cases[x][y].type_case == 2:  # Éviter les herbes
                continue
            distance = abs(x - target.x) + abs(y - target.y)
            if distance < min_distance:
                min_distance = distance
                best_cell = cell

        if best_cell:
            enemy.x, enemy.y = best_cell
            print(f"{enemy.nom} se déplace vers ({best_cell[0]}, {best_cell[1]}).")
