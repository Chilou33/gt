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
        # Check if the placement is valid before placing
        if not self.can_place():
            return self.plateau, False
            
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]):
                self.plateau[x][y] = self.numero
        return self.plateau, True
    
    def can_place(self):
        # Check if all coordinates are valid and not occupied
        for x, y in self.actual_coordinates:
            if not (0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0])):
                return False
            if isinstance(self.plateau[x][y], int) and self.plateau[x][y] != 0 and self.plateau[x][y] != self.numero:
                return False
        return True

    def deplacement(self, dy, dx):
        # Sauvegarde de l'état actuel pour restauration en cas d'échec
        old_coordinates = self.actual_coordinates.copy()
        
        # Effacer la pièce actuelle du plateau
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]):
                self.plateau[x][y] = 0

        # Calculer les nouvelles coordonnées
        new_coordinates = []
        for x, y in self.actual_coordinates:
            new_x, new_y = x + dx, y + dy
            new_coordinates.append([new_x, new_y])
        
        self.actual_coordinates = new_coordinates
        
        # Vérifier si les nouvelles coordonnées sont valides
        if not self.can_place():
            # Restaurer l'état initial si le déplacement est impossible
            self.actual_coordinates = old_coordinates
            return self.place_on_plateau()[0], False
        
        # Placer la pièce aux nouvelles coordonnées
        return self.place_on_plateau()[0], True

    def rotate(self):
        # Save current coordinates in case rotation is not possible
        old_coordinates = self.actual_coordinates.copy()
        
        # Clear the current position of the piece on the plateau
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]):
                self.plateau[x][y] = 0

        # Find the center for rotation
        if self.numero in [6, 8, 4]:
            rotation_anchor = self.actual_coordinates[1]  # Use a specific point as anchor
        else:
            rotation_anchor = self.actual_coordinates[2]

        anchor_x, anchor_y = rotation_anchor[0], rotation_anchor[1]

        # Apply rotation (90 degrees clockwise)
        translated_coordinates = [[x - anchor_x, y - anchor_y] for x, y in self.actual_coordinates]
        rotated_coordinates = [[y, -x] for x, y in translated_coordinates]
        self.actual_coordinates = [[x + anchor_x, y + anchor_y] for x, y in rotated_coordinates]

        # Check if rotation is valid
        if not self.can_place():
            # Restore original position if rotation is not possible
            self.actual_coordinates = old_coordinates
            return self.place_on_plateau()[0], False
            
        # Place the piece at the rotated position
        return self.place_on_plateau()[0], True

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
        Piece(10,[[10, 10], [0, 10], [0, 10, 10]], plateau),
        Piece(11,[[11, 11], [0, 11], [11, 11]], plateau),
        Piece(12,[[12], [12], [12, 12], [0, 12]], plateau)
    ]
    return piece

def plateau_clear():
    plateau = [[0 for _ in range(18)] for _ in range(11)]
    for y in range(11):
        for x in range(18):
            if 2 < y < 8 and 2 < x < 15:
                pass
            else:
                plateau[y][x] = ""
    return plateau

# Initialize plateau
plateau = plateau_clear()

# Create pieces
pieces = create_pieces(plateau)

# Place a piece on the plateau
# plateau = pieces[0].place_on_plateau()

# Rotate a piece and place it on the plateau
# pieces[1].rotate()
# plateau = pieces[1].place_on_plateau()