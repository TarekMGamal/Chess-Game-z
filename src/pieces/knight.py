from pieces.piece import Piece

class Knight(Piece):
    def __init__(self , color):
        super().__init__(color)
        self.value = 3
        self.name = 'knight'
    
    def get_value(self):
        return self.value
    
    def get_name(self):
        return self.name