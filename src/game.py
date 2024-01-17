import pygame as p
import os
from boards.board import Board
from boards.move import Move


def load_image(image_name):
    relative_path = os.getcwd()
    image = p.image.load(relative_path + "/assets/images/" + image_name + ".png")
    return image


class Game:
    def __init__(self):
        p.init()

        self.board_width = self.board_height = 512
        self.dimension = 8
        self.sq_size = self.board_height // self.dimension
        self.max_fps = 15
        self.assets = {}
        self.load_assets()
        self.board = Board()
        self.is_game_running = False
        self.screen = p.display.set_mode((self.board_width, self.board_height))
        self.clock = p.time.Clock()
        self.selected_squares = []
        self.valid_moves = []

    def load_assets(self):
        """ load all the assets in a dictionary to be easily and efficiently accessed later """

        pieces = ['black bishop', 'black king', 'black knight', 'black pawn', 'black queen', 'black rook',
                  'white bishop', 'white king', 'white knight', 'white pawn', 'white queen', 'white rook']

        for piece in pieces:
            self.assets[piece] = load_image(piece)

    def draw_board(self):
        for row in range(self.dimension):
            for col in range(self.dimension):
                color = self.board.get_square(row, col).get_color()

                p.draw.rect(self.screen, color,
                            p.Rect(col * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size))

    def draw_pieces(self):
        for row in range(self.dimension):
            for col in range(self.dimension):
                piece = self.board.get_piece(row, col)
                if piece is not None:
                    color = piece.get_color()
                    name = piece.get_name()
                    image_name = color + ' ' + name

                    # access the piece image stored in the "IMAGES" dict previously loaded in the "load_images" function
                    piece_image = self.assets[image_name]

                    # draw the piece in it's required square
                    self.screen.blit(piece_image,
                                     p.Rect(col * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size))

    def highlight_valid_moves(self, current_square):
        # highlight current square
        row = current_square.get_row()
        col = current_square.get_col()
        current_square = self.board.get_square(row, col)
        current_square.highlight()

        # highlight valid squares
        for valid_move in self.valid_moves:
            row = valid_move.get_final_square().get_row()
            col = valid_move.get_final_square().get_col()
            square = self.board.get_square(row, col)
            if current_square == valid_move.get_initial_square():
                square.highlight()

        # necessary to update the board's graphics
        p.display.flip()

    def clear_valid_moves_highlight(self, current_square):
        # clear current square highlight
        current_square.clear_highlight()

        # clear valid squares highlight
        for valid_move in self.valid_moves:
            valid_move.get_final_square().clear_highlight()

        # necessary to update the board's graphics
        p.display.flip()

    def check_move_validity(self, move):
        for valid_move in self.valid_moves:
            if move == valid_move:
                return True

        return False

    def get_valid_move(self, move):
        """ search for the object in "self.valid_moves" as it contains important info which is not found in "move" """

        for valid_move in self.valid_moves:
            if move == valid_move:
                return valid_move

        return move

    def check_selected_square_validity(self, selected_square):
        current_color = "white" if self.board.is_white_turn else "black"

        if selected_square.get_piece() is None or selected_square.get_piece().get_color() is not current_color:
            return False
        else:
            return True

    def update_game_state(self):
        self.board.count_checks()
        valid_moves_num = 0

        pieces_squares = self.board.get_pieces_squares("white" if self.board.is_white_turn else "black")
        for piece_square in pieces_squares:
            piece = piece_square.get_piece()
            piece_valid_moves = self.board.get_valid_moves(piece_square)
            piece.set_valid_moves(piece_valid_moves)
            valid_moves_num += len(piece_valid_moves)

        if self.board.checks_count > 0 and valid_moves_num == 0:
            self.is_game_running = False
            print("Game Ended by Checkmate")
        elif self.board.checks_count == valid_moves_num == 0:
            self.is_game_running = False
            print("Game Ended by Stalemate")

    def handle_mouse_press(self):
        # a square is selected
        mouse_location = p.mouse.get_pos()
        row = mouse_location[1] // self.sq_size
        col = mouse_location[0] // self.sq_size
        selected_square = self.board.get_square(row, col)
        self.selected_squares.append(selected_square)

        if len(self.selected_squares) == 1:
            # initial square selection
            selected_square = self.selected_squares[0]

            if not self.check_selected_square_validity(selected_square):
                # the selected square is empty
                self.selected_squares.clear()
            else:
                # highlight valid moves
                piece = selected_square.get_piece()
                self.valid_moves = piece.get_valid_moves()
                self.highlight_valid_moves(selected_square)
        elif len(self.selected_squares) == 2:
            # final square selection
            initial_square = self.selected_squares[0]
            final_square = self.selected_squares[1]

            if initial_square != final_square:
                # if the two selected squares are different
                # get the move object in "self.valid_moves" as it contains important info which is not found in "move"
                move = Move(initial_square, final_square)
                move = self.get_valid_move(move)

                if self.check_move_validity(move):
                    self.board.execute_move(move)
                    # if self.board.count_checks() > 0:
                    print("checks count: ", self.board.checks_count)

                    self.board.update_board_state()
                    self.update_game_state()

            # if the move is executed or the two selected squares are invalid
            self.clear_valid_moves_highlight(initial_square)
            self.selected_squares.clear()
        else:
            self.selected_squares.clear()
            print("unexpected number of clicks: ", len(self.selected_squares))

    def run_game(self):
        self.is_game_running = True
        self.update_game_state()

        # game loop
        while self.is_game_running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    self.is_game_running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    self.handle_mouse_press()
                else:
                    pass
                    # print("event: ", e)

            # update board
            self.draw_board()
            self.draw_pieces()
            self.clock.tick(self.max_fps)
            p.display.flip()
