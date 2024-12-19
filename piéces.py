import pyxel
def update():
    pass

def draw():
    #ddfg
    pyxel.cls(0)
    pyxel.blt(80, 60, 1, 0, 0, 16, 16, 0)
    
    
    
pyxel.init(160, 120)
pyxel.load("my_resource.pyxres")
pyxel.run(update, draw)