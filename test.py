import pyxel

# Initialize global variables
x = 80  
y = 60
tirs = []  # Initialize empty list for shots

def vaisseau_deplacement(x, y):
    if pyxel.btn(pyxel.KEY_D) and x < 120:
        x = x + 1
    if pyxel.btn(pyxel.KEY_Q) and x > 0:
        x = x - 1
    if pyxel.btn(pyxel.KEY_S) and y < 120:
        y = y + 1
    if pyxel.btn(pyxel.KEY_Z) and y > 0:
        y = y - 1
    return x, y

def creation_tirs(x, y):
    if pyxel.btnr(pyxel.KEY_SPACE):  # Changed btnr() to btnp()
        return [x, y]
    return None

def move_shots(tirs):
    valid_tirs = []
    for tir in tirs:
        tir[1] = tir[1] - 1
        if tir[1] >= 0:
            valid_tirs.append(tir)
    return valid_tirs

def update():
    global x, y, tirs
    x, y = vaisseau_deplacement(x, y)
    
    # Handle new shots
    nouveau_tir = creation_tirs(x, y)
    if nouveau_tir:
        tirs.append(nouveau_tir)
    
    # Update existing shots
    tirs = move_shots(tirs)

def draw():
    pyxel.cls(0)
    pyxel.blt(x, y, 0, 0, 0, 16, 16, 0)  # Draw ship
    # Draw shots
    for tir in tirs:
        pyxel.rect(tir[0], tir[1], 2, 2, 10)

pyxel.init(160, 120)
pyxel.run(update, draw)
pyxel.load("my_resource.pyxres")