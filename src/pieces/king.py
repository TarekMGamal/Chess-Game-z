from pieces.piece import Piece

class King(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.value = 1000
        self.name = 'king'