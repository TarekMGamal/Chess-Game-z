from pieces.piece import Piece

class Square:
    def __init__(self , x , y , color , piece = None):
        self.x = x
        self.y = y
        self.piece = piece
        self.color = color

    