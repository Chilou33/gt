import pyxel

# class PlateauFinal: 
#     def __init__(self, plateau, cell_size=30):
#         self.board = plateau
#         self.cell_size = cell_size
#         self.ligne = len(plateau)
#         self.cols = len(plateau[0]) if self.ligne > 0 else 0
#         self.plateau_final = plateau_clear()

#         width = self.cols * cell_size
#         height = self.ligne * cell_size

#         pyxel.colors.from_list([0x000000, 0xFFFFFF, 0x7F7F7F, 0xC3C3C3, 0x64BCED, 0x200CFF, 0xFF1E27, 0x880015, 0xFFFF00, 0xF58B1A, 0x20BD0F, 0x104F12, 0xF585B1, 0xCA42D1, 0x6325D4, 0x807625])
#         self.colors = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

#         self.pieces = create_pieces(self.board)
#         self.selected_piece_index = 0
#         self.selected_piece = self.pieces[self.selected_piece_index]

        
        
#     def check_if_deplacement_possible():

        



class KataminoBoard:
    def __init__(self, plateau_final, cell_size=30):
        self.plateau_final = plateau_final
        self.cell_size = cell_size
        self.ligne = len(plateau_final)
        self.cols = len(plateau_final[0]) if self.ligne > 0 else 0
        self.plateau_deplacement = plateau_clear() 

        width = self.cols * cell_size   # Extra space for piece selection
        height = self.ligne * cell_size + 200
        pyxel.init(width, height, title="Katamino Board")

        pyxel.colors.from_list([0x000000, 0xFFFFFF, 0x7F7F7F, 0xC3C3C3, 0x64BCED, 0x200CFF, 0xFF1E27, 0x880015, 0xFFFF00, 0xF58B1A, 0x20BD0F, 0x104F12, 0xF585B1, 0xCA42D1, 0x6325D4, 0x807625])
        self.colors = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        pyxel.load("NouvellePalette.pyxres")

        self.pieces = create_pieces(self.plateau_deplacement)
        self.selected_piece_index = 0
        self.selected_piece = self.pieces[self.selected_piece_index]

        pyxel.run(self.update, self.draw)

    def update(self):
        
        pyxel.mouse(True)
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_P):
            self.plateau_deplacement = self.selected_piece.place_on_plateau_final()
        if pyxel.btnp(pyxel.KEY_R):
            self.plateau_deplacement = self.selected_piece.rotate()
        if pyxel.btnp(pyxel.KEY_E):
            self.plateau_deplacement = self.selected_piece.symetrie()
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.plateau_deplacement = self.selected_piece.deplacement(-1, 0)
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.plateau_deplacement = self.selected_piece.deplacement(1, 0)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.plateau_deplacement = self.selected_piece.deplacement(0, 1)
        if pyxel.btnp(pyxel.KEY_UP):
            self.plateau_deplacement = self.selected_piece.deplacement(0, -1)
        if pyxel.btnp(pyxel.KEY_N):
            self.selected_piece_index = (self.selected_piece_index + 1) % len(self.pieces)
            self.selected_piece = self.pieces[self.selected_piece_index]

    def draw(self):
        pyxel.cls(1)
        for x in range(self.ligne):
            for y in range(self.cols):
                value = self.plateau_final[x][y]
                if value > 0:
                    color = self.colors[(value % len(self.colors))-1]
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
        for x in range(self.ligne):
            for y in range(self.cols):
                value_2 = self.plateau_deplacement[y][x]
                if value_2 > 0: 
                    color = self.colors[(value % len(self.colors))-1]
                    pyxel.rect(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size -10,
                        self.cell_size -10,
                        color
                    )

        # Draw piece selection area
        pyxel.text(10, self.ligne * self.cell_size + 10, "Select Piece:", 0)
        for i, piece in enumerate(self.pieces):
            pyxel.blt(30 + i * 20, self.ligne * self.cell_size + 30, 0, i * 8, 0, 8, 8, 0, 0, 2.0)
            if i == self.selected_piece_index:
                pyxel.rectb(
                    30 + i * 20,
                    self.ligne * self.cell_size + 10,
                    10,
                    10,
                    0,
                )

