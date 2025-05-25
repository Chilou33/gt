import pyxel
import math
from random import randint
import random
#from sauvegarde import save_game_file
width = 12 * 32
height = 5 * 32 + 200
pyxel.init(width,height,title="PYTHOMINOES",display_scale=2,fps=30)

musique = True
effets = True

pieces_selectionnees = []
#pieces_selectionnees = [1,2,3,4,5,6,7,8,9,10,11,12]

mode_grand_chelem = False    
grand_chelem = [
    # Niveau A
    [2, 3, 6, 11, 8, 4, 5, 10, 9, 1, 7, 12],
    # Niveau B
    [2, 3, 7, 9, 8, 5, 6, 4, 10, 1, 12, 11],
    # Niveau C
    [2, 4, 6, 7, 8, 1, 3, 9, 11, 5, 12, 10],
    # Niveau D
    [3, 4, 6, 7, 8, 1, 5, 2, 11, 10, 12, 9],
    # Niveau E
    [3, 6, 7, 9, 10, 2, 12, 11, 4, 1, 5, 8],
    # Niveau F
    [2, 3, 5, 6, 4, 9, 11, 10, 8, 12, 1, 7],
    # Niveau G
    [2, 3, 5, 7, 8, 1, 9, 10, 12, 4, 11, 6],
    # Niveau H
    [2, 3, 6, 10, 11, 8, 9, 12, 4, 1, 7, 5],
    # Niveau I
    [2, 3, 6, 8, 5, 11, 9, 7, 12, 10, 1, 4],
    # Niveau J
    [2, 4, 5, 8, 7, 10, 6, 1, 12, 9, 11, 3],
    # Niveau K
    [3, 4, 5, 10, 9, 1, 6, 11, 8, 12, 7, 2],
    # Niveau L
    [2, 6, 7, 9, 11, 3, 8, 4, 5, 10, 12, 1]
]
niveau_grand_chelem = 0

class App:
    def __init__(self, page_affichée):
        pyxel.run(page_affichée.update, page_affichée.draw)

