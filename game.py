import pygame
from terain import * # Vérifiez que 'terain' est bien importé, cela semble être une faute de frappe pour 'terrain'
from unit import *
from main import *
from Feu import *
from Competence import *


#Bibliothèque pour lire et afficher un gif derrière le menu démarrage 
from PIL import Image, ImageSequence

# Constantes globales

NUM_COLUMNS = 37
NUM_ROWS = 18
WIDTH = NUM_COLUMNS* 40  # Largeur de la fenêtre (15 cases de 40 pixels)
HEIGHT = NUM_ROWS * 40  
CREAM = (245, 245, 220)  # Couleur crème pour l'arrière-plan
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TABLEAU_HEIGHT = 40  # Hauteur du tableau d'affichage en bas
CELL_SIZE = 40  # Taille de chaque case (40x40 pixels)

# Taille des images des unités
UNIT_IMAGE_SIZE = (40, 40)  # Taille redimensionnée des images (40x40 pixels)

class Game:
    def __init__(self, screen):
        self.start_time = pygame.time.get_ticks()
        self.screen = screen
        self.tour = 0
        self.player_score = 0
        self.enemy_score = 0
        self.message_log =[]
        self.max_messages = 2
        self.player_units = []  
        self.enemy_units = [] 
        self.units_with_active_skills = []
  
        

        # Création des compétences
        competence_soin = Competence ("Soin", "Restaure 20 points de vie", soin_effet)
        competence_bouclier = Competence("Bouclier Protecteur", "Réduit les dégâts reçus de 50 % pendant 1 tour.", bouclier_effet)
        competence_poison = Competence("Poison", "Inflige 10 points de dégâts par tour pendant 3 tours.", poison_effet)
        competence_glace = Competence( "galce", "ne bouge pas ",glace_eclatante_effet)
        

        epee = Arme("Épée", degats=30, deplacement_distance=5, effet=epee_effet)
        arc = Arme("Arc", degats=20, deplacement_distance=10, effet=arc_effet)
        lance = Arme("Lance", degats=25, deplacement_distance=8, effet=lance_effet)
        bombe = Arme("Bombe", degats=40, deplacement_distance=3, effet=bombe_effet)

        # Initialisation des unités des joueurs
        self.player_units = [
            Type_Unite("Alex", 0, 0,  100, 30, "player", 10, 1, [competence_soin],epee ,"0"),
            Type_Unite("Clara", 0, 1, 100, 25, "player", 15, 2, [competence_bouclier],arc,"1"),
            Type_Unite("Maxime", 0, 2, 100, 35, "player", 10, 3, [competence_poison],lance ,"2"),
            Type_Unite("Sophie", 0, 3, 100, 20, "player", 20, 4, [competence_glace], bombe ,"3"),
        ]

        self.enemy_units = [
            Type_Unite("Alex", 0, 5, 100, 30, "enemy", 10, 1, [competence_soin], epee ,"0"),
            Type_Unite("Clara", 0, 6, 100, 25, "enemy", 15, 2, [competence_bouclier], arc , "1"),
            Type_Unite("Maxime", 0, 7, 100, 35, "enemy", 10, 3, [competence_poison],lance , "2"),
            Type_Unite("Sophie", 0, 8, 100, 20, "enemy", 20, 4, [competence_poison], arc, "3"),
        ]

        for unit in self.player_units + self.enemy_units:
            if unit.image:
                unit.image = pygame.transform.scale(unit.image, UNIT_IMAGE_SIZE)

        # Initialisation du terrain
        self.terrain = Terrain(NUM_COLUMNS, NUM_ROWS)  # Correction de 'terain' en 'terrain'
        self.terrain.generer_grille()

    def update_skill_effects(self):
        # Supprimer les unités dont l'effet est expiré (par exemple, après 3 secondes)
        current_time = pygame.time.get_ticks()
        self.units_with_active_skills = [
            (unit, start_time) for unit, start_time in self.units_with_active_skills
            if current_time - start_time < 3000  # 3 secondes
        ]

        # Dessiner les icônes pour les unités restantes
        for unit, _ in self.units_with_active_skills:
            self.draw_skill_icon(unit)

    def highlight_game_area(self, center_x, center_y, radius=5):
        """
        Affiche une partie du terrain avec des unités et des mouvements visibles,
        et assombrit les zones en dehors de cette zone.
        
        Args:
            center_x (int): Coordonnée x du centre de la zone visible.
            center_y (int): Coordonnée y du centre de la zone visible.
            radius (int): Rayon de la zone visible.
        """
        # Afficher le terrain normalement
        self.flip_display()

        # Créer un overlay sombre pour tout l'écran
        dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 180))  # Couleur sombre avec transparence (180 sur 255)

        # Calculer les dimensions de la zone visible (en pixels)
        visible_x = max(0, center_x - radius) * CELL_SIZE
        visible_y = max(0, center_y - radius) * CELL_SIZE
        visible_width = min(2 * radius + 1, NUM_COLUMNS - max(0, center_x - radius)) * CELL_SIZE
        visible_height = min(2 * radius + 1, NUM_ROWS - max(0, center_y - radius)) * CELL_SIZE

        # Découper la zone visible (rectangle)
        visible_rect = pygame.Rect(visible_x, visible_y, visible_width, visible_height)

        # Appliquer l'effet sombre partout sauf dans la zone visible
        dark_overlay.fill((0, 0, 0, 0), rect=visible_rect)
        self.screen.blit(dark_overlay, (0, 0))

        # Mettre à jour l'affichage
        pygame.display.update()


    def get_all_units(self):
        """Retourne toutes les unités (joueurs et ennemis)."""
        return self.player_units + self.enemy_units


    def ajouter_message(self, message):
        """Ajoute un message au tableau d'affichage."""
        self.message_log.append(message)
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)  # Supprime les anciens messages


    def handle_player_turn(self):
        # Tour du joueur : choisir une unité parmi les 4
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            

            self.highlight_game_area(selected_unit.x, selected_unit.y, radius=4)
            # Calcul et affichage des cases accessibles
            accessible_cells = self.get_accessible_cells(selected_unit)
            self.draw_accessible_cells(accessible_cells)
            pygame.display.flip()

            # Position actuelle du curseur pour sélectionner une case
            cursor_x, cursor_y = selected_unit.x, selected_unit.y

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return "menu"

                        # Déplacement du curseur avec les flèches du clavier
                        if event.key == pygame.K_LEFT:
                            if (cursor_x - 1, cursor_y) in accessible_cells:
                                cursor_x -= 1
                        elif event.key == pygame.K_RIGHT:
                            if (cursor_x + 1, cursor_y) in accessible_cells:
                                cursor_x += 1
                        elif event.key == pygame.K_UP:
                            if (cursor_x, cursor_y - 1) in accessible_cells:
                                cursor_y -= 1
                        elif event.key == pygame.K_DOWN:
                            if (cursor_x, cursor_y + 1) in accessible_cells:
                                cursor_y += 1

                        # Mise à jour de l'affichage du curseur
                        self.flip_display()
                        self.draw_accessible_cells(accessible_cells)
                        # Dessiner le curseur en rouge
                        cursor_rect = pygame.Rect(cursor_x * CELL_SIZE, cursor_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, (255, 0, 0), cursor_rect, 3)  # Rouge pour le curseur
                        pygame.display.flip()

                        # Valider le déplacement avec Entrée
                        if event.key == pygame.K_RETURN:
                            if (cursor_x, cursor_y) in accessible_cells:
                                # Déplacer l'unité vers la case sélectionnée
                                selected_unit.move(cursor_x, cursor_y, self.terrain)
                                self.flip_display()
                                has_acted = True  # Fin du tour pour cette unité

                        # Attaque avec la barre espace
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= selected_unit.deplacement_distance and abs(selected_unit.y - enemy.y) <= selected_unit.deplacement_distance:
                                    if selected_unit.arme.nom == "Bombe":
                                    # Utiliser l'effet de la bombe
                                        bombe_effet(
                                            utilisateur=selected_unit,
                                            cible=enemy,
                                            terrain=self.terrain,
                                            game_instance=self
                                        )
                                    else:
                                        selected_unit.attaquer_avec_arme(enemy, self.terrain)
                                    # selected_unit.attaquer_avec_arme(enemy, self.terrain)
                                    message = f"{selected_unit.nom} utilise {selected_unit.arme.nom} sur {enemy.nom}!"
                                    self.ajouter_message(message)
                                    if enemy.vie <= 0:
                                        self.enemy_units.remove(enemy)
                                        self.ajouter_message(f"{enemy.nom} est éliminé!")
                                        print(enemy.nom, 'est éliminé ')
                                        self.player_score += 1
                                    has_acted = True  # Fin du tour pour cette unité
                        competence_used = False
                        if event.key == pygame.K_c and not competence_used:
                            if selected_unit.competences:
                                print(f"Compétences disponibles : {[c.nom for c in selected_unit.competences]}")
                                # Utiliser la première compétence par défaut (ou une logique pour choisir)
                                competence = selected_unit.competences[0]
                                competence.appliquer(selected_unit)  # Applique la compétence sur l'unité elle-même
                                self.ajouter_message(f"{selected_unit.nom} utilise la compétence {competence.nom}!")
                                self.draw_skill_icon(selected_unit)
                                self.units_with_active_skills.append((selected_unit, pygame.time.get_ticks()))
                                competence_used = True  # Empêche une autre utilisation de compétence ce tour
                            else:
                                print(f"{selected_unit.nom} n'a pas de compétence disponible.")

            selected_unit.is_selected = False  # Désélectionner l'unité
            self.tour += 1  # Passer au tour suivant



    def handle_enemy_turn(self):
        # Tour de l'ennemi : choisir une unité parmi les ennemis
        for selected_unit in self.enemy_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            
            # Calcul et affichage des cases accessibles
            self.highlight_game_area(selected_unit.x, selected_unit.y, radius=4)
            accessible_cells = self.get_accessible_cells(selected_unit)
            self.draw_accessible_cells(accessible_cells)
            pygame.display.flip()

            # Position actuelle du curseur pour sélectionner une case
            cursor_x, cursor_y = selected_unit.x, selected_unit.y

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return "menu"

                        # Déplacement du curseur avec les flèches du clavier
                        if event.key == pygame.K_LEFT:
                            if (cursor_x - 1, cursor_y) in accessible_cells:
                                cursor_x -= 1
                        elif event.key == pygame.K_RIGHT:
                            if (cursor_x + 1, cursor_y) in accessible_cells:
                                cursor_x += 1
                        elif event.key == pygame.K_UP:
                            if (cursor_x, cursor_y - 1) in accessible_cells:
                                cursor_y -= 1
                        elif event.key == pygame.K_DOWN:
                            if (cursor_x, cursor_y + 1) in accessible_cells:
                                cursor_y += 1

                        # Mise à jour de l'affichage du curseur
                        self.flip_display()
                        self.draw_accessible_cells(accessible_cells)
                        # Dessiner le curseur en rouge
                        cursor_rect = pygame.Rect(cursor_x * CELL_SIZE, cursor_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, (255, 0, 0), cursor_rect, 3)  # Rouge pour le curseur
                        pygame.display.flip()

                        # Valider le déplacement avec Entrée
                        if event.key == pygame.K_RETURN:
                            if (cursor_x, cursor_y) in accessible_cells:
                                # Déplacer l'unité vers la case sélectionnée
                                selected_unit.x, selected_unit.y = cursor_x, cursor_y
                                self.flip_display()
                                has_acted = True  # Fin du tour pour cette unité

                        # Attaque avec la barre espace
                        if event.key == pygame.K_SPACE:
                            for player in self.player_units:
                                # Vérifie si le joueur est adjacent à l'ennemi
                                if abs(selected_unit.x - player.x) <= selected_unit.deplacement_distance and abs(selected_unit.y - player.y) <= selected_unit.deplacement_distance: 
                                    # Effectue l'attaque
                                    selected_unit.attaquer_avec_arme(player, self.terrain)
                                    
                                    # Si la vie du joueur tombe à 0, il est retiré
                                    if player.vie <= 0:
                                        self.player_units.remove(player)
                                        self.enemy_score += 1
                                        print(f"{player.nom} est éliminé")
                                    has_acted = True  # Fin du tour pour cette unité

            selected_unit.is_selected = False  # Désélectionner l'unité
            self.tour += 1  # Passer au tour suivant


    

    # def get_nearest_player(self, unit):
    #     """Retourne l'unité du joueur la plus proche."""
    #     nearest_player = self.player_units[0]
    #     min_distance = float('inf')

    #     for player in self.player_units:
    #         distance = abs(unit.x - player.x) + abs(unit.y - player.y)
    #         if distance < min_distance:
    #             min_distance = distance
    #             nearest_player = player

    #     return nearest_player





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

               if unit in [u[0] for u in self.units_with_active_skills]:
                    self.draw_skill_icon(unit)

        # Dessiner le tableau d'affichage
        self.afficher_tableau()

        pygame.display.flip()

 

    def afficher_tableau(self):
        """Affiche le tableau d'affichage des scores et les messages."""
        font = pygame.font.Font(None, 36)
        tableau_rect = pygame.Rect(0, HEIGHT - TABLEAU_HEIGHT * 2, WIDTH, TABLEAU_HEIGHT * 2)
        SAND_COLOR = (194, 178, 128)

        # Dessiner le fond du tableau
        pygame.draw.rect(self.screen, SAND_COLOR, tableau_rect)

        # Texte des scores et tours
        score_text = font.render(
            f"Tour: {self.tour} | Player: {self.player_score} - {self.enemy_score} :Enemy", True, BLACK
        )
        
        # Affichage du score centré
        text_width = score_text.get_width()
        text_height = score_text.get_height()
        text_x = (WIDTH - text_width) // 2
        text_y = HEIGHT - TABLEAU_HEIGHT * 2 + 10  # Espace au-dessus des messages
        
        message_fond = pygame.font.Font(None, 24)
        self.screen.blit(score_text, (text_x, text_y))

        # Afficher les messages récents
        y_offset = text_y + text_height + 10  # Espace entre le score et les messages
        for message in self.message_log:
            message_text = message_fond.render(message, True, BLACK)
            self.screen.blit(message_text, (20, y_offset))  # Alignement à gauche
            y_offset += text_height + 2  # Espacement entre les lignes


    def get_accessible_cells(self, unit):
        accessible_cells = []
        max_distance = unit.deplacement_distance


        # Vérification de toutes les cases dans un carré de côté 2*max_distance+1 centré sur l'unité
        for dx in range(-max_distance, max_distance + 1):
            for dy in range(-max_distance, max_distance + 1):
                # Calcul des coordonnées de la case cible
                target_x = unit.x + dx
                target_y = unit.y + dy

                # Vérifier que la case est dans les limites de la grille
                if 0 <= target_x < NUM_COLUMNS and 0 <= target_y < NUM_ROWS -1:
                    # Récupérer la case cible dans le terrain
                    target_case = self.terrain.cases[target_x][target_y]  

                    # Vérifier que la case n'est pas un obstacle
                    if target_case.type_case == 1 or any(u.x == target_x and u.y == target_y for u in self.player_units + self.enemy_units) :
                        # print(f"Case ({target_x}, {target_y}) est un obstacle, ignorée.")
                        continue  # Ignorer cette case

                    # Vérifier qu'aucune unité ne se trouve sur la case
                    else :
                        accessible_cells.append((target_x, target_y))

        return accessible_cells

    
    def draw_skill_icon(self, unit, icon_path="image/skill_activation_icon.jpg"):
        """
        Dessine une icône au-dessus d'une unité pour indiquer qu'une compétence est activée.
        
        Args:
            unit (Type_Unite): L'unité pour laquelle afficher l'icône.
            icon_path (str): Chemin vers l'image de l'icône.
        """
        try:
            # Charger l'icône
            icon = pygame.image.load(icon_path)
            icon = pygame.transform.scale(icon, (15, 15))  # Redimensionner l'icône si nécessaire

            # Positionner l'icône juste au-dessus de l'unité
            icon_x = unit.x * CELL_SIZE + (CELL_SIZE - icon.get_width()) // 2
            icon_y = unit.y * CELL_SIZE - 15  # Placer l'icône au-dessus de l'unité

            # Dessiner l'icône
            self.screen.blit(icon, (icon_x, icon_y))
        except FileNotFoundError:
            print(f"Erreur : Icône introuvable à {icon_path}")


    def draw_accessible_cells(self, accessible_cells):
        """Dessine les cases accessibles ."""
        for x, y in accessible_cells:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 255, 150), rect, 2)  # Dessine les cases en bleu





                    
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
   
    splash_image = pygame.image.load("image/menu12.jpg")  
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
    
    splash_screen(screen)
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
                    if game.tour %8 == 0 :
                        game.terrain.melanger()
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
   

