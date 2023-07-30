class Move:
    def __init__(self, initial_square, final_square):
        self.initial_square = initial_square
        self.final_square = final_square

    def get_initial_square(self):
        return self.initial_square

    def get_final_square(self):
        return self.final_square