class MainMenu:
    def __init__(self):
        global musique,effets
        
        pyxel.load("ressources.pyxres")
        if musique :
            pyxel.playm(0,loop=True)

        self.pieces_cascade_liste = []  # Liste des pièces en cascade
        self.val = randint(1, 12) * 16 + 8  # Valeur initiale

        self.message = "Bienvenue dans Pythominos\nAppuyez sur Entree pour jouer"

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
            App(Choix_du_mode_et_niveaux())

    def draw(self):
        """Dessine le menu principal."""
        pyxel.cls(1)  # Efface l'écran avec une couleur de fond
        pyxel.text(36, (5 * 30 + 200) // 2, self.message, 0)  # Affiche le message

        # Dessiner les pièces en cascade
        for piece in self.pieces_cascade_liste:
            if len(piece) >= 3:  # Si la pièce contient une valeur d'image
                piece_val = piece[2]
            else:
                piece_val = self.val  # Utiliser la valeur par défaut si non spécifiée
            
            pyxel.blt(piece[0], piece[1], 0, piece_val, 16, 16, 16, 0, scale=2.0)
        pyxel.bltm(3*32+16,64,2,0,0,20*8,2*8,colkey=3,scale=2.0)


class Choix_du_mode_et_niveaux:
    def __init__(self):
        global pieces_selectionnees,grand_chelem
    
        self.grand_chelem = grand_chelem
        pyxel.load("ressources.pyxres")
        self.mode_grand_chelem = False
        self.mode_libre = False
        
        self.nom_niveau = "ABCDEFGHIJKL"
        self.selecteur = 0
        
    def update(self):

        if pyxel.btnr(pyxel.KEY_RETURN):
            if self.mode_grand_chelem :
                global pieces_selectionnees,niveau_grand_chelem,mode_grand_chelem
                
                mode_grand_chelem = True
                niveau_grand_chelem = self.selecteur
                pieces_selectionnees = [self.grand_chelem[self.selecteur][i]-1 for i in range(4)]
                App(Plateau_de_jeu(Plateau(4).clear))

            elif self.mode_libre :
                App(EcranChoixPieces(self.selecteur+1))

        if pyxel.btnr(pyxel.KEY_G):
            self.mode_grand_chelem = True
            
        if pyxel.btnr(pyxel.KEY_L):
            self.selecteur = 3 
            self.mode_libre = True
            

        if self.mode_grand_chelem or self.mode_libre:
            if pyxel.btnp(pyxel.KEY_RIGHT,repeat=20):
                if self.selecteur == 11:
                    if self.mode_grand_chelem :
                        self.selecteur = 0
                    else :
                        self.selecteur = 3

                else: 
                    self.selecteur += 1

            if pyxel.btnp(pyxel.KEY_LEFT,repeat=20):
                if self.mode_libre :
                    if self.selecteur == 3:
                        self.selecteur = 11
                    else: 
                        self.selecteur -= 1

                elif self.mode_grand_chelem :
                    if self.selecteur == 0:
                        self.selecteur = 11
                    else: 
                        self.selecteur -= 1


    def draw(self):
        pyxel.cls(1)
        if self.mode_grand_chelem : 
            for i in range(4):
                num = self.grand_chelem[self.selecteur][i]
                pyxel.bltm((4+i)*32,32*5,0,(num-1)*16,8*8,16,16,0,scale=2.0)
            pyxel.text((4*32-30),85,"Bienvenue dans le mode grand chelem choisissez votre serie",0)
            pyxel.text(4*32+16,32*4,f"Niveau {self.nom_niveau[self.selecteur]} \nPieces de depart :",0)

        elif self.mode_libre:
            pyxel.text(2*32,130,"Choisissez la taille du plateau puis appuyez sur ENTREE",0)
            for i in range(self.selecteur+1):
                for j in range(5):
                    pyxel.rect(3*32-16+i*16, 150+j*16, 16, 16, 3)
                    pyxel.rectb(3*32-16+i*16, 150+j*16, 16, 16, 2)
                    pyxel.text(3*32-16+i*16+4,155+5*16,f"{i+1}",0)
        else :
            pyxel.text(4*32,150,"Choisissez votre mode de jeu : \n\nG pour le GRAND CHELEM\nL pour le mode LIBRE",0)


class EcranChoixPieces:
    def __init__(self,nb_pieces:int):
        global pieces_selectionnees

        self.liste_pieces_deja_choisies = pieces_selectionnees
        self.liste_piece_choisies = []
        self.position_curseur = 0
        self.nb_pieces = nb_pieces
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
                
        if pyxel.btnp(pyxel.KEY_S):
            if self.nb_pieces!=0:
                if self.position_curseur not in self.liste_piece_choisies:
                    if len(self.liste_piece_choisies) < self.nb_pieces:
                        self.liste_piece_choisies.append(self.position_curseur)  
            else:
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
            global pieces_selectionnees
            if self.nb_pieces!=0:
                if self.nb_pieces==len(self.liste_piece_choisies):
                    pieces_selectionnees = self.liste_pieces_deja_choisies + self.liste_piece_choisies
                    App(Plateau_de_jeu(Plateau(len(pieces_selectionnees)).clear))
            else :
                if (self.etape == 0 and len(self.liste_piece_choisies) == 4) or \
                (self.etape > 0 and len(self.liste_piece_choisies) == 1):
                    pieces_selectionnees = self.liste_pieces_deja_choisies + self.liste_piece_choisies
                    App(Plateau_de_jeu(Plateau(len(pieces_selectionnees)).clear))

    def draw(self):
        pyxel.cls(1)
        if self.nb_pieces != 0:
            pyxel.text(3*32,3*32,f"Sélectionnez {self.nb_pieces} pieces en appuyant sur S",0)
        else:
            if self.etape==0:
                pyxel.text(3*32,3*32,"Sélectionnez 4 pieces en appuyant sur S",0)
            else:  
                pyxel.text(3*32,3*32,"Sélectionnez 1 piece en appuyant sur S",0)
        pyxel.bltm(3*32,4*32,0,0,8*8,12*16,16,0,scale=2)
        for i in self.liste_pieces_deja_choisies+self.liste_piece_choisies:
            pyxel.rect(i*32,4*32-8,32,32,1)
        pyxel.rectb(self.position_curseur*32,4*32-8,32,32,2)
        pyxel.text(3*32,5*32,"Pieces Selectionnees :",0)
        decalage = 0
        for image_piece in self.liste_pieces_deja_choisies+self.liste_piece_choisies:
            pyxel.bltm(8+decalage,6*32,0,image_piece*16,8*8,16,16,0,scale=2.0)
            decalage+=32
        pyxel.text(3*32,32*5+180,"Une fois vos pieces choisies, appuyez sur Entree pour jouer",0)

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
            global mode_grand_chelem,pieces_selectionnees
            if mode_grand_chelem:
                App(Plateau_de_jeu(Plateau(len(pieces_selectionnees)).clear))
            else :
                App(EcranChoixPieces(0))

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()


    def draw(self):
        pyxel.cls(1) 
        pyxel.text(width // 2 - len(self.message)*2, height // 2 - 4, self.message, 0)  


        for piece in self.pieces_cascade_liste:
            x, y, piece_val, _, _ = piece 
            pyxel.blt(x, y, 0, piece_val, 16, 16, 16, 0, scale=2.0)

class Ecran_de_fin:
    def __init__(self):
        global mode_grand_chelem,niveau_grand_chelem

        pyxel.load("ressources.pyxres")

        self.pieces_cascade_liste = []  # Liste des pièces en cascade [x, y, image_val, angle_rad, speed]
        self.val = randint(1, 12) * 16 + 8  # Valeur initiale
        self.piece_size = 32 

        self.nom_niveau = "ABCDEFGHIJKL"
        self.message= f"Vous avez résolu le dernier niveau de votre partie en mode libre"

        if mode_grand_chelem :
            self.message = f"Vous avez résolu le dernier niveau de la série {self.nom_niveau[niveau_grand_chelem]}"
            
    def pieces_deplacement(self):
        for piece in self.pieces_cascade_liste.copy():  
            x, y, _, angle, speed = piece

            dx = speed * math.cos(angle)
            dy = -speed * math.sin(angle)

            piece[0] += dx
            piece[1] -= dy

            if piece[1] < -self.piece_size:
                self.pieces_cascade_liste.remove(piece)
    def ajouter_piece_cascade_chelem(self):
        corner = random.randint(0, 1)
        speed = random.uniform(1.5, 3.0) 
        piece_val = randint(1, 12) * 16 + 8  

        if corner == 0:
            x_position = 0  

            angle_rad = random.uniform(0, math.pi / 2)
        else:
            x_position = width - self.piece_size 

            angle_rad = random.uniform(math.pi / 2, math.pi)

        y_position = 0
        self.pieces_cascade_liste.append([x_position, y_position, piece_val, angle_rad, speed])
        
    def update(self):
        if pyxel.btnr(pyxel.KEY_RETURN):
            global mode_grand_chelem,niveau_grand_chelem,pieces_selectionnees

            mode_grand_chelem = False
            niveau_grand_chelem = 0
            pieces_selectionnees = []
            App(MainMenu())
        self.ajouter_piece_cascade_chelem() 
        self.pieces_deplacement() 

    def draw(self):
        pyxel.cls(1)
        for piece in self.pieces_cascade_liste:
            x, y, piece_val, _, _ = piece 
            pyxel.blt(x, y, 0, piece_val, 16, 16, 16, 0, scale=2.0)
        pyxel.bltm(4*32,90,2,0,16,14*8,16,3,scale=2.0)
        pyxel.text(4*32+26,150,"Felicitations !",0)   
        pyxel.text(2*32,170,self.message,0)
        pyxel.text(3*32,200,"Appuyez sur ENTREE pour retourner au Menu Titre",0)
        

class Plateau:
    def __init__(self,taille: int):
        self.taille = taille
        self.clear = self.plateau_clear()

    def plateau_clear(self):
        plateau = [[0 for _ in range(self.taille)] for _ in range(5)]
        return plateau
    
taille = 12
plateau = Plateau(taille).clear 

class Plateau_de_jeu:
    def __init__(self, plateau, cell_size=32):
        global pieces_selectionnees,musique,effets

        pyxel.load("ressources.pyxres")

        if musique :
            pyxel.playm(1,loop=True)

        self.Dplateau = [row[:] for row in plateau]
        self.plateau = plateau
        
        self.etape = len(pieces_selectionnees)

        self.cell_size = cell_size
        self.ligne = len(plateau)
        self.cols = len(plateau[0]) if self.ligne > 0 else 0
        pyxel.colors.from_list([0x000000, 0xFFFFFF, 0x7F7F7F, 0xC3C3C3, 0x64BCED, 0x200CFF, 0xFF1E27, 0x880015, 0xFFFF00, 0xF58B1A, 0x20BD0F, 0x104F12, 0xF585B1, 0xCA42D1, 0x6325D4, 0x807625])
        self.colors = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


        self.pieces = create_pieces(self.plateau)
        self.pieces_jouables = [[self.pieces[piece],False,False] for piece in pieces_selectionnees]
        self.index_pieces_non_jouables = [i for i in range(12) if i not in pieces_selectionnees]
        self.index_piece_selectionnee = 0
        self.piece_selectionnee = self.pieces_jouables[self.index_piece_selectionnee][0]

        self.liste_des_coordonnees_des_boutons = [(32*3,32*6),(32*4,32*6),(32*5,32*6),(32*6,32*6),(32*7,32*6),(32*8,32*6),(32*3,32*7),(32*4,32*7),(32*5,32*7),(32*6,32*7),(32*7,32*7),(32*8,32*7)]
        
        self.menu_rapide = False
        self.alert_message = ""
        self.alert_timer = 0
        self.alert_duration = 50  

    def verif_victoire(self):
        for y in range(self.ligne):
            for x in range(self.cols):
                if self.plateau[y][x] == 0:
                    return False  
        return True 

    def update(self):
        pyxel.mouse(True)

        if pyxel.btnp(pyxel.KEY_M):
            self.menu_rapide = True
            if pyxel.btnp(pyxel.KEY_M):
                for piece in self.pieces_jouables :
                    piece[1] = False
                    piece[2] = False
                    piece[0].retirer()
                    piece[0].cos_de_départ()
                global pieces_selectionnees
                pieces_selectionnees = []
                App(MainMenu())
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
        
        if pyxel.btn(pyxel.KEY_C):
            for piece in self.pieces_jouables :
                piece[1] = False
                piece[2] = False
                piece[0].retirer()
                piece[0].cos_de_départ()

        if pyxel.btnp(pyxel.KEY_A):
            self.piece_selectionnee.retirer()
            self.pieces_jouables[self.index_piece_selectionnee][1] = False
            self.pieces_jouables[self.index_piece_selectionnee][2] = False
            pyxel.play(3,32)

        if pyxel.btnp(pyxel.KEY_P,repeat=10):
            self.plateau, success = self.piece_selectionnee.place_on_plateau()
            if not success :
                self.alert_message = "Placement impossible!"
                self.alert_timer = self.alert_duration
            else :  
                self.pieces_jouables[self.index_piece_selectionnee][1] = True
                self.pieces_jouables[self.index_piece_selectionnee][2] = True

        if pyxel.btnp(pyxel.KEY_R,repeat=10):
            self.Dplateau, success = self.piece_selectionnee.rotate()
            if not success:
                self.alert_message = "Rotation impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouables[self.index_piece_selectionnee][2] = True

        if pyxel.btnp(pyxel.KEY_E,repeat=8):
            self.Dplateau, success = self.piece_selectionnee.symetrie()
            if not success:
                self.alert_message = "Symetrie impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouables[self.index_piece_selectionnee][2] = True

        if pyxel.btnp(pyxel.KEY_LEFT,repeat=8):
            self.Dplateau, success = self.piece_selectionnee.deplacement(-1, 0)
            if not success:
                self.alert_message = "Deplacement impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouables[self.index_piece_selectionnee][2] = True
                pyxel.play(3,33)

        if pyxel.btnp(pyxel.KEY_RIGHT,repeat=8):
            self.Dplateau, success = self.piece_selectionnee.deplacement(1, 0)
            if not success:
                self.alert_message = "Deplacement impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouables[self.index_piece_selectionnee][2] = True
                pyxel.play(3,33)

        if pyxel.btnp(pyxel.KEY_DOWN,repeat=8):
            self.Dplateau, success = self.piece_selectionnee.deplacement(0, 1)
            if not success:
                self.alert_message = "Deplacement impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouables[self.index_piece_selectionnee][2] = True
                pyxel.play(3,33)

        if pyxel.btnp(pyxel.KEY_UP,repeat=8):
            self.Dplateau, success = self.piece_selectionnee.deplacement(0, -1)
            if not success:
                self.alert_message = "Deplacement impossible!"
                self.alert_timer = self.alert_duration
            else :
                self.pieces_jouables[self.index_piece_selectionnee][2] = True     
                pyxel.play(3,33)

        if pyxel.btnp(pyxel.KEY_N):
            if self.piece_selectionnee.etat_deplacement:
                if self.piece_selectionnee.test_placement():
                    if self.pieces_jouables[self.index_piece_selectionnee][2]:
                        self.piece_selectionnee.place_on_plateau()
                        self.pieces_jouables[self.index_piece_selectionnee][1] = True  
                    self.index_piece_selectionnee = (self.index_piece_selectionnee + 1) % len(self.pieces_jouables)
                    self.piece_selectionnee = self.pieces_jouables[self.index_piece_selectionnee][0]
                    
                    if self.pieces_jouables[self.index_piece_selectionnee][1]:
                        self.piece_selectionnee.etat_deplacement = False
                    else:
                        self.piece_selectionnee.etat_deplacement = True
                else:
                    self.piece_selectionnee.retirer()
                    self.pieces_jouables[self.index_piece_selectionnee][1] = False  
                    
                    self.index_piece_selectionnee = (self.index_piece_selectionnee + 1) % len(self.pieces_jouables)
                    self.piece_selectionnee = self.pieces_jouables[self.index_piece_selectionnee][0]
                    
                    if self.pieces_jouables[self.index_piece_selectionnee][1]:
                        self.piece_selectionnee.etat_deplacement = False
                    else:
                        self.piece_selectionnee.etat_deplacement = True
            else:
                self.index_piece_selectionnee = (self.index_piece_selectionnee + 1) % len(self.pieces_jouables)
                self.piece_selectionnee = self.pieces_jouables[self.index_piece_selectionnee][0]
                
                if self.pieces_jouables[self.index_piece_selectionnee][1]:
                    self.piece_selectionnee.etat_deplacement = False
                else:
                    self.piece_selectionnee.etat_deplacement = True

        if self.verif_victoire():
            global grand_chelem, niveau_grand_chelem, mode_grand_chelem

            self.alert_message = "Victoire!"
            self.alert_timer = self.alert_duration
            
            if self.etape == 12 :
                App(Ecran_de_fin())
            if mode_grand_chelem : 
                pieces_selectionnees = [grand_chelem[niveau_grand_chelem][i]-1 for i in range(len(pieces_selectionnees)+1)]
            App(Ecran_de_victoire())

        if pyxel.btn(pyxel.KEY_G):

            self.alert_message = "Victoire!"
            self.alert_timer = self.alert_duration

            if self.etape == 12 :
                App(Ecran_de_fin())
            if mode_grand_chelem : 
                pieces_selectionnees = [grand_chelem[niveau_grand_chelem][i]-1 for i in range(len(pieces_selectionnees)+1)]
            App(Ecran_de_victoire())
            
        
        if self.alert_timer > 0:
            self.alert_timer -= 1
        

    def draw(self):
        pyxel.cls(1)
        if self.menu_rapide :
            
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
        
        rect_cos = self.liste_des_coordonnees_des_boutons[self.piece_selectionnee.numero - 1]
        pyxel.bltm(32*3, self.ligne * self.cell_size+32, 0, 0, 0,  24*8, 8*8, 0,scale=2.0)
        pyxel.rectb(rect_cos[0],rect_cos[1],32,32,2)
        
        for i in self.index_pieces_non_jouables :
            pyxel.rect(self.liste_des_coordonnees_des_boutons[i][0],self.liste_des_coordonnees_des_boutons[i][1],32,32,1)
        
        for piece in self.pieces_jouables :
            if piece[1]:
                num = piece[0].numero - 1 
                pyxel.bltm(self.liste_des_coordonnees_des_boutons[num][0]+8,self.liste_des_coordonnees_des_boutons[num][1]+8,0,num*16,10*8,16,16,4,scale=2.0)
        
        # Afficher l'alerte si nécessaire
        if self.alert_timer > 0:
            message_x = 10
            message_y = self.ligne * self.cell_size + 150
            pyxel.text(message_x, message_y, self.alert_message, 2)

        cmd_color = 0

        hauteur_txt = 12
        nbr_col = 3
        ecart_bas = 5

        Y_normal = pyxel.height - (nbr_col * hauteur_txt) - ecart_bas

        x_left = 20
        pyxel.text(x_left, Y_normal, "C: Effacer le plateau", cmd_color)
        pyxel.text(x_left, Y_normal + hauteur_txt, "R: Rotation", cmd_color)
        pyxel.text(x_left, Y_normal + 2 * hauteur_txt, "E: Symetrie", cmd_color)


        x_mid = 145 
        pyxel.text(x_mid, Y_normal, "P: Placer Piece", cmd_color)
        pyxel.text(x_mid, Y_normal + hauteur_txt, "A: Retirer Piece", cmd_color)
        pyxel.text(x_mid, Y_normal + 2 * hauteur_txt, "N: Piece Suivante", cmd_color)

        x_right = 270
        pyxel.text(x_right, Y_normal, "G: Choix Pieces", cmd_color)
        pyxel.text(x_right, Y_normal + hauteur_txt, "M: Menu Principal", cmd_color)
        pyxel.text(x_right, Y_normal + 2 * hauteur_txt, "Q: Quitter", cmd_color)

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

        if self.etat_deplacement:
            for x, y in self.cos_actuelles:
                self.Dplateau[x][y] = self.numero

        if not self.etat_deplacement:
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
        Piece(1, [[1], \
                                [1], \
                                [1], \
                                [1], \
                                [1]], plateau),\
                                \
        Piece(2, [[2, 2],\
                                [2], \
                                [2], \
                                [2]], plateau),\
                                \
        Piece(3, [[3], \
                                [3, 3], \
                                [3], \
                                [3]], plateau),\
                                \
        Piece(4,[ [4], \
                                [4, 4], \
                                [0, 4], \
                                [0, 4]], plateau),\
                                \
        Piece(5, [[5], \
                                [5], \
                                [5, 5, 5]], plateau),\
                                \
        Piece(6, [[6], \
                                [6, 6], \
                                [6, 6]], plateau),\
                                \
        Piece(7,[ [7, 7], \
                                [0, 7], \
                                [7, 7]], plateau),\
                                \
        Piece(8,[ [8, 8], \
                                [0, 8], \
                                [0, 8, 8]], plateau),\
                                \
        Piece(9, [[9],\
                                [9, 9, 9], \
                                [0, 9]], plateau),\
                                \
        Piece(10, [[10, 10, 10], \
                                  [0, 10], \
                                  [0, 10]], plateau),\
                                \
        Piece(11, [[11], \
                                 [11, 11], \
                                  [0, 11, 11]], plateau),\
                                \
        Piece(12, [[0, 12],\
                                [12, 12, 12], \
                                 [0, 12]], plateau)\
    ]
    return pieces
 
App(MainMenu())