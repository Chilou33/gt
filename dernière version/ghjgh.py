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

        # Mode prévisualisation et plateaux - les initialiser AVANT de créer les pièces
        self.preview_mode = True  # Toujours en mode prévisualisation
        self.original_board = [row[:] for row in self.board]  # Plateau principal (pièces fixées)
        self.preview_board = [row[:] for row in self.board]   # Plateau de prévisualisation
        self.free_placement = True  # Permet de déplacer librement la pièce

        # Variables pour gérer le placement des pièces
        self.confirm_key = pyxel.KEY_RETURN  # Touche Entrée
        
        # Ajouter un système d'alerte
        self.alert_message = ""
        self.alert_timer = 0
        self.alert_duration = 30  # Environ 1 seconde à 30 FPS
        
        # Initialiser les pièces APRÈS avoir créé les plateaux
        self.pieces = create_pieces(self.board)
        self.selected_piece_index = 0
        self.selected_piece = self.pieces[self.selected_piece_index]
        
        # Initialiser la position de la première pièce
        self.init_piece_position(self.selected_piece)

        pyxel.run(self.update, self.draw)
        
    def init_piece_position(self, piece):
        # Effacer la pièce du plateau de prévisualisation si elle y était déjà
        for y in range(self.ligne):
            for x in range(self.cols):
                if self.preview_board[y][x] == piece.numero:
                    self.preview_board[y][x] = 0
                    
        # Positionner la pièce au centre du plateau pour faciliter le placement
        offset_x = self.cols // 2 - 1
        offset_y = self.ligne // 2 - 1
        new_coords = []
        for i, row in enumerate(piece.patron):
            for j, val in enumerate(row):
                if val != 0:
                    new_coords.append([offset_y + i, offset_x + j])
        piece.actual_coordinates = new_coords
        
        # Recréer le plateau de prévisualisation à partir du plateau principal
        self.preview_board = [row[:] for row in self.original_board]
        
        # Placer la nouvelle pièce sur le plateau de prévisualisation
        piece.place_on_plateau(True, self.preview_board)

    def update(self):
        pyxel.mouse(True)
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Gestion de la touche Entrée - Confirmation du placement
        if pyxel.btnp(self.confirm_key):
            # Vérifier si le placement est valide, même en mode libre
            # On vérifie s'il y a des collisions avec d'autres pièces déjà placées
            has_collision = self.check_collision_with_placed_pieces()
            
            if has_collision:
                self.alert_message = "Collision détectée! Déplacez la pièce."
                self.alert_timer = self.alert_duration
                return
                
            # Si pas de collision, on procède au placement
            # Conserver les pièces déjà placées lors du placement d'une nouvelle pièce
            # Sauvegarde temporaire des valeurs du plateau principal
            new_board = [row[:] for row in self.original_board]
            
            # Pour chaque cellule, ne mettre à jour que les cellules correspondant à la pièce actuelle
            for y in range(self.ligne):
                for x in range(self.cols):
                    if self.preview_board[y][x] == self.selected_piece.numero:
                        new_board[y][x] = self.selected_piece.numero
            
            # Mettre à jour le plateau principal
            self.original_board = new_board
            self.alert_message = f"Pièce {self.selected_piece.numero} placée!"
            self.alert_timer = self.alert_duration
            
            # Passer automatiquement à la pièce suivante
            self.selected_piece_index = (self.selected_piece_index + 1) % len(self.pieces)
            self.selected_piece = self.pieces[self.selected_piece_index]
            self.init_piece_position(self.selected_piece)
                
        if pyxel.btnp(pyxel.KEY_F):
            # Touche F pour activer/désactiver le mode de placement libre
            self.free_placement = not self.free_placement
            if self.free_placement:
                self.alert_message = "Mode libre activé - placement sans contraintes"
            else:
                self.alert_message = "Mode réglementé activé - vérification des collisions"
            self.alert_timer = self.alert_duration
                
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            # Annuler les changements et réinitialiser la position de la pièce
            self.preview_board = [row[:] for row in self.original_board]
            self.alert_message = "Placement annulé"
            self.alert_timer = self.alert_duration
            self.init_piece_position(self.selected_piece)

        # Gestion des commandes de manipulation des pièces sur le plateau de prévisualisation
        if pyxel.btnp(pyxel.KEY_R):
            result, _ = self.selected_piece.rotate(True, self.preview_board, self.free_placement)
            self.preview_board = result
                
        if pyxel.btnp(pyxel.KEY_E):
            result, _ = self.selected_piece.symetrie(True, self.preview_board, self.free_placement)
            self.preview_board = result
                
        if pyxel.btnp(pyxel.KEY_LEFT):
            result, _ = self.selected_piece.deplacement(-1, 0, True, self.preview_board, self.free_placement)
            self.preview_board = result
                
        if pyxel.btnp(pyxel.KEY_RIGHT):
            result, _ = self.selected_piece.deplacement(1, 0, True, self.preview_board, self.free_placement)
            self.preview_board = result
                
        if pyxel.btnp(pyxel.KEY_DOWN):
            result, _ = self.selected_piece.deplacement(0, 1, True, self.preview_board, self.free_placement)
            self.preview_board = result
                
        if pyxel.btnp(pyxel.KEY_UP):
            result, _ = self.selected_piece.deplacement(0, -1, True, self.preview_board, self.free_placement)
            self.preview_board = result
                
        if pyxel.btnp(pyxel.KEY_N):
            # Changer manuellement la pièce sans la placer
            self.selected_piece_index = (self.selected_piece_index + 1) % len(self.pieces)
            self.selected_piece = self.pieces[self.selected_piece_index]
            self.init_piece_position(self.selected_piece)
            self.alert_message = f"Pièce {self.selected_piece.numero} sélectionnée"
            self.alert_timer = self.alert_duration
        
        # Mettre à jour le timer d'alerte
        if self.alert_timer > 0:
            self.alert_timer -= 1

    def check_valid_placement(self):
        # Vérifier uniquement les collisions avec les pièces déjà placées sur le plateau principal
        piece_coords = self.selected_piece.actual_coordinates
        
        # Vérifier les limites du plateau
        if not all(0 <= x < len(self.original_board) and 0 <= y < len(self.original_board[0]) for x, y in piece_coords):
            return False
            
        # Vérifier les collisions avec d'autres pièces du plateau principal
        for x, y in piece_coords:
            if self.original_board[x][y] != 0 and self.original_board[x][y] != self.selected_piece.numero:
                return False
                
        return True

    def check_collision_with_placed_pieces(self):
        """Vérifie si la pièce actuelle entre en collision avec des pièces déjà placées sur le plateau original."""
        piece_coords = []
        
        # Récupérer les coordonnées de la pièce sélectionnée dans le plateau de prévisualisation
        for y in range(self.ligne):
            for x in range(self.cols):
                if self.preview_board[y][x] == self.selected_piece.numero:
                    piece_coords.append([y, x])
        
        # Vérifier les collisions avec les pièces déjà placées
        for y, x in piece_coords:
            if self.original_board[y][x] != 0 and self.original_board[y][x] != self.selected_piece.numero:
                return True  # Collision détectée
        
        return False  # Pas de collision

    def draw(self):
        pyxel.cls(1)
        
        # Dessiner deux plateaux côte à côte si la fenêtre est assez large
        plateau_width = self.cols * self.cell_size
        
        # Dessiner le plateau principal (pièces déjà placées)
        for y in range(self.ligne):
            for x in range(self.cols):
                value = self.original_board[y][x]
                if value > 0:
                    color = self.colors[(value % len(self.colors))-1]
                    pyxel.rect(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                        color
                    )
                # Dessiner la grille
                pyxel.rectb(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                    0
                )
                
        # Dessiner le plateau de prévisualisation avec la pièce actuelle
        # (la pièce actuelle est déjà incluse dans preview_board)
        for y in range(self.ligne):
            for x in range(self.cols):
                # N'afficher que la pièce en cours de manipulation (celle qui n'est pas encore placée)
                if self.preview_board[y][x] == self.selected_piece.numero:
                    pyxel.rect(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                        self.colors[(self.selected_piece.numero % len(self.colors))-1]
                    )
                    
                    # Ajouter un contour de surbrillance pour la pièce active
                    pyxel.rectb(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                        7  # Couleur de surbrillance
                    )

        # Afficher les informations de l'interface utilisateur
        pyxel.text(10, self.ligne * self.cell_size + 5, "Select Piece:", 0)
        liste_des_coordonnees_des_boutons = []
        for i, piece in enumerate(self.pieces):
            pyxel.blt(30 + i * 20, self.ligne * self.cell_size + 30, 0, i * 8, 0, 8, 8, 0, 0, 2.0)
            if i == self.selected_piece_index:
                pyxel.rectb(
                    30 + i * 20,
                    self.ligne * self.cell_size + 30,
                    16,  # Taille du cadre
                    16,  # Taille du cadre
                    8,  # Couleur du cadre
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
        pyxel.text(10, controls_y + 30, "Entrée: Placer et passer à la pièce suivante", 0)
        pyxel.text(10, controls_y + 40, "N: Changer de pièce, ESC: Annuler", 0)
        pyxel.text(10, controls_y + 50, "F: Mode libre On/Off", 0)
        
        # Afficher le mode actuel
        mode_text = "Mode: " + ("Libre" if self.free_placement else "Réglementé")
        pyxel.text(10, controls_y + 70, mode_text, 8 if self.free_placement else 3)


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
            if 0 <= x < len(board) and 0 <= y < len(board[0]):
                if board[x][y] != 0 and board[x][y] != self.numero:
                    return True  # Collision avec une autre pièce
                
        return False  # Pas de collision
        
    def confirm_placement(self):
        # Cette méthode est maintenant gérée par KataminoBoard.check_valid_placement()
        return True

    def deplacement(self, dy, dx, is_preview=False, target_board=None, free_mode=False):
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
        
        # En mode libre, on ignore les collisions
        if free_mode:
            # Filtrer les coordonnées qui sont hors plateau
            valid_coordinates = []
            for x, y in new_coordinates:
                if 0 <= x < len(board) and 0 <= y < len(board[0]):
                    valid_coordinates.append([x, y])
                    
            if valid_coordinates:  # Si au moins une partie de la pièce reste visible
                self.actual_coordinates = new_coordinates
                return self.place_on_plateau(is_preview, board), True
            else:
                # Si toute la pièce sort du plateau, on ne déplace pas
                self.actual_coordinates = old_coordinates
                return self.place_on_plateau(is_preview, board), False
        else:
            # En mode normal, on vérifie les collisions
            if not self.check_collision(new_coordinates, is_preview, board):
                self.actual_coordinates = new_coordinates
                return self.place_on_plateau(is_preview, board), True
            
            # Si le déplacement est impossible, restaurer l'état initial
            self.actual_coordinates = old_coordinates
            return self.place_on_plateau(is_preview, board), False

    def rotate(self, is_preview=False, target_board=None, free_mode=False):
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

        # En mode libre, on ignore les collisions
        if free_mode:
            # Filtrer les coordonnées qui sont hors plateau
            valid_coordinates = []
            for x, y in final_coordinates:
                if 0 <= x < len(board) and 0 <= y < len(board[0]):
                    valid_coordinates.append([x, y])
                    
            if valid_coordinates:  # Si au moins une partie de la pièce reste visible
                self.actual_coordinates = final_coordinates
                return self.place_on_plateau(is_preview, board), True
            else:
                # Si toute la pièce sort du plateau, on ne fait pas la rotation
                self.actual_coordinates = old_coordinates
                return self.place_on_plateau(is_preview, board), False
        else:
            # En mode normal, on vérifie les collisions
            if not self.check_collision(final_coordinates, is_preview, board):
                self.actual_coordinates = final_coordinates
                return self.place_on_plateau(is_preview, board), True
            
            # Si la rotation est impossible, restaurer l'état initial
            self.actual_coordinates = old_coordinates
            return self.place_on_plateau(is_preview, board), False

    def symetrie(self, is_preview=False, target_board=None, free_mode=False):
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

        # En mode libre, on ignore les collisions
        if free_mode:
            # Filtrer les coordonnées qui sont hors plateau
            valid_coordinates = []
            for x, y in symetrie_coordinates:
                if 0 <= x < len(board) and 0 <= y < len(board[0]):
                    valid_coordinates.append([x, y])
                    
            if valid_coordinates:  # Si au moins une partie de la pièce reste visible
                self.actual_coordinates = symetrie_coordinates
                return self.place_on_plateau(is_preview, board), True
            else:
                # Si toute la pièce sort du plateau, on ne fait pas la symétrie
                self.actual_coordinates = old_coordinates
                return self.place_on_plateau(is_preview, board), False
        else:
            # En mode normal, on vérifie les collisions
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
