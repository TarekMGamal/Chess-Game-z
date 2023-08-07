from boards.square import Square
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.king import King
from pieces.queen import Queen
from pieces.pawn import Pawn
from pieces.rook import Rook
from boards.move import Move


class Board:
    def __init__(self):
        self.squares = [[0] * 8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                color = 'white' if (i + j) % 2 == 0 else 'dark grey'
                self.squares[i][j] = Square(i, j, color, "yellow")

        for color in ['black', 'white']:
            if color == 'black':
                pieces_row, pawns_row = 0, 1
            else:
                pieces_row, pawns_row = 7, 6

            self.add_piece(Rook(color), pieces_row, 0)
            self.add_piece(Rook(color), pieces_row, 7)
            self.add_piece(Knight(color), pieces_row, 1)
            self.add_piece(Knight(color), pieces_row, 6)
            self.add_piece(Bishop(color), pieces_row, 2)
            self.add_piece(Bishop(color), pieces_row, 5)
            self.add_piece(Queen(color), pieces_row, 3)
            self.add_piece(King(color), pieces_row, 4)

            for j in range(8):
                self.add_piece(Pawn(color), pawns_row, j)

    def add_piece(self, piece, x, y):
        self.squares[x][y].add_piece(piece)

    def change_piece(self, piece, x, y):
        self.squares[x][y].change_piece(piece)

    def get_piece(self, x, y):
        return self.squares[x][y].get_piece()

    def get_square(self, x, y):
        if not self.in_board(x, y):
            return None
        else:
            return self.squares[x][y]

    def get_squares(self):
        return self.squares

    def execute_en_passant(self, move):
        pass

    def execute_promotion(self, move):
        pass

    def execute_castling(self, move):
        initial_square = move.get_initial_square()
        final_square = move.get_final_square()

        if final_square.get_col() > initial_square.get_col():
            # castle right side
            rook_initial_square = self.get_square(initial_square.get_row(), initial_square.get_col() + 3)
            rook_final_square = self.get_square(initial_square.get_row(), initial_square.get_col() + 1)

            rook = rook_initial_square.get_piece()

            rook_initial_square.remove_piece()
            rook_final_square.add_piece(rook)
        else:
            # castle left side
            rook_initial_square = self.get_square(initial_square.get_row(), initial_square.get_col() - 4)
            rook_final_square = self.get_square(initial_square.get_row(), initial_square.get_col() - 1)

            rook = rook_final_square.get_piece()

            rook_initial_square.remove_piece()
            rook_final_square.add_piece(rook)

    def execute_move(self, move):
        initial_square = move.get_initial_square()
        final_square = move.get_final_square()

        piece = initial_square.get_piece()
        initial_square.remove_piece()

        old_piece = final_square.get_piece()
        if old_piece is None:
            final_square.add_piece(piece)
        else:
            old_piece.kill_piece()
            final_square.change_piece(piece)

        # handling special moves
        if isinstance(piece, King) or isinstance(piece, Rook) or isinstance(piece, Pawn):
            piece.set_moved()

        if move.is_castling():
            self.execute_castling(move)
        if move.is_en_passant():
            self.execute_en_passant(move)
        if move.is_promotion():
            self.execute_promotion(move)

    def get_valid_moves(self, square):
        piece = square.get_piece()
        x = square.get_row()
        y = square.get_col()
        empty_valid_moves = []

        if piece is None:
            return empty_valid_moves
        elif piece.get_name() == 'pawn':
            return self.get_pawn_valid_moves(piece, x, y)
        elif piece.get_name() == 'king':
            return self.get_king_valid_moves(piece, x, y)
        elif piece.get_name() == 'queen':
            return self.get_queen_valid_moves(piece, x, y)
        elif piece.get_name() == 'rook':
            return self.get_rook_valid_moves(piece, x, y)
        elif piece.get_name() == 'bishop':
            return self.get_bishop_valid_moves(piece, x, y)
        elif piece.get_name() == 'knight':
            return self.get_knight_valid_moves(piece, x, y)
        else:
            return empty_valid_moves

    def in_board(self, x, y):
        return True if 8 > x >= 0 and 8 > y >= 0 else False

    def can_castle(self, king_square, rook_square):
        if king_square is None or rook_square is None:
            return False
        if not isinstance(king_square.get_piece(), King) or not isinstance(rook_square.get_piece(), Rook):
            return False

        king = king_square.get_piece()
        rook = rook_square.get_piece()

        if king.is_moved() or rook.is_moved():
            return False

        increment = 1 if rook_square.get_col() > king_square.get_col() else -1

        row = king_square.get_row()
        for col in range(king_square.get_col() + increment, rook_square.get_col(), increment):
            if not self.in_board(row, col):
                return False

            cur_square = self.squares[row][col]
            if cur_square.get_piece() is not None:
                return False

        return True

    def get_pawn_valid_moves(self, piece, x, y):
        valid_moves = []
        squares = self.squares
        initial_square = squares[x][y]

        board_direction = 1 if piece.get_color() == 'black' else -1

        for i in [x + board_direction, x + (board_direction * 2)]:
            if not self.in_board(i, y):
                break

            final_square = squares[i][y]

            if final_square.get_piece() is not None:
                break
            else:
                new_move = Move(initial_square, final_square)
                valid_moves.append(new_move)

        for j in [y - 1, y + 1]:
            if not self.in_board(x + board_direction, j):
                continue

            final_square = squares[x + board_direction][j]

            if final_square.get_piece() is not None:
                if final_square.get_piece().get_color() != piece.get_color():
                    new_move = Move(initial_square, final_square)
                    valid_moves.append(new_move)

        return valid_moves

    def get_king_valid_moves(self, piece, x, y):
        valid_moves = []
        squares = self.squares
        initial_square = squares[x][y]

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if not self.in_board(x + i, y + j):
                    continue

                final_square = squares[x + i][y + j]
                if final_square.get_piece() is not None:
                    if final_square.get_piece().get_color() != piece.get_color():
                        new_move = Move(initial_square, final_square)
                        valid_moves.append(new_move)
                else:
                    new_move = Move(initial_square, final_square)
                    valid_moves.append(new_move)

        # castling moves handling
        # there are more handling at "execute_move" function
        # we have two rooks: right rook at (king.x, king.y + 3) & left rook at (king.x, king.y - 4)
        # final king squares are: (king.x, king.y + 2) for right castling & (king.x, king.y - 2) for left castling
        # final rook squares are: (king.x, king.y + 1) for right castling & (king.x, king.y - 1) for left castling

        right_rook_square = self.get_square(x, y + 3)
        left_rook_square = self.get_square(x, y - 4)

        if self.can_castle(initial_square, right_rook_square):
            final_square = self.get_square(x, y + 2)
            castle_right_side_move = Move(initial_square, final_square)
            castle_right_side_move.set_castling()
            valid_moves.append(castle_right_side_move)
        if self.can_castle(initial_square, left_rook_square):
            final_square = self.get_square(x, y - 2)
            castle_left_side_move = Move(initial_square, final_square)
            castle_left_side_move.set_castling()
            valid_moves.append(castle_left_side_move)

        return valid_moves

    def get_queen_valid_moves(self, piece, x, y):
        rook_moves = self.get_rook_valid_moves(piece, x, y)
        bishop_moves = self.get_bishop_valid_moves(piece, x, y)

        valid_moves = rook_moves + bishop_moves

        return valid_moves

    def get_rook_valid_moves(self, piece, x, y):
        valid_moves = []
        squares = self.squares
        initial_square = squares[x][y]

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if i != 0 and j != 0:
                    continue

                range_end_x = 8 if i == 1 else -1
                range_end_y = 8 if j == 1 else -1

                range_start = x if i != 0 else y
                range_end = range_end_x if i != 0 else range_end_y

                increment = i if i != 0 else j

                for index in range(range_start + increment, range_end, increment):
                    xx = index if i != 0 else x
                    yy = index if j != 0 else y
                    if not self.in_board(xx, yy):
                        continue

                    final_square = squares[index][y] if i != 0 else squares[x][index]

                    if final_square.get_piece() is not None:
                        if final_square.get_piece().get_color() != piece.get_color():
                            move = Move(initial_square, final_square)
                            valid_moves.append(move)
                        break
                    else:
                        move = Move(initial_square, final_square)
                        valid_moves.append(move)

        return valid_moves

    def get_bishop_valid_moves(self, piece, x, y):
        valid_moves = []
        squares = self.squares
        initial_square = squares[x][y]

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 or j == 0:
                    continue

                range_end_x = 8 if i == 1 else -1
                range_end_y = 8 if j == 1 else -1

                for index_x, index_y in zip(range(x + i, range_end_x, i), range(y + j, range_end_y, j)):
                    if not self.in_board(index_x, index_y):
                        continue

                    final_square = squares[index_x][index_y]

                    if final_square.get_piece() is not None:
                        if final_square.get_piece().get_color() != piece.get_color():
                            move = Move(initial_square, final_square)
                            valid_moves.append(move)
                        break
                    else:
                        move = Move(initial_square, final_square)
                        valid_moves.append(move)

        return valid_moves

    def get_knight_valid_moves(self, piece, x, y):
        valid_moves = []
        squares = self.squares
        initial_square = squares[x][y]

        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) + abs(j) != 3:
                    continue
                if not self.in_board(x + i, y + j):
                    continue

                final_square = squares[x + i][y + j]
                if final_square.get_piece() is not None:
                    if final_square.get_piece().get_color() != piece.get_color():
                        new_move = Move(initial_square, final_square)
                        valid_moves.append(new_move)
                else:
                    new_move = Move(initial_square, final_square)
                    valid_moves.append(new_move)

        return valid_moves
