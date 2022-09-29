from pieces.piece import Piece

class Pawn(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 1
        self.name = 'pawn'