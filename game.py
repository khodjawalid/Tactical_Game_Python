import pygame
from terain import * 
from unit import *
from main import *
from Feu import *

# Constantes globales
WIDTH = 15 * 40  # Largeur de la fenêtre (15 cases de 50 pixels)
HEIGHT = 15 * 40  # Hauteur de la fenêtre (15 cases de 50 pixels)
TABLEAU_HEIGHT = 100  # Hauteur du tableau d'affichage en bas
CELL_SIZE = 40  # Taille de chaque case (50x50 pixels)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NUM_COLUMNS = 15 
NUM_ROWS = 15

# Taille des images des unités
UNIT_IMAGE_SIZE = (40, 40)  # Taille redimensionnée des images (40x40 pixels)

class Game:
    def __init__(self, screen):
        self.start_time = pygame.time.get_ticks()
        self.screen = screen
        self.tour = 1
        self.player_score = 0
        self.enemy_score = 0
        

        # Création des compétences
        competence_soin = Competence ("Soin", "Restaure 20 points de vie", soin_effet)
        competence_attaque_puissante = Competence("Attaque Puissante", "Inflige 50 dégâts", attaque_puissante_effet)

        epee = Arme("Épée", degats=30, deplacement_distance=5, effet=epee_effet)
        arc = Arme("Arc", degats=20, deplacement_distance=10, effet=arc_effet)
        lance = Arme("Lance", degats=25, deplacement_distance=8, effet=lance_effet)
        bombe = Arme("Bombe", degats=40, deplacement_distance=3, effet=bombe_effet)

        # Initialisation des unités des joueurs
        self.player_units = [
            Type_Unite("Alex", 0, 0, 100, 30, "player", 10, 1, [competence_soin],epee ,"0"),
            Type_Unite("Clara", 0, 1, 100, 25, "player", 15, 2, [competence_attaque_puissante],arc,"1"),
            Type_Unite("Maxime", 0, 2, 100, 35, "player", 10, 3, [competence_attaque_puissante],lance ,"2"),
            Type_Unite("Sophie", 0, 3, 100, 20, "player", 20, 4, [competence_soin], bombe ,"3"),
        ]

        self.enemy_units = [
            Type_Unite("Alex", 14, 14, 100, 30, "enemy", 10, 1, [competence_soin], epee ,"0"),
            Type_Unite("Clara", 14, 13, 100, 25, "enemy", 15, 2, [competence_attaque_puissante], arc , "1"),
            Type_Unite("Maxime", 14, 12, 100, 35, "enemy", 10, 3, [competence_attaque_puissante],lance , "2"),
            Type_Unite("Sophie", 14, 11, 100, 20, "enemy", 20, 4, [competence_soin], bombe, "3"),
        ]

        for unit in self.player_units + self.enemy_units:
            if unit.image:
                unit.image = pygame.transform.scale(unit.image, UNIT_IMAGE_SIZE)

        # Initialisation du terrain
        self.terrain = Terrain(15, 15)  # Correction de 'terain' en 'terrain'
        self.terrain.generer_grille()
    


    def handle_player_turn(self):
        # Tour du joueur : choisir une unité parmi les 4
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            # Calcul et affichage des cases accessibles
            accessible_cells = self.get_accessible_cells(selected_unit)
            self.draw_accessible_cells(accessible_cells)
            pygame.display.flip()

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return "menu"
                        dx, dy = 0, 0

                        # Gestion du déplacement en fonction de l'unité
                        if selected_unit.nom == "Alex":
                            max_distance = 1  
                        elif selected_unit.nom == "Clara":
                            max_distance = 2  
                        elif selected_unit.nom == "Maxime":
                            max_distance = 3  
                        elif selected_unit.nom == "Sophie":
                            max_distance = 4  
                        else:
                            max_distance = selected_unit.deplacement_distance  

                        # Déplacement
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        distance_moved = 0
                        while distance_moved < max_distance:
                            target_x = selected_unit.x + dx
                            target_y = selected_unit.y + dy

                            if any(unit.x == target_x and unit.y == target_y for unit in self.player_units + self.enemy_units):
                                break

                            if selected_unit.move(dx, dy, self.terrain):
                                distance_moved += 1
                                self.flip_display()
                            else:
                                break

                        if (selected_unit.x + dx, selected_unit.y + dy) in accessible_cells:
                            target_x = selected_unit.x + dx
                            target_y = selected_unit.y + dy
                            if not any(unit.x == target_x and unit.y == target_y for unit in self.player_units + self.enemy_units):
                                if selected_unit.move(dx, dy, self.terrain):
                                    self.flip_display()
                                    self.draw_accessible_cells(accessible_cells)
                                    pygame.display.flip()
                        # Attaque avec la barre espace
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attaquer_avec_arme(enemy, self.terrain)
                                    # print(f" {enemy.nom} est à attaquer ")
                                    # print(f"{ enemy.nom } est le reste { enemy.vie}")
                                    if enemy.vie <= 0:
                                        self.enemy_units.remove(enemy)
                                        print(enemy.nom , 'est éliminé ')
                                        self.player_score += 1

                        # Après que l'unité ait agi, fin du tour pour cette unité
                        has_acted = True
                        selected_unit.is_selected = False  # Désélectionner l'unité
                        # Vérifie les collisions après chaque tour
            # Fin du tour du joueur (quand une unité a agi)
            self.tour += 1


    def handle_enemy_turn(self):
        # Tour de l'ennemi : choisir une unité parmi les 4
        for selected_unit in self.enemy_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            # Calcul et affichage des cases accessibles
            accessible_cells = self.get_accessible_cells(selected_unit)
            self.draw_accessible_cells(accessible_cells)
            pygame.display.flip()

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return "menu"
                        dx, dy = 0, 0

                        # Gestion du déplacement en fonction de l'unité
                        if selected_unit.nom == "Alex":
                            max_distance = 1  # Alex bouge de 1 case
                        elif selected_unit.nom == "Clara":
                            max_distance = 2  # Clara bouge de 2 cases
                        elif selected_unit.nom == "Maxime":
                            max_distance = 3  # Maxime bouge de 3 cases
                        elif selected_unit.nom == "Sophie":
                            max_distance = 4  # Sophie bouge de 4 cases
                        else:
                            max_distance = selected_unit.deplacement_distance  

                        # Déplacement
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        distance_moved = 0
                        while distance_moved < max_distance:
                            target_x = selected_unit.x + dx
                            target_y = selected_unit.y + dy

                            if any(unit.x == target_x and unit.y == target_y for unit in self.player_units + self.enemy_units):
                                break

                            if selected_unit.move(dx, dy, self.terrain):
                                distance_moved += 1
                                self.flip_display()
                            else:
                                break

                        if (selected_unit.x + dx, selected_unit.y + dy) in accessible_cells:
                            target_x = selected_unit.x + dx
                            target_y = selected_unit.y + dy
                            if not any(unit.x == target_x and unit.y == target_y for unit in self.player_units + self.enemy_units):
                                if selected_unit.move(dx, dy, self.terrain):
                                    self.flip_display()
                                    self.draw_accessible_cells(accessible_cells)
                                    pygame.display.flip()

                        # Attaque avec la barre espace
                        if event.key == pygame.K_SPACE:
                            for player in self.player_units:
                                # Vérifie si le joueur est adjacent à l'ennemi
                                if abs(selected_unit.x - player.x) <= 1 and abs(selected_unit.y - player.y) <= 1: ## si le nombre de case < 3 il peut attaquer ( à chnager après)
                                    # Effectue l'attaque
                                    selected_unit.attaquer_avec_arme(player, self.terrain)
                                    # print(f"{player.nom} est attaqué")
                                    # print(f"La vie restante de {player.nom} est {player.vie}")
                                    
                                    # Si la vie du joueur tombe à 0, il est retiré
                                    if player.vie <= 0:
                                        self.player_units.remove(player)
                                        self.enemy_score += 1
                                        print(f"{player.nom} est éliminé")

                        # Après que l'unité ait agi, fin du tour pour cette unité
                        has_acted = True
                        selected_unit.is_selected = False  # Désélectionner l'unité

            # Fin du tour de l'ennemi (quand une unité a agi)
            self.tour += 1


    

    def get_nearest_player(self, unit):
        """Retourne l'unité du joueur la plus proche."""
        nearest_player = self.player_units[0]
        min_distance = float('inf')

        for player in self.player_units:
            distance = abs(unit.x - player.x) + abs(unit.y - player.y)
            if distance < min_distance:
                min_distance = distance
                nearest_player = player

        return nearest_player

    def flip_display(self):
        """Affiche l'état actuel du jeu."""
        # Afficher le fond d'écran
        window_width = CELL_SIZE * NUM_COLUMNS
        window_height = CELL_SIZE * NUM_ROWS
        background = pygame.image.load("image/Desert2.jpg")
        background = pygame.transform.scale(background, (window_width, window_height))
        self.screen.blit(background, (0, 0))

        # Affiche la grille
        self.terrain.afficher_grille(self.screen)

        # Affiche toutes les unités et leurs barres de santé
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)  # Dessine l'unité
            unit.update_health(self.screen)  # Dessine la barre de santé

        # Dessiner le tableau d'affichage
        self.afficher_tableau()

        pygame.display.flip()


    def afficher_tableau(self):
        """Affiche le tableau d'affichage des scores en bas."""
        font = pygame.font.Font(None, 36)
        tableau_rect = pygame.Rect(0, HEIGHT - TABLEAU_HEIGHT + 120, WIDTH, TABLEAU_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, tableau_rect)

        # Vérifier que les variables de score et de tour sont bien initialisées
        if hasattr(self, 'player_score') and hasattr(self, 'enemy_score') and hasattr(self, 'tour'):
            score_text = font.render(
                f"Tour: {self.tour} | Player: {self.player_score} - {self.enemy_score} :Enemy", True, BLACK
            )
            self.screen.blit(score_text, (100, HEIGHT - TABLEAU_HEIGHT + 150))

        # Vérifier que start_time est défini avant de calculer le temps
        if hasattr(self, 'start_time'):
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Temps écoulé en secondes
            time_text = font.render(f"Temps écoulé: {elapsed_time}s", True, BLACK)

            # Affichage du temps au centre
            time_x = WIDTH // 2 - time_text.get_width() // 2  # Centrer horizontalement
            time_y = HEIGHT - TABLEAU_HEIGHT + 120  # Position verticale alignée
            self.screen.blit(time_text, (time_x, time_y))

        # Mise à jour de l'écran (si nécessaire)
        pygame.display.flip()

    
    def get_accessible_cells(self, unit):
        """
        Retourne une liste de cases accessibles dans les 4 directions cardinales,
        en vérifiant que les cases sont dans la grille et qu'aucune unité ne s'y trouve.
        """
        accessible_cells = []
        max_distance = unit.deplacement_distance
        max_height = (HEIGHT ) // CELL_SIZE  # Nombre de lignes disponibles dans la grille
        max_width = NUM_COLUMNS  # Nombre de colonnes disponibles dans la grille

        # Directions rectilignes (haut, bas, gauche, droite)
        directions = [
            (0, -1),  # Haut
            (0, 1),   # Bas
            (-1, 0),  # Gauche
            (1, 0)    # Droite
        ]

        for dx, dy in directions:
            for step in range(1, max_distance + 1):
                target_x = unit.x + dx * step
                target_y = unit.y + dy * step

                # Vérifier que la case est dans les limites de la grille
                if 0 <= target_x < max_width and 0 <= target_y < max_height:
                    # Vérifier qu'aucune unité ne se trouve sur la case
                    if not any(u.x == target_x and u.y == target_y for u in self.player_units + self.enemy_units):
                        accessible_cells.append((target_x, target_y))
                    else:
                        # Si une unité bloque la case, arrêter l'exploration dans cette direction
                        break
                else:
                    # Si la case dépasse la grille, arrêter l'exploration dans cette direction
                    break

        return accessible_cells


    def draw_accessible_cells(self, accessible_cells):
        """Dessine les cases accessibles en bleu."""
        for x, y in accessible_cells:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (0, 0, 255), rect, 3)  # Dessine les cases en bleu



