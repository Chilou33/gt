# Pythominoes

## 📝 Description du projet

Pythominoes est une implémentation en Python du jeu de puzzle Katamino. Dans ce jeu, les joueurs doivent placer stratégiquement différentes pièces de pentomino sur un plateau rectangulaire. Le projet utilise le moteur de jeu Pyxel pour créer une interface graphique rétro.

## 🎮 Fonctionnalités

* **Jeu de base Katamino** : Règles fondamentales du Katamino avec plusieurs pentominos
* **Mode Campagne** : Séries de niveaux de difficulté progressive
* **Interface graphique rétro** : Utilisation de Pyxel pour un style visuel 8-bit nostalgique
* **Mouvements de pièces** : Déplacement et rotation des pièces sur le plateau
* **Interface utilisateur intuitive** : Menu d'accueil simple et fonctionnel

## 💻 Prérequis

* Python 3.6 ou version ultérieure
* Pyxel (moteur de jeu rétro)
* Pygame (pour l'écran d'accueil)

## 🎲 Comment jouer

1. Lancez le jeu depuis l'écran d'accueil
2. Sélectionnez une pièce à placer sur le plateau
3. Utilisez les touches directionnelles pour déplacer la pièce:
   * `G`: Déplacer vers la gauche
   * `D`: Déplacer vers la droite
   * `H`: Déplacer vers le haut
   * `B`: Déplacer vers le bas
4. Utilisez la touche d'espace pour faire pivoter la pièce
5. Complétez le puzzle en remplissant le plateau

## 🧩 Fonctions principales

* [place(piece)](vscode-file://vscode-app/c:/Users/achil/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html): Place une pièce sur le plateau
* [deplacement(sens, norme, piece)](vscode-file://vscode-app/c:/Users/achil/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html): Déplace une pièce dans une direction donnée
* [rotation(plateau)](vscode-file://vscode-app/c:/Users/achil/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html): Fait pivoter une pièce sur le plateau
* [convert_piece(piece)](vscode-file://vscode-app/c:/Users/achil/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html): Convertit une définition de pièce en coordonnées utilisables

## 📊 Classes

### Classe [Piece](vscode-file://vscode-app/c:/Users/achil/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)

Représente une pièce du jeu avec:

* Numéro d'identification
* Patron (modèle) de la pièce
* Coordonnées calculées à partir du patron
* Représentation sur un plateau

## 🛣️ Plan de développement

* [X] Définition des pièces de base
* [X] Logique de déplacement et rotation
* [X] Interface utilisateur basique
* [ ] Conception des niveaux complets
* [ ] Système de score
* [ ] Mode multijoueur (envisagé)
* [ ] Effets sonores et musique

## 👥 Contributeurs

* Camille
* Achille
* Léandre
* Gabriel
