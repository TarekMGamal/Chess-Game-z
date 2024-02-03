from game import Game
from network.network import Network

if __name__ == '__main__':
    print("Hello Chess!")

    network = Network()

    while True:
        board = network.send_and_receive("get")

        if board:
            print("found a board")
            game = Game(board, network)
            game.run_game()

        print('done')
