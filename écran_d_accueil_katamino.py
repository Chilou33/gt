import pyxel

# Paramètres du jeu
screen_width = 160
screen_height = 120
background_color = 7  # Fond d'écran blanc


def update():
    pyxel.mouse(True)
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        mouse_x = pyxel.mouse_x
        mouse_y = pyxel.mouse_y
        if 50 <= mouse_x <= 110 and 70 <= mouse_y <= 90:
            pyxel.quit()



# Fonction de dessin (affiche l'écran d'accueil)
def draw():
    pyxel.cls(background_color)  # Efface l'écran avec la couleur de fond
    pyxel.text(55, 10, "Phytominoes", 2)  # Affiche le titre du jeu
    pyxel.blt(50, 70, 0, 0, 0, 60, 20)  # Affiche le sprite à la position (50, 40)

# Initialisation de Pyxel
pyxel.init(screen_width, screen_height, title="Phytominoes", fps=30)

# Charger les sprites du fichier Pyxel
pyxel.load("my_resource.pyxres")  # Remplace par le chemin de ton fichier Pyxel

# Lancer le jeu
pyxel.run(update, draw)
