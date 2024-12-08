import pygame
from terain import * # Vérifiez que 'terain' est bien importé, cela semble être une faute de frappe pour 'terrain'
from unit import *
from main import *

#Bibliothèque pour lire et afficher un gif derrière le menu démarrage 
from PIL import Image, ImageSequence

# Constantes globales
WIDTH = 25* 40  # Largeur de la fenêtre (15 cases de 50 pixels)
HEIGHT = 13 * 40  # Hauteur de la fenêtre (15 cases de 50 pixels)

TABLEAU_HEIGHT = 100  # Hauteur du tableau d'affichage en bas
CELL_SIZE = 40  # Taille de chaque case (50x50 pixels)
CREAM = (245, 245, 220)  # Couleur crème pour l'arrière-plan
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NUM_COLUMNS = 15 
NUM_ROWS = 15

# Taille des images des unités
UNIT_IMAGE_SIZE = (40, 40)  # Taille redimensionnée des images (40x40 pixels)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.tour = 1
        self.player_score = 0
        self.enemy_score = 0

        # Création des compétences
        competence_soin = Competence ("Soin", "Restaure 20 points de vie", soin_effet)
        competence_attaque_puissante = Competence("Attaque Puissante", "Inflige 50 dégâts", attaque_puissante_effet)

        # Initialisation des unités des joueurs
        self.player_units = [
            Type_Unite("Alex", 0, 0, 50, 30, "player", 10, 1, [competence_soin],"0"),
            Type_Unite("Clara", 0, 2, 100, 25, "player", 15, 2, [competence_attaque_puissante],"1"),
            Type_Unite("Maxime", 0, 3, 100, 35, "player", 10, 3, [competence_attaque_puissante],"2"),
            Type_Unite("Sophie", 0, 1, 100, 20, "player", 20, 4, [competence_soin], "3"),
        ]

        self.enemy_units = [
            Type_Unite("Alex", 14, 14, 100, 30, "enemy", 10, 1, [competence_soin], "0"),
            Type_Unite("Clara", 14, 13, 100, 25, "enemy", 15, 2, [competence_attaque_puissante], "1"),
            Type_Unite("Maxime", 14, 12, 100, 35, "enemy", 10, 3, [competence_attaque_puissante], "2"),
            Type_Unite("Sophie", 14, 11, 100, 20, "enemy", 20, 4, [competence_soin], "3"),
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
                            # Déplace l'unité de 1 case si elle peut se déplacer
                            if selected_unit.move(dx, dy, self.terrain):
                                distance_moved += 1
                                self.flip_display()
                            else:
                                break  # L'unité ne peut plus avancer, on arrête le mouvement

                        # Vérifie si la case est accessible
                        if (selected_unit.x + dx, selected_unit.y + dy) in accessible_cells:
                            if selected_unit.move(dx, dy, self.terrain):
                                self.flip_display()
                                self.draw_accessible_cells(accessible_cells)  # Redessine les cases accessibles
                                pygame.display.flip()

                        # Attaque avec la barre espace
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)
                                        self.player_score += 1

                        # Après que l'unité ait agi, fin du tour pour cette unité
                        has_acted = True
                        selected_unit.is_selected = False  # Désélectionner l'unité

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
                            # Déplace l'unité de 1 case si elle peut se déplacer
                            if selected_unit.move(dx, dy, self.terrain):
                                distance_moved += 1
                                self.flip_display()
                            else:
                                break  # L'unité ne peut plus avancer, on arrête le mouvement

                        # Vérifie si la case est accessible
                        if (selected_unit.x + dx, selected_unit.y + dy) in accessible_cells:
                            if selected_unit.move(dx, dy, self.terrain):
                                self.flip_display()
                                self.draw_accessible_cells(accessible_cells)  # Redessine les cases accessibles
                                pygame.display.flip()

                        # Attaque avec la barre espace
                        if event.key == pygame.K_SPACE:
                            for player in self.player_units:
                                if abs(selected_unit.x - player.x) <= 1 and abs(selected_unit.y - player.y) <= 1:
                                    selected_unit.attack(player)
                                    if player.health <= 0:
                                        self.player_units.remove(player)
                                        self.enemy_score += 1

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
        background = pygame.transform.scale(background, (WIDTH , HEIGHT))
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
        tableau_rect = pygame.Rect(0, HEIGHT - TABLEAU_HEIGHT  + 120, WIDTH, TABLEAU_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, tableau_rect)

        # Texte des scores et tours
        score_text = font.render(
            f"Tour: {self.tour} | Player: {self.player_score} - {self.enemy_score}   :Enemy", True, BLACK
        )
        self.screen.blit(score_text, (100, HEIGHT - TABLEAU_HEIGHT + 150))

    
    def get_accessible_cells(self, unit):
        """Retourne une liste de cases accessibles dans les 4 directions cardinales."""
        accessible_cells = []
        max_distance = unit.deplacement_distance

        # On ne parcourt que les 4 directions rectilignes (haut, bas, gauche, droite)
        # Haut
        accessible_cells.append((unit.x, unit.y - max_distance))  # Case la plus haute
        # Bas
        accessible_cells.append((unit.x, unit.y + max_distance))  # Case la plus basse
        # Gauche
        accessible_cells.append((unit.x - max_distance, unit.y))  # Case la plus à gauche
        # Droite
        accessible_cells.append((unit.x + max_distance, unit.y))  # Case la plus à droite

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
        screen.fill(CREAM)

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
                    
        

def play_gif_background(gif_path, screen):
    """Lit un GIF et l'affiche en arrière-plan."""
    # Charger le GIF avec Pillow
    gif = Image.open(gif_path)
    frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
    
    clock = pygame.time.Clock()
    frame_index = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        # Obtenir la frame actuelle
        frame = frames[frame_index]
        frame = frame.resize((WIDTH, HEIGHT))  # Redimensionner à la taille de l'écran
        frame_surface = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
        
        # Afficher la frame
        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()
        
        # Passer à la frame suivante
        frame_index = (frame_index + 1) % len(frames)
        clock.tick(10)  # Contrôle la vitesse (10 FPS ici)


def menu(screen):
    """Affiche le menu principal et permet de naviguer avec la souris."""
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    start_button = pygame.Rect(WIDTH // 3, HEIGHT // 4 + 100, 200, 50)
    settings_button = pygame.Rect(WIDTH // 3, HEIGHT // 4 + 160, 200, 50)
    exit_button = pygame.Rect(WIDTH // 3, HEIGHT // 4 + 220, 200, 50)


    clock = pygame.time.Clock()

    # Charger le GIF
    gif_path = "gif.gif"
    gif = Image.open(gif_path)
    frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
    frame_index = 0


    while True:

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
        
        # Obtenir la frame actuelle du GIF
        frame = frames[frame_index]
        frame = frame.resize((WIDTH, HEIGHT))
        frame_surface = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)

        # Afficher le GIF en arrière-plan
        screen.blit(frame_surface, (0, 0))


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

         # Passer à la frame suivante
        frame_index = (frame_index + 1) % len(frames)
        clock.tick(10)  # Contrôle de la vitesse du GIF (10 FPS)



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
                # L'IA et le joueur alternent les tours
                result = game.handle_player_turn()  # Le joueur joue son tour
                if result == "menu":
                    break
                game.handle_enemy_turn()  # L'IA joue après
 



if __name__ == "__main__":
    main()
   

