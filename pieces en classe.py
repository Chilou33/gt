class Piece:
    def __init__(self, numero, patron, plateau):
        self.numero = numero
        self.patron = patron
        self.plateau = plateau
        self.coordinates_on_plateau = self.check_for_coordinates()
        self.firsts_coordinates = self.convert_to_coordinates()

    def check_for_coordinates(self):
        coordinates = []
        for i, y in enumerate(self.plateau):
            for j, val in enumerate(y):
                if val == self.numero:
                    coordinates.append([i, j])
        return coordinates

    def convert_to_coordinates(self):
        coordinates = []
        for i, row in enumerate(self.patron):
            for j, val in enumerate(row):
                if val != 0:
                    coordinates.append([i, j])
        return coordinates 
    #def deplacement(self,x:int,y:int):
        #coordinates = self.coordinates_on_plateau

    def rotate(self):
        # Find the top-left corner of the piece
        min_x = min(coord[0] for coord in self.firsts_coordinates)
        min_y = min(coord[1] for coord in self.firsts_coordinates)

        # Translate coordinates to the origin
        translated_coordinates = [[x - min_x, y - min_y] for x, y in self.firsts_coordinates]

        # Apply rotation (90 degrees clockwise)
        rotated_coordinates = [[y, -x] for x, y in translated_coordinates]

        # Translate coordinates back to original position
        self.firsts_coordinates = [[x + min_x, y + min_y] for x, y in rotated_coordinates]

    def place_on_plateau(self, plateau):
        for x, y in self.firsts_coordinates:
            if 0 <= x < len(plateau) and 0 <= y < len(plateau[0]):
                plateau[x][y] = self.numero
        return plateau

# Example usage
def create_pieces(plateau):
    piece = [
        Piece(1, [[1, 1], [1], [1], [1]], plateau),
        Piece(2, [[0, 2], [2, 2, 2], [0, 2]], plateau),
        Piece(3, [[3], [3, 3, 3], [0, 3]], plateau),
        Piece(4, [[4], [4, 4], [4, 4]], plateau),
        Piece(5, [[5], [5], [5, 5, 5]], plateau),
        Piece(6, [[6, 6, 6], [0, 6], [0, 6]], plateau),
        Piece(7, [[7], [7, 7], [0, 7, 7]], plateau),
        Piece(8, [[8], [8, 8], [8], [8]], plateau),
        Piece(9, [[9], [9], [9], [9], [9]], plateau),
        Piece(10, [[10, 10], [0, 10], [0, 10, 10]], plateau),
        Piece(11, [[11, 11], [0, 11], [11, 11]], plateau),
        Piece(12, [[12], [12], [12, 12], [0, 12]], plateau)
    ]
    return piece

# Initialize plateau
plateau = [[0 for _ in range(18)] for _ in range(11)]
for y in range(11):
    for x in range(18):
        if 2 < y < 8 and 2 < x < 15:
            pass
        else:
            plateau[y][x] = ""

# Create pieces
piece = create_pieces(plateau)

# Place a piece on the plateau
# plateau = pieces[0].place_on_plateau()

# Rotate a piece and place it on the plateau
# pieces[1].rotate()
# plateau = pieces[1].place_on_plateau()