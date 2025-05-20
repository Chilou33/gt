import pyxel
min_size = 4  
max_size = 12 
taille = 12
width = 12 * 32
height = 5*32+200
pyxel.init(width,height,title="PYTHOMINOES",display_scale=2,fps=30)
class App:
    def __init__(self, page_affichée):
        self.contenu_fenetre = page_affichée
        
        pyxel.run(self.update, self.draw)

    def update(self):
        self.contenu_fenetre.update()

    def draw(self):
        self.contenu_fenetre.draw()

class Plateau:
    def __init__(self, taille: int):
        self.taille = taille
        self.clear = self.plateau_clear()

    def plateau_clear(self):
        plateau = [[0 for _ in range(self.taille)] for _ in range(5)]
        return plateau

plateau = Plateau(taille).clear 

class parametre:
    def __init__(self):
        self.taille = 12 
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.taille < max_size:
            self.taille += 1
        elif pyxel.btnp(pyxel.KEY_LEFT) and self.taille > min_size:
            self.taille-= 1
        if pyxel.btnp(pyxel.KEY_J): 
            App(parametre())

    def draw(self):
        pyxel.cls(0) 
        screen_width = pyxel.width
        screen_height = pyxel.height
        square_size = 10  # Taille des carrés
        espace_size= 1
        total_height = 4 * square_size 
        start_x = (screen_width - square_size*taille) // 2
        start_y = (screen_height - total_height) // 2
        for i in range(self.taille):
            x = start_x + i * square_size + i*espace_size
            for i in range(4):
                y = start_y + i * square_size + i*espace_size
                pyxel.rect(x, y, square_size, square_size, 16)  # Couleur 9 (bleu clair)

# Properly initialize the application with the parametre class
App(parametre())