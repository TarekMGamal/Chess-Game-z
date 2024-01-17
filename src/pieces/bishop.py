from pieces.piece import Piece
from boards.move import Move


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 3.1, 'bishop')

    @staticmethod
    def calculate_valid_moves(board, initial_square):
        valid_moves = []
        piece = initial_square.get_piece()
        x = initial_square.get_row()
        y = initial_square.get_col()

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 or j == 0:
                    continue

                range_end_x = 8 if i == 1 else -1
                range_end_y = 8 if j == 1 else -1

                for index_x, index_y in zip(range(x + i, range_end_x, i), range(y + j, range_end_y, j)):
                    final_square = board.get_square(index_x, index_y)

                    if not board.in_board(index_x, index_y):
                        continue
                    if final_square.get_piece() is not None and \
                            final_square.get_piece().get_color() == piece.get_color():
                        break

                    valid_move = Move(initial_square, final_square)
                    valid_moves.append(valid_move)

                    # bishop can't jump over pieces
                    if final_square.get_piece() is not None:
                        break

        return valid_moves
