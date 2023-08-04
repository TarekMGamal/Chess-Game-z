class Move:
    def __init__(self, initial_square, final_square):
        self.initial_square = initial_square
        self.final_square = final_square

    def __eq__(self, other):
        if not isinstance(other, Move):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.initial_square == other.initial_square and self.final_square == other.final_square

    def __ne__(self, other):
        if not isinstance(other, Move):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return not self.__eq__(other)

    def get_initial_square(self):
        return self.initial_square

    def get_final_square(self):
        return self.final_square
