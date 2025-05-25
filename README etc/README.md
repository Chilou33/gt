# Pythominoes

## 📝 Description du projet

Pythominoes est une implémentation en Python du jeu de puzzle Katamino. Les joueurs placent stratégiquement des pièces de pentomino sur un plateau rectangulaire. Le projet utilise le moteur de jeu Pyxel pour une interface graphique rétro.

## 🎮 Fonctionnalités

* **Jeu de base Katamino**: Règles fondamentales avec divers pentominos.
* **Modes de Jeu**:
  * **Mode Libre**: Permet de choisir le nombre de pièces pour résoudre le puzzle.
  * **Mode Grand Chelem**: Une série de niveaux prédéfinis (A à L) avec des ensembles de pièces spécifiques pour chaque niveau, offrant une difficulté progressive.
* **Interface Graphique Rétro**: Style visuel 8-bit nostalgique grâce à Pyxel.
* **Mouvements de Pièces Intuitifs**: Déplacement (haut, bas, gauche, droite), rotation et symétrie des pièces.
* **Gestion de la Progression**:
  * Sauvegarde et chargement des parties en cours.
  * Navigation entre les étapes d'un niveau.
* **Interface Utilisateur Complète**:
  * Menu principal avec options pour démarrer une nouvelle partie ou charger une partie sauvegardée.
  * Écran de sélection du mode de jeu (Libre ou Grand Chelem).
  * Écran de sélection des pièces (pour le mode libre).
  * Affichage clair du plateau de jeu et des pièces.
  * Écrans de victoire et de fin de partie.
* **Personnalisation**: Options pour activer/désactiver la musique et les effets sonores (fonctionnalité prévue).

## 💻 Prérequis

* Python 3.6 ou version ultérieure
* Pyxel (moteur de jeu rétro)

## 🎲 Comment jouer

1. **Lancer le jeu**: Exécutez le script principal.
2. **Menu Principal**:
   * Appuyez sur `Entrée` pour démarrer une nouvelle partie.
   * Appuyez sur `D` pour charger une partie sauvegardée.
3. **Choix du Mode**:
   * Sélectionnez "Mode Libre" ou "Mode Grand Chelem".
   * En Mode Grand Chelem, sélectionnez le niveau (A à L).
   * En Mode Libre, choisissez le nombre de pièces.
4. **Sélection des Pièces (Mode Libre)**:
   * Utilisez `Gauche`/`Droite` pour naviguer entre les pièces disponibles.
   * Appuyez sur `S` pour sélectionner/désélectionner une pièce.
   * Appuyez sur `Entrée` pour commencer à jouer avec les pièces choisies.
5. **Sur le Plateau de Jeu**:
   * **Sélectionner une pièce**: Cliquez sur l'icône de la pièce ou utilisez les touches `A` (précédente) / `E` (suivante).
   * **Déplacer la pièce active**:
     * Touches directionnelles (`Haut`/`Bas`/`Gauche`/`Droite`) ou `Z`/`S`/`Q`/`D`.
   * **Rotation**: Touche `R` ou `Espace`.
   * **Symétrie**: Touche `M`.
   * **Placer la pièce**: Touche `P`.
   * **Retirer la pièce active**: Touche `W`.
   * **Menu rapide/Pause**: Touche `G`.
   * **Sauvegarder la partie**: Via le menu rapide.
6. **Objectif**: Remplir complètement la zone de jeu définie par l'étape actuelle du niveau.
7. **Fin de partie**: Un écran de victoire s'affiche lorsque le puzzle est résolu. En mode Grand Chelem, vous progressez au niveau suivant.

## 🛠️ Structure du Code (Classes Principales)

* `App`: Gère le lancement et le cycle de vie de l'application Pyxel.
* `MainMenu`: Gère l'écran d'accueil et la navigation initiale.
* `Choix_du_mode_et_niveaux`: Permet de sélectionner le mode de jeu (Libre, Grand Chelem) et le niveau.
* `EcranChoixPieces`: Interface pour la sélection des pièces en mode libre.
* `Plateau_de_jeu`: Représente l'aire de jeu principale, gère la logique de placement des pièces, la vérification de victoire, la sauvegarde/chargement.
* `Piece`: Définit une pièce de pentomino, ses rotations, sa symétrie, et ses interactions avec le plateau.
* `Plateau`: Structure de données représentant l'état du plateau de jeu.
* `Ecran_de_victoire`: S'affiche lorsque le joueur réussit un niveau.
* `Ecran_de_fin`: S'affiche à la complétion de tous les niveaux du Grand Chelem ou d'une partie en mode libre.

## 🧩 Fonctions Clés (Exemples)

* `Plateau_de_jeu.verif_victoire()`: Vérifie si le plateau est complété.
* `Plateau_de_jeu.update()`: Gère les entrées utilisateur et la logique du jeu.
* `Piece.place_on_plateau()`: Tente de placer une pièce sur le plateau.
* `Piece.rotate()`: Fait pivoter la pièce.
* `Piece.symetrie()`: Applique une symétrie à la pièce.
* `sauvegarde.save_game_file()` / `load_game_file()`: Gèrent la persistance des données du jeu.

## 🛣️ Plan de développement

* [X] Définition des pièces de base et de leurs formes.
* [X] Logique de déplacement, rotation et symétrie des pièces.
* [X] Interface utilisateur graphique (menus, écrans de jeu, etc.).
* [X] Modes de jeu : Libre et Grand Chelem.
* [X] Système de sélection des pièces par niveau/étape.
* [X] Système de sauvegarde et chargement de la progression.
* [X] Conception des niveaux du Grand Chelem.
* [ ] Système de temps (envisagé).
* [ ] Effets sonores et musique (implémentation partielle, à finaliser).
* [ ] Mode multijoueur (envisagé pour le futur).

## 👥 Contributeurs

* Camille
* Achille
* Léandre
* Gabriel
