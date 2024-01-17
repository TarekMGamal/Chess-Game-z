from pieces.piece import Piece
from pieces.rook import Rook
from pieces.bishop import Bishop


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 9, 'queen')

    @staticmethod
    def calculate_valid_moves(board, initial_square):
        rook_moves = Rook.calculate_valid_moves(board, initial_square)
        bishop_moves = Bishop.calculate_valid_moves(board, initial_square)

        valid_moves = rook_moves + bishop_moves

        return valid_moves
