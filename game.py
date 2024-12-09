import pygame
from terain import * # Vérifiez que 'terain' est bien importé, cela semble être une faute de frappe pour 'terrain'
from unit import *
from main import *
from Feu import *

#Bibliothèque pour lire et afficher un gif derrière le menu démarrage 
from PIL import Image, ImageSequence

# Constantes globales

WIDTH = 37* 40  # Largeur de la fenêtre (15 cases de 40 pixels)
HEIGHT = 18 * 40  # Hauteur de la fenêtre (15 cases de 40 pixels)

TABLEAU_HEIGHT = 40  # Hauteur du tableau d'affichage en bas
CELL_SIZE = 40  # Taille de chaque case (40x40 pixels)

CREAM = (245, 245, 220)  # Couleur crème pour l'arrière-plan
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

NUM_COLUMNS = 37
NUM_ROWS = 18

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
            Type_Unite("Alex", 0, 0,  100, 30, "player", 10, 1, [competence_soin],epee ,"0"),
            Type_Unite("Clara", 0, 1, 100, 25, "player", 15, 2, [competence_attaque_puissante],arc,"1"),
            Type_Unite("Maxime", 0, 2, 100, 35, "player", 10, 3, [competence_attaque_puissante],lance ,"2"),
            Type_Unite("Sophie", 0, 3, 100, 20, "player", 20, 4, [competence_soin], bombe ,"3"),
        ]

        self.enemy_units = [
            Type_Unite("Alex", 28, 10, 100, 30, "enemy", 10, 1, [competence_soin], epee ,"0"),
            Type_Unite("Clara", 28, 9, 100, 25, "enemy", 15, 2, [competence_attaque_puissante], arc , "1"),
            Type_Unite("Maxime", 28, 12, 100, 35, "enemy", 10, 3, [competence_attaque_puissante],lance , "2"),
            Type_Unite("Sophie", 28, 11, 100, 20, "enemy", 20, 4, [competence_soin], bombe, "3"),
        ]

        for unit in self.player_units + self.enemy_units:
            if unit.image:
                unit.image = pygame.transform.scale(unit.image, UNIT_IMAGE_SIZE)

        # Initialisation du terrain
        self.terrain = Terrain(NUM_COLUMNS, NUM_ROWS)  # Correction de 'terain' en 'terrain'
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
        window_width = WIDTH
        window_height = HEIGHT
        background = pygame.image.load("image/Desert2.jpg")
        background = pygame.transform.scale(background, (WIDTH , HEIGHT - TABLEAU_HEIGHT))
        self.screen.blit(background, (0, 0))


        # Affiche la grille
        self.terrain.afficher_grille(self.screen)

        # Affiche toutes les unités et leurs barres de santé
        for unit in self.player_units + self.enemy_units:
            if 0 <= unit.x < NUM_COLUMNS and 0 <= unit.y < NUM_ROWS:
               unit.draw(self.screen)
               unit.update_health(self.screen)

        # Dessiner le tableau d'affichage
        self.afficher_tableau()

        pygame.display.flip()

 

    def afficher_tableau(self):
        #Affichage au milieu de la fenetre 
        """Affiche le tableau d'affichage des scores en bas."""
        font = pygame.font.Font(None, 36)
        tableau_rect = pygame.Rect(0, HEIGHT - TABLEAU_HEIGHT, WIDTH, TABLEAU_HEIGHT)
        SAND_COLOR = (194, 178, 128)

        pygame.draw.rect(self.screen, SAND_COLOR, tableau_rect)

        # Texte des scores et tours
        score_text = font.render(
            f"Tour: {self.tour} | Player: {self.player_score} - {self.enemy_score} :Enemy", True, BLACK
        )

        # Calcul de la position centrée
        text_width = score_text.get_width()
        text_height = score_text.get_height()
        text_x = (WIDTH - text_width) // 2
        text_y = HEIGHT - TABLEAU_HEIGHT + (TABLEAU_HEIGHT - text_height) // 2 

        # Affichage du texte
        self.screen.blit(score_text, (text_x, text_y))
    
    def get_accessible_cells(self, unit):
        """
        Retourne une liste de cases accessibles dans les 4 directions cardinales,
        en vérifiant que les cases sont dans la grille et qu'aucune unité ne s'y trouve.
        """
        accessible_cells = []
        max_distance = unit.deplacement_distance
        max_width = 34 *40 
        max_height = 18*34
 

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

    # Charger l'image en arrière-plan
    background_image_path = "image/menu2.jpg"  # Chemin vers ton image
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Redimensionner à la taille de l'écran

    # Calculer la position pour centrer les boutons
    total_buttons_width = len(units) * 150 + (len(units) - 1) * 20  # Largeur totale avec l'espacement
    start_x = (WIDTH - total_buttons_width) // 2
    y_pos_buttons = HEIGHT // 2

    while True:
        # Afficher l'image comme arrière-plan
        screen.blit(background_image, (0, 0))

        # Affiche le titre
        title_text = font.render(title, True, CREAM)
        screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 6))

        # Afficher les boutons
        buttons = []
        for i, unit in enumerate(units):
            x_pos = start_x + i * 170  # Espacement de 170 entre chaque bouton
            button = pygame.Rect(x_pos, y_pos_buttons, CELL_SIZE, CELL_SIZE)
            buttons.append((button, unit))

            # Dessiner le bouton
            pygame.draw.rect(screen, CREAM, button)  # Fond noir pour les boutons
            if unit.image:
                screen.blit(unit.image, (x_pos, y_pos_buttons))  # Afficher l'image de l'unité
            # Afficher le nom de l'unité en dessous
            unit_name = small_font.render(unit.nom, True, CREAM)
            screen.blit(unit_name, (x_pos + 25 - unit_name.get_width() // 2, y_pos_buttons + 2*CELL_SIZE))

        # Actualiser l'écran
        pygame.display.flip()

        # Gestion des événements
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
    """Affiche le menu principal avec des boutons centrés et un GIF en arrière-plan."""
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    # Dimensions des boutons
    button_width = 200
    button_height = 50
    button_spacing = 20  # Espace entre les boutons

    # Calcul des positions pour centrer les boutons verticalement
    total_height = 3 * button_height + 2 * button_spacing  # Hauteur totale des boutons et des espaces
    start_button = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - total_height) // 2, button_width, button_height)
    settings_button = pygame.Rect(
        (WIDTH - button_width) // 2, start_button.y + button_height + button_spacing, button_width, button_height
    )
    exit_button = pygame.Rect(
        (WIDTH - button_width) // 2, settings_button.y + button_height + button_spacing, button_width, button_height
    )

    clock = pygame.time.Clock()

    # Charger le GIF
    gif_path = "gif.gif"
    gif = Image.open(gif_path)
    frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
    frame_index = 0
    is_last_frame = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return "Solo"
                elif settings_button.collidepoint(event.pos):
                    return "Multiplayers"
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        # Ajouter un arrière-plan uni (ou une image fixe)
        screen.fill((30, 30, 30))  # Couleur de fond gris foncé

        # Obtenir la frame actuelle du GIF
        """cette partie est faite afin de supprimer le dernier frame du gif car il afficher un ecran blanc"""
        if not is_last_frame:
            frame = frames[frame_index]
            frame = frame.resize((WIDTH, HEIGHT))
            frame_surface = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            screen.blit(frame_surface, (0, 0))

            # Passer à la frame suivante
            frame_index += 1
            if frame_index == len(frames):  # Si c'est la dernière frame
                frame_index = 0
                is_last_frame = True
        else:
            # Afficher la dernière frame et le texte "Menu Principal"
            last_frame = frames[-1]
            last_frame = last_frame.resize((WIDTH, HEIGHT))
            last_frame_surface = pygame.image.fromstring(last_frame.tobytes(), last_frame.size, last_frame.mode)
            screen.blit(last_frame_surface, (0, 0))
            is_last_frame = False

        # Afficher le GIF en arrière-plan
        screen.blit(frame_surface, (0, 0))

        # Titre centré
        title = font.render("Menu Principal", True, BLACK)
        screen.blit(title, ((WIDTH - title.get_width()) // 2, start_button.y - 100))

        # Dessiner les boutons et centrer le texte
        for button, text in [
            (start_button, "Solo"),
            (settings_button, "Multiplayers"),
            (exit_button, "Exit"),
        ]:
            pygame.draw.rect(screen, (0, 0, 0), button)  # Fond noir pour les boutons
            text_surface = small_font.render(text, True, (255, 255, 255))  # Texte blanc
            text_x = button.x + (button.width - text_surface.get_width()) // 2
            text_y = button.y + (button.height - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_x, text_y))

        # Mettre à jour l'écran
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
                # L'IA et le joueur alternent les tours
                result = game.handle_player_turn()  # Le joueur joue son tour
                if result == "menu":
                    break
                game.handle_enemy_turn()  # L'IA joue après
 

if __name__ == "__main__":
    main()
   

