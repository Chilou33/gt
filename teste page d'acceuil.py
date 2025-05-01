import pyxel

class KataminoGame:
    def __init__(self):
        pyxel.init(160, 120, title="Katamino")
        self.start_game = False
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.start_game = True

    def draw(self):
        pyxel.cls(0)
        if not self.start_game:
            # Title
            pyxel.text(50, 40, "KATAMINO", pyxel.frame_count % 16)
            # Instructions
            pyxel.text(30, 70, "Press ENTER to Start", 7)
        else:
            # Placeholder for game screen
            pyxel.text(50, 50, "Game Starting...", 7)

KataminoGame()