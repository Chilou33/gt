import pyxel
from random import randint

width = 12 * 32
height = 5 * 32 + 200
pyxel.init(width,height,title="PYTHOMINOES",display_scale=2,fps=30)

class App:
    def __init__(self, page_affichée):
        self.contenu_fenetre = page_affichée
        
        pyxel.run(self.contenu_fenetre.update, self.contenu_fenetre.draw)
   

class MainMenu:
    def __init__(self):
        self.message = "Bienvenue dans Pythominoes\nAppuyez sur Entree pour jouer"
        pyxel.load("tilemap.pyxres")
        self.pieces_cascade_liste = []  # Liste des pièces en cascade
        self.val = randint(1, 12) * 16 + 8  # Valeur initiale
        
    def ajouter_piece_cascade(self):
        """Ajoute une pièce à la cascade toutes les secondes."""
        if pyxel.frame_count % 5 == 0:  # Une pièce toutes les 10 frames
            x_position = randint(0, 12*32)  # Position aléatoire sur l'axe X
            piece_val = randint(1, 12) * 16 + 8  # Valeur aléatoire pour l'image de la pièce
            # Stocker à la fois la position et l'image à utiliser
            self.pieces_cascade_liste.append([x_position, 0, piece_val])

    def pieces_deplacement(self):
        """Déplace les pièces vers le bas et les supprime si elles sortent de l'écran."""
        for piece in self.pieces_cascade_liste.copy():  # Utiliser une copie pour éviter les problèmes de suppression pendant l'itération
            piece[1] += 2  # Déplacement vers le bas (vitesse ajustable)
            if piece[1] > height:  # Si la pièce sort de l'écran
                self.pieces_cascade_liste.remove(piece)

    def update(self):
        """Met à jour l'état du menu principal."""
        # Mettre à jour la valeur globale périodiquement (pour l'animation)
        if pyxel.frame_count % 30 == 0:
            self.val = randint(1, 12) * 16 + 8
            
        self.ajouter_piece_cascade()  # Ajouter des pièces à la cascade
        self.pieces_deplacement()  # Déplacer les pièces
        if pyxel.btnp(pyxel.KEY_RETURN):  # Lancer le jeu quand "Entrée" est pressé
            App(KataminoBoard(plateau))

    def draw(self):
        """Dessine le menu principal."""
        pyxel.cls(1)  # Efface l'écran avec une couleur de fond
        pyxel.text(30, (5 * 30 + 200) // 2, self.message, 0)  # Affiche le message

        # Dessiner les pièces en cascade
        for piece in self.pieces_cascade_liste:
            if len(piece) >= 3:  # Si la pièce contient une valeur d'image
                piece_val = piece[2]
            else:
                piece_val = self.val  # Utiliser la valeur par défaut si non spécifiée
            
            pyxel.blt(piece[0], piece[1], 0, piece_val, 16, 16, 16, 0, scale=2.0)
        
    
class Plateau:
    def __init__(self, taille: int):
        self.taille = taille
        self.clear = self.plateau_clear()

    def plateau_clear(self):
        plateau = [[0 for _ in range(self.taille)] for _ in range(5)]
        return plateau

taille = 12
plateau = Plateau(taille).clear 

class KataminoBoard:
    def __init__(self, plateau, cell_size=32):
        self.plateau = plateau
        self.cell_size = cell_size
        self.ligne = len(plateau)
        self.cols = len(plateau[0]) if self.ligne > 0 else 0

        pyxel.colors.from_list([0x000000, 0xFFFFFF, 0x7F7F7F, 0xC3C3C3, 0x64BCED, 0x200CFF, 0xFF1E27, 0x880015, 0xFFFF00, 0xF58B1A, 0x20BD0F, 0x104F12, 0xF585B1, 0xCA42D1, 0x6325D4, 0x807625])
        self.colors = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        pyxel.load("tilemap.pyxres")

        self.pieces = create_pieces(self.plateau)
        self.selected_piece_index = 0
        self.selected_piece = self.pieces[self.selected_piece_index]
        self.liste_des_coordonnees_des_boutons = [(32*3,32*6),(32*4,32*6),(32*5,32*6),(32*6,32*6),(32*7,32*6),(32*8,32*6),(32*3,32*7),(32*4,32*7),(32*5,32*7),(32*6,32*7),(32*7,32*7),(32*8,32*7)]
        # Ajouter un système d'alerte
        self.alert_message = ""
        self.alert_timer = 0
        self.alert_duration = 30  # Environ 1 seconde à 30 FPS

        #pyxel.run(self.update, self.draw)

    def update(self):
        pyxel.mouse(True)
        if pyxel.btnp(pyxel.KEY_M):
            App(MainMenu())
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_P,repeat=10):
            self.plateau = self.selected_piece.place_on_plateau()
        if pyxel.btnp(pyxel.KEY_R,repeat=10):
            self.plateau, success = self.selected_piece.rotate()
            if not success:
                self.alert_message = "Rotation impossible!"
                self.alert_timer = self.alert_duration
        if pyxel.btnp(pyxel.KEY_E,repeat=8):
            self.plateau, success = self.selected_piece.symetrie()
            if not success:
                self.alert_message = "Symetrie impossible!"
                self.alert_timer = self.alert_duration
        if pyxel.btnp(pyxel.KEY_LEFT,repeat=8):
            self.plateau, success = self.selected_piece.deplacement(-1, 0)
            if not success:
                self.alert_message = "Deplacement impossible!"
                self.alert_timer = self.alert_duration
        if pyxel.btnp(pyxel.KEY_RIGHT,repeat=8):
            self.plateau, success = self.selected_piece.deplacement(1, 0)
            if not success:
                self.alert_message = "Deplacement impossible!"
                self.alert_timer = self.alert_duration
        if pyxel.btnp(pyxel.KEY_DOWN,repeat=8):
            self.plateau, success = self.selected_piece.deplacement(0, 1)
            if not success:
                self.alert_message = "Deplacement impossible!"
                self.alert_timer = self.alert_duration
        if pyxel.btnp(pyxel.KEY_UP,repeat=8):
            self.plateau, success = self.selected_piece.deplacement(0, -1)
            if not success:
                self.alert_message = "Deplacement impossible!"
                self.alert_timer = self.alert_duration
        if pyxel.btnp(pyxel.KEY_N):
                    
            # Changer l'index de la pièce sélectionnée
            self.selected_piece_index = (self.selected_piece_index + 1) % len(self.pieces)
            self.selected_piece = self.pieces[self.selected_piece_index]
        
        # Mettre à jour le timer d'alerte
        if self.alert_timer > 0:
            self.alert_timer -= 1

    def draw(self):
        pyxel.cls(1)
        for y in range(self.ligne):
            for x in range(self.cols):
                value = self.plateau[y][x]
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
                    2
                )

        # Draw piece selection area
        pyxel.text(10, self.ligne * self.cell_size + 10, "Piece selectionnee :", 0)
        #self.liste_des_coordonnees_des_boutons = [(32*3,32*6),(32*4,32*6),(32*5,32*6),(32*6,32*6),(32*7,32*6),(32*8,32*6),(32*3,32*7),(32*4,32*7),(32*5,32*7),(32*6,32*7),(32*7,32*7),(32*8,32*7)]
        rect_cos = self.liste_des_coordonnees_des_boutons[self.selected_piece_index]
        pyxel.bltm(32*3, self.ligne * self.cell_size+32, 0, 0, 0,  24*8, 8*8, 0,scale=2.0)
        pyxel.rectb(rect_cos[0],rect_cos[1],32,32,2)

        
        # Afficher l'alerte si nécessaire
        if self.alert_timer > 0:
            message_x = 10
            message_y = self.ligne * self.cell_size + 150
            pyxel.text(message_x, message_y, self.alert_message, 2)

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
        
        # Vérifier si les nouvelles coordonnées sont valides et si les cases sont libres
        if all(0 <= new_x < len(self.plateau) and 0 <= new_y < len(self.plateau[0]) 
               for new_x, new_y in new_coordinates):
            # Vérifier que toutes les cases cibles sont vides
            if all(self.plateau[new_x][new_y] == 0 for new_x, new_y in new_coordinates):
                self.actual_coordinates = new_coordinates
                return self.place_on_plateau(), True
        
        # Si le déplacement est impossible, restaurer l'état initial
        self.actual_coordinates = old_coordinates
        return self.place_on_plateau(), False

    def rotate(self):
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]):
                self.plateau[x][y] = 0

        if self.numero in [6, 8,4]:
            self.rotation_anchor = self.actual_coordinates[1]
        if self.numero in [1, 2, 3, 5, 7, 9, 10, 11, 12]:
            self.rotation_anchor = self.actual_coordinates[2]

        anchor_x = self.rotation_anchor[0]
        anchor_y = self.rotation_anchor[1]

        translated_coordinates = [[x - anchor_x, y - anchor_y] for x, y in self.actual_coordinates]
        rotated_coordinates = [[y, -x] for x, y in translated_coordinates]
        final_coordinates = [[x + anchor_x, y + anchor_y] for x, y in rotated_coordinates]

        if all(0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]) for x, y in final_coordinates):
            self.actual_coordinates = final_coordinates
            return self.place_on_plateau(), True
        else:
            # Remettre les pièces à leur position d'origine si la rotation est impossible
            return self.place_on_plateau(), False

    def symetrie(self):
        # Sauvegarde de l'état actuel
        old_coordinates = self.actual_coordinates.copy()
        
        for x, y in self.actual_coordinates:
            if 0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]):
                self.plateau[x][y] = 0

        max_y = max(y for x, y in self.actual_coordinates)
        symetrie_coordinates = [[x, max_y - y] for x, y in self.actual_coordinates]

        min_y = min(y for x, y in self.actual_coordinates)
        decalage = min_y - min(y for x, y in symetrie_coordinates)

        symetrie_coordinates = [[x, y + decalage] for x, y in symetrie_coordinates]

        if all(0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]) for x, y in symetrie_coordinates):
            # Vérifier que les cases cibles sont vides
            if all(self.plateau[x][y] == 0 for x, y in symetrie_coordinates):
                self.actual_coordinates = symetrie_coordinates
                return self.place_on_plateau(), True
            
        # Restaurer l'état initial si la symétrie est impossible
        self.actual_coordinates = old_coordinates
        return self.place_on_plateau(), False

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

# Start the game with the main menu
App(MainMenu())