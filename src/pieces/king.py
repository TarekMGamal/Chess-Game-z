from pieces.piece import Piece
from boards.move import Move


class King(Piece):
    def __init__(self, color):
        super().__init__(color, 1000, 'king')

    @staticmethod
    def can_reach(board, initial_square, final_square):
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
        not_defended = True
        piece = initial_square.get_piece()
        x = initial_square.get_row()
        y = initial_square.get_col()

        for i in range(-1, 2):
            for j in range(-1, 2):
                final_square = board.get_square(x + i, y + j)
                if initial_square == final_square:
                    continue

                can_reach = King.can_reach(board, initial_square, final_square)

                pieces_squares = board.get_pieces_squares(board.get_opposite_color(piece.get_color()))
                for piece_square in pieces_squares:
                    enemy_piece = piece_square.get_piece()
                    piece_class = enemy_piece.__class__

                    if piece_class.can_defend(board, piece_square, final_square):
                        not_defended = False
                        break

                if can_reach and not_defended:
                    valid_move = Move(initial_square, final_square)
                    valid_moves.append(valid_move)

        return valid_moves
