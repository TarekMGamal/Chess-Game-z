from pieces.piece import Piece


class King(Piece):
    def __init__(self, color):
        super().__init__(color, 1000, 'king')

        self.moved = False

    def is_moved(self):
        return self.moved

    def set_moved(self):
        self.moved = True
