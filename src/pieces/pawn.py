from pieces.piece import Piece
from boards.move import Move


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 1, 'pawn')

    @staticmethod
    def can_reach(board, initial_square, final_square, consider_in_between_pieces=True):
        can_reach = False

        if initial_square is None or final_square is None:
            return can_reach

        row_diff = final_square.get_row() - initial_square.get_row()
        col_diff = final_square.get_col() - initial_square.get_col()
        pawn = initial_square.get_piece()

        if row_diff == board.get_board_direction() and col_diff == 0:
            # pawn push
            can_reach = True
        elif row_diff == board.get_board_direction() * 2 and col_diff == 0 and not pawn.get_is_moved():
            # pawn first move
            if consider_in_between_pieces:
                intermediate_square = board.get_square(initial_square.get_row() + 1, initial_square.get_col())

                if intermediate_square is not None and intermediate_square.get_piece() is None:
                    can_reach = True
            else:
                can_reach = True
        elif abs(col_diff) == 1 and row_diff == board.get_board_direction():
            # pawn takes
            if final_square.get_piece() is not None:
                if final_square.get_piece().get_color() != pawn.get_color():
                    can_reach = True

        # enpassant
        last_move_final_square_x = board.last_move.get_final_square().get_row()
        last_move_final_square_y = board.last_move.get_final_square().get_col()

        if board.last_move is not None:
            if board.last_move.get_final_square().get_piece() is not None:
                if board.last_move.get_final_square().get_piece().get_name() == 'pawn':
                    if last_move_final_square_x == initial_square.get_row():
                        if abs(last_move_final_square_y - initial_square.get_col()) == 1:
                            if abs(board.last_move.get_initial_square().get_row() - last_move_final_square_x) == 2:
                                cur_final_square = board.get_square(
                                    initial_square.get_row() + board.get_board_direction(), last_move_final_square_y)

                                if cur_final_square == final_square:
                                    can_reach = True

        return can_reach

    @staticmethod
    def can_attack(board, initial_square, final_square):
        can_attack = False

        attacking_piece = initial_square.get_piece()
        attacked_piece = final_square.get_piece()

        row_diff = final_square.get_row() - initial_square.get_row()
        col_diff = final_square.get_col() - initial_square.get_col()

        if abs(col_diff) == 1 and row_diff == board.get_board_direction():
            # pawn takes
            can_attack = True

        # # enpassant
        # last_move_final_square_x = board.last_move.get_final_square().get_row()
        # last_move_final_square_y = board.last_move.get_final_square().get_col()
        #
        # if board.last_move is not None:
        #     if board.last_move.get_final_square().get_piece() is not None:
        #         if board.last_move.get_final_square().get_piece().get_name() == 'pawn':
        #             if last_move_final_square_x == initial_square.get_row():
        #                 if abs(last_move_final_square_y - initial_square.get_col()) == 1:
        #                     if abs(board.last_move.get_initial_square().get_row() - last_move_final_square_x) == 2:
        #                         cur_final_square = board.get_square(
        #                             initial_square.get_row() + board.get_board_direction(), last_move_final_square_y)
        #
        #                         if cur_final_square == final_square:
        #                             can_attack = True

        are_different_color = attacked_piece.get_color() != attacking_piece.get_color()

        if can_attack and are_different_color:
            can_attack = True
        else:
            can_attack = False

        return can_attack

    @staticmethod
    def can_defend(board, initial_square, final_square):
        can_defend = False

        if initial_square is None or final_square is None:
            return can_defend

        attacking_piece = initial_square.get_piece()
        attacked_piece = final_square.get_piece()

        row_diff = final_square.get_row() - initial_square.get_row()
        col_diff = final_square.get_col() - initial_square.get_col()

        if abs(col_diff) == 1 and row_diff == -1 * board.get_board_direction():
            # pawn takes
            can_defend = True

        # enpassant
        last_move_final_square_x = board.last_move.get_final_square().get_row()
        last_move_final_square_y = board.last_move.get_final_square().get_col()

        if board.last_move is not None:
            if board.last_move.get_final_square().get_piece() is not None:
                if board.last_move.get_final_square().get_piece().get_name() == 'pawn':
                    if last_move_final_square_x == initial_square.get_row():
                        if abs(last_move_final_square_y - initial_square.get_col()) == 1:
                            if abs(board.last_move.get_initial_square().get_row() - last_move_final_square_x) == 2:
                                cur_final_square = board.get_square(
                                    initial_square.get_row() + board.get_board_direction(), last_move_final_square_y)

                                if cur_final_square == final_square:
                                    can_defend = True

        are_different_color = True
        if attacked_piece is not None:
            are_different_color = attacked_piece.get_color() == attacking_piece.get_color()

        if can_defend and are_different_color:
            can_defend = True
        else:
            can_defend = False

        return can_defend

    @staticmethod
    def calculate_valid_moves(board, initial_square):
        valid_moves = []
        piece = initial_square.get_piece()
        x = initial_square.get_row()
        y = initial_square.get_col()

        for i in [x + board.get_board_direction(), x + (board.get_board_direction() * 2)]:
            if i == x + (board.get_board_direction() * 2) and piece.get_is_moved():
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
