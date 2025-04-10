import pyxel 

class PageAccueil:
    def __init__(self):
        pyxel.init(160, 120, title="Page d'Accueil")
        self.message = "Bienvenue sur Katamino!"
        pyxel.run(self.update, self.draw)  # Lancer la boucle principale de Pyxel, qui appelle 'update' et 'draw' en boucle

    def update(self):  # Fonction pour mettre à jour les événements du jeu
        if self.page == "accueil":
            if pyxel.btnp(pyxel.KEY_Q):  # Si la touche 'Q' est pressée
              pyxel.quit()  # Quitter le programme
            if pyxel.btnp(pyxel.KEY_ENTER):  # Appuyer sur 'ENTER' pour changer de page
              self.page = "jeu"

    def draw(self):   # Fonction pour dessiner les éléments à l'écran
        pyxel.cls(0)  # Efface l'écran avec la couleur noire (0 correspond au noir dans Pyxel)
        pyxel.text(40, 50, self.message, pyxel.frame_count % 16)  # Afficher le message "Bienvenue sur Katamino!" à la position (40, 50), avec une couleur qui change selon le nombre de frames
        pyxel.text(30, 90, "Q pour quitter", 7)  # Afficher un message d'instruction à la position (30, 90) avec la couleur blanche (7)
        pyxel.text()

# Lancer la page d'accueil en créant une instance de la classe PageAccueil
PageAccueil()
class PageJeu:
    def __init__(self):
        pyxel.init(160, 120, title="Page de Jeu")
        self.message = "Bienvenue dans le jeu!"
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.page == jeu :
            if pyxel.btnp(pyxel.KEY_Q):
              pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(40, 50, self.message, pyxel.frame_count % 16)
        pyxel.text(30, 90, "Appuyez sur Q pour quitter", 7)

class Application:
    def __init__(self):
        self.page = "accueil"
        pyxel.init(160, 120, title="Katamino")
        pyxel.run(self.update, self.draw)

Application()