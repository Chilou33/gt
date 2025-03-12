import pyxel

class KataminoBoard:
    def __init__(self, board, cell_size=50):
        self.board = board
        self.cell_size = cell_size
        self.ligne = len(board)
        self.cols = len(board[0]) if self.ligne > 0 else 0
        

        width = self.cols * cell_size
        height = self.ligne * cell_size
        pyxel.init(width, height, title="Katamino Board")
        

        self.colors = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        
        pyxel.run(self.update, self.draw)
    
    def update(self):

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
    def draw(self):

        pyxel.cls(7) 
        

        for y in range(self.ligne):
            for x in range(self.cols):
                value = self.board[y][x]
                if value > 0:

                    color = self.colors[value % len(self.colors)]

                    pyxel.rect(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                        color
                    )
                

                pyxel.rectb(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                    0 )



plateau1=  [[0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

KataminoBoard(plateau1)