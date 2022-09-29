from board.square import Square
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.king import King
from pieces.queen import Queen
from pieces.pawn import Pawn
from pieces.rook import Rook

class Board:
    def __init__(self):
        self.squares = [[0]*8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                color = 'white' if (i + j) % 2 == 0 else 'black'
                self.squares[i][j] = Square(i,j,color)
        
        for color in ['black' , 'white']:
            # pieces_row , pawns_row = 0 , 0
            if color == 'black':
                pieces_row , pawns_row = 0 , 1
            else:
                pieces_row , pawns_row = 7 , 6

            self.add_piece(Rook(pieces_row,0,color),pieces_row,0)
            self.add_piece(Rook(pieces_row,7,color),pieces_row,7)
            self.add_piece(Knight(pieces_row,1,color),pieces_row,1)
            self.add_piece(Knight(pieces_row,6,color),pieces_row,6)
            self.add_piece(Bishop(pieces_row,2,color),pieces_row,2)
            self.add_piece(Bishop(pieces_row,5,color),pieces_row,5)
            self.add_piece(Queen(pieces_row,3,color),pieces_row,3)
            self.add_piece(King(pieces_row,4,color),pieces_row,4)

            for j in range(8):
                self.add_piece(Pawn(pawns_row,j,color),pawns_row,j)
    
        
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