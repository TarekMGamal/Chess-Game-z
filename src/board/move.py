class Move:
    def __init__(self , initial , final):
        self.initial = initial
        self.final = final

    def get_initail_move(self):
        return self.initial
    
    def get_final_move(self):
        return self.final