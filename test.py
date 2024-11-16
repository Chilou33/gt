import pyxel

# Initialize global variables for ship position
x = 80  # middle of screen horizontally
y = 60  # middle of screen vertically

def vaisseau_deplacement(x, y):
    """prend en paramètres les valeurs des variables x et y 
    et renvoie les valeurs des variables x et y modifiées 
    suivant certaines touches du clavier."""
    # déplacement avec les touches de directions :
    if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
        if x < 120:
            x = x + 1  # 1 pixel vers la droite
    if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT):
        if x > 0:
            x = x - 1  # 1 pixel vers la gauche
    if pyxel.btn(pyxel.KEY_S) or  pyxel.btn(pyxel.KEY_DOWN):
        if y < 120:
            y = y + 1  # 1 pixel vers le bas
    if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP):
        if y > 0:
            y = y - 1  # 1 pixel vers le haut
    return x, y

def update():
    global x, y
    x, y = vaisseau_deplacement(x, y)

def draw():
    pyxel.cls(0)
    # Assuming sprite is 16x16 pixels
    pyxel.blt(x, y, 0, 0, 0, 16, 16, 0)

# Initialize Pyxel with window size
pyxel.init(160, 120)
# Load the resource file (you need to create a .pyxres file)
pyxel.load("my_resource.pyxres")
# Start the game loop
pyxel.run(update, draw)