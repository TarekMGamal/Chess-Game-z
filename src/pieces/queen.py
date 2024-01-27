from pieces.piece import Piece
from pieces.rook import Rook
from pieces.bishop import Bishop


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 9, 'queen')

    @staticmethod
    def can_reach(board, initial_square, final_square, consider_in_between_pieces=True):
        can_reach = Bishop.can_reach(board, initial_square, final_square, consider_in_between_pieces)
        can_reach |= Rook.can_reach(board, initial_square, final_square, consider_in_between_pieces)

        return can_reach

    @staticmethod
    def can_attack(board, initial_square, final_square):
        can_attack = Bishop.can_attack(board, initial_square, final_square)
        can_attack |= Rook.can_attack(board, initial_square, final_square)

        return can_attack

    @staticmethod
    def can_defend(board, initial_square, final_square):
        can_defend = Bishop.can_defend(board, initial_square, final_square)
        can_defend |= Rook.can_defend(board, initial_square, final_square)

        return can_defend

    @staticmethod
    def calculate_valid_moves(board, initial_square):
        rook_moves = Rook.calculate_valid_moves(board, initial_square)
        bishop_moves = Bishop.calculate_valid_moves(board, initial_square)

        valid_moves = rook_moves + bishop_moves

        return valid_moves
