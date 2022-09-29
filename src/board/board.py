from board.square import Square


class Board:
    def __init__(self):
        self.squares = [[0]*8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                color = 'white' if (i + j) % 2 == 0 else 'black'
                self.squares[i][j] = Square(i,j,color)
        
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