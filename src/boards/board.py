from boards.square import Square
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.king import King
from pieces.queen import Queen
from pieces.pawn import Pawn
from pieces.rook import Rook
from boards.move import Move


class Board:
    def __init__(self, game_id):
        temp_square = Square(-1, -1, "white", "white")

        self.game_id = game_id
        self.is_ready = False
        self.is_game_running = False
        self.pinned_pieces = []
        self.board_direction = 1
        self.checking_pieces_squares = []
        self.is_white_turn = False
        self.checks_count = 0
        self.last_move = Move(temp_square, temp_square)
        self.squares = [[temp_square] * 8 for _ in range(8)]
        self.valid_moves = []

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

        self.update_board_state()

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
        initial_square = self.get_square(move.get_initial_square().get_row(), move.get_initial_square().get_col())
        final_square = self.get_square(move.get_final_square().get_row(), move.get_final_square().get_col())
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

    def check_move_validity(self, move):
        for valid_move in self.valid_moves:
            if move == valid_move:
                return True

        return False

    def update_board_state(self):
        # clear the state
        self.checking_pieces_squares.clear()
        self.flip_turn()
        self.flip_board_direction()
        for pinned_piece in self.pinned_pieces:
            pinned_piece.clear_pins()
        self.pinned_pieces.clear()

        # calculate the new state
        checks_count = self.count_checks()
        print("checks count", checks_count)
        valid_moves_num = 0

        pieces_squares = self.get_pieces_squares("white" if self.is_white_turn else "black")
        for piece_square in pieces_squares:
            piece = piece_square.get_piece()
            piece_valid_moves = self.get_valid_moves(piece_square)
            for move in piece_valid_moves:
                print(move.get_initial_square().get_piece())
            self.valid_moves += piece_valid_moves
            piece.set_valid_moves(piece_valid_moves)
            valid_moves_num += len(piece_valid_moves)

        print(valid_moves_num)

        if self.checks_count > 0 and valid_moves_num == 0:
            self.is_game_running = False
            print("Game Ended by Checkmate")
        elif self.checks_count == valid_moves_num == 0:
            self.is_game_running = False
            print("Game Ended by Stalemate")

    def get_valid_moves(self, initial_square):
        """ Get the list of valid moves of the given square """
        piece = initial_square.get_piece()
        empty_valid_moves = []

        # if there is a check generate only check valid moves
        if self.checks_count > 0:
            return self.get_check_valid_moves()

        if piece is None:
            return empty_valid_moves
        else:
            return piece.__class__.calculate_valid_moves(board=self, initial_square=initial_square)

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

    def check_is_protected(self, square, color):
        """ Check if the piece in the square is protected by a piece of the same color or not """
        pieces_squares = self.get_pieces_squares(color)
        for piece_square in pieces_squares:
            if square == piece_square:
                continue

            piece = piece_square.get_piece()
            if piece.__class__.can_defend(self, piece_square, square):
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
                piece = initial_square.get_piece()
                if isinstance(piece, King):
                    continue

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
                if increment_x == 0 and increment_y == 0:
                    continue

                # loop on squares between the king and the checking piece
                if increment_x != 0 and increment_y != 0:
                    for covering_row, covering_col in zip(
                            range(king_row + increment_x, attacking_piece_square.get_row(), increment_x),
                            range(king_col + increment_y, attacking_piece_square.get_col(), increment_y)):
                        covering_square = self.get_square(covering_row, covering_col)
                        # if current piece can cover the check
                        if piece.__class__.can_reach(self, initial_square, covering_square):
                            valid_move = Move(initial_square, covering_square)
                            check_valid_moves.append(valid_move)
                elif increment_x == 0:
                    covering_row = checked_king_square.get_row()

                    for covering_col in range(king_col + increment_y, attacking_piece_square.get_col(), increment_y):
                        covering_square = self.get_square(covering_row, covering_col)
                        # if current piece can cover the check
                        if piece.__class__.can_reach(self, initial_square, covering_square):
                            valid_move = Move(initial_square, covering_square)
                            check_valid_moves.append(valid_move)
                elif increment_y == 0:
                    covering_col = checked_king_square.get_col()

                    for covering_row in range(king_row + increment_x, attacking_piece_square.get_row(), increment_x):
                        covering_square = self.get_square(covering_row, covering_col)
                        # if current piece can cover the check
                        if piece.__class__.can_reach(self, initial_square, covering_square):
                            valid_move = Move(initial_square, covering_square)
                            check_valid_moves.append(valid_move)

        # 2) kill the checking piece (not available in case of double checks)
        if len(self.checking_pieces_squares) == 1:
            attacking_piece_square = self.checking_pieces_squares[0]

            # loop through all pieces and check if any piece can attack the attacking piece
            pieces_squares = self.get_pieces_squares(checked_king.get_color())
            for cur_square in pieces_squares:
                piece = cur_square.get_piece()
                if piece.__class__.can_attack(self, cur_square, attacking_piece_square):
                    valid_move = Move(cur_square, attacking_piece_square)
                    check_valid_moves.append(valid_move)

        # 3) move the king to safety
        check_valid_moves += King.calculate_valid_moves(board=self, initial_square=checked_king_square)

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
                    cur_square = self.get_square(row, col)
                    cur_piece = cur_square.get_piece()

                    if cur_piece is not None:
                        if not (isinstance(cur_piece, King) and cur_piece.get_color() == king.get_color()):
                            if cur_piece.get_color() == king.get_color():
                                covering_pieces.append(cur_piece)
                            else:
                                self.board_direction *= -1
                                if isinstance(cur_piece, Pawn):
                                    if Pawn.can_attack(self, cur_square, king_square):
                                        if len(covering_pieces) == 1:
                                            pinned_piece = covering_pieces[0]
                                            self.pinned_pieces.append(pinned_piece)
                                            pinned_piece.set_pin((row_increment, col_increment))
                                        elif len(covering_pieces) == 0:
                                            # check
                                            checks_count += 1
                                            self.checking_pieces_squares.append(cur_square)
                                else:
                                    if cur_piece.__class__.can_reach(self, cur_square, king_square, False):
                                        if len(covering_pieces) == 1:
                                            pinned_piece = covering_pieces[0]
                                            self.pinned_pieces.append(pinned_piece)
                                            pinned_piece.set_pin((row_increment, col_increment))
                                        elif len(covering_pieces) == 0:
                                            # check
                                            checks_count += 1
                                            self.checking_pieces_squares.append(cur_square)
                                self.board_direction *= -1

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
                if isinstance(self.get_square(x + row, y + col).get_piece(), Knight):
                    # check
                    checks_count += 1
                    self.checking_pieces_squares.append(self.get_square(x + row, y + col))

        self.checks_count = checks_count
        return checks_count

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
