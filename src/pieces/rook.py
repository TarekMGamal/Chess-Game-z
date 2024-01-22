from pieces.piece import Piece
from boards.move import Move


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 5, 'rook')

    @staticmethod
    def can_reach(board, initial_square, final_square, consider_in_between_pieces=True):
        can_reach = False
        diff_x = final_square.get_row() - initial_square.get_row()
        diff_y = final_square.get_col() - initial_square.get_col()

        if diff_x == 0 or diff_y == 0:
            can_reach = True

            if consider_in_between_pieces:
                can_reach = not board.check_inbetween_pieces(initial_square, final_square)

        return can_reach

    @staticmethod
    def can_attack(board, initial_square, final_square):
        can_attack = False
        attacking_piece = initial_square.get_piece()
        attacked_piece = final_square.get_piece()

        can_reach = Rook.can_reach(board, initial_square, final_square)

        if attacked_piece is None:
            return can_reach

        are_different_color = attacked_piece.get_color() != attacking_piece.get_color()

        if can_reach and are_different_color:
            can_attack = True

        return can_attack

    @staticmethod
    def can_defend(board, initial_square, final_square):
        can_defend = False
        attacking_piece = initial_square.get_piece()
        attacked_piece = final_square.get_piece()

        can_reach = Rook.can_reach(board, initial_square, final_square)
        are_same_color = attacked_piece.get_color() == attacking_piece.get_color()

        if can_reach and are_same_color:
            can_defend = True

        return can_defend

    @staticmethod
    def calculate_valid_moves(board, initial_square):
        valid_moves = []
        piece = initial_square.get_piece()
        x = initial_square.get_row()
        y = initial_square.get_col()

        for i in range(0, 8):
            for j in range(0, 8):
                final_square = board.get_square(i, j)
                index_x = final_square.get_row()
                index_y = final_square.get_col()

                if Rook.can_attack(board, initial_square, final_square):
                    # check for pins
                    direction_tuple = (board.get_sign(index_x - x), board.get_sign(index_y - y))
                    reverse_direction_tuple = (-board.get_sign(index_x - x), -board.get_sign(index_y - y))

                    if not piece.is_pinned or piece.get_pin_direction() == direction_tuple \
                            or piece.get_pin_direction() == reverse_direction_tuple:
                        valid_move = Move(initial_square, final_square)
                        valid_moves.append(valid_move)

        return valid_moves
