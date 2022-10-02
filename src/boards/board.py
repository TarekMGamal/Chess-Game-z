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
        self.squares = [[0]*8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                color = 'white' if (i + j) % 2 == 0 else 'black'
                self.squares[i][j] = Square(i,j,color)
        
        for color in ['black' , 'white']:
            if color == 'black':
                pieces_row , pawns_row = 0 , 1
            else:
                pieces_row , pawns_row = 7 , 6

            self.add_piece(Rook(color),pieces_row,0)
            self.add_piece(Rook(color),pieces_row,7)
            self.add_piece(Knight(color),pieces_row,1)
            self.add_piece(Knight(color),pieces_row,6)
            self.add_piece(Bishop(color),pieces_row,2)
            self.add_piece(Bishop(color),pieces_row,5)
            self.add_piece(Queen(color),pieces_row,3)
            self.add_piece(King(color),pieces_row,4)

            for j in range(8):
                self.add_piece(Pawn(color),pawns_row,j)
    
    def add_piece(self , piece , x , y):
        self.squares[x][y].add_piece(piece)

    def change_piece(self , piece , x , y):
        self.squares[x][y].change_piece(piece)

    def get_piece(self , x , y):
        return self.squares[x][y].get_piece()

    def get_square(self , x , y):
        return self.squares[x][y]

    def get_squares(self):
        return self.squares
    
    def move_piece(self , move):
        squares = self.squares
        
        initial_square = move.get_initial_square()
        final_square = move.get_final_square()
        
        initial_x = initial_square.get_row()
        initial_y = initial_square.get_col()
        final_x = final_square.get_row()
        final_y = final_square.get_col()
        
        initial_square = squares[initial_x][initial_y]
        final_square = squares[final_x][final_y]
        
        piece = initial_square.get_piece()
        initial_square.remove_piece()
        
        old_piece = final_square.get_piece()
        if old_piece == None:
            final_square.add_piece(piece)
        else:
            old_piece.kill_piece()
            final_square.change_piece(piece)
        
    def get_valid_moves(self , square):
        piece = square.get_piece()
        x = square.get_row()
        y = square.get_col()
        empty_valid_moves = []
        
        if piece == None:
            return empty_valid_moves
        elif piece.get_name() == 'pawn':
            return self.get_pawn_valid_moves(piece , x , y)
        elif piece.get_name() == 'king':
            return self.get_king_valid_moves(piece , x , y)
        elif piece.get_name() == 'queen':
            return self.get_queen_valid_moves(piece , x , y)
        elif piece.get_name() == 'rook':
            return self.get_rook_valid_moves(piece , x , y)
        elif piece.get_name() == 'bishop':
            return self.get_bishop_valid_moves(piece , x , y)
        elif piece.get_name() == 'knight':
            return self.get_knight_valid_moves(piece , x , y)
        else:
            return empty_valid_moves
    
    def get_pawn_valid_moves(piece , x , y):
        valid_moves = []
        return valid_moves
    
    def get_king_valid_moves(piece , x , y):
        valid_moves = []
        return valid_moves
    
    def get_queen_valid_moves(piece , x , y):
        valid_moves = []
        return valid_moves
    
    def get_rook_valid_moves(piece , x , y):
        valid_moves = []
        return valid_moves
    
    def get_bishop_valid_moves(piece , x , y):
        valid_moves = []
        return valid_moves
    
    def get_knight_valid_moves(piece , x , y):
        valid_moves = []
        return valid_moves