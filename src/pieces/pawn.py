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

            if final_square.get_piece() is not None:
                break
            else:
                if final_square.get_row() == 0 or final_square.get_row() == 7:
                    is_promotion = True
                else:
                    is_promotion = False

                new_move = Move(initial_square, final_square, promotion=is_promotion)
                valid_moves.append(new_move)

        for j in [y - 1, y + 1]:
            if not board.in_board(x + board.get_board_direction(), j):
                continue

            final_square = board.get_square(x + board.get_board_direction(), j)

            if final_square.get_piece() is not None:
                if final_square.get_piece().get_color() != piece.get_color():
                    if final_square.get_row() == 0 or final_square.get_row() == 7:
                        is_promotion = True
                    else:
                        is_promotion = False

                    new_move = Move(initial_square, final_square, promotion=is_promotion)
                    valid_moves.append(new_move)

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
                                en_passant = Move(initial_square, final_square, en_passant=True)
                                valid_moves.append(en_passant)

        return valid_moves
