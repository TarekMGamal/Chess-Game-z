import socket
import pickle
import random


class Network:
    def __init__(self, is_dummy=False):
        self.is_dummy = is_dummy
        self.server = "192.168.1.101"
        self.port = 5555
        self.address = (self.server, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player, self.is_white = self.connect()

    def get_player(self):
        return self.player

    def get_is_white(self):
        return self.is_white

    def connect(self):
        if self.is_dummy:
            return 0, True if random.randint(0, 1) == 1 else False

        try:
            self.client.connect(self.address)
            player_id = self.client.recv(2048*4).decode()
            is_white = self.client.recv(2048*4).decode()  # string value
            is_white = True if is_white == "True" else False  # converted to bool value

            return player_id, is_white
        except socket.error as e:
            print("an error occurred: ", e)

    def send_and_receive(self, move):
        if self.is_dummy:
            return

        try:
            self.client.sendall(pickle.dumps(move))
            new_board = pickle.loads(self.client.recv(2048 * 128))
            return new_board
        except socket.error as e:
            print(e)
