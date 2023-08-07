class Square:
    def __init__(self, x, y, color, highlight_color, piece=None):
        self.x = x
        self.y = y
        self.piece = piece
        self.color = color
        self.is_highlighted = False
        self.highlight_color = highlight_color

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
        return self.highlight_color if self.is_highlighted else self.color

    def set_color(self, new_color):
        self.color = new_color

    def highlight(self):
        self.is_highlighted = True

    def clear_highlight(self):
        self.is_highlighted = False

    def add_piece(self, piece):
        self.piece = piece

    def change_piece(self, piece):
        self.piece = piece

    def remove_piece(self):
        self.piece = None
