import pygame
from terain import * # Vérifiez que 'terain' est bien importé, cela semble être une faute de frappe pour 'terrain'
from unit import *
from game import *
from Competence import *



# Constantes globales
WIDTH = 15 * 40  # Largeur de la fenêtre (15 cases de 50 pixels)
HEIGHT = 15 * 40  # Hauteur de la fenêtre (15 cases de 50 pixels)
TABLEAU_HEIGHT = 100  # Hauteur du tableau d'affichage en bas
CELL_SIZE = 40  # Taille de chaque case (50x50 pixels)
CREAM = (245, 245, 220)  # Couleur crème pour l'arrière-plan
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NUM_COLUMNS = 15 
NUM_ROWS = 15

# Taille des images des unités
UNIT_IMAGE_SIZE = (40, 40)  # Taille redimensionnée des images (40x40 pixels)



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
                    
        


def menu(screen):
    """Affiche le menu principal et permet de naviguer avec la souris."""
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    start_button = pygame.Rect(WIDTH // 3, HEIGHT // 4 + 100, 200, 50)
    settings_button = pygame.Rect(WIDTH // 3, HEIGHT // 4 + 160, 200, 50)
    exit_button = pygame.Rect(WIDTH // 3, HEIGHT // 4 + 220, 200, 50)

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
            game = Game (screen)  # Utilise Affichage ici
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
                if game.tour  == 0:  # Si c'est un tour impair, c'est à l'IA de jouer
                    game.handle_enemy_turn()
                if game.tour  == 1:  # Si c'est un tour pair, c'est au joueur de jouer
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
