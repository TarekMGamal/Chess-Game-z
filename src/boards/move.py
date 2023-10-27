class Move:
    def __init__(self, initial_square, final_square, castling=False, en_passant=False, promotion=False):
        self.initial_square = initial_square
        self.final_square = final_square
        self.castling = castling
        self.en_passant = en_passant
        self.promotion = promotion

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

    def is_castling(self):
        return self.castling

    def set_castling(self):
        self.castling = True

    def is_en_passant(self):
        return self.en_passant

    def set_en_passant(self):
        self.en_passant = True

    def is_promotion(self):
        return self.promotion

    def set_promotion(self):
        self.promotion = True
