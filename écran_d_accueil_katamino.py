import pyxel

# Paramètres du jeu
screen_width = 160
screen_height = 120
background_color = 7  # Fond d'écran blanc

# Fonction pour dessiner le titre du jeu
def draw_title():
    pyxel.text(63, 30, "PYTHOMINO", pyxel.COLOR_YELLOW)
    pyxel.text(50, 50, "Press [ENTER] to Start", pyxel.COLOR_WHITE)

# Fonction pour dessiner un bouton "START"
def draw_button():
    pyxel.rect(50, 70, 60, 20, pyxel.COLOR_RED)
    pyxel.text(70, 74, "START", pyxel.COLOR_WHITE)

# Fonction de mise à jour du jeu (entrée utilisateur)
def update():
    if pyxel.btnp(pyxel.KEY_RETURN):  # Utilise KEY_RETURN pour détecter Enter
        launch_game()  # Lance le jeu ou l'éditeur

# Fonction pour lancer le jeu ou l'éditeur
def launch_game():
    print("Le jeu commence !")
    # Code pour démarrer le jeu
    # Par exemple, afficher un personnage à l'écran.

# Fonction de dessin (affiche l'écran d'accueil)
def draw():
    pyxel.cls(background_color)  # Efface l'écran avec la couleur de fond
    draw_title()  # Dessine le titre
    draw_button()  # Dessine le bouton "START"
    
    # Dessiner un personnage à partir d'un sprite
    # Utilise le numéro d'index de ton sprite, supposons que ton personnage est à l'index 0
    pyxel.blt(50, 70, 0, 0, 0, 60, 20)  # Affiche le sprite à la position (50, 40)

# Initialisation de Pyxel
pyxel.init(screen_width, screen_height, title="Katamino Game", fps=30)

# Charger les sprites du fichier Pyxel
pyxel.load("my_resource.pyxres")  # Remplace par le chemin de ton fichier Pyxel

# Lancer le jeu
pyxel.run(update, draw)
