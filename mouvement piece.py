def place(piece:list):
    print(piece)
    plateau = [[0 for _ in range (0,12)]for _ in range(0,5)]
    for Py in piece:
        for Px in Py: 
            if Px != 0:
                plateau[Px[0]][Px[1]] = 1
    return plateau

class Piece():
    def __init__(self, numero, patron: list):
        self.numero = numero
        self.patron = patron
        self.coord = self.convert_to_coordinates()
        self.plateau = self.place()
        

def piece1():
    numPiece=1
    piece = [[1,1],
             [1],
             [1],
             [1]]
    return convert_piece(piece)
       
def piece2(): 
    numPiece=2
    piece = [[0,2],
             [2,2,2],
             [0,2]]
    return convert_piece(piece)

def piece3():
    numPiece=3
    piece = [[3],
             [3,3,3],
             [0,3]]
    return convert_piece(piece)

def piece4():
    numPiece=4
    piece = [[4],
             [4,4],
             [4,4]]
    return convert_piece(piece)

def piece5():
    numPiece=5
    piece=[[5],
           [5],
           [5,5,5]]
    return convert_piece(piece)

def piece6():
    numPiece=6
    piece=[[6,6,6],
           [0,6],
           [0,6]]
    return convert_piece(piece)

def piece7():
    numPiece=7
    piece=[[7],
           [7,7],
           [0,7,7],]
    return convert_piece(piece)

def piece8():
    numPiece=8
    piece=[[8],
           [8,8],
           [8],
           [8]]
    return convert_piece(piece)

def piece9():
    numPiece=9
    piece=[[9],
           [9],
           [9],
           [9],
           [9]]
    return convert_piece(piece)

def piece10():
    numPiece=10
    piece=[[10,10],
           [0,10],
           [0,10,10]]
    return convert_piece(piece)

def piece11():
    numPiece=11
    piece=[[11,11],
           [0,11],
           [11,11]]
    return convert_piece(piece)

def piece12():
    numPiece=12
    piece=[[12],
           [12],
           [12,12],
           [0,12],]
    return convert_piece(piece)


plateau = [[0 for Tx in range (0,12)]for Ty in range(0,5)]

def deplacement(sens:str,norme:int,piece:list):
    plateau = [[0 for Tx in range (0,12)]for Ty in range(0,5)]
    print(plateau)
    nouvPiece=piece.copy()
    if sens=='g':
        for Py in nouvPiece:
            for Px in Py:
                Px[1]-=norme
    if sens=='d':
        for Py in nouvPiece:
            for Px in Py:
                Px[1]+=norme
    if sens=='b':
        for Py in nouvPiece:
            for Px in Py:
                Px[0]+=norme
    if sens=='h':
        for Py in nouvPiece:
            for Px in Py:
                Px[0]-=norme
    for Py in nouvPiece:
        for Px in Py: 
                plateau[Px[0]][Px[1]] = 1
    return plateau,nouvPiece

def rotation(plateau):
    piece_coordinates=[]
    for i, plateau_row in enumerate(plateau):
        row=[]
        for j, piece_coordinate in enumerate(plateau_row):
            if piece_coordinate == 1:
                row.append([i, j])
        piece_coordinates.append(row)
    while [] in piece_coordinates:
        piece_coordinates.pop(piece_coordinates.index([]))
    print(piece_coordinates)
    pO_Coordinate=piece_coordinates.copy()
    translation_y=0
    translation_x=0
    while pO_Coordinate[0][0]!=[0,0]:
        while pO_Coordinate[0][0][0]!=0:
            pO_Coordinate[0][0][0]-=1
            translation_y+=1
        while pO_Coordinate[0][0][1]!=0:
            pO_Coordinate[0][0][1]-=1
            translation_x+=1
    plateau=[[0 for Tx in range (0,12)]for Ty in range(0,5)]
    print(pO_Coordinate)
    print(piece_coordinates)
    for row in piece_coordinates:
        for point_coordinate in row:
            point_coordinate[0]-=translation_y
            point_coordinate[1]-=translation_x
            print(point_coordinate)
            plateau[point_coordinate[0]][point_coordinate[1]]=1
    return plateau

    # nouvPiece=[]
    # #origin = piece_coordinates[0][0]
    # for ligne in piece_coordinates:
    #     for coordonnées in ligne:
    #         print(type(coordonnées))
    #         nouvCo=[]
    #         nouvCo.append(-coordonnées[1])
    #         nouvCo.append(coordonnées[0])
            
    #         print(nouvCo)
    #         nouvPiece.append(nouvCo)
    #         plateau[nouvCo[0]][nouvCo[1]]=1
    # print(nouvPiece)
    # return plateau

def convert_piece(piece: list) -> list:
    new_piece = []
    for i, row in enumerate(piece):
        new_row = []
        for j, val in enumerate(row):
            if val != 0:
                new_row.append([i, j])
            else:
                new_row.append(0)
        new_piece.append(new_row)
    return new_piece

plateau1=  [[0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# def rotation(plateau):
#     piece_coordinates=[]
#     for i, plateau_row in enumerate(plateau):
#         for j, piece_coordinate in enumerate(plateau_row):
#             if piece_coordinate == 1:
#                 piece_coordinates.append([i, j])
#     print(piece_coordinates)
#     nouvPiece=[]
#     matrice=[[0,-1],[0,1]]

    # for ligne in nouvPiece:
    #     for coordonnées in ligne:
    #         coordonnées[0]+=translation[0]
    #         coordonnées[1]+=translation[1]
    # origine[0]+=translation[0]
    # origine[1]+=translation[1]
    # nouvPiece = []
    # for ligne in nouvPiece:
    #     for coordonnées in ligne:
    #         nouvCoo=["",""]
    #         nouvCoo[0] -= coordonnées[1]
    #         nouvCoo[1] = coordonnées[0]
    #         nouvCoo[0] -= translation[0]
    #         nouvCoo[1] -= translation
    #         nouvPiece.append(nouvCoo)
    #         plateau[nouvCoo[0]][nouvCoo[1]]=1
    # return plateau







