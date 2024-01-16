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
        temp_square = Square(-1, -1, "white", "white")

        self.pinned_pieces = []
        self.board_direction = -1
        self.checking_pieces_squares = []
        self.is_white_turn = True
        self.last_move = Move(temp_square, temp_square)
        self.squares = [[temp_square] * 8 for _ in range(8)]

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

        self.white_king_square = self.get_square(7, 4)
        self.black_king_square = self.get_square(0, 4)

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

    def get_board_direction(self):
        return self.board_direction

    def flip_board_direction(self):
        self.board_direction *= -1

    def flip_turn(self):
        self.is_white_turn = not self.is_white_turn

    @staticmethod
    def get_opposite_color(color):
        return "white" if color == "black" else "black"

    def get_pieces_squares(self, color):
        pieces_squares = []

        for row in range(0, 8):
            for col in range(0, 8):
                cur_square = self.get_square(row, col)
                cur_piece = cur_square.get_piece()

                if cur_piece is not None and cur_piece.get_color() == color:
                    pieces_squares.append(cur_square)

        return pieces_squares

    def execute_en_passant(self, move):
        initial_row = move.get_initial_square().get_row()
        final_col = move.get_final_square().get_col()

        square = self.get_square(initial_row, final_col)
        square.remove_piece()

    @staticmethod
    def execute_promotion(move):
        """ Promote pawns to Queens only (for now) """
        promoted_pawn = Queen(move.get_final_square().get_piece().get_color())
        move.get_final_square().change_piece(promoted_pawn)

    def execute_castling(self, move):
        initial_square = move.get_initial_square()
        final_square = move.get_final_square()

        if final_square.get_col() > initial_square.get_col():
            # castle right side
            initial_increment = 3
            final_increment = 1
        else:
            # castle left side
            initial_increment = -4
            final_increment = -1

        rook_initial_square = self.get_square(initial_square.get_row(), initial_square.get_col() + initial_increment)
        rook_final_square = self.get_square(initial_square.get_row(), initial_square.get_col() + final_increment)

        rook = rook_initial_square.get_piece()

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
        # why don't we make set_moved to all pieces?
        if isinstance(piece, King) or isinstance(piece, Rook) or isinstance(piece, Pawn):
            piece.set_moved()

        if move.is_castling():
            self.execute_castling(move)
        if move.is_en_passant():
            self.execute_en_passant(move)
        if move.is_promotion():
            self.execute_promotion(move)

        # updates
        if isinstance(piece, King):
            if piece.get_color() == 'white':
                self.white_king_square = final_square
            else:
                self.black_king_square = final_square

        self.last_move = move

    def get_valid_moves(self, square):
        """ Get the list of valid moves of the given square """

        piece = square.get_piece()
        x = square.get_row()
        y = square.get_col()
        empty_valid_moves = []

        # if there is a check generate only check valid moves
        if self.count_checks() > 0:
            return self.get_check_valid_moves()

        # if piece is pinned -> can't move except in the direction of the pin

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

    @staticmethod
    def in_board(x, y):
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

        # check if there are any pieces between king and rook
        increment = 1 if rook_square.get_col() > king_square.get_col() else -1
        row = king_square.get_row()
        for col in range(king_square.get_col() + increment, rook_square.get_col(), increment):
            if not self.in_board(row, col):
                return False

            cur_square = self.get_square(row, col)
            if cur_square.get_piece() is not None:
                return False

        return True

    def get_pawn_valid_moves(self, piece, x, y):
        valid_moves = []
        squares = self.squares
        initial_square = squares[x][y]

        for i in [x + self.get_board_direction(), x + (self.get_board_direction() * 2)]:
            if i == x + (self.get_board_direction() * 2) and piece.is_moved():
                break
            if not self.in_board(i, y):
                break

            final_square = squares[i][y]

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
            if not self.in_board(x + self.get_board_direction(), j):
                continue

            final_square = squares[x + self.get_board_direction()][j]

            if final_square.get_piece() is not None:
                if final_square.get_piece().get_color() != piece.get_color():
                    if final_square.get_row() == 0 or final_square.get_row() == 7:
                        is_promotion = True
                    else:
                        is_promotion = False

                    new_move = Move(initial_square, final_square, promotion=is_promotion)
                    valid_moves.append(new_move)

        # enpassant conditions
        last_move_final_square_x = self.last_move.get_final_square().get_row()
        last_move_final_square_y = self.last_move.get_final_square().get_col()

        if self.last_move is not None:
            if self.last_move.get_final_square().get_piece() is not None:
                if self.last_move.get_final_square().get_piece().get_name() == 'pawn':
                    if last_move_final_square_x == x:
                        if last_move_final_square_y == y+1 or last_move_final_square_y == y-1:
                            if abs(self.last_move.get_initial_square().get_row() - last_move_final_square_x) == 2:
                                final_square = self.get_square(initial_square.get_row() + self.get_board_direction(),
                                                               last_move_final_square_y)
                                en_passant = Move(initial_square, final_square, en_passant=True)
                                valid_moves.append(en_passant)

        return valid_moves

    def get_king_valid_moves(self, piece, x, y):
        valid_moves = []
        initial_square = self.get_square(x, y)

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if not self.in_board(x + i, y + j):
                    continue

                final_square = self.get_square(x + i, y + j)
                if final_square.get_piece() is not None:
                    if final_square.get_piece().get_color() != piece.get_color():
                        if not self.check_is_protected(final_square):
                            new_move = Move(initial_square, final_square)
                            valid_moves.append(new_move)
                else:
                    opposite_color_pieces_squares = self.get_pieces_squares(self.get_opposite_color(piece.get_color()))
                    is_threatened = False

                    for cur_square in opposite_color_pieces_squares:
                        if self.can_attack(cur_square, final_square):
                            is_threatened = True
                            break

                    if not is_threatened:
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
            y_increment = 2
            can_castle = True
        elif self.can_castle(initial_square, left_rook_square):
            y_increment = -2
            can_castle = True
        else:
            y_increment = 0
            can_castle = False

        if can_castle:
            final_square = self.get_square(x, y + y_increment)
            castle_move = Move(initial_square, final_square, castling=True)
            valid_moves.append(castle_move)

        return valid_moves

    def check_is_protected(self, square):
        """ Check if the piece in the square is protected by a piece of the same color or not """

        piece = square.get_piece()

        if piece is None:
            print("Error: 'check is protected' is called for an empty square")
            return False

        for row_increment in range(-1, 2):
            for col_increment in range(-1, 2):
                if row_increment == col_increment == 0:
                    continue

                row = square.get_row()
                col = square.get_col()
                while self.in_board(row, col):
                    cur_piece = self.get_square(row, col).get_piece()

                    if cur_piece is not None:
                        if cur_piece.get_color() == piece.get_color():
                            return True
                        else:
                            # For example if there is a queen checking a king
                            # and there is a rook on the same file on the king's side, the queen is still protected
                            # like this:
                            # # # # # # # # # #
                            # . . . . . . . . #
                            # . . . . . . . . #
                            # . . . . . . . . #
                            # R . . . . . K Q #
                            # . . . . . . . . #
                            # . . . . . . . . #
                            # . . . . . . . . #
                            # . . . . . . . . #
                            # # # # # # # # # #
                            if isinstance(cur_piece, King):
                                continue
                            else:
                                break

                    row += row_increment
                    col += col_increment

        # knight protection
        for row in range(-2, 3):
            for col in range(-2, 3):
                if abs(row) + abs(col) != 3:
                    continue
                if not self.in_board(square.get_row() + row, square.get_col() + col):
                    continue

                knight_square = self.get_square(square.get_row() + row, square.get_col() + col)
                knight_piece = knight_square.get_piece()

                if knight_piece is None:
                    continue

                if isinstance(knight_piece, Knight) and knight_piece.get_color() == square.get_color():
                    return True

        return False

    def get_queen_valid_moves(self, piece, x, y):
        rook_moves = self.get_rook_valid_moves(piece, x, y)
        bishop_moves = self.get_bishop_valid_moves(piece, x, y)

        valid_moves = rook_moves + bishop_moves

        return valid_moves

    def get_rook_valid_moves(self, piece, x, y):
        valid_moves = []
        initial_square = self.get_square(x, y)

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

                    if not self.in_board(index_x, index_y):
                        continue

                    final_square = self.get_square(index, y) if i != 0 else self.get_square(x, index)

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
        initial_square = self.get_square(x, y)

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 or j == 0:
                    continue

                range_end_x = 8 if i == 1 else -1
                range_end_y = 8 if j == 1 else -1

                for index_x, index_y in zip(range(x + i, range_end_x, i), range(y + j, range_end_y, j)):
                    final_square = self.get_square(index_x, index_y)

                    if not self.in_board(index_x, index_y):
                        continue
                    if final_square.get_piece() is not None and\
                            final_square.get_piece().get_color() == piece.get_color():
                        break

                    valid_move = Move(initial_square, final_square)
                    valid_moves.append(valid_move)

                    # bishop can't jump over pieces
                    if final_square.get_piece() is not None:
                        break

        return valid_moves

    def get_knight_valid_moves(self, piece, x, y):
        valid_moves = []
        initial_square = self.get_square(x, y)

        for i in range(-2, 3):
            for j in range(-2, 3):
                final_square = self.get_square(x + i, y + j)

                if abs(i) + abs(j) != 3 or not self.in_board(x + i, y + j):
                    continue
                if final_square.get_piece() is not None and final_square.get_piece().get_color() == piece.get_color():
                    continue

                valid_move = Move(initial_square, final_square)
                valid_moves.append(valid_move)

        return valid_moves

    def get_check_valid_moves(self):
        """ get valid moves when king is in check (assuming there is a check) """

        if len(self.checking_pieces_squares) <= 0:
            print("Error: 'get check valid moves' function called when there is no check")
            return []

        check_valid_moves = []
        checked_king_square = self.white_king_square if self.is_white_turn else self.black_king_square
        king_row = checked_king_square.get_row()
        king_col = checked_king_square.get_col()
        checked_king = checked_king_square.get_piece()

        # 1) cover the check
        if len(self.checking_pieces_squares) == 1:
            attacking_piece_square = self.checking_pieces_squares[0]

            # loop on all squares to find same-color pieces that can cover the check
            for row in range(0, 8):
                for col in range(0, 8):
                    initial_square = self.get_square(row, col)
                    piece = initial_square.get_piece()

                    if piece is not None and piece.get_color() == checked_king.get_color():  # same-color piece found
                        x = attacking_piece_square.get_row() - checked_king_square.get_row()
                        y = attacking_piece_square.get_col() - checked_king_square.get_col()

                        increment_x = 0
                        increment_y = 0

                        if x > 0:
                            increment_x = 1
                        elif x < 0:
                            increment_x = -1

                        if y > 0:
                            increment_y = 1
                        elif y < 0:
                            increment_y = -1

                        if increment_x == 0 or increment_y == 0:
                            continue

                        # loop on squares between the king and the checking piece
                        for covering_row, covering_col in zip(
                                range(king_row + increment_x, attacking_piece_square.get_row(), increment_x),
                                range(king_col + increment_y, attacking_piece_square.get_col(), increment_y)):
                            covering_square = self.get_square(covering_row, covering_col)
                            if self.can_attack(initial_square, covering_square):  # if current piece can cover the check
                                new_move = Move(initial_square, covering_square)
                                check_valid_moves.append(new_move)

        # 2) kill the checking piece (not available in case of double checks)
        if len(self.checking_pieces_squares) == 1:
            attacking_piece_square = self.checking_pieces_squares[0]

            # loop through all pieces and check if the can attack the attacking piece
            for row in range(0, 8):
                for col in range(0, 8):
                    cur_square = self.get_square(row, col)
                    piece = cur_square.get_piece()

                    if cur_square == checked_king_square:
                        continue

                    if piece is not None and piece.get_color() == checked_king.get_color():
                        if self.can_attack(cur_square, attacking_piece_square):
                            new_move = Move(cur_square, attacking_piece_square)
                            check_valid_moves.append(new_move)

        # 3) move the king to safety
        check_valid_moves += self.get_king_valid_moves(checked_king, king_row, king_col)

        return check_valid_moves

    def count_checks(self):
        white_checks = self.count_checks_for_king(self.white_king_square.get_row(), self.white_king_square.get_col())
        black_checks = self.count_checks_for_king(self.black_king_square.get_row(), self.black_king_square.get_col())

        if white_checks > 0 and black_checks > 0:
            print('Error: The two kings are in check')

        checks = white_checks + black_checks

        return checks

    def count_checks_for_king(self, x, y):
        """ count number of checks & keep track of pinned, covering and checking pieces """

        checks_count = 0

        king = self.get_square(x, y).get_piece()

        if king is None or not isinstance(king, King):
            print("warning: 'count_checks' function is called for a non king")
            return checks_count

        for row_increment in range(-1, 2):
            for col_increment in range(-1, 2):
                if row_increment == col_increment == 0:
                    continue

                covering_pieces = []
                row = x
                col = y
                while self.in_board(row, col):
                    cur_piece = self.get_square(row, col).get_piece()

                    if cur_piece is not None:
                        if not isinstance(cur_piece, King):
                            if cur_piece.get_color() == king.get_color():
                                covering_pieces.append(cur_piece)
                            else:
                                if self.can_jump_attack(self.get_square(row, col), self.get_square(x, y)):
                                    if len(covering_pieces) == 1:
                                        pinned_piece = covering_pieces[0]
                                        pinned_piece.set_pin((row_increment, col_increment))
                                    elif len(covering_pieces) == 0:
                                        # check
                                        checks_count += 1
                                        self.checking_pieces_squares.append(self.get_square(row, col))

                                break

                    row += row_increment
                    col += col_increment

        # knight checks
        for row in range(-2, 3):
            for col in range(-2, 3):
                if abs(row) + abs(col) != 3:
                    continue
                if not self.in_board(x + row, y + col):
                    continue
                if self.get_square(x + row, y + col).get_piece() is None:
                    continue
                if self.get_square(x + row, y + col).get_piece().get_color() == king.get_color():
                    continue

                if self.can_jump_attack(self.get_square(x + row, y + col), self.get_square(x, y)):
                    # check
                    checks_count += 1
                    self.checking_pieces_squares.append(self.get_square(x + row, y + col))

        return checks_count

    def can_jump_attack(self, initial_square, final_square):
        """ Determine if the piece in the initial square can attack the piece in the final square
        (without considering the pieces between them) """

        if initial_square is None or final_square is None:
            return False

        x = final_square.get_row() - initial_square.get_row()
        y = final_square.get_col() - initial_square.get_col()
        attacking_piece = initial_square.get_piece()

        if x == 0 and y == 0:
            return False
        if attacking_piece is None:
            return False

        if isinstance(attacking_piece, Bishop) and abs(x) == abs(y):
            return True

        if isinstance(attacking_piece, Rook) and (x == 0 or y == 0):
            return True

        if isinstance(attacking_piece, Queen) and (abs(x) == abs(y) or (x == 0 or y == 0)):
            return True

        if isinstance(attacking_piece, Knight) and (x != 0 and y != 0) and (abs(x) + abs(y) == 3):
            return True

        # check for pawn attacks
        x1 = initial_square.get_row() + self.get_board_direction()
        y11 = initial_square.get_col() + 1
        y12 = initial_square.get_col() - 1

        x2 = final_square.get_row()
        y2 = final_square.get_col()

        if isinstance(attacking_piece, Pawn) and (x1 == x2 and (y11 == y2 or y12 == y2)):
            return True

        if isinstance(attacking_piece, Knight):
            x = initial_square.get_row()
            y = initial_square.get_col()

            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i) + abs(j) != 3 or not self.in_board(x + i, y + j):
                        continue

                    if x+i == x2 and y+j == y2:
                        return True

        return False

    def check_inbetween_pieces(self, initial_square, final_square):
        """ Determine if there are any pieces between the pieces in the initial position and the final position
        (assuming that the piece in the initial square can go jump attack the piece in the final square) """

        x = final_square.get_row() - initial_square.get_row()
        y = final_square.get_col() - initial_square.get_col()

        increment_x = 0
        increment_y = 0

        if x > 0:
            increment_x = 1
        elif x < 0:
            increment_x = -1

        if y > 0:
            increment_y = 1
        elif y < 0:
            increment_y = -1

        if increment_x == 0 or increment_y == 0:
            return False

        for row, col in zip(range(initial_square.get_row() + increment_x, final_square.get_row(), increment_x),
                            range(initial_square.get_col() + increment_y, final_square.get_col(), increment_y)):
            if self.get_square(row, col).get_piece() is not None:
                return True

        return False

    def can_attack(self, initial_square, final_square):
        """ Determine if the piece in the initial square can attack the piece in the final square
        (with considering the pieces between them) """

        if initial_square is None or final_square is None:
            return False

        x = final_square.get_row() - initial_square.get_row()
        y = final_square.get_col() - initial_square.get_col()
        attacking_piece = initial_square.get_piece()

        if x == 0 and y == 0:
            return False
        if attacking_piece is None:
            return False

        if isinstance(attacking_piece, Bishop) and abs(x) == abs(y):
            return not self.check_inbetween_pieces(initial_square, final_square)

        if isinstance(attacking_piece, Rook) and (x == 0 or y == 0):
            return not self.check_inbetween_pieces(initial_square, final_square)

        if isinstance(attacking_piece, Queen) and (abs(x) == abs(y) or (x == 0 or y == 0)):
            return not self.check_inbetween_pieces(initial_square, final_square)

        if isinstance(attacking_piece, Knight) and (x != 0 and y != 0) and (abs(x) + abs(y) == 3):
            return True

        # check for pawn attacks
        x1 = initial_square.get_row() + self.get_board_direction()
        y11 = initial_square.get_col() + 1
        y12 = initial_square.get_col() - 1

        x2 = final_square.get_row()
        y2 = final_square.get_col()

        if isinstance(attacking_piece, Pawn) and (x1 == x2 and (y11 == y2 or y12 == y2)):
            return True

        if isinstance(attacking_piece, Knight):
            x = initial_square.get_row()
            y = initial_square.get_col()

            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i) + abs(j) != 3 or not self.in_board(x + i, y + j):
                        continue

                    if x + i == x2 and y + j == y2:
                        return True

        return False

    def check_for_checkmate(self):
        checks_count = self.count_checks()
        if checks_count > 0:
            valid_moves = self.get_check_valid_moves()
            if len(valid_moves) == 0:
                return True

        return False

    def get_pins(self):
        pass

    def update_board_state(self):
        self.checking_pieces_squares.clear()
        self.flip_turn()
        self.flip_board_direction()

        for pinned_piece in self.pinned_pieces:
            pinned_piece.clear_pins()

        self.pinned_pieces.clear()
