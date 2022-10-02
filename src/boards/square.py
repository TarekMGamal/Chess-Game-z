from pieces.piece import Piece

class Square:
    def __init__(self , x , y , color , piece = None):
        self.x = x
        self.y = y
        self.piece = piece
        self.color = color

    def get_row(self):
        return self.x
    
    def get_col(self):
        return self.y
    
    def get_piece(self):
        return self.piece

    def get_color(self):
        return self.color
    
    def add_piece(self , piece):
        self.piece = piece

    def change_piece(self , piece):
        self.piece = piece
    
    def remove_piece(self):
        self.piece = None