import pyxel
from random import randint
import math
import random

width = 12 * 32
height = 5 * 32 + 200
pyxel.init(width,height,title="PYTHOMINOES",display_scale=2,fps=30)

class App:
    def __init__(self, page_affichée):
        pyxel.run(page_affichée.update, page_affichée.draw)
   
class MainMenu:
    def __init__(self):
        self.message = "Bienvenue dans Pythominoes\nAppuyez sur Entree pour jouer"
        pyxel.load("ressources.pyxres")
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
            App(EcranChoixPieces())

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

pieces_selectionnees = []

class EcranChoixPieces:
    def __init__(self):
        global pieces_selectionnees
        self.liste_pieces_deja_choisies = pieces_selectionnees
        self.liste_piece_choisies = []
        self.position_curseur = 0
        pyxel.load("ressources.pyxres")
        self.etape =len(pieces_selectionnees)

    def update(self):
        if pyxel.btnp(pyxel.KEY_RIGHT,repeat=10):
            if self.position_curseur == 11:
                self.position_curseur = 0
            else: 
                self.position_curseur += 1
        if pyxel.btnp(pyxel.KEY_LEFT,repeat=10):
            if self.position_curseur == 0: 
                self.position_curseur = 11
            else: 
                self.position_curseur -=1
                
        if pyxel.btnp(pyxel.KEY_S):  # Changé à btnp pour éviter répétitions
            if self.etape==0:
                if self.position_curseur not in self.liste_piece_choisies:
                    if len(self.liste_piece_choisies) < 4:
                        self.liste_piece_choisies.append(self.position_curseur)
            else:
                if self.position_curseur not in self.liste_piece_choisies:
                    if len(self.liste_piece_choisies) < 1:
                        self.liste_piece_choisies.append(self.position_curseur)   
        
        if pyxel.btnp(pyxel.KEY_E): 
            self.liste_piece_choisies = []
            
        if pyxel.btnp(pyxel.KEY_RETURN):
            if (self.etape == 0 and len(self.liste_piece_choisies) == 4) or \
               (self.etape > 0 and len(self.liste_piece_choisies) == 1):
                # Mise à jour des variables globales
                global pieces_selectionnees
                pieces_selectionnees = self.liste_pieces_deja_choisies + self.liste_piece_choisies
                App(KataminoBoard(Plateau(len(pieces_selectionnees)).clear))

    def draw(self):
        pyxel.cls(0)
        if self.etape==0:
            pyxel.text(3*32,3*32,"Sélectionnez 4 pieces en appuyant sur S",1,)
        else:  pyxel.text(3*32,3*32,"Sélectionnez 1 piece en appuyant sur S",1,)
        pyxel.bltm(3*32,4*32,0,0,8*8,12*16,16,0,scale=2)
        for i in self.liste_pieces_deja_choisies+self.liste_piece_choisies:
            pyxel.rect(i*32,4*32-8,32,32,0)
        pyxel.rectb(self.position_curseur*32,4*32-8,32,32,1)
        pyxel.text(3*32,5*32,"Pieces Selectionnees :",1)
        decalage = 0
        for image_piece in self.liste_pieces_deja_choisies+self.liste_piece_choisies:
            pyxel.blt(8+decalage,6*32,0,24+image_piece*16,16,16,16,0,scale=2.0)
            decalage+=32
        pyxel.text(3*32,32*5+180,"Une fois vos pieces choisies, appuyez sur Entree pour jouer",1)

