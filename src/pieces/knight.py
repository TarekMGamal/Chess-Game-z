from pieces.piece import Piece
from boards.move import Move


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 3, 'knight')

    @staticmethod
    def calculate_valid_moves(board, initial_square):
        valid_moves = []
        piece = initial_square.get_piece()
        x = initial_square.get_row()
        y = initial_square.get_col()

        if piece.get_is_pinned():
            return valid_moves

        for i in range(-2, 3):
            for j in range(-2, 3):
                final_square = board.get_square(x + i, y + j)

                if abs(i) + abs(j) != 3 or not board.in_board(x + i, y + j):
                    continue
                if final_square.get_piece() is not None and final_square.get_piece().get_color() == piece.get_color():
                    continue

                valid_move = Move(initial_square, final_square)
                valid_moves.append(valid_move)

        return valid_moves
