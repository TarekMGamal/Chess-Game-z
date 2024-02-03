from pieces.piece import Piece
from boards.move import Move


class King(Piece):
    def __init__(self, color):
        super().__init__(color, 1000, 'king')

    @staticmethod
    def can_reach(board, initial_square, final_square, consider_in_between_pieces=True):
        can_reach = False

        if initial_square is None or final_square is None:
            return can_reach
        if not board.in_board(final_square.get_row(), final_square.get_col()):
            return can_reach

        row_diff = abs(final_square.get_row() - initial_square.get_row())
        col_diff = abs(final_square.get_col() - initial_square.get_col())

        if row_diff <= 1 and col_diff <= 1:
            can_reach = True

        return can_reach

    @staticmethod
    def can_attack(board, initial_square, final_square):
        can_attack = False
        not_defended = True

        if initial_square is None or final_square is None:
            return can_attack

        can_reach = King.can_reach(board, initial_square, final_square)

        attacking_piece = initial_square.get_piece()
        attacked_piece = final_square.get_piece()

        are_different_color = attacked_piece.get_color() != attacking_piece.get_color()

        pieces_squares = board.get_pieces_squares(attacked_piece.get_color())
        for piece_square in pieces_squares:
            piece = piece_square.get_piece()
            piece_class = piece.__class__

            if piece_class.can_defend(board, piece_square, final_square):
                not_defended = False
                break

        if can_reach and are_different_color and not_defended:
            can_attack = True

        return can_attack

    @staticmethod
    def can_defend(board, initial_square, final_square):
        can_defend = False

        if initial_square is None or final_square is None:
            return can_defend

        can_reach = King.can_reach(board, initial_square, final_square)

        attacking_piece = initial_square.get_piece()
        attacked_piece = final_square.get_piece()

        are_same_color = True
        if attacked_piece is not None:
            are_same_color = attacked_piece.get_color() == attacking_piece.get_color()

        if can_reach and are_same_color:
            can_defend = True

        return can_defend

    @staticmethod
    def calculate_valid_moves(board, initial_square):
        valid_moves = []
        king = initial_square.get_piece()
        x = initial_square.get_row()
        y = initial_square.get_col()

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if not board.in_board(x + i, y + j):
                    continue

                final_square = board.get_square(x + i, y + j)
                if final_square.get_piece() is not None and final_square.get_piece().get_color() == king.get_color():
                    continue

                initial_square.remove_piece()
                if not board.check_is_protected(final_square, board.get_opposite_color(king.get_color())):
                    new_move = Move(initial_square, final_square)
                    valid_moves.append(new_move)
                initial_square.add_piece(king)

        # castling moves handling
        # there are more handling at "execute_move" function
        # we have two rooks: right rook at (king.x, king.y + 3) & left rook at (king.x, king.y - 4)
        # final king squares are: (king.x, king.y + 2) for right castling & (king.x, king.y - 2) for left castling
        # final rook squares are: (king.x, king.y + 1) for right castling & (king.x, king.y - 1) for left castling

        right_rook_square = board.get_square(x, y + 3)
        left_rook_square = board.get_square(x, y - 4)

        if board.can_castle(initial_square, right_rook_square):
            y_increment = 2
            can_castle = True
        elif board.can_castle(initial_square, left_rook_square):
            y_increment = -2
            can_castle = True
        else:
            y_increment = 0
            can_castle = False

        if can_castle:
            final_square = board.get_square(x, y + y_increment)
            castle_move = Move(initial_square, final_square, castling=True)
            valid_moves.append(castle_move)

        return valid_moves