class Ecran_de_victoire:
    def __init__(self):
        self.message = "Victoire!"
        pyxel.load("ressources.pyxres")
        self.pieces_cascade_liste = []  # Liste des pièces en cascade [x, y, image_val, angle_rad, speed]
        self.val = randint(1, 12) * 16 + 8  # Valeur initiale
        self.piece_size = 32 # Piece size after scaling (16 * 2.0)

    def ajouter_piece_cascade(self):
            corner = random.randint(0, 1)
            speed = random.uniform(1.5, 3.0) 
            piece_val = randint(1, 12) * 16 + 8  

            if corner == 0:
                x_position = 0  

                angle_rad = random.uniform(0, math.pi / 2)
            else:
                x_position = width - self.piece_size 

                angle_rad = random.uniform(math.pi / 2, math.pi)

            y_position = height 
            self.pieces_cascade_liste.append([x_position, y_position, piece_val, angle_rad, speed])

    def pieces_deplacement(self):
        for piece in self.pieces_cascade_liste.copy():  
            x, y, _, angle, speed = piece


            dx = speed * math.cos(angle)
            dy = -speed * math.sin(angle)


            piece[0] += dx
            piece[1] += dy

            if piece[1] < -self.piece_size:
                self.pieces_cascade_liste.remove(piece)

    def update(self):

        if pyxel.frame_count % 30 == 0:
            self.val = randint(1, 12) * 16 + 8

        self.ajouter_piece_cascade()  
        self.pieces_deplacement()  
        if pyxel.btn(pyxel.KEY_RETURN):
            App(EcranChoixPieces())
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()


    def draw(self):
        pyxel.cls(1) 
        pyxel.text(width // 2 - len(self.message)*2, height // 2 - 4, self.message, 0)  


        for piece in self.pieces_cascade_liste:
            x, y, piece_val, _, _ = piece 
            pyxel.blt(x, y, 0, piece_val, 16, 16, 16, 0, scale=2.0)
    
class Plateau:
    def __init__(self,taille: int):
        self.taille = taille
        self.clear = self.plateau_clear()

    def plateau_clear(self):
        plateau = [[0 for _ in range(self.taille)] for _ in range(5)]
        return plateau
    
taille = 12
plateau = Plateau(taille).clear 

class KataminoBoard:
    def __init__(self, plateau, cell_size=32):
        self.Dplateau = [row[:] for row in plateau]
        self.plateau = plateau

        self.etape = len(pieces_selectionnees)
        print(self.etape)

        self.cell_size = cell_size
        self.ligne = len(plateau)
        self.cols = len(plateau[0]) if self.ligne > 0 else 0
        pyxel.colors.from_list([0x000000, 0xFFFFFF, 0x7F7F7F, 0xC3C3C3, 0x64BCED, 0x200CFF, 0xFF1E27, 0x880015, 0xFFFF00, 0xF58B1A, 0x20BD0F, 0x104F12, 0xF585B1, 0xCA42D1, 0x6325D4, 0x807625])
        self.colors = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    
        pyxel.load("ressources.pyxres")

        self.pieces = create_pieces(self.plateau)
        self.pieces_jouables = [self.pieces[piece] for piece in pieces_selectionnees]
        self.index_pieces_non_jouables = [i for i in range(12) if i not in pieces_selectionnees]
        self.index_piece_selectionnee = 0
        self.piece_selectionnee = self.pieces_jouables[self.index_piece_selectionnee]
        self.pieces_deja_placees = []
        self.pieces_jouees = []
        

        self.liste_des_coordonnees_des_boutons = [(32*3,32*6),(32*4,32*6),(32*5,32*6),(32*6,32*6),(32*7,32*6),(32*8,32*6),(32*3,32*7),(32*4,32*7),(32*5,32*7),(32*6,32*7),(32*7,32*7),(32*8,32*7)]
        
        # Ajouter un système d'alerte
        self.alert_message = ""
        self.alert_timer = 0
        self.alert_duration = 30  # Environ 1 seconde à 30 FPS

    def verif_victoire(self):
        for y in range(self.ligne):
            for x in range(self.cols):
                if self.plateau[y][x] == 0:
                    return False  
        return True 

    def update(self):
        pyxel.mouse(True)

        if pyxel.btnp(pyxel.KEY_M):
            App(MainMenu())

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_A):
            self.piece_selectionnee.retirer()
            if self.index_piece_selectionnee in self.pieces_deja_placees : 
                self.pieces_deja_placees.remove(self.index_piece_selectionnee)

        if pyxel.btnp(pyxel.KEY_P,repeat=10):
            self.plateau, success = self.piece_selectionnee.place_on_plateau()
            if self.index_piece_selectionnee not in self.pieces_deja_placees :
                self.pieces_deja_placees.append(self.index_piece_selectionnee)
            if not success :
                self.alert_message = "Placement impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouees.append(self.index_piece_selectionnee)


        if pyxel.btnp(pyxel.KEY_R,repeat=10):
            self.Dplateau, success = self.piece_selectionnee.rotate()
            if not success:
                self.alert_message = "Rotation impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouees.append(self.index_piece_selectionnee)

        if pyxel.btnp(pyxel.KEY_E,repeat=8):
            self.Dplateau, success = self.piece_selectionnee.symetrie()
            if not success:
                self.alert_message = "Symetrie impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouees.append(self.index_piece_selectionnee)

        if pyxel.btnp(pyxel.KEY_LEFT,repeat=8):
            self.Dplateau, success = self.piece_selectionnee.deplacement(-1, 0)
            if not success:
                self.alert_message = "Deplacement impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouees.append(self.index_piece_selectionnee)

        if pyxel.btnp(pyxel.KEY_RIGHT,repeat=8):
            self.Dplateau, success = self.piece_selectionnee.deplacement(1, 0)
            if not success:
                self.alert_message = "Deplacement impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouees.append(self.index_piece_selectionnee)

        if pyxel.btnp(pyxel.KEY_DOWN,repeat=8):
            self.Dplateau, success = self.piece_selectionnee.deplacement(0, 1)
            if not success:
                self.alert_message = "Deplacement impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouees.append(self.index_piece_selectionnee)

        if pyxel.btnp(pyxel.KEY_UP,repeat=8):
            self.Dplateau, success = self.piece_selectionnee.deplacement(0, -1)
            if not success:
                self.alert_message = "Deplacement impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouees.append(self.index_piece_selectionnee)

        
        if pyxel.btnp(pyxel.KEY_N):
                print(self.pieces_deja_placees)
                if self.piece_selectionnee.etat_deplacement :
                    if self.piece_selectionnee.test_placement() :
                        if self.index_piece_selectionnee in self.pieces_jouees :
                            self.piece_selectionnee.place_on_plateau()
                            if self.index_piece_selectionnee not in self.pieces_deja_placees :
                                self.pieces_deja_placees.append(self.index_piece_selectionnee)
                        self.index_piece_selectionnee = (self.index_piece_selectionnee + 1) % len(self.pieces_jouables)
                        self.piece_selectionnee = self.pieces_jouables[self.index_piece_selectionnee]
                        if self.index_piece_selectionnee in self.pieces_deja_placees :
                            self.piece_selectionnee.etat_deplacement = False
                        else :
                            self.piece_selectionnee.etat_deplacement = True
                    else :
                        self.piece_selectionnee.retirer()
                        if self.index_piece_selectionnee in self.pieces_deja_placees :
                                self.pieces_deja_placees.remove(self.index_piece_selectionnee)
                        self.index_piece_selectionnee = (self.index_piece_selectionnee + 1) % len(self.pieces_jouables)
                        self.piece_selectionnee = self.pieces_jouables[self.index_piece_selectionnee]
                        if self.index_piece_selectionnee in self.pieces_deja_placees :
                            self.piece_selectionnee.etat_deplacement = False
                        else :
                            self.piece_selectionnee.etat_deplacement = True
                else :
                    self.index_piece_selectionnee = (self.index_piece_selectionnee + 1) % len(self.pieces_jouables)
                    self.piece_selectionnee = self.pieces_jouables[self.index_piece_selectionnee]
                    if self.index_piece_selectionnee in self.pieces_deja_placees :
                        self.piece_selectionnee.etat_deplacement = False
                    else :
                        self.piece_selectionnee.etat_deplacement = True
        
        if self.verif_victoire():
            self.alert_message = "Victoire!"
            self.alert_timer = self.alert_duration
            App(Ecran_de_victoire())

        if pyxel.btn(pyxel.KEY_G):
            App(EcranChoixPieces())
        
        if self.alert_timer > 0:
            self.alert_timer -= 1
        

    def draw(self):
        pyxel.cls(1)
        pyxel.bltm(3*32,40,0,0,16*8,24*8,10*8,scale=2.0)
        pyxel.bltm(3*32+(self.etape-1)*32,40,1,0,0,16*8,10*8,scale=2.0)
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
                    0
                )
                pyxel.rectb(
                    (x * self.cell_size)+1,
                    (y * self.cell_size)+1,
                    self.cell_size-2,
                    self.cell_size-2,
                    0
                )
        for y in range(self.ligne):
            for x in range(self.cols):
                value = self.Dplateau[y][x]
                if value > 0:
                    color = self.colors[(value % len(self.colors))-1]
                    pyxel.rect(
                        (x * self.cell_size)+4,
                        (y * self.cell_size)+4,
                        self.cell_size-8,
                        self.cell_size-8,
                        color
                    )
        # Draw piece selection area
        pyxel.text(10, self.ligne * self.cell_size + 10, "Piece selectionnee :", 0)
        #self.liste_des_coordonnees_des_boutons = [(32*3,32*6),(32*4,32*6),(32*5,32*6),(32*6,32*6),(32*7,32*6),(32*8,32*6),(32*3,32*7),(32*4,32*7),(32*5,32*7),(32*6,32*7),(32*7,32*7),(32*8,32*7)]
        rect_cos = self.liste_des_coordonnees_des_boutons[self.piece_selectionnee.numero - 1]
        pyxel.bltm(32*3, self.ligne * self.cell_size+32, 0, 0, 0,  24*8, 8*8, 0,scale=2.0)
        pyxel.rectb(rect_cos[0],rect_cos[1],32,32,2)
        
        for i in self.index_pieces_non_jouables :
            pyxel.rect(self.liste_des_coordonnees_des_boutons[i][0],self.liste_des_coordonnees_des_boutons[i][1],32,32,1)
        
        
        # Afficher l'alerte si nécessaire
        if self.alert_timer > 0:
            message_x = 10
            message_y = self.ligne * self.cell_size + 150
            pyxel.text(message_x, message_y, self.alert_message, 2)

        cmd_color = 0

        hauteur_txt = 12
        nbr_col = 3
        ecart_bas = 5

        y_start_cmds = pyxel.height - (nbr_col * hauteur_txt) - ecart_bas

        x_left = 20
        pyxel.text(x_left, y_start_cmds, "Fleches: Deplacer", cmd_color)
        pyxel.text(x_left, y_start_cmds + hauteur_txt, "R: Rotation", cmd_color)
        pyxel.text(x_left, y_start_cmds + 2 * hauteur_txt, "E: Symetrie", cmd_color)


        x_mid = 145 
        pyxel.text(x_mid, y_start_cmds, "P: Placer Piece", cmd_color)
        pyxel.text(x_mid, y_start_cmds + hauteur_txt, "A: Retirer Piece", cmd_color)
        pyxel.text(x_mid, y_start_cmds + 2 * hauteur_txt, "N: Piece Suivante", cmd_color)

        x_right = 270
        pyxel.text(x_right, y_start_cmds, "G: Choix Pieces", cmd_color)
        pyxel.text(x_right, y_start_cmds + hauteur_txt, "M: Menu Principal", cmd_color)
        pyxel.text(x_right, y_start_cmds + 2 * hauteur_txt, "Q: Quitter", cmd_color)

