import pyxel

width = 12*32
heigt = 5*32+200
pyxel.init(width,heigt,display_scale=2)
pyxel.mouse(True)

# Variable globale pour stocker les pièces choisies
pieces_selectionnees = []

class App:
    def __init__(self, page_affichée):
        pyxel.run(page_affichée.update, page_affichée.draw)

class EcranSuivant:
    def __init__(self, etape, liste_pieces):
        self.etape = etape
        self.liste_pieces = liste_pieces
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_G):
            App(EcranChoixPieces(self.etape))
            
    def draw(self):
        pyxel.cls(1)
        pyxel.text(30, 30, f"Etape {self.etape} terminee!", 7)
        pyxel.text(30, 50, f"Pieces selectionnees: {self.liste_pieces}", 7)
        pyxel.text(30, 70, "Appuyez sur G pour revenir à l'ecran de choix", 7)

class EcranChoixPieces:
    def __init__(self, etape=0):
        self.etape = etape
        global pieces_selectionnees
        self.liste_pieces_deja_choisies = pieces_selectionnees
        self.liste_piece_choisies = []
        self.position_curseur = 0
        pyxel.load("tilemap.pyxres")

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
        
        if pyxel.btnp(pyxel.KEY_E):  # Changé à btnp pour éviter répétitions
            self.liste_piece_choisies = []
            
        if pyxel.btnp(pyxel.KEY_RETURN):
            if (self.etape == 0 and len(self.liste_piece_choisies) == 4) or \
               (self.etape > 0 and len(self.liste_piece_choisies) == 1):
                # Mise à jour des variables globales
                global pieces_selectionnees
                pieces_selectionnees = self.liste_pieces_deja_choisies + self.liste_piece_choisies
                # Passer à l'écran suivant
                App(EcranSuivant(self.etape + 1, pieces_selectionnees))

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

App(EcranChoixPieces())