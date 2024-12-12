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

        # Si la vie est inférieure à 100, chercher une case cœur
        if enemy.vie < 100:
            closest_heart = self.find_closest_case(enemy, accessible_cells, case_type=3)
            if closest_heart:
                self.move_to_cell(enemy, closest_heart)
                return True  # Une action a été effectuée

        # Trouver l'unité alliée la plus proche
        closest_player_unit = self.find_closest_unit(enemy, self.game.player_units)

        if closest_player_unit:
            # Calculer la distance à l'unité alliée la plus proche
            distance = abs(enemy.x - closest_player_unit.x) + abs(enemy.y - closest_player_unit.y)

            if self.should_attack(enemy, closest_player_unit):
                # Si l'ennemi est en position de force, il attaque
                self.attack(enemy, closest_player_unit)
            elif distance <= enemy.range and enemy.vie > 30:
                # Si dans la portée d'attaque et santé suffisante, attaque
                self.attack(enemy, closest_player_unit)
            elif enemy.vie < 30:
                # Si la santé est faible, s'éloigner
                self.move_away(enemy, closest_player_unit, accessible_cells)
            else:
                # Sinon, se rapprocher tout en évitant l'herbe
                self.move_towards(enemy, closest_player_unit, accessible_cells)

        # Passer à l'unité ennemie suivante
        self.current_enemy_index = (self.current_enemy_index + 1) % len(self.game.enemy_units)
        return True  # Une action a été effectuée

    def find_closest_unit(self, enemy, player_units):
        """Trouve l'unité alliée la plus proche d'une unité ennemie."""
        closest_unit = None
        min_distance = float('inf')

        for player_unit in player_units:
            distance = abs(enemy.x - player_unit.x) + abs(enemy.y - player_unit.y)
            if distance < min_distance:
                min_distance = distance
                closest_unit = player_unit

        return closest_unit

    def find_closest_case(self, enemy, accessible_cells, case_type):
        """
        Trouve la case la plus proche d'un type spécifique (cœur, etc.).

        Args:
            enemy (Type_Unite): L'unité ennemie.
            accessible_cells (list): Liste des cases accessibles.
            case_type (int): Type de la case à chercher.

        Returns:
            tuple: Coordonnées de la case la plus proche.
        """
        closest_case = None
        min_distance = float('inf')

        for cell in accessible_cells:
            x, y = cell
            if self.game.terrain.cases[x][y].type_case == case_type:
                distance = abs(enemy.x - x) + abs(enemy.y - y)
                if distance < min_distance:
                    min_distance = distance
                    closest_case = cell

        return closest_case

    def should_attack(self, enemy, target):
        """
        Décide si l'ennemi doit attaquer en fonction de la puissance de l'arme et des compétences.
        """
        # Puissance totale de l'ennemi
        enemy_power = enemy.arme.degats if enemy.arme else 0
        if enemy.competences:
            enemy_power += sum(c.effet for c in enemy.competences if isinstance(c.effet, (int, float)))

        # Puissance totale du joueur
        player_power = target.arme.degats if target.arme else 0
        if target.competences:
            player_power += sum(c.effet for c in target.competences if isinstance(c.effet, (int, float)))

        return enemy_power > player_power

    def move_towards(self, enemy, target, accessible_cells):
        """Déplace l'unité ennemie vers une unité cible tout en évitant les herbes."""
        best_cell = None
        min_distance = float('inf')

        for cell in accessible_cells:
            x, y = cell
            # Vérifier que la case n'est pas de l'herbe (type_case != 2)
            if self.game.terrain.cases[x][y].type_case == 2:
                continue
            distance = abs(x - target.x) + abs(y - target.y)
            if distance < min_distance:
                min_distance = distance
                best_cell = cell

        if best_cell:
            self.move_to_cell(enemy, best_cell)

    def move_to_cell(self, enemy, cell):
        """Déplace une unité ennemie vers une cellule spécifique."""
        enemy.x, enemy.y = cell

    def move_away(self, enemy, target, accessible_cells):
        """Déplace l'unité ennemie pour s'éloigner d'une unité cible."""
        best_cell = None
        max_distance = 0

        for cell in accessible_cells:
            x, y = cell
            # Vérifier que la case n'est pas de l'herbe (type_case != 2)
            if self.game.terrain.cases[x][y].type_case == 2:
                continue
            distance = abs(x - target.x) + abs(y - target.y)
            if distance > max_distance:
                max_distance = distance
                best_cell = cell

        if best_cell:
            self.move_to_cell(enemy, best_cell)

    def attack(self, enemy, target):
        """Fait attaquer une unité ennemie une unité cible."""
        target.vie -= enemy.arme.degats
        if target.vie <= 0:
            self.game.player_units.remove(target)
