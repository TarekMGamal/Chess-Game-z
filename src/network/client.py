from game import Game
from network import Network


def main():
    print("Hello Chess!")

    network = Network()

    while True:
        board = network.send_and_receive("get")

        if board:
            print("found a board: ", board)
            game = Game(board, network)
            game.run_game()
            break

    print('done')


main()
