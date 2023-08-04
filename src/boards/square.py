class Square:
    def __init__(self, x, y, color, piece=None):
        self.x = x
        self.y = y
        self.piece = piece
        self.color = color

    def __eq__(self, other):
        if not isinstance(other, Square):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        if not isinstance(other, Square):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return not self.__eq__(other)

    def get_row(self):
        return self.x

    def get_col(self):
        return self.y

    def get_piece(self):
        return self.piece

    def get_color(self):
        return self.color

    def add_piece(self, piece):
        self.piece = piece

    def change_piece(self, piece):
        self.piece = piece

    def remove_piece(self):
        self.piece = None
