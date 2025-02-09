def place(piece:list):
    print(piece)
    plateau = [[0 for _ in range (0,12)]for _ in range(0,5)]
    for Py in piece:
        for Px in Py: 
            if Px != 0:
                plateau[Px[0]][Px[1]] = 1
    return plateau

class Piece():
    def __init__(self,numero,patron:list):
        self.numero = numero
        self.patron = patron
    def tradEnCoordonnées(self,patron):
        for Py in patron:
            for Px in Py:
                if Px!=0:
                    patron[patron.index(Py)][Py.index(Px)]=[patron.index(Py),Py.index(Px)]
        self.coord=patron
        return self.coord

def piece1():
    
    piece = [[1,1],
             [1],
             [1],
             [1]]
    for Py in piece:
        for Px in range(len(Py)):
            if Py[Px] != 0:
                piece[piece.index(Py)][Px] = [piece.index(Py), Px]
    return piece
       
def piece2(): 
    piece = [[0,1],
             [1,1,1],
             [0,1]]
    for Py in piece:
        for Px in Py:
            if Px!=0:
                piece[piece.index(Py)][Py.index(Px)] = [piece.index(Py),Py.index(Px)]
    return piece

def piece3():
    piece= [[1],
            [1,1,1],
            [0,1]]
    for Py in piece:
        for Px in Py:
            if Px!=0:
                piece[piece.index(Py)][Py.index(Px)] = [piece.index(Py),Py.index(Px)]
    return piece

def piece4():
    piece=[[1],
           [1,1],
           [1,1]]
    for Py in piece:
        for Px in Py:
            if Px!=0:
                piece[piece.index(Py)][Py.index(Px)] = [piece.index(Py),Py.index(Px)]
    return piece

def deplacement(sens:str,norme:int,piece:list):
    plateau = [[0 for Tx in range (0,12)]for Ty in range(0,5)]
    print(plateau)
    if sens=='g':
        for Py in piece:
            for Px in Py:
                Px[1]-=norme
    if sens=='d':
        for Py in piece:
            for Px in Py:
                Px[1]+=norme
    if sens=='b':
        for Py in piece:
            for Px in Py:
                Px[0]+=norme
    if sens=='h':
        for Py in piece:
            for Px in Py:
                Px[0]-=norme
    for Py in piece:
        for Px in Py: 
                plateau[Px[0]][Px[1]] = 1
    return plateau