import pyxel

class KataminoBoard:
    def __init__(self, board, cell_size=30):
        self.board = board
        self.cell_size = cell_size
        self.ligne = len(board)
        self.cols = len(board[0]) if self.ligne > 0 else 0

        width = self.cols * cell_size   # Extra space for piece selection
        height = self.ligne * cell_size + 200
        pyxel.init(width, height, title="Katamino Board")

        pyxel.colors.from_list([0x000000, 0xFFFFFF, 0x7F7F7F, 0xC3C3C3, 0x64BCED, 0x200CFF, 0xFF1E27, 0x880015, 0xFFFF00, 0xF58B1A, 0x20BD0F, 0x104F12, 0xF585B1, 0xCA42D1, 0x6325D4, 0x807625])
        self.colors = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.gray_color = 2  # Couleur grisée pour les pièces en mode prévisualisation

        pyxel.load("NouvellePalette.pyxres")

        self.pieces = create_pieces(self.board)
        self.selected_piece_index = 0
        self.selected_piece = self.pieces[self.selected_piece_index]
        
        # Ajouter un système d'alerte
        self.alert_message = ""
        self.alert_timer = 0
        self.alert_duration = 30  # Environ 1 seconde à 30 FPS
        
        # Mode prévisualisation pour le placement des pièces
        self.preview_mode = False
        self.original_board = [row[:] for row in self.board]  # Copie profonde du plateau
        self.preview_board = [row[:] for row in self.board]   # Plateau de prévisualisation

        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel.mouse(True)
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        if pyxel.btnp(pyxel.KEY_P):
            if self.preview_mode:
                # En mode prévisualisation, confirmer le placement
                success = self.check_valid_placement()
                if success:
                    # Copier le plateau de prévisualisation dans le plateau principal
                    self.board = [row[:] for row in self.preview_board]
                    self.original_board = [row[:] for row in self.board]
                    self.preview_mode = False
                    self.alert_message = "Pièce placée!"
                    self.alert_timer = self.alert_duration
                else:
                    self.alert_message = "Placement invalide!"
                    self.alert_timer = self.alert_duration
            else:
                # En mode normal, entrer en mode prévisualisation
                self.preview_mode = True
                self.original_board = [row[:] for row in self.board]
                # Initialiser le plateau de prévisualisation
                self.preview_board = [row[:] for row in self.board]
                # Passer la référence du plateau à la pièce sélectionnée
                self.selected_piece.preview_plateau = self.preview_board
                self.alert_message = "Positionnez la pièce puis appuyez sur P pour confirmer"
                self.alert_timer = self.alert_duration
                
        if pyxel.btnp(pyxel.KEY_ESCAPE) and self.preview_mode:
            # Annuler le mode prévisualisation
            self.preview_mode = False
            self.preview_board = [row[:] for row in self.board]
            self.alert_message = "Placement annulé"
            self.alert_timer = self.alert_duration

        if self.preview_mode:
            # En mode prévisualisation, manipuler la pièce sur le plateau de prévisualisation
            active_board = self.preview_board
        else:
            active_board = self.board

        # SECTION MODIFIÉE: Gestion des commandes avec mode prévisualisation
        if pyxel.btnp(pyxel.KEY_R):
            result, success = self.selected_piece.rotate(self.preview_mode, active_board)
            if self.preview_mode:
                self.preview_board = result
                # Ne pas afficher d'alerte en mode prévisualisation
            else:
                self.board = result
                if not success:
                    self.alert_message = "Rotation impossible!"
                    self.alert_timer = self.alert_duration
                
        if pyxel.btnp(pyxel.KEY_E):
            result, success = self.selected_piece.symetrie(self.preview_mode, active_board)
            if self.preview_mode:
                self.preview_board = result
                # Ne pas afficher d'alerte en mode prévisualisation
            else:
                self.board = result
                if not success:
                    self.alert_message = "Symétrie impossible!"
                    self.alert_timer = self.alert_duration
                
        if pyxel.btnp(pyxel.KEY_LEFT):
            result, success = self.selected_piece.deplacement(-1, 0, self.preview_mode, active_board)
            if self.preview_mode:
                self.preview_board = result
                # Ne pas afficher d'alerte en mode prévisualisation
            else:
                self.board = result
                if not success:
                    self.alert_message = "Déplacement impossible!"
                    self.alert_timer = self.alert_duration
                
        if pyxel.btnp(pyxel.KEY_RIGHT):
            result, success = self.selected_piece.deplacement(1, 0, self.preview_mode, active_board)
            if self.preview_mode:
                self.preview_board = result
                # Ne pas afficher d'alerte en mode prévisualisation
            else:
                self.board = result
                if not success:
                    self.alert_message = "Déplacement impossible!"
                    self.alert_timer = self.alert_duration
                
        if pyxel.btnp(pyxel.KEY_DOWN):
            result, success = self.selected_piece.deplacement(0, 1, self.preview_mode, active_board)
            if self.preview_mode:
                self.preview_board = result
                # Ne pas afficher d'alerte en mode prévisualisation
            else:
                self.board = result
                if not success:
                    self.alert_message = "Déplacement impossible!"
                    self.alert_timer = self.alert_duration
                
        if pyxel.btnp(pyxel.KEY_UP):
            result, success = self.selected_piece.deplacement(0, -1, self.preview_mode, active_board)
            if self.preview_mode:
                self.preview_board = result
                # Ne pas afficher d'alerte en mode prévisualisation
            else:
                self.board = result
                if not success:
                    self.alert_message = "Déplacement impossible!"
                    self.alert_timer = self.alert_duration
                
        if pyxel.btnp(pyxel.KEY_N) and not self.preview_mode:
            # Changer l'index de la pièce sélectionnée (uniquement hors mode prévisualisation)
            self.selected_piece_index = (self.selected_piece_index + 1) % len(self.pieces)
            self.selected_piece = self.pieces[self.selected_piece_index]
        
        # Mettre à jour le timer d'alerte
        if self.alert_timer > 0:
            self.alert_timer -= 1

    def check_valid_placement(self):
        # Vérifier s'il y a des collisions entre la pièce sélectionnée et les pièces déjà placées
        piece_coords = self.selected_piece.actual_coordinates
        
        # Vérifier les limites du plateau
        if not all(0 <= x < len(self.board) and 0 <= y < len(self.board[0]) for x, y in piece_coords):
            return False
            
        # Vérifier les collisions avec d'autres pièces
        for x, y in piece_coords:
            if self.board[x][y] != 0 and self.board[x][y] != self.selected_piece.numero:
                return False
                
        return True

    def draw(self):
        pyxel.cls(1)
        
        # Déterminer quel plateau dessiner (principal ou prévisualisation)
        display_board = self.preview_board if self.preview_mode else self.board
        
        for y in range(self.ligne):
            for x in range(self.cols):
                value = display_board[y][x]
                if value > 0:
                    # En mode prévisualisation, utiliser une couleur grisée pour les pièces déjà placées 
                    # mais pas pour la pièce actuelle
                    if self.preview_mode and value != self.selected_piece.numero:
                        color = self.gray_color
                    else:
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
        
        # Si en mode prévisualisation, dessiner un contour spécial autour de la pièce active
        if self.preview_mode:
            for x, y in self.selected_piece.actual_coordinates:
                if 0 <= x < len(self.board) and 0 <= y < len(self.board[0]):
                    pyxel.rectb(
                        y * self.cell_size,
                        x * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                        7  # Couleur de surbrillance
                    )

        # Draw piece selection area
        pyxel.text(10, self.ligne * self.cell_size + 5, "Select Piece:", 0)
        liste_des_coordonnees_des_boutons = []
        for i, piece in enumerate(self.pieces):
            pyxel.blt(30 + i * 20, self.ligne * self.cell_size + 30, 0, i * 8, 0, 8, 8, 0, 0, 2.0)
            if i == self.selected_piece_index:
                pyxel.rectb(
                    30 + i * 20,
                    self.ligne * self.cell_size + 30,
                    16,  # Augmenter la taille du cadre
                    16,  # Augmenter la taille du cadre
                    8,  # Couleur plus visible
                )
        
        liste_des_coordonnees_des_boutons.append((30 + i * 20, self.ligne * self.cell_size + 30))

        # Afficher l'alerte si nécessaire
        if self.alert_timer > 0:
            message_x = 10
            message_y = self.ligne * self.cell_size + 70
            pyxel.text(message_x, message_y, self.alert_message, 8)
            
        # Afficher les contrôles
        controls_y = self.ligne * self.cell_size + 100
        pyxel.text(10, controls_y, "Contrôles:", 0)
        pyxel.text(10, controls_y + 10, "Flèches: Déplacer", 0)
        pyxel.text(10, controls_y + 20, "R: Rotation, E: Symétrie", 0)
        pyxel.text(10, controls_y + 30, "P: Placer/Confirmer, ESC: Annuler", 0)
        pyxel.text(10, controls_y + 40, "N: Pièce suivante", 0)
        
        # Afficher le mode actuel
        mode_text = "Mode: Prévisualisation" if self.preview_mode else "Mode: Sélection"
        pyxel.text(10, controls_y + 60, mode_text, 8 if self.preview_mode else 3)