class Piece:
    def __init__(self, numero, patron, plateau):
        
        self.numero = numero
        self.patron = patron
        self.plateau = plateau
        # Créer une copie indépendante du plateau
        self.Dplateau = [row[:] for row in plateau]
        self.etat_deplacement = False
        self.cos_actuelles = self.cos_de_départ()

    def cos_de_départ(self):
        coordinates = []
        for i, row in enumerate(self.patron):
            for j, val in enumerate(row):
                if val != 0:
                    coordinates.append([i, j])
        return coordinates

    def place_on_Dplateau(self):
        for i in range(len(self.Dplateau)):
            for j in range(len(self.Dplateau[0])):
                self.Dplateau[i][j] = 0

        if self.etat_deplacement == True:
            for x, y in self.cos_actuelles:
                self.Dplateau[x][y] = self.numero

        if self.etat_deplacement == False:
            for x, y in self.cos_actuelles:
                self.plateau[x][y] = 0
                self.Dplateau[x][y] = self.numero
                self.etat_deplacement = True
        return self.Dplateau
    
    def test_placement(self):
        if all( self.plateau[x][y] == 0  for x, y in self.cos_actuelles):
            return True
        else:
            return False

    def place_on_plateau(self):
        # Check if the placement is valid
        if not self.test_placement():
            return self.plateau, False
        
        if self.etat_deplacement:
            for x, y in self.cos_actuelles:
                self.Dplateau[x][y] = 0
                self.plateau[x][y] = self.numero
            self.etat_deplacement = False
            return self.plateau, True
        else:  
            for x, y in self.cos_actuelles:
                self.plateau[x][y] = self.numero
            self.etat_deplacement = False
            return self.plateau, True

    def retirer(self):
        if self.etat_deplacement:
            for x,y in self.cos_actuelles :
                self.Dplateau[x][y] = 0
        else :
            for x,y in self.cos_actuelles :
                self.plateau[x][y] = 0
        self.etat_deplacement = True
        
    def deplacement(self, dy, dx):
        self.place_on_Dplateau()
        # Sauvegarde de l'état actuel pour restauration en cas d'échec
        old_coordinates = self.cos_actuelles.copy()

        # Calculer les nouvelles coordonnées
        new_coordinates = []
        for x, y in self.cos_actuelles:
            new_x, new_y = x + dx, y + dy
            new_coordinates.append([new_x, new_y])
        
        # Vérifier si les nouvelles coordonnées sont valides et si les cases sont libres
        if all(0 <= new_x < len(self.plateau) and 0 <= new_y < len(self.plateau[0]) for new_x, new_y in new_coordinates):
            self.cos_actuelles = new_coordinates
            return self.place_on_Dplateau(), True
        
        # Si le déplacement est impossible, restaurer l'état initial
        self.cos_actuelles = old_coordinates
        return self.place_on_Dplateau(), False

    def rotate(self):
        self.place_on_Dplateau()

        if self.numero in [6,8,4,5]:
            self.rotation_anchor = self.cos_actuelles[1]
        if self.numero in [1, 2, 3, 7, 9, 10, 11, 12]:
            self.rotation_anchor = self.cos_actuelles[2]

        anchor_x = self.rotation_anchor[0]
        anchor_y = self.rotation_anchor[1]

        translated_coordinates = [[x - anchor_x, y - anchor_y] for x, y in self.cos_actuelles]
        rotated_coordinates = [[y, -x] for x, y in translated_coordinates]
        final_coordinates = [[x + anchor_x, y + anchor_y] for x, y in rotated_coordinates]

        if all(0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]) for x, y in final_coordinates):
            self.cos_actuelles = final_coordinates
            return self.place_on_Dplateau(), True
        else:
            # Remettre les pièces à leur position d'origine si la rotation est impossible
            return self.place_on_Dplateau(), False

    def symetrie(self):
        self.place_on_Dplateau()
        # Sauvegarde de l'état actuel
        old_coordinates = self.cos_actuelles.copy()
        

        max_y = max(y for x, y in self.cos_actuelles)
        symetrie_coordinates = [[x, max_y - y] for x, y in self.cos_actuelles]

        min_y = min(y for x, y in self.cos_actuelles)
        decalage = min_y - min(y for x, y in symetrie_coordinates)

        symetrie_coordinates = [[x, y + decalage] for x, y in symetrie_coordinates]

        if all(0 <= x < len(self.plateau) and 0 <= y < len(self.plateau[0]) for x, y in symetrie_coordinates):
            self.cos_actuelles = symetrie_coordinates
            return self.place_on_Dplateau(), True
            
        # Restaurer l'état initial si la symétrie est impossible
        self.cos_actuelles = old_coordinates
        return self.place_on_Dplateau(), False

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


App(MainMenu())