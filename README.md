# Jeu de Tactique Tour par Tour en 2D

## Description
Ce projet est un jeu de tactique tour par tour en 2D développé en Python avec la bibliothèque Pygame. Les joueurs contrôlent des unités avec des caractéristiques et des compétences spécifiques sur un terrain composé de différentes cases aux propriétés variées. Le but est d'éliminer toutes les unités adverses.

## Fonctionnalités Principales
1. **Contrôle des Unités :**
   - Chaque joueur contrôle plusieurs unités avec des statistiques spécifiques : points de vie, attaque, défense, vitesse, etc.
   - Chaque unité dispose de compétences uniques (ex. : soin, bouclier protecteur, poison).

2. **Gestion du Terrain :**
   - Terrain sous forme de grille 2D, avec différents types de cases :
     - Obstacles : non traversables.
     - Herbes : réduisent les points de vie.
     - Cases de soin : restaurent les points de vie.
     - Cases de protection : empêchent de recevoir des dégâts.
     - Trous : déplacent les unités de manière aléatoire.

3. **Système de Combat :**
   - Les unités peuvent attaquer avec des armes (épée, arc, lance, bombe).
   - Calcul des dégâts basé sur les statistiques des unités et des compétences.
   - Effets de zone pour certaines compétences, comme la bombe.

4. **Intelligence Artificielle (IA) :**
   - Les ennemis contrôlés par l'IA peuvent se déplacer stratégiquement et attaquer les unités du joueur.
   - L'IA utilise des algorithmes pour choisir les cibles et éviter les cases dangereuses.

5. **Interface Graphique :**
   - Menu interactif avec sélection des modes de jeu (solo, multijoueur).
   - Affichage des unités, terrain et informations (barre de vie, messages).
   - Effets visuels pour les compétences et les déplacements.

6. **Musique et Sons :**
   - Musique de fond et effets sonores pour les actions clés (attaque, soin, etc.).


