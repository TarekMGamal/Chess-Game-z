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
        self.checks_count = 0
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

    def get_pieces_squares(self, color):
        pieces_squares = []

        for row in range(0, 8):
            for col in range(0, 8):
                cur_square = self.get_square(row, col)
                cur_piece = cur_square.get_piece()
                if cur_piece is not None and cur_piece.get_color() == color:
                    pieces_squares.append(cur_square)

        return pieces_squares

    @staticmethod
    def get_sign(num):
        return (num > 0) - (num < 0)

    @staticmethod
    def get_opposite_color(color):
        return "white" if color == "black" else "black"

    @staticmethod
    def in_board(x, y):
        return True if 8 > x >= 0 and 8 > y >= 0 else False

    @staticmethod
    def execute_promotion(move):
        """ Promote pawns to Queens only (for now) """
        promoted_pawn = Queen(move.get_final_square().get_piece().get_color())
        move.get_final_square().change_piece(promoted_pawn)

    def execute_en_passant(self, move):
        initial_row = move.get_initial_square().get_row()
        final_col = move.get_final_square().get_col()
        square = self.get_square(initial_row, final_col)
        square.remove_piece()

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
        if self.checks_count > 0:
            return self.get_check_valid_moves()

        if piece is None:
            return empty_valid_moves
        elif piece.get_name() == 'pawn':
            return Pawn.calculate_valid_moves(self, square)
        elif piece.get_name() == 'king':
            return self.get_king_valid_moves(x, y)
        elif piece.get_name() == 'queen':
            return Queen.calculate_valid_moves(self, square)
        elif piece.get_name() == 'rook':
            return piece.calculate_valid_moves(board=self, initial_square=square)
        elif piece.get_name() == 'bishop':
            return piece.calculate_valid_moves(board=self, initial_square=square)
        elif piece.get_name() == 'knight':
            return Knight.calculate_valid_moves(self, square)
        else:
            return empty_valid_moves

    def can_castle(self, king_square, rook_square):
        if king_square is None or rook_square is None:
            return False
        if not isinstance(king_square.get_piece(), King) or not isinstance(rook_square.get_piece(), Rook):
            return False

        king = king_square.get_piece()
        rook = rook_square.get_piece()

        if king.get_is_moved() or rook.get_is_moved():
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

    def get_king_valid_moves(self, x, y):
        valid_moves = []
        king_square = self.get_square(x, y)
        king = king_square.get_piece()

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if not self.in_board(x + i, y + j):
                    continue

                final_square = self.get_square(x + i, y + j)
                if final_square.get_piece() is not None and final_square.get_piece().get_color() == king.get_color():
                    continue

                if not self.check_is_protected(final_square, self.get_opposite_color(king.get_color())):
                    new_move = Move(king_square, final_square)
                    valid_moves.append(new_move)

        # castling moves handling
        # there are more handling at "execute_move" function
        # we have two rooks: right rook at (king.x, king.y + 3) & left rook at (king.x, king.y - 4)
        # final king squares are: (king.x, king.y + 2) for right castling & (king.x, king.y - 2) for left castling
        # final rook squares are: (king.x, king.y + 1) for right castling & (king.x, king.y - 1) for left castling

        right_rook_square = self.get_square(x, y + 3)
        left_rook_square = self.get_square(x, y - 4)

        if self.can_castle(king_square, right_rook_square):
            y_increment = 2
            can_castle = True
        elif self.can_castle(king_square, left_rook_square):
            y_increment = -2
            can_castle = True
        else:
            y_increment = 0
            can_castle = False

        if can_castle:
            final_square = self.get_square(x, y + y_increment)
            castle_move = Move(king_square, final_square, castling=True)
            valid_moves.append(castle_move)

        return valid_moves

    def check_is_protected(self, square, color):
        """ Check if the piece in the square is protected by a piece of the same color or not """
        pieces_squares = self.get_pieces_squares(color)
        for piece_square in pieces_squares:
            if self.can_attack(piece_square, square, consider_in_between_pieces=True):
                return True

        return False

    def get_check_valid_moves(self):
        """ get valid moves when king is in check """

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
            pieces_squares = self.get_pieces_squares(checked_king.get_color())
            for initial_square in pieces_squares:
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
                    # if current piece can cover the check
                    if self.can_attack(initial_square, covering_square, consider_in_between_pieces=True):
                        valid_move = Move(initial_square, covering_square)
                        check_valid_moves.append(valid_move)

        # 2) kill the checking piece (not available in case of double checks)
        if len(self.checking_pieces_squares) == 1:
            attacking_piece_square = self.checking_pieces_squares[0]

            # loop through all pieces and check if any piece can attack the attacking piece
            pieces_squares = self.get_pieces_squares(checked_king.get_color())
            for cur_square in pieces_squares:
                if self.can_attack(cur_square, attacking_piece_square, consider_in_between_pieces=True):
                    valid_move = Move(cur_square, attacking_piece_square)
                    check_valid_moves.append(valid_move)

        # 3) move the king to safety
        check_valid_moves += self.get_king_valid_moves(king_row, king_col)

        return check_valid_moves

    def count_checks(self):
        """ count number of checks & keep track of pinned, covering, and checking pieces """
        checks_count = 0
        king_square = self.white_king_square if self.is_white_turn else self.black_king_square
        king = king_square.get_piece()
        x = king_square.get_row()
        y = king_square.get_col()

        if king is None or not isinstance(king, King):
            print("Error: 'count_checks' function is called for a non king")
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
                                if self.can_attack(self.get_square(row, col), king_square, False):
                                    if len(covering_pieces) == 1:
                                        pinned_piece = covering_pieces[0]
                                        self.pinned_pieces.append(pinned_piece)
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

                if self.can_attack(self.get_square(x + row, y + col), self.get_square(x, y), False):
                    # check
                    checks_count += 1
                    self.checking_pieces_squares.append(self.get_square(x + row, y + col))

        self.checks_count = checks_count

    def check_inbetween_pieces(self, initial_square, final_square):
        """ Determine if there are any pieces between the pieces in the initial position and the final position """
        diff_x = final_square.get_row() - initial_square.get_row()
        diff_y = final_square.get_col() - initial_square.get_col()
        increment_x = 0
        increment_y = 0

        if diff_x > 0:
            increment_x = 1
        elif diff_x < 0:
            increment_x = -1
        if diff_y > 0:
            increment_y = 1
        elif diff_y < 0:
            increment_y = -1

        if increment_x == 0 and increment_y != 0:
            row = initial_square.get_row()
            for col in range(initial_square.get_col() + increment_y, final_square.get_col(), increment_y):
                if self.get_square(row, col).get_piece() is not None:
                    return True
        elif increment_x != 0 and increment_y == 0:
            col = initial_square.get_col()
            for row in range(initial_square.get_row() + increment_x, final_square.get_row(), increment_x):
                if self.get_square(row, col).get_piece() is not None:
                    return True
        elif increment_x != 0 and increment_y != 0:
            for row, col in zip(range(initial_square.get_row() + increment_x, final_square.get_row(), increment_x),
                                range(initial_square.get_col() + increment_y, final_square.get_col(), increment_y)):
                if self.get_square(row, col).get_piece() is not None:
                    return True

        return False

    def can_attack(self, initial_square, final_square, consider_in_between_pieces=True):
        """ Determine if the piece in the initial square can attack the piece in the final square """

        if initial_square is None or final_square is None:
            return False

        x = final_square.get_row() - initial_square.get_row()
        y = final_square.get_col() - initial_square.get_col()
        attacking_piece = initial_square.get_piece()

        if x == 0 and y == 0:
            return False
        if attacking_piece is None:
            return False

        # has to be set to determine if the attacked_piece can go to this square or not
        if isinstance(attacking_piece, King):
            # this is another function use it as a starting point
            attacked_piece = final_square.get_piece()
            x = final_square.get_row()
            y = final_square.get_col()

            if attacked_piece is None:
                return True

            for row_increment in range(-1, 2):
                for col_increment in range(-1, 2):
                    if row_increment == col_increment == 0:
                        continue

                    row = x
                    col = y
                    while self.in_board(row, col):
                        cur_piece = self.get_square(row, col).get_piece()

                        if cur_piece is not None:
                            if isinstance(cur_piece, King) and cur_piece.get_color() != attacked_piece.get_color():
                                continue

                            if cur_piece.get_color() == attacked_piece.get_color():
                                pass

                        row += row_increment
                        col += col_increment

            # knight defence
            for row in range(-2, 3):
                for col in range(-2, 3):
                    if abs(row) + abs(col) != 3:
                        continue
                    if not self.in_board(x + row, y + col):
                        continue
                    if self.get_square(x + row, y + col).get_piece() is None:
                        continue
                    if self.get_square(x + row, y + col).get_piece().get_color() != attacked_piece.get_color():
                        continue
                    if not isinstance(self.get_square(x + row, y + col).get_piece(), Knight):
                        continue

                    return True

        if isinstance(attacking_piece, Bishop) and abs(x) == abs(y):
            return True if not consider_in_between_pieces \
                else not self.check_inbetween_pieces(initial_square, final_square)

        if isinstance(attacking_piece, Rook) and (x == 0 or y == 0):
            return True if not consider_in_between_pieces \
                else not self.check_inbetween_pieces(initial_square, final_square)

        if isinstance(attacking_piece, Queen) and (abs(x) == abs(y) or (x == 0 or y == 0)):
            return True if not consider_in_between_pieces \
                else not self.check_inbetween_pieces(initial_square, final_square)

        if isinstance(attacking_piece, Knight) and (x != 0 and y != 0) and (abs(x) + abs(y) == 3):
            return True

        x1 = initial_square.get_row()
        y1 = initial_square.get_col()

        x2 = final_square.get_row()
        y2 = final_square.get_col()

        if isinstance(attacking_piece, Pawn):
            if x1 + self.board_direction == x2 and (y1 + 1 == y2 or y1 - 1 == y2):
                if final_square.get_piece() is not None \
                        and final_square.get_piece().get_color() != attacking_piece.get_color():
                    return True
            elif y1 == y2 and x2 - x1 == self.board_direction:
                if final_square.get_piece() is None:
                    return True if not consider_in_between_pieces \
                        else not self.check_inbetween_pieces(initial_square, final_square)
            elif y1 == y2 and x2 - x1 == self.board_direction * 2:
                if final_square.get_piece() is None:
                    return True if not consider_in_between_pieces \
                        else not self.check_inbetween_pieces(initial_square, final_square)

        return False

    def update_board_state(self):
        self.checking_pieces_squares.clear()
        self.flip_turn()
        self.flip_board_direction()

        for pinned_piece in self.pinned_pieces:
            pinned_piece.clear_pins()
        self.pinned_pieces.clear()