class Piece:
    def __init__(self, numero, patron, plateau):
        self.numero = numero
        self.patron = patron
        self.plateau = plateau
        self.actual_coordinates = self.convert_to_coordinates()
        self.preview_plateau = None

    def convert_to_coordinates(self):
        coordinates = []
        for i, row in enumerate(self.patron):
            for j, val in enumerate(row):
                if val != 0:
                    coordinates.append([i, j])
        return coordinates

    def place_on_plateau(self, is_preview=False, target_board=None):
        # Utiliser le plateau spécifié ou le plateau par défaut
        board = target_board if target_board is not None else self.plateau
        
        for x, y in self.actual_coordinates:
            if 0 <= x < len(board) and 0 <= y < len(board[0]):
                board[x][y] = self.numero
        return board
    
    def check_collision(self, coordinates, is_preview=False, target_board=None):
        # Utiliser le plateau spécifié ou le plateau par défaut
        board = target_board if target_board is not None else self.plateau
        
        # Vérifier si toutes les coordonnées sont dans les limites du plateau
        if not all(0 <= x < len(board) and 0 <= y < len(board[0]) for x, y in coordinates):
            return True  # Collision avec les bords du plateau
            
        # Vérifier les collisions avec d'autres pièces
        for x, y in coordinates:
            if board[x][y] != 0 and board[x][y] != self.numero:
                return True  # Collision avec une autre pièce
                
        return False  # Pas de collision
        
    def confirm_placement(self):
        # Cette méthode est maintenant gérée par KataminoBoard.check_valid_placement()
        return True

    def deplacement(self, dy, dx, is_preview=False, target_board=None):
        # Utiliser le plateau spécifié ou le plateau par défaut
        board = target_board if target_board is not None else self.plateau
        
        # Sauvegarde de l'état actuel pour restauration en cas d'échec
        old_coordinates = self.actual_coordinates.copy()
        
        # Effacer la pièce actuelle du plateau
        for x, y in self.actual_coordinates:
            if 0 <= x < len(board) and 0 <= y < len(board[0]):
                board[x][y] = 0

        # Calculer les nouvelles coordonnées
        new_coordinates = []
        for x, y in self.actual_coordinates:
            new_x, new_y = x + dx, y + dy
            new_coordinates.append([new_x, new_y])
        
        # Vérifier les collisions
        if not self.check_collision(new_coordinates, is_preview, board):
            self.actual_coordinates = new_coordinates
            return self.place_on_plateau(is_preview, board), True
        
        # Si le déplacement est impossible, restaurer l'état initial
        self.actual_coordinates = old_coordinates
        return self.place_on_plateau(is_preview, board), False

    def rotate(self, is_preview=False, target_board=None):
        # Utiliser le plateau spécifié ou le plateau par défaut
        board = target_board if target_board is not None else self.plateau
        
        # Sauvegarde des coordonnées actuelles
        old_coordinates = self.actual_coordinates.copy()
        
        # Effacer la pièce actuelle du plateau
        for x, y in self.actual_coordinates:
            if 0 <= x < len(board) and 0 <= y < len(board[0]):
                board[x][y] = 0

        # Trouver le pivot de rotation
        if self.numero in [6, 8, 4]:
            self.rotation_anchor = self.actual_coordinates[1]
        if self.numero in [1, 2, 3, 5, 7, 9, 10, 11, 12]:
            self.rotation_anchor = self.actual_coordinates[2]

        anchor_x = self.rotation_anchor[0]
        anchor_y = self.rotation_anchor[1]

        # Calculer les nouvelles coordonnées
        translated_coordinates = [[x - anchor_x, y - anchor_y] for x, y in self.actual_coordinates]
        rotated_coordinates = [[y, -x] for x, y in translated_coordinates]
        final_coordinates = [[x + anchor_x, y + anchor_y] for x, y in rotated_coordinates]

        # Vérifier les collisions
        if not self.check_collision(final_coordinates, is_preview, board):
            self.actual_coordinates = final_coordinates
            return self.place_on_plateau(is_preview, board), True
        
        # Si la rotation est impossible, restaurer l'état initial
        self.actual_coordinates = old_coordinates
        return self.place_on_plateau(is_preview, board), False

    def symetrie(self, is_preview=False, target_board=None):
        # Utiliser le plateau spécifié ou le plateau par défaut
        board = target_board if target_board is not None else self.plateau
        
        # Sauvegarde de l'état actuel
        old_coordinates = self.actual_coordinates.copy()
        
        # Effacer la pièce actuelle du plateau
        for x, y in self.actual_coordinates:
            if 0 <= x < len(board) and 0 <= y < len(board[0]):
                board[x][y] = 0

        # Calculer les nouvelles coordonnées pour la symétrie
        max_y = max(y for x, y in self.actual_coordinates)
        symetrie_coordinates = [[x, max_y - y] for x, y in self.actual_coordinates]

        min_y = min(y for x, y in self.actual_coordinates)
        decalage = min_y - min(y for x, y in symetrie_coordinates)

        symetrie_coordinates = [[x, y + decalage] for x, y in symetrie_coordinates]

        # Vérifier les collisions
        if not self.check_collision(symetrie_coordinates, is_preview, board):
            self.actual_coordinates = symetrie_coordinates
            return self.place_on_plateau(is_preview, board), True
            
        # Restaurer l'état initial si la symétrie est impossible
        self.actual_coordinates = old_coordinates
        return self.place_on_plateau(is_preview, board), False


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
