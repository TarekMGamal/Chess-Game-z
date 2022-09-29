from pieces.piece import Piece

class Bishop(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 1000

