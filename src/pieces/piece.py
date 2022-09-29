class Piece:
    def __init__(self , x , y , color):
        self.x = x
        self.y = y
        self.color = color
        self.alive = True
        self.name = 'piece'

    def move(self , new_x , new_y):
        self.x = new_x
        self.y = new_y

    def kill_piece(self):
        self.alive = False