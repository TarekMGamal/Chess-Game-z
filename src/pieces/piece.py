class Piece:
    def __init__(self , color):
        self.color = color
        self.alive = True
        self.name = 'piece'
        self.value = 0
        self.valid_moves = []

    def kill_piece(self):
        self.alive = False
        
    def update_valid_moves(self , valid_moves):
        self.valid_moves = valid_moves