from piece import Piece


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 9, 'queen')
