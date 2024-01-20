from pieces.piece import Piece
from boards.move import Move


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 5, 'rook')

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

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0) or (i != 0 and j != 0):
                    continue

                range_end_x = 8 if i == 1 else -1
                range_end_y = 8 if j == 1 else -1

                range_start = x if i != 0 else y
                range_end = range_end_x if i != 0 else range_end_y

                increment = i if i != 0 else j

                for index in range(range_start + increment, range_end, increment):
                    index_x = index if i != 0 else x
                    index_y = index if j != 0 else y

                    if not board.in_board(index_x, index_y):
                        continue

                    final_square = board.get_square(index, y) if i != 0 else board.get_square(x, index)
                    direction_tuple = (board.get_sign(index_x - x), board.get_sign(index_y - y))
                    reverse_direction_tuple = (-board.get_sign(index_x - x), -board.get_sign(index_y - y))

                    if final_square.get_piece() is not None:
                        if final_square.get_piece().get_color() != piece.get_color():
                            valid_move = Move(initial_square, final_square)
                            if piece.get_pin_direction() == () or piece.get_pin_direction() == direction_tuple \
                                    or piece.get_pin_direction() == reverse_direction_tuple:
                                valid_moves.append(valid_move)
                        break
                    else:
                        valid_move = Move(initial_square, final_square)
                        if piece.get_pin_direction() == () or piece.get_pin_direction() == direction_tuple \
                                or piece.get_pin_direction() == reverse_direction_tuple:
                            valid_moves.append(valid_move)

        return valid_moves
