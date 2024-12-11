class EnemyAI:
    def __init__(self, game):
        self.game = game
        self.current_enemy_index = 0  # Index pour suivre quelle unité ennemie agit

    def play_turn(self):
        """
        Fait jouer un tour à une seule unité ennemie.
        """
        if not self.game.enemy_units:  # Si aucune unité ennemie n'est disponible
            return False  # Aucun tour joué

        # Récupérer l'unité ennemie qui doit jouer ce tour
        enemy = self.game.enemy_units[self.current_enemy_index]

        # Trouver les cases accessibles
        accessible_cells = self.game.get_accessible_cells(enemy)

        # Trouver l'unité alliée la plus proche
        closest_player_unit = self.find_closest_unit(enemy, self.game.player_units)

        if closest_player_unit:
            # Calculer la distance à l'unité alliée la plus proche
            distance = abs(enemy.x - closest_player_unit.x) + abs(enemy.y - closest_player_unit.y)

            if distance <= enemy.range:  # Si l'ennemi peut attaquer
                self.attack(enemy, closest_player_unit)
                self.current_enemy_index = (self.current_enemy_index + 1) % len(self.game.enemy_units)
                return True  # Une action a été effectuée
            else:  # Sinon, se déplacer pour se rapprocher
                self.move_towards(enemy, closest_player_unit, accessible_cells)
                self.current_enemy_index = (self.current_enemy_index + 1) % len(self.game.enemy_units)
                return True  # Une action a été effectuée

        # Si aucune action n'a été effectuée
        self.current_enemy_index = (self.current_enemy_index + 1) % len(self.game.enemy_units)
        return False


    def find_closest_unit(self, enemy, player_units):
        """
        Trouve l'unité alliée la plus proche d'une unité ennemie.

        Args:
            enemy (Type_Unite): L'unité ennemie.
            player_units (list): Liste des unités du joueur.

        Returns:
            Type_Unite: L'unité alliée la plus proche.
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
        Déplace l'unité ennemie vers une unité cible.

        Args:
            enemy (Type_Unite): L'unité ennemie.
            target (Type_Unite): L'unité cible.
            accessible_cells (list): Liste des cases accessibles pour l'ennemi.
        """
        best_cell = None
        min_distance = float('inf')

        for cell in accessible_cells:
            distance = abs(cell[0] - target.x) + abs(cell[1] - target.y)
            if distance < min_distance:
                min_distance = distance
                best_cell = cell

        if best_cell:
            enemy.x, enemy.y = best_cell  # Déplace l'unité ennemie
            print(f"L'unité ennemie s'est déplacée vers {best_cell}.")

    def attack(self, enemy, target):
        """
        Fait attaquer une unité ennemie une unité cible.

        Args:
            enemy (Type_Unite): L'unité ennemie.
            target (Type_Unite): L'unité cible.
        """
        if not hasattr(enemy, "attaque") or not isinstance(enemy.attaque, int):
            print(f"Erreur : l'unité {enemy.nom} n'a pas d'attribut 'attaque' valide.")
            return

        target.vie -= enemy.attaque  # Réduire la vie de l'unité cible
        print(f"L'unité ennemie attaque {target.nom} pour {enemy.attaque} dégâts.")
        if target.vie <= 0:
            self.game.player_units.remove(target)
            print(f"L'unité {target.nom} a été éliminée.")
