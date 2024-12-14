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

        # Zone de protection et régénération
        for ally in self.game.enemy_units:
            if ally != enemy:
                distance = abs(enemy.x - ally.x) + abs(enemy.y - ally.y)
                if distance <= 2:  # Zone de protection
                    if enemy.vie < 0.5 * 100:
                        enemy.vie += 10  # Régénérer
                        return True

        # Gestion des compétences
        if enemy.competences:
            for competence in enemy.competences:
                if competence.nom == "Soin" and enemy.vie < 0.3 * 100:
                    competence.appliquer(enemy)  # Appliquer une compétence
                    return True

        # Trouver une cible prioritaire
        priority_target = self.find_priority_target(enemy, self.game.player_units)
        if priority_target:
            self.attack(enemy, priority_target)
            return True

        # Trouver l'unité alliée la plus proche
        closest_player_unit = self.find_closest_unit(enemy, self.game.player_units)

        if closest_player_unit:
            distance = abs(enemy.x - closest_player_unit.x) + abs(enemy.y - closest_player_unit.y)
            if distance <= enemy.range and enemy.vie > 30:
                self.attack(enemy, closest_player_unit)
            elif enemy.vie < 30:
                self.move_away(enemy, closest_player_unit, accessible_cells)
            else:
                self.move_towards(enemy, closest_player_unit, accessible_cells)

        # Passer à l'unité ennemie suivante
        self.current_enemy_index = (self.current_enemy_index + 1) % len(self.game.enemy_units)
        return True  # Une action a été effectuée

    def find_priority_target(self, enemy, player_units):
        """Trouve une cible prioritaire parmi les unités joueur."""
        priority_target = None
        min_health = float('inf')

        for player_unit in player_units:
            distance = abs(enemy.x - player_unit.x) + abs(enemy.y - player_unit.y)
            if distance <= enemy.range and player_unit.vie < min_health:
                min_health = player_unit.vie
                priority_target = player_unit

        return priority_target

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

    def move_towards(self, enemy, target, accessible_cells):
        """Déplace l'unité ennemie vers une unité cible tout en évitant les herbes."""
        best_cell = None
        min_distance = float('inf')

        for cell in accessible_cells:
            x, y = cell
            # Vérifier que la case n'est pas occupée par un joueur
            if any(u.x == x and u.y == y for u in self.game.player_units):
                continue
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
            # Vérifier que la case n'est pas occupée par un joueur
            if any(u.x == x and u.y == y for u in self.game.player_units):
                continue
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
        else:
            # Après une attaque, essayer de s'éloigner
            accessible_cells = self.game.get_accessible_cells(enemy)
            self.move_away(enemy, target, accessible_cells)