def select_player(screen, title, units):
    """Permet de sélectionner un joueur ou un ennemi avec la souris."""
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 36)

    while True:
        screen.fill(WHITE)

        # Affiche le titre
        title_text = font.render(title, True, BLACK)
        screen.blit(title_text, (WIDTH // 4 - 80, HEIGHT // 6))

        # Affiche les unités à sélectionner
        buttons = []
        for i, unit in enumerate(units):
            x_pos = WIDTH // 8 + i * 120
            y_pos = HEIGHT // 3
            button = pygame.Rect(x_pos, y_pos, 150, 150)
            buttons.append((button, unit))

            # Afficher les images et les noms des unités
            if unit.image:
                screen.blit(unit.image, (x_pos, y_pos))
            unit_name = small_font.render(unit.nom, True, BLACK)
            screen.blit(unit_name, (x_pos - 25, y_pos + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, unit in buttons:
                    if button.collidepoint(event.pos):
                        return unit
                    
        
def splash_screen(screen):
    """Affiche un écran de démarrage avec une image de fond et attend une touche."""
   
    splash_image = pygame.image.load("image/K.png")  
    splash_image = pygame.transform.scale(splash_image, (WIDTH, HEIGHT + + TABLEAU_HEIGHT))
    
 
    font = pygame.font.Font(None, 50)
    message = font.render("Appuyez sur Entrée pour continuer", True, WHITE)
    
    while True:
        screen.blit(splash_image, (0, 0))  
        
        
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 100))
        
        pygame.display.flip()
        
        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Si l'utilisateur appuie sur "Entrée"
                    return



def menu(screen):
    """Affiche le menu principal et permet de naviguer avec la souris."""
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    start_button = pygame.Rect(WIDTH // 3, HEIGHT // 4 + 100, 200, 50)
    settings_button = pygame.Rect(WIDTH // 3, HEIGHT // 4 + 160, 200, 50)
    exit_button = pygame.Rect(WIDTH // 3, HEIGHT // 4 + 220, 200, 50)
    
    splash_screen(screen)

    while True:
        screen.fill(WHITE)

        title = font.render("Menu Principal", True, BLACK)
        start_text = small_font.render("Solo", True, WHITE)
        settings_text = small_font.render("Multiplayers", True, WHITE)
        exit_text = small_font.render("Exit", True, WHITE)

        screen.blit(title, (WIDTH // 3 - 100, HEIGHT // 4))
        pygame.draw.rect(screen, BLACK, start_button)
        pygame.draw.rect(screen, BLACK, settings_button)
        pygame.draw.rect(screen, BLACK, exit_button)
        screen.blit(start_text, (start_button.x + 20, start_button.y + 10))
        screen.blit(settings_text, (settings_button.x + 20, settings_button.y + 10))
        screen.blit(exit_text, (exit_button.x + 20, exit_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return "Solo"
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()
                elif settings_button.collidepoint(event.pos):
                    return "Multiplayers"



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + TABLEAU_HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    while True:
        action = menu(screen)
        if action == "Solo":
            game = Game(screen)  # Utilise Affichage ici
            selected_player = select_player(screen, "Select Your Player", game.player_units)
            selected_enemy = select_player(screen, "Select Enemy Player", game.enemy_units)
            # Vérifie les collisions après chaque tour
             # à vérifier ! 

            game.player_units = [selected_player]
            game.enemy_units = [selected_enemy]

            while True:
                # Affiche le jeu et le tableau à chaque tour
                game.flip_display()

                # Tour du joueur
                game.handle_player_turn()

                # Vérifie si le jeu continue ou si le joueur a choisi de revenir au menu
                if game.tour  % 2 == 0:  # Si c'est un tour impair, c'est à l'IA de jouer
                    game.handle_player_turn()
                else :  # Si c'est un tour pair, c'est au joueur de jouer
                    result = game.handle_player_turn()
                    if result == "menu":
                        break
        elif action == "Multiplayers":
            game = Game(screen)  # Utilise Affichage ici
            game.flip_display()  # Affiche le terrain et les unités
            while True:
                
                result = game.handle_player_turn()  # Le joueur joue son tour
                if result == "menu":
                    break
                game.handle_enemy_turn()  # L'IA joue après
 

if __name__ == "__main__":
    main()
   

