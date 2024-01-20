from pieces.piece import Piece
from boards.move import Move


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 1, 'pawn')

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

        for i in [x + board.get_board_direction(), x + (board.get_board_direction() * 2)]:
            if i == x + (board.get_board_direction() * 2) and piece.is_moved():
                continue
            if not board.in_board(i, y):
                break

            final_square = board.get_square(i, y)
            direction_tuple = (board.get_sign(i - x), 0)
            reverse_direction_tuple = (-board.get_sign(i - x), 0)

            if final_square.get_piece() is not None:
                break
            else:
                if final_square.get_row() == 0 or final_square.get_row() == 7:
                    is_promotion = True
                else:
                    is_promotion = False

                valid_move = Move(initial_square, final_square, promotion=is_promotion)
                if not piece.get_is_pinned() or piece.get_pin_direction() == direction_tuple \
                        or piece.get_pin_direction() == reverse_direction_tuple:
                    valid_moves.append(valid_move)

        for j in [y - 1, y + 1]:
            if not board.in_board(x + board.get_board_direction(), j):
                continue

            final_square = board.get_square(x + board.get_board_direction(), j)
            direction_tuple = (board.get_sign(x + board.get_board_direction() - x), board.get_sign(j - y))
            reverse_direction_tuple = (-board.get_sign(x + board.get_board_direction() - x), -board.get_sign(j - y))

            if final_square.get_piece() is not None:
                if final_square.get_piece().get_color() != piece.get_color():
                    if final_square.get_row() == 0 or final_square.get_row() == 7:
                        is_promotion = True
                    else:
                        is_promotion = False

                    valid_move = Move(initial_square, final_square, promotion=is_promotion)
                    if not piece.get_is_pinned() or piece.get_pin_direction() == direction_tuple \
                            or piece.get_pin_direction() == reverse_direction_tuple:
                        valid_moves.append(valid_move)

        # enpassant conditions
        last_move_final_square_x = board.last_move.get_final_square().get_row()
        last_move_final_square_y = board.last_move.get_final_square().get_col()

        if board.last_move is not None:
            if board.last_move.get_final_square().get_piece() is not None:
                if board.last_move.get_final_square().get_piece().get_name() == 'pawn':
                    if last_move_final_square_x == x:
                        if last_move_final_square_y == y + 1 or last_move_final_square_y == y - 1:
                            if abs(board.last_move.get_initial_square().get_row() - last_move_final_square_x) == 2:
                                final_square = board.get_square(initial_square.get_row() + board.get_board_direction(),
                                                                last_move_final_square_y)
                                direction_tuple = (board.get_sign(final_square.get_row() - x),
                                                   board.get_sign(final_square.get_col() - y))
                                reverse_direction_tuple = (-board.get_sign(final_square.get_row() - x),
                                                           -board.get_sign(final_square.get_col() - y))

                                en_passant_move = Move(initial_square, final_square, en_passant=True)
                                if not piece.get_is_pinned() or piece.get_pin_direction() == direction_tuple \
                                        or piece.get_pin_direction() == reverse_direction_tuple:
                                    valid_moves.append(en_passant_move)

        return valid_moves
