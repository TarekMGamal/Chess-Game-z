class Piece:
    def __init__(self, color, value, name):
        self.color = color
        self.is_alive = True
        self.name = name
        self.value = value
        self.valid_moves = []
        self.is_pinned = False

        # list of tuples indicating the directions of the pin
        self.pins = []

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def get_value(self):
        return self.value

    def get_is_alive(self):
        return self.is_alive

    def kill_piece(self):
        self.is_alive = False

    def get_valid_moves(self):
        return self.valid_moves

    def set_valid_moves(self, valid_moves):
        self.valid_moves = valid_moves

    def clear_valid_moves(self):
        self.valid_moves.clear()

    def get_is_pinned(self):
        return self.is_pinned

    def set_pin(self, direction_tuple):
        self.is_pinned = True
        self.pins.append(direction_tuple)

    def clear_pins(self):
        self.pins.clear()
