from pieces.piece import Piece


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 3, 'knight')
