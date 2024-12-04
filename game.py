import pygame
from terain import *
from unit import *

# Constantes globales
WIDTH = 15 * 50  # Largeur de la fenêtre (15 cases de 50 pixels)
HEIGHT = 15 * 50  # Hauteur de la fenêtre (15 cases de 50 pixels)
CELL_SIZE = 50  # Taille de chaque case (50x50 pixels)
CREAM = (245, 245, 220)  # Couleur crème pour l'arrière-plan
NUM_COLUMNS = 15 #nombre de colonnes 
NUM_ROWS = 15 #nombre de ligne


class Game:
    def __init__(self, screen):
        self.screen = screen

        # Création des compétences
        competence_soin = Competence("Soin", "Restaure 20 points de vie", soin_effet)
        competence_attaque_puissante = Competence("Attaque Puissante", "Inflige 50 dégâts", attaque_puissante_effet)

        # Initialisation des unités des joueurs
        self.player_units = [
            Type_Unite("Alex", 0, 0, 100, 30, "player", 10, 3, [competence_soin], 0),
            Type_Unite("Clara", 0, 1, 100, 25, "player", 15, 4, [competence_attaque_puissante], 1),
            Type_Unite("Maxime", 0, 2, 100, 35, "player", 10, 3, [competence_attaque_puissante], 2),
            Type_Unite("Sophie", 0, 3, 100, 20, "player", 20, 2, [competence_soin], 3),
        ]

        # Initialisation des unités ennemies
        self.enemy_units = [
            Type_Unite("Alex", 14, 14, 100, 30, "enemy", 10, 3, [competence_soin], 0),
            Type_Unite("Clara", 14, 12, 100, 25, "enemy", 15, 4, [competence_attaque_puissante], 1),
            Type_Unite("Maxime", 14, 13, 100, 35, "enemy", 10, 3, [competence_attaque_puissante],2),
            Type_Unite("Sophie", 14, 11, 100, 20, "enemy", 20, 2, [competence_soin], 3),
        ]

        # Initialisation du terrain
        self.terain = Terrain(NUM_COLUMNS, NUM_ROWS)
        self.terain.generer_grille()

    def handle_player_turn(self):
        """Gère le tour du joueur."""
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        if selected_unit.move(dx, dy, self.terain):
                            self.flip_display()

                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """IA pour les ennemis."""
        for enemy in self.enemy_units:
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0

            enemy.move(dx, dy, self.terain)
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self):
        """Affiche l'état actuel du jeu."""
        
        #Affichage de la photo en arriere plan 
        window_width = CELL_SIZE * NUM_COLUMNS
        window_height = CELL_SIZE * NUM_ROWS
        background = pygame.image.load("Desert2.jpg.")
        background = pygame.transform.scale(background, (window_width, window_height))
        self.screen.blit(background, (0, 0))

        #Affichage de la grille 
        self.terain.afficher_grille(self.screen)

        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")
 
    game = Game(screen)

    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()

if __name__ == "__main__":
    main()
