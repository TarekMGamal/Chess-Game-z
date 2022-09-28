class Board:
    def __init__(self):
        self.squares = [[0]*8 for _ in range(8)]
        
    def add_piece(self , piece , x , y):
        self.squares[x][y] = piece