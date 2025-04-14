import pyxel
import unicodedata

def remove_accents(text):
    """Remplace les caractères accentués par leurs équivalents sans accent."""
    try:
        text = unicodedata.normalize('NFKD', text)
        text = ''.join([c for c in text if not unicodedata.combining(c)])
        # Remplacements manuels pour certains caractères spécifiques
        replacements = {
            'œ': 'oe', 'Œ': 'OE',
            'æ': 'ae', 'Æ': 'AE',
            'ç': 'c', 'Ç': 'C',
            '«': '"', '»': '"'
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text
    except:
        # En cas d'erreur, renvoyer le texte original
        return text

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
        
        # Système d'alerte amélioré
        self.alert_message = ""
        self.alert_timer = 0
        self.alert_duration = 30  # Environ 1 seconde à 30 FPS
        
        # Variables pour la sélection de pièces déjà placées
        self.reselect_mode = False  # Mode de re-sélection des pièces déjà placées
        self.reselected_piece = None  # Pièce re-sélectionnée (déjà placée)
        self.reselected_piece_numero = 0  # Numéro de la pièce re-sélectionnée
        
        # Ajouter une variable pour stocker les coordonnées des boutons de pièces
        self.piece_buttons = []
        
        # Initialiser les pièces APRÈS avoir créé les plateaux
        self.pieces = create_pieces(self.board)
        self.selected_piece_index = 0
        self.selected_piece = self.pieces[self.selected_piece_index]
        
        # Ensemble pour suivre les numéros des pièces déjà placées sur le plateau principal
        self.placed_pieces_numero = set()
        # Remplir l'ensemble initialement si le plateau n'est pas vide
        for r in self.original_board:
            for cell_value in r:
                if cell_value > 0:
                    self.placed_pieces_numero.add(cell_value)
                    
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

    def cancel_reselection(self):
        """Annule le mode de re-sélection et restaure la pièce sur le plateau principal."""
        if not self.reselect_mode or self.reselected_piece is None:
            return False # Rien à annuler

        piece_to_restore = self.reselected_piece
        
        # Replacer correctement la pièce sur le plateau principal
        # Vérifier si la case est libre avant de replacer (sécurité)
        can_restore = True
        for y, x in piece_to_restore.actual_coordinates:
            if not (0 <= y < self.ligne and 0 <= x < self.cols and self.original_board[y][x] == 0):
                can_restore = False
                break # Collision lors de la restauration - ne devrait pas arriver normalement

        if can_restore:
            for y, x in piece_to_restore.actual_coordinates:
                 self.original_board[y][x] = piece_to_restore.numero
            
            # Ajouter la pièce de nouveau à l'ensemble des pièces placées
            self.placed_pieces_numero.add(piece_to_restore.numero)
            self.alert_message = f"Déplacement de la pièce {piece_to_restore.numero} annulé"
        else:
             # Gérer l'erreur si la restauration échoue (rare)
             self.alert_message = f"Erreur: Impossible de restaurer pièce {piece_to_restore.numero}"
             # Optionnel: essayer de sélectionner une pièce valide?

        # Recréer le plateau de prévisualisation à partir du plateau principal mis à jour
        self.preview_board = [row[:] for row in self.original_board]
        
        # Sortir du mode re-sélection
        self.reselect_mode = False
        self.reselected_piece = None
        self.reselected_piece_numero = 0
        self.alert_timer = self.alert_duration
        
        return True # Annulation réussie (ou tentative effectuée)

    def update(self):
        pyxel.mouse(True)
        mouse_x = pyxel.mouse_x
        mouse_y = pyxel.mouse_y
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Gestion du clic de souris pour sélectionner une pièce déjà placée ou depuis la zone de sélection
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # Vérifier d'abord si le clic est sur un des boutons de pièces en bas
            button_clicked = False
            for i, (btn_x, btn_y) in enumerate(self.piece_buttons):
                # Zone de clic de 16x16 pixels pour chaque bouton
                if btn_x <= mouse_x < btn_x + 16 and btn_y <= mouse_y < btn_y + 16:
                    # Si on était en mode re-sélection, annuler avant de sélectionner une nouvelle pièce
                    if self.reselect_mode:
                        self.cancel_reselection()
                        # Important: Mettre à jour preview_board *avant* init_piece_position
                        self.preview_board = [row[:] for row in self.original_board] 

                    # Sélectionner cette pièce
                    self.selected_piece_index = i
                    self.selected_piece = self.pieces[i]
                    self.init_piece_position(self.selected_piece) # Ceci met à jour preview_board
                    self.alert_message = f"Pièce {self.selected_piece.numero} sélectionnée"
                    self.alert_timer = self.alert_duration
                    button_clicked = True
                    break
            
            # Si aucun bouton n'a été cliqué, vérifier si le clic est sur le plateau
            if not button_clicked:
                cell_x = mouse_x // self.cell_size
                cell_y = mouse_y // self.cell_size
                
                # Vérifier si le clic est dans la grille
                if 0 <= cell_x < self.cols and 0 <= cell_y < self.ligne:
                    clicked_piece_numero = self.original_board[cell_y][cell_x]
                    
                    # Si on a cliqué sur une pièce existante (non vide)
                    if clicked_piece_numero > 0:
                        # Si on clique sur la pièce déjà en cours de re-sélection, ne rien faire
                        if self.reselect_mode and self.reselected_piece_numero == clicked_piece_numero:
                            return 

                        # Si on était en mode re-sélection (d'une *autre* pièce), annuler d'abord
                        if self.reselect_mode:
                             self.cancel_reselection()
                             # Mettre à jour preview_board *avant* de continuer
                             self.preview_board = [row[:] for row in self.original_board]

                        # --- Début de la re-sélection de la pièce cliquée ---
                        self.reselect_mode = True
                        self.reselected_piece_numero = clicked_piece_numero
                        
                        # Récupérer toutes les coordonnées de la pièce cliquée
                        piece_coords = []
                        for y in range(self.ligne):
                            for x in range(self.cols):
                                if self.original_board[y][x] == clicked_piece_numero:
                                    piece_coords.append([y, x])
                        
                        # Trouver l'instance de pièce correspondante
                        for piece in self.pieces:
                            if piece.numero == clicked_piece_numero:
                                # Mettre à jour la sélection
                                self.selected_piece = piece
                                self.selected_piece_index = self.pieces.index(piece)
                                self.reselected_piece = piece
                                
                                # Mettre à jour les coordonnées actuelles de la pièce
                                piece.actual_coordinates = piece_coords.copy()
                                
                                # Retirer UNIQUEMENT la pièce cliquée du plateau principal
                                for y_coord, x_coord in piece_coords:
                                    if 0 <= y_coord < self.ligne and 0 <= x_coord < self.cols:
                                         self.original_board[y_coord][x_coord] = 0

                                # Retirer la pièce de l'ensemble des pièces placées
                                if clicked_piece_numero in self.placed_pieces_numero:
                                    self.placed_pieces_numero.remove(clicked_piece_numero)
                                
                                # Mettre à jour le plateau de prévisualisation (sera écrasé par place_on_plateau mais bon)
                                self.preview_board = [row[:] for row in self.original_board]
                                piece.place_on_plateau(True, self.preview_board) # Place la pièce dans preview_board
                                
                                self.alert_message = f"Pièce {clicked_piece_numero} sélectionnée pour déplacement"
                                self.alert_timer = self.alert_duration
                                break
                    # Si on clique sur une case vide alors qu'on est en mode re-sélection, annuler la re-sélection
                    elif self.reselect_mode:
                         self.cancel_reselection()
                         # Sélectionner la première pièce non placée après annulation
                         found_next = False
                         for i, piece in enumerate(self.pieces):
                             if piece.numero not in self.placed_pieces_numero:
                                 self.selected_piece_index = i
                                 self.selected_piece = self.pieces[i]
                                 self.init_piece_position(self.selected_piece)
                                 found_next = True
                                 break
                         if not found_next and self.pieces: # Si tout est placé, resélectionner la première?
                              self.selected_piece_index = 0
                              self.selected_piece = self.pieces[0]
                              self.init_piece_position(self.selected_piece)


        # Gestion de la touche Entrée - Confirmation du placement
        if pyxel.btnp(self.confirm_key):
            # Vérifier si la pièce est déjà placée (sauf si on est en mode re-sélection)
            if not self.reselect_mode and self.selected_piece.numero in self.placed_pieces_numero:
                self.alert_message = f"Pièce {self.selected_piece.numero} déjà placée!"
                self.alert_timer = self.alert_duration
                return # Ne pas placer la pièce

            # Vérifier si le placement est valide (collisions, limites)
            has_collision = self.check_collision_with_placed_pieces()
            
            if has_collision:
                self.alert_message = "Placement invalide (collision ou hors limites)!"
                self.alert_timer = self.alert_duration
                return
                
            # Si pas de collision et pièce non déjà placée (ou en re-sélection), on procède au placement
            # Sauvegarde temporaire des valeurs du plateau principal
            new_board = [row[:] for row in self.original_board]
            
            # Pour chaque cellule, mettre à jour les cellules correspondant à la pièce actuelle
            piece_placed = False
            for y in range(self.ligne):
                for x in range(self.cols):
                    if self.preview_board[y][x] == self.selected_piece.numero:
                        new_board[y][x] = self.selected_piece.numero
                        piece_placed = True # Marquer qu'au moins une partie a été placée
            
            # Si la pièce n'a pas pu être placée (par ex. entièrement hors champ après manip)
            if not piece_placed:
                 self.alert_message = "Erreur lors du placement."
                 self.alert_timer = self.alert_duration
                 # Optionnel: réinitialiser la position de la pièce?
                 # self.init_piece_position(self.selected_piece)
                 return

            # Mettre à jour le plateau principal
            self.original_board = new_board
            # Ajouter la pièce à l'ensemble des pièces placées
            self.placed_pieces_numero.add(self.selected_piece.numero)
            self.alert_message = f"Pièce {self.selected_piece.numero} placée!"
            self.alert_timer = self.alert_duration
            
            # Si on était en mode de re-sélection, désactiver ce mode
            if self.reselect_mode:
                self.reselect_mode = False
                self.reselected_piece = None
                # Trouver la prochaine pièce non placée pour la sélection auto
                found_next = False
                start_index = (self.selected_piece_index + 1) % len(self.pieces)
                for i in range(len(self.pieces)):
                    check_index = (start_index + i) % len(self.pieces)
                    if self.pieces[check_index].numero not in self.placed_pieces_numero:
                        self.selected_piece_index = check_index
                        self.selected_piece = self.pieces[check_index]
                        self.init_piece_position(self.selected_piece)
                        found_next = True
                        break
                # Si toutes les pièces sont placées
                if not found_next:
                     self.alert_message = "Toutes les pièces sont placées!"
                     self.alert_timer = self.alert_duration
                     # Optionnel: garder la dernière pièce sélectionnée active pour d'éventuels déplacements
                     # self.init_piece_position(self.selected_piece)

            else:
                # Sinon passer automatiquement à la pièce suivante non placée
                found_next = False
                start_index = (self.selected_piece_index + 1) % len(self.pieces)
                for i in range(len(self.pieces)):
                    check_index = (start_index + i) % len(self.pieces)
                    if self.pieces[check_index].numero not in self.placed_pieces_numero:
                        self.selected_piece_index = check_index
                        self.selected_piece = self.pieces[check_index]
                        self.init_piece_position(self.selected_piece)
                        found_next = True
                        break
                # Si toutes les pièces sont placées
                if not found_next:
                     self.alert_message = "Toutes les pièces sont placées!"
                     self.alert_timer = self.alert_duration
                     # Optionnel: garder la dernière pièce sélectionnée active
                     # self.init_piece_position(self.selected_piece)
                
        if pyxel.btnp(pyxel.KEY_F):
            # Touche F pour activer/désactiver le mode de placement libre
            self.free_placement = not self.free_placement
            if self.free_placement:
                self.alert_message = "Mode libre activé - placement sans contraintes"
            else:
                self.alert_message = "Mode réglementé activé - vérification des collisions"
            self.alert_timer = self.alert_duration
                
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            # Si on était en mode re-sélection, annuler en utilisant la nouvelle méthode
            if self.reselect_mode:
                cancelled = self.cancel_reselection()
                if cancelled:
                    # Sélectionner la première pièce non placée après annulation
                    found_next = False
                    for i, piece in enumerate(self.pieces):
                        if piece.numero not in self.placed_pieces_numero:
                            self.selected_piece_index = i
                            self.selected_piece = self.pieces[i]
                            self.init_piece_position(self.selected_piece)
                            found_next = True
                            break
                    if not found_next and self.pieces: # Si tout est placé, resélectionner la première?
                         self.selected_piece_index = 0
                         self.selected_piece = self.pieces[0]
                         # Pas besoin d'init_piece_position si cancel_reselection a déjà mis à jour preview_board
                         # self.init_piece_position(self.selected_piece) 
            else:
                # Annuler les changements et réinitialiser la position de la pièce sélectionnée (non placée)
                self.preview_board = [row[:] for row in self.original_board]
                self.alert_message = "Placement annulé"
                self.init_piece_position(self.selected_piece) # Réaffiche la pièce au centre
                self.alert_timer = self.alert_duration

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
            current_index = self.selected_piece_index
            for i in range(1, len(self.pieces) + 1):
                 next_index = (current_index + i) % len(self.pieces)
                 # Optionnel: Ne proposer que les pièces non encore placées?
                 # if self.pieces[next_index].numero not in self.placed_pieces_numero:
                 self.selected_piece_index = next_index
                 self.selected_piece = self.pieces[next_index]
                 self.init_piece_position(self.selected_piece)
                 self.alert_message = f"Pièce {self.selected_piece.numero} sélectionnée"
                 self.alert_timer = self.alert_duration
                 break # Sortir après avoir trouvé la suivante (ou fait le tour complet)
        
        # Mettre à jour le timer d'alerte
        if self.alert_timer > 0:
            self.alert_timer -= 1

    def check_collision_with_placed_pieces(self):
        """Vérifie si la pièce actuelle entre en collision avec des pièces déjà placées ou dépasse les limites du plateau."""
        piece_coords = []
        
        # Récupérer les coordonnées de la pièce sélectionnée dans le plateau de prévisualisation
        for y in range(self.ligne):
            for x in range(self.cols):
                if self.preview_board[y][x] == self.selected_piece.numero:
                    piece_coords.append([y, x])
        
        # Si aucune coordonnée n'est trouvée, cela signifie que la pièce est entièrement hors du plateau
        if not piece_coords:
            return True  # La pièce est hors limites
            
        # Comparer avec le nombre de coordonnées original de la pièce
        # Si certaines parties sont manquantes, c'est que la pièce dépasse les limites
        original_piece_size = len(self.selected_piece.actual_coordinates)
        if len(piece_coords) < original_piece_size:
            return True  # La pièce est partiellement hors limites
        
        # Vérifier les collisions avec les pièces déjà placées
        for y, x in piece_coords:
            if self.original_board[y][x] != 0 and self.original_board[y][x] != self.selected_piece.numero:
                return True  # Collision détectée
        
        return False  # Pas de collision ni de pièce hors limites

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
                    # Si la pièce est celle qu'on vient de sélectionner (en mode resélection)
                    if self.reselect_mode and self.preview_board[y][x] == self.reselected_piece_numero:
                        # Couleur plus vive pour la pièce resélectionnée
                        color = self.colors[(self.selected_piece.numero % len(self.colors))-1]
                        
                        # Dessiner la pièce avec une couleur plus vive
                        pyxel.rect(
                            x * self.cell_size,
                            y * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                            color
                        )
                        
                        # Ajouter un contour de surbrillance pour la pièce active
                        pyxel.rectb(
                            x * self.cell_size + 1,
                            y * self.cell_size + 1,
                            self.cell_size - 2,
                            self.cell_size - 2,
                            7  # Couleur de surbrillance
                        )
                    else:
                        # Affichage normal pour les pièces en prévisualisation
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
        pyxel.text(10, self.ligne * self.cell_size + 5, remove_accents("Select Piece:"), 0)
        
        # Réinitialiser la liste des boutons de pièces
        self.piece_buttons = []
        
        for i, piece in enumerate(self.pieces):
            # Position du bouton pour cette pièce
            btn_x = 30 + i * 20
            btn_y = self.ligne * self.cell_size + 30
            
            # Stocker les coordonnées du bouton
            self.piece_buttons.append((btn_x, btn_y))
            
            # Dessiner l'icône de la pièce
            pyxel.blt(btn_x, btn_y, 0, i * 8, 0, 8, 8, 0, 0, 2.0)

            # Griser l'icône si la pièce est déjà placée
            if piece.numero in self.placed_pieces_numero:
                 # Dessiner un rectangle semi-transparent par-dessus
                 for row in range(0, 16, 2):
                     for col in range(0, 16, 2):
                          pyxel.pset(btn_x + col + (row % 4)//2, btn_y + row, 2) # Draw grey dots

            # Mettre en surbrillance la pièce sélectionnée
            if i == self.selected_piece_index:
                pyxel.rectb(
                    btn_x,
                    btn_y,
                    16,  # Taille du cadre
                    16,  # Taille du cadre
                    8,  # Couleur du cadre (jaune)
                )

        # Afficher "Cliquez pour sélectionner" sous les pièces
        pyxel.text(10, self.ligne * self.cell_size + 50, remove_accents("Cliquez pour sélectionner"), 0)
        
        # Supprimer la boucle redondante pour dessiner les icônes
        # pyxel.text(10, self.ligne * self.cell_size + 5, remove_accents("Select Piece:"), 0)
        # liste_des_coordonnees_des_boutons = [] # Déjà géré par self.piece_buttons
        # for i, piece in enumerate(self.pieces):
        #     pyxel.blt(30 + i * 20, self.ligne * self.cell_size + 30, 0, i * 8, 0, 8, 8, 0, 0, 2.0)
        #     if i == self.selected_piece_index:
        #         pyxel.rectb(
        #             30 + i * 20,
        #             self.ligne * self.cell_size + 30,
        #             16,  # Taille du cadre
        #             16,  # Taille du cadre
        #             8,  # Couleur du cadre
        #         )
        # liste_des_coordonnees_des_boutons.append((30 + i * 20, self.ligne * self.cell_size + 30)) # Déjà géré

        # Afficher l'alerte si nécessaire - NOUVEAU STYLE AMÉLIORÉ
        if self.alert_timer > 0:
            # Variables pour le message d'alerte amélioré
            alert_message = remove_accents(self.alert_message)  # Supprimer les accents du message
            message_width = len(alert_message) * 4  # Largeur approximative du texte
            padding = 10  # Espace autour du texte
            box_width = message_width + padding * 2
            box_height = 20  # Hauteur fixe pour la boîte
            
            # Position centrée pour la boîte d'alerte
            box_x = (self.cols * self.cell_size - box_width) // 2
            box_y = self.ligne * self.cell_size // 2  # Centrer verticalement sur le plateau
            
            # Dessiner un fond pour le message d'alerte
            pyxel.rect(box_x, box_y, box_width, box_height, 5)  # Fond bleu
            pyxel.rectb(box_x, box_y, box_width, box_height, 7)  # Bordure blanche
            
            # Dessiner le texte centré dans la boîte
            text_x = box_x + padding
            text_y = box_y + (box_height - 8) // 2  # 8 est la hauteur approximative du texte
            pyxel.text(text_x, text_y, alert_message, 7)  # Texte en blanc
            
        # Afficher les contrôles
        controls_y = self.ligne * self.cell_size + 100
        pyxel.text(10, controls_y, remove_accents("Contrôles:"), 0)
        pyxel.text(10, controls_y + 10, remove_accents("Flèches: Déplacer"), 0)
        pyxel.text(10, controls_y + 20, remove_accents("R: Rotation, E: Symétrie"), 0)
        pyxel.text(10, controls_y + 30, remove_accents("Entrée: Placer et passer à la pièce suivante"), 0)
        pyxel.text(10, controls_y + 40, remove_accents("N: Changer de pièce, ESC: Annuler"), 0)
        pyxel.text(10, controls_y + 50, remove_accents("F: Mode libre On/Off"), 0)
        pyxel.text(10, controls_y + 60, remove_accents("Clic souris: sélectionner pièce déjà placée"), 0)
        
        # Afficher le mode actuel
        mode_text = remove_accents("Mode: " + ("Libre" if self.free_placement else "Reglemente"))
        pyxel.text(10, controls_y + 80, mode_text, 8 if self.free_placement else 3)


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
        
        # Empêcher le mouvement hors plateau en mode prévisualisation
        if is_preview and not all(0 <= x < len(board) and 0 <= y < len(board[0]) for x, y in new_coordinates):
            # Restaurer l'état initial
            self.actual_coordinates = old_coordinates
            return self.place_on_plateau(is_preview, board), False
        
        # En mode libre (mais dans les limites du plateau)
        elif free_mode:
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
        
        # Sauvegarde des coordonnées actuelles
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
