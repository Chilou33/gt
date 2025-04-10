import pyxel  # Importer la bibliothèque Pyxel pour créer le jeu

# Paramètres du jeu
SCREEN_WIDTH = 360  # Largeur de la fenêtre de jeu (en pixels)
SCREEN_HEIGHT = 320  # Hauteur de la fenêtre de jeu (en pixels)
BACKGROUND_COLOR = 0  # Couleur de fond de l'écran (0 = noir en Pyxel)

# Paramètres des boutons
quit_button_color = 7  # Couleur normale du bouton "Quit" (gris clair en Pyxel)
quit_button_hover_color = 8  # Couleur du bouton "Quit" lorsque la souris est dessus (gris plus foncé)
quit_button_text_color = 7  # Couleur du texte sur le bouton "Quit" (blanc en Pyxel)
quit_button_height = 20  # Hauteur du bouton "Quit"
quit_button_width = 60  # Largeur du bouton "Quit"
quit_button_x = SCREEN_WIDTH // 2 - quit_button_width // 2  # Position X du bouton "Quit" (centré horizontalement)
quit_button_y = SCREEN_HEIGHT // 2 - quit_button_height // 2 - 100  # Position Y du bouton "Quit" (centré verticalement mais décalé vers le haut)

play_button_color = 7  # Couleur normale du bouton "Play" (gris clair en Pyxel)
play_button_hover_color = 8  # Couleur du bouton "Play" lorsque la souris est dessus (gris plus foncé)
play_button_text_color = 7  # Couleur du texte sur le bouton "Play" (blanc en Pyxel)
play_button_height = 20  # Hauteur du bouton "Play"
play_button_width = 60  # Largeur du bouton "Play"
play_button_x = SCREEN_WIDTH // 2 - play_button_width // 2  # Position X du bouton "Play" (centré horizontalement)
play_button_y = SCREEN_HEIGHT // 2 - play_button_height // 2  # Position Y du bouton "Play" (centré verticalement)

# Variables de jeu
button_hover = None  # Variable pour stocker quel bouton est survolé (initialement aucun)
action_taken = False  # Variable pour indiquer si l'action "Play" a été prise

# Initialisation de Pyxel
def init():  # Fonction pour initialiser Pyxel
    pyxel.init(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

# Fonction pour dessiner un bouton
def draw_button(x, y, width, height, color, hover_color, text, text_color):
    if button_hover == (x, y):  # Si la souris est sur ce bouton
        pyxel.rect(x, y, width, height, hover_color)  # Dessiner le bouton avec la couleur de survol
    else:
        pyxel.rect(x, y, width, height, color)  # Sinon, dessiner avec la couleur normale
    
    pyxel.rect(x, y, width, height, 0)  # Dessiner le contour du bouton (couleur 0 = noir en Pyxel)

    # Afficher le texte du bouton centré
    pyxel.text(x + (width - len(text) * 4) // 2, y + (height - 8) // 2, text, text_color)  # Afficher le texte centré dans le bouton

# Fonction pour mettre à jour les événements
def update():
    global button_hover, action_taken  # Déclarer ces variables comme globales pour pouvoir les modifier

    mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y  # Obtenir la position actuelle de la souris

    # Vérifier si la souris survole le bouton "Quit"
    if (quit_button_x <= mouse_x <= quit_button_x + quit_button_width and
        quit_button_y <= mouse_y <= quit_button_y + quit_button_height):
        button_hover = (quit_button_x, quit_button_y)  # Mettre à jour la variable pour signaler que le bouton "Quit" est survolé
    # Vérifier si la souris survole le bouton "Play"
    elif (play_button_x <= mouse_x <= play_button_x + play_button_width and
          play_button_y <= mouse_y <= play_button_y + play_button_height):
        button_hover = (play_button_x, play_button_y)  # Mettre à jour la variable pour signaler que le bouton "Play" est survolé
    else:
        button_hover = None  # Si la souris n'est sur aucun bouton, réinitialiser

    # Vérifier si un clic de souris gauche a eu lieu
    if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
        if button_hover == (quit_button_x, quit_button_y):  # Si l'utilisateur a cliqué sur le bouton "Quit"
            pyxel.quit()  # Quitter le jeu
        elif button_hover == (play_button_x, play_button_y):  # Si l'utilisateur a cliqué sur le bouton "Play"
            action_taken = True  # Marquer que l'action "Play" a été prise
            print("Play")  # Afficher "Play" dans la console

# Fonction pour dessiner les éléments à l'écran
def draw():
    pyxel.cls(BACKGROUND_COLOR)  # Effacer l'écran avec la couleur de fond (noir)

    # Afficher le titre du jeu au centre
    pyxel.text(SCREEN_WIDTH // 2 - 35, 10, "Pytominoes", 7)  # Texte en blanc (couleur 7)

    # Dessiner les boutons "Quit" et "Play"
    draw_button(quit_button_x, quit_button_y, quit_button_width, quit_button_height,
                quit_button_color, quit_button_hover_color, "Quit", quit_button_text_color)
    draw_button(play_button_x, play_button_y, play_button_width, play_button_height,
                play_button_color, play_button_hover_color, "Play", play_button_text_color)

# Initialisation et lancement du jeu
init()  # Appeler la fonction d'initialisation de Pyxel

# Boucle principale du jeu
def game_loop():
    while True:  # La boucle continue tant que le jeu est en cours
        update()  # Mettre à jour les événements (vérification des clics et de la souris)
        draw()  # Dessiner tous les éléments du jeu (boutons, titre, etc.)
        pyxel.flip()  # Mettre à jour l'affichage de la fenêtre
        pyxel.sleep(16)  # Pause pour ralentir la boucle et viser 30 FPS (frames par seconde)

# Lancer le jeu
game_loop()  # Appeler la boucle principale du jeu pour démarrer le jeu
