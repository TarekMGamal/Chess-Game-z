from pieces.piece import Piece
from boards.move import Move


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 5, 'rook')

        self.moved = False

    def is_moved(self):
        return self.moved

    def set_moved(self):
        self.moved = True

    @staticmethod
    def calculate_valid_moves(board, initial_square):
        valid_moves = []
        piece = initial_square.get_piece()
        x = initial_square.get_row()
        y = initial_square.get_col()

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0) or (i != 0 and j != 0):
                    continue

                range_end_x = 8 if i == 1 else -1
                range_end_y = 8 if j == 1 else -1

                range_start = x if i != 0 else y
                range_end = range_end_x if i != 0 else range_end_y

                increment = i if i != 0 else j

                for index in range(range_start + increment, range_end, increment):
                    index_x = index if i != 0 else x
                    index_y = index if j != 0 else y

                    if not board.in_board(index_x, index_y):
                        continue

                    final_square = board.get_square(index, y) if i != 0 else board.get_square(x, index)

                    if final_square.get_piece() is not None:
                        if final_square.get_piece().get_color() != piece.get_color():
                            move = Move(initial_square, final_square)
                            valid_moves.append(move)
                        break
                    else:
                        move = Move(initial_square, final_square)
                        valid_moves.append(move)

        return valid_moves
