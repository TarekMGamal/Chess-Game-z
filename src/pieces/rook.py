from pieces.piece import Piece

class Rook(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 5
        self.name = 'rook'