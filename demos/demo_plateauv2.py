import pyxel

class KataminoBoard:
    def __init__(self, board, cell_size=30):
        self.board = board
        self.cell_size = cell_size
        self.ligne = len(board)
        self.cols = len(board[0]) if self.ligne > 0 else 0

        width = self.cols * cell_size
        height = self.ligne * cell_size
        pyxel.init(width, height, title="Katamino Board")

        self.colors = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        self.piece = Piece(1, [[1, 1], [1], [1], [1]], self.board)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_P):
            self.board = self.piece.place_on_plateau()
        if pyxel.btnp(pyxel.KEY_R):
            self.board = self.piece.rotate()
        if pyxel.btnp(pyxel.KEY_E):
            self.board = self.piece.symetrie()
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.board = self.piece.deplacement(-1, 0)
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.board = self.piece.deplacement(1, 0)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.board = self.piece.deplacement(0, 1)
        if pyxel.btnp(pyxel.KEY_UP):
            self.board = self.piece.deplacement(0, -1)
        

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
                    0
                )

class Piece:
    def __init__(self, numero, patron, plateau):
        self.numero = numero
        self.patron = patron
        self.plateau = plateau
        self.actual_coordinates = self.convert_to_coordinates()

    def convert_to_coordinates(self):
        coordinates = []
        for i, row in enumerate(self.patron):
            for j, val in enumerate(row):
                if val != 0:
                    coordinates.append([i, j])
        return coordinates

    def place_on_plateau(self):
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]):
                self.plateau[x][y] = self.numero
        return self.plateau

    def deplacement(self, dy, dx):
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]):
                self.plateau[x][y] = 0

        new_coordinates = []
        for x, y in self.actual_coordinates:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.plateau) and 0 <= new_y < len(self.plateau[0]):
                new_coordinates.append([new_x, new_y])
        if len(new_coordinates) == len(self.actual_coordinates):
            self.actual_coordinates = new_coordinates

        return self.place_on_plateau()

    def rotate(self):
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]):
                self.plateau[x][y] = 0

        if self.numero in [6, 8]:
            self.rotation_anchor = self.actual_coordinates[1]
        if self.numero in [1, 2, 3, 4, 5, 7, 9, 10, 11, 12]:
            self.rotation_anchor = self.actual_coordinates[2]

        anchor_x = self.rotation_anchor[0]
        anchor_y = self.rotation_anchor[1]

        translated_coordinates = [[x - anchor_x, y - anchor_y] for x, y in self.actual_coordinates]
        rotated_coordinates = [[y, -x] for x, y in translated_coordinates]
        final_coordinates = [[x + anchor_x, y + anchor_y] for x, y in rotated_coordinates]

        if all(0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]) for x, y in final_coordinates):
            self.actual_coordinates = final_coordinates

        return self.place_on_plateau()

    def symetrie(self):
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]):
                self.plateau[x][y] = 0

        # Find the maximum y-coordinate
        max_y = max(y for x, y in self.actual_coordinates)

       
        symetrie_coordinates = [[x, max_y - y] for x, y in self.actual_coordinates]

        min_y = min(y for x, y in self.actual_coordinates)
        decalage = min_y - min(y for x, y in symetrie_coordinates)

        symetrie_coordinates = [[x, y + decalage] for x, y in symetrie_coordinates]

        if all(0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]) for x, y in symetrie_coordinates):
            self.actual_coordinates = symetrie_coordinates

        return self.place_on_plateau()

def create_pieces(plateau):
    piece = [
        Piece(1, [[1, 1],\
                                [1], \
                                [1], \
                                [1]], plateau),\
                                \
        Piece(2, [[0, 2],\
                                [2, 2, 2], \
                                [0, 2]], plateau),\
                                \
        Piece(3, [[3],\
                                [3, 3, 3], \
                                [0, 3]], plateau),\
                                \
        Piece(4, [[4], \
                                [4, 4], \
                                [4, 4]], plateau),\
                                \
        Piece(5, [[5], \
                                [5], \
                                [5, 5, 5]], plateau),\
                                \
        Piece(6, [[6, 6, 6], \
                                [0, 6], \
                                [0, 6]], plateau),\
                                \
        Piece(7, [[7], \
                                [7, 7], \
                                [0, 7, 7]], plateau),\
                                \
        Piece(8, [[8], \
                                [8, 8], \
                                [8], \
                                [8]], plateau),\
                                \
        Piece(9, [[9], \
                                [9], \
                                [9], \
                                [9], \
                                [9]], plateau),\
                                \
        Piece(10,[[10,10], \
                                [0, 10], \
                                [0, 10, 10]], plateau),\
                                \
        Piece(11,[[11, 11], \
                                [0, 11], \
                                [11, 11]], plateau),\
                                \
        Piece(12,[[12], \
                                [12,12], \
                                [0, 12], \
                                [0, 12]], plateau)\
    ]
    return piece

def plateau_clear():
    plateau = [[0 for _ in range(18)] for _ in range(11)]

    return plateau

plateau = [[0 for _ in range(12)] for _ in range(5)]

KataminoBoard(plateau)