class Piece:
    def __init__(self, numero, patron, plateau_final):
        self.numero = numero
        self.patron = patron
        self.plateau_final = plateau_final
        self.plateau_deplacement = plateau_clear() 
        self.actual_coordinates = self.convert_to_coordinates()

    def convert_to_coordinates(self):
        coordinates = []
        for i, row in enumerate(self.patron):
            for j, val in enumerate(row):
                if val != 0:
                    coordinates.append([i, j])
        return coordinates  
      
    def place_on_plateau_final(self):
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau_final) and 0 <= y < len(self.plateau_final[0]):
                self.plateau_final[x][y] = self.numero
        return self.plateau_final

    

    def place_on_plateau_deplacement(self):
        self.plateau_deplacement = plateau_clear()
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau_deplacement) and 0 <= y < len(self.plateau[0]):
                self.plateau_deplacement[x][y] = self.numero
        return self.plateau_deplacement

    def deplacement(self, dx, dy):
        self.place_on_plateau_deplacement()
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau_deplacement) and 0 <= y < len(self.plateau_deplacement[0]):
                self.plateau_deplacement[x][y] = 0

        new_coordinates = []
        for x, y in self.actual_coordinates:
            new_x, new_y = x + dy, y + dx
            if 0 <= new_x < len(self.plateau_deplacement) and 0 <= new_y < len(self.plateau_deplacement[0]):
                new_coordinates.append([new_x, new_y])
        if len(new_coordinates) == len(self.actual_coordinates):
            self.actual_coordinates = new_coordinates

        return self.place_on_plateau_deplacement()

    def rotate(self):
        self.place_on_plateau_deplacement()
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau_deplacement) and 0 <= y < len(self.plateau_deplacement[0]):
                self.plateau_deplacement[x][y] = 0

        if self.numero in [6, 8,4]:
            self.rotation_anchor = self.actual_coordinates[1]
        if self.numero in [1, 2, 3, 5, 7, 9, 10, 11, 12]:
            self.rotation_anchor = self.actual_coordinates[2]

        anchor_x = self.rotation_anchor[0]
        anchor_y = self.rotation_anchor[1]

        translated_coordinates = [[x - anchor_x, y - anchor_y] for x, y in self.actual_coordinates]
        rotated_coordinates = [[y, -x] for x, y in translated_coordinates]
        final_coordinates = [[x + anchor_x, y + anchor_y] for x, y in rotated_coordinates]

        if all(0 <= x < len(self.plateau_deplacement) and 0 <= y < len(self.plateau_deplacement[0]) for x, y in final_coordinates):
            self.actual_coordinates = final_coordinates

        return self.place_on_plateau_deplacement()

    def symetrie(self):
        self.place_on_plateau_deplacement()
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau_deplacement) and 0 <= y < len(self.plateau_deplacement[0]):
                self.plateau_deplacement[x][y] = 0

        max_y = max(y for x, y in self.actual_coordinates)
        symetrie_coordinates = [[x, max_y - y] for x, y in self.actual_coordinates]

        min_y = min(y for x, y in self.actual_coordinates)
        decalage = min_y - min(y for x, y in symetrie_coordinates)

        symetrie_coordinates = [[x, y + decalage] for x, y in symetrie_coordinates]

        if all(0 <= x < len(self.plateau_deplacement) and 0 <= y < len(self.plateau_deplacement[0]) for x, y in symetrie_coordinates):
            self.actual_coordinates = symetrie_coordinates

        return self.place_on_plateau_deplacement()

def create_pieces(plateau):
    pieces = [
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
    return pieces

def plateau_clear():
    plateau = [[0 for _ in range(12)] for _ in range(5)]
    return plateau

# Initialize plateau
plateau = plateau_clear()

# Create and display the Katamino board
KataminoBoard(plateau)
