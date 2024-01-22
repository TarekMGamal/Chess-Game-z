class Piece:
    def __init__(self, color, value, name):
        self.color = color
        self.is_alive = True
        self.name = name
        self.value = value
        self.valid_moves = []
        self.is_pinned = False
        self.is_moved = False

        # tuple of two values indicating the direction of the pin
        # the tuple is calculated by subtracting final square from initial square coordinates
        # and simplifying the values to ones and zeros
        # a piece can't be pinned in more than one direction, so only one tuple is needed
        self.pin = ()

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

    def get_pin_direction(self):
        return self.pin

    def set_pin(self, direction_tuple):
        self.is_pinned = True
        self.pin = direction_tuple

    def clear_pins(self):
        self.is_pinned = False
        self.pin = ()

    def get_is_moved(self):
        return self.is_moved

    def set_moved(self):
        self.is_moved = True
