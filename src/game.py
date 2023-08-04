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

    def draw_board(self, first_color, second_color):
        for row in range(self.dimension):
            for c in range(self.dimension):
                is_first_color = True if (row + c) % 2 == 0 else False
                color = p.Color(first_color) if is_first_color else p.Color(second_color)
                p.draw.rect(self.screen, color, p.Rect(c * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size)
                            )

    def draw_pieces(self):
        for r in range(self.dimension):
            for c in range(self.dimension):
                piece = self.board.get_piece(r, c)
                if piece is not None:
                    color = piece.get_color()
                    name = piece.get_name()
                    image_name = color + ' ' + name

                    # access the piece image stored in the "IMAGES" dict previously loaded in the "load_images" function
                    piece_image = self.assets[image_name]

                    # draw the piece in it's required square
                    self.screen.blit(piece_image, p.Rect(c * self.sq_size, r * self.sq_size, self.sq_size, self.sq_size)
                                     )

    def highlight_valid_moves(self, valid_moves_color):
        print("highlight valid moves")

    def clear_valid_moves_highlight(self):
        print("clear valid moves highlight")

    def check_move_validity(self, move):
        for valid_move in self.valid_moves:
            if move == valid_move:
                return True

        return False

    def handle_mouse_press(self):
        # a square is selected
        mouse_location = p.mouse.get_pos()
        row = mouse_location[1] // self.sq_size
        col = mouse_location[0] // self.sq_size
        selected_square = self.board.get_square(row, col)
        self.selected_squares.append(selected_square)

        if len(self.selected_squares) == 1:
            # initial square selection
            if self.selected_squares[0].get_piece() is None:
                # the selected square is empty
                self.selected_squares.clear()
            else:
                # highlight valid moves
                selected_square = self.selected_squares[0]
                self.valid_moves = self.board.get_valid_moves(selected_square)
                self.highlight_valid_moves("yellow")
        elif len(self.selected_squares) == 2:
            # final square selection
            if self.selected_squares[0] != self.selected_squares[1]:
                # if the two selected squares are different
                initial_square = self.selected_squares[0]
                final_square = self.selected_squares[1]
                move = Move(initial_square, final_square)

                if self.check_move_validity(move):
                    self.board.execute_move(move)

            self.selected_squares.clear()
            self.valid_moves = []
            self.clear_valid_moves_highlight()
        else:
            self.selected_squares.clear()
            print("unexpected number of clicks: ", len(self.selected_squares))

    def run_game(self):
        self.is_game_running = True

        # game loop
        while self.is_game_running:
            for e in p.event.get():
                if e.type == p.quit:
                    self.is_game_running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    self.handle_mouse_press()

            self.draw_board("white", "dark grey")
            self.draw_pieces()
            self.clock.tick(self.max_fps)
            p.display.flip()
