from pieces.piece import Piece
from boards.move import Move


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 3, 'knight')

    @staticmethod
    def can_reach(board, initial_square, final_square, consider_in_between_pieces=True):
        can_reach = False

        if initial_square is None or final_square is None:
            return can_reach

        knight = initial_square.get_piece()
        if knight.get_is_pinned():
            return can_reach

        row_diff = abs(final_square.get_row() - initial_square.get_row())
        col_diff = abs(final_square.get_col() - initial_square.get_col())

        can_reach = board.in_board(final_square.get_row(), final_square.get_col())
        can_reach &= (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

        return can_reach

    @staticmethod
    def can_attack(board, initial_square, final_square):
        if initial_square is None or final_square is None:
            return False

        can_attack = False
        can_reach = Knight.can_reach(board, initial_square, final_square)

        attacking_piece = initial_square.get_piece()
        attacked_piece = final_square.get_piece()
        if can_reach:
            if attacked_piece is None or attacked_piece.get_color() != attacking_piece.get_color():
                can_attack = True

        return can_attack

    @staticmethod
    def can_defend(board, initial_square, final_square):
        can_defend = False

        if initial_square is None or final_square is None:
            return can_defend

        can_reach = Knight.can_reach(board, initial_square, final_square)

        attacking_piece = initial_square.get_piece()
        attacked_piece = final_square.get_piece()
        if can_reach:
            if attacked_piece is None or attacked_piece.get_color() == attacking_piece.get_color():
                can_defend = True

        return can_defend

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

                if Knight.can_attack(board, initial_square, final_square):
                    valid_move = Move(initial_square, final_square)
                    valid_moves.append(valid_move)

        return valid_moves
