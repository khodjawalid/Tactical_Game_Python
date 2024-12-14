import pygame
import random
import numpy as np
from game import *

from PIL import Image, ImageSequence


def select_player(screen, title, units):
    """Permet de sélectionner un joueur ou un ennemi avec la souris."""
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 36)

    # Charger l'image en arrière-plan
    background_image_path = "image/menu1234.png"  # Chemin vers l'image d'arrière-plan
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Redimensionner à la taille de l'écran

    # Taille des images agrandies
    enlarged_image_size = (100, 100)  # Taille augmentée

    # Calculer la position pour centrer les boutons
    total_buttons_width = len(units) * 150 + (len(units) - 1) * 20  # Largeur totale avec l'espacement
    start_x = (WIDTH - total_buttons_width) // 2
    y_pos_buttons = HEIGHT // 2

    while True:
        # Afficher l'image comme arrière-plan
        screen.blit(background_image, (0, 0))

        # Affiche le titre
        title_text = font.render(title, True, (255, 255, 255))  # Texte blanc
        screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 6))

        # Afficher les boutons
        buttons = []
        for i, unit in enumerate(units):
            x_pos = start_x + i * 170  # Espacement de 170 entre chaque bouton
            button = pygame.Rect(x_pos, y_pos_buttons, *enlarged_image_size)
            buttons.append((button, unit))

            # Redimensionner l'image pour cette phase de sélection
            enlarged_image = pygame.transform.scale(unit.image, enlarged_image_size)

            # Dessiner le bouton avec une image agrandie
            screen.blit(enlarged_image, (x_pos, y_pos_buttons))

            # Afficher le nom de l'unité en dessous
            unit_name = small_font.render(unit.nom, True, (255, 255, 255))  # Texte blanc
            screen.blit(unit_name, (x_pos + enlarged_image_size[0] // 2 - unit_name.get_width() // 2,
                                    y_pos_buttons + enlarged_image_size[1] + 10))

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
   
    splash_image = pygame.image.load("image/menu123.jpg")  
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
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)

    while True:
        action = menu(screen)

        # if action == "Solo":
        if action == "Solo":
            game = Game(screen)  # Initialisation du jeu pour le mode solo
            selected_player = select_player(screen, "Select Your Player", game.player_units)
            selected_enemy = select_player(screen, "Select Enemy Player", game.enemy_units)

            # Configurer les unités du joueur et de l'ennemi
            game.player_units = [selected_player]
            game.enemy_units = [selected_enemy]
            game.display_loading_screen("Solo")
            is_player_turn = True  # Variable pour alterner les tours

            # while game.running:
            while game.running:
                # Gestion des tours et logique du jeu
                game.flip_display()
                if is_player_turn:
                    result = game.handle_player_turn()
                    if result == "menu":
                        game.running = False
                    is_player_turn = False
                else:
                    result = game.enemy_ai.play_turn()
                    is_player_turn = True

                result = game.check_end_game()
                if result == "menu":
                    game.running = False


                # Mélanger le terrain tous les 8 tours
                if game.tour % 2 == 0:
                    game.terrain.melanger()

                # Incrémenter les tours pour affichage


        # elif action == "Multiplayers":
        elif action == "Multiplayers":
            game = Game(screen)  # Initialisation du jeu pour le mode multijoueur
            game.display_loading_screen("Multiplayer")
            game.flip_display()

            # while game.running:
            while game.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:  # Touche Pause
                        result = game.show_pause_menu()
                        if result == "menu":
                            game.running = False
                            break
                        elif result == "resume":
                            continue
                
                game.flip_display()
                # Logique des tours pour les joueurs
                for player_unit, enemy_unit in zip(game.player_units[:4], game.enemy_units[:4]):
                    result = game.handle_player_turn()
                    if result == "menu":
                        game.running = False
                        break

                    result = game.check_end_game()
                    if result == "menu":
                        game.running = False
                        break

                    result = game.handle_enemy_turn()
                    if result == "menu":
                        game.running = False
                        break

                    # Mélanger le terrain tous les 8 tours
                if game.tour % 2 == 0:
                    game.terrain.melanger()




if __name__ == "__main__":
    main()
