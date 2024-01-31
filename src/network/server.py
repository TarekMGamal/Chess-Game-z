import pickle
import socket
from _thread import *
from boards.board import Board
from boards.move import Move
import random

server = "192.168.1.67"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
id_count = 0
connected = set()
boards = {}
players_colors = {}

try:
    s.bind((server, port))
except socket.error as e:
    print("an error occurred: ", e)

s.listen(2)
print("server started, waiting for connections...")


def threaded_client(connection, player_id, game_id, is_white):
    global id_count
    connection.sendall(str.encode(str(player_id)))
    connection.sendall(str.encode(str(is_white)))

    while True:
        try:
            if game_id in boards:
                board = boards[game_id]
                if board.is_game_running and board.is_white_turn == is_white:
                    client_move = pickle.loads(connection.recv(2048 * 8))

                    if not client_move:
                        print("disconnected")
                        break
                    else:
                        print("received: ", client_move)
                        # check if the move is valid and then execute the move and update the other player
                        if isinstance(client_move, Move) and board.check_move_validity(client_move):
                            board.execute_move(client_move)
                            print("this should not be pawn in the second time: ", board.get_square(6, 0).get_piece())
                            board.update_board_state()

                            boards[game_id] = board

                        connection.sendall(pickle.dumps(board))
                        print("sending board to: ", player_id)
                elif board.is_game_running:
                    print("sending board to: ", player_id)
                    connection.recv(2048 * 4)
                    connection.sendall(pickle.dumps(board))

        except error:
            print("an error occurred: ", error)
            break

    print("Lost connection")
    try:
        del boards[game_id]
        del players_colors[game_id, player_id]
        print("Closing Game", game_id)
    except error:
        print("an error occurred: ", error)

    id_count -= 1
    connection.close()


def run_server():
    global id_count

    while True:
        connection, address = s.accept()
        print("connected to: ", address)

        id_count += 1
        player_id = 0
        game_id = (id_count - 1)//2

        if id_count % 2 == 1:
            boards[game_id] = Board(game_id)
            is_white = True if random.randint(0, 1) == 1 else False
            players_colors[game_id, player_id] = is_white
            print("creating a new game with game id: ", game_id)
        else:
            player_id = 1
            boards[game_id].is_ready = True
            boards[game_id].is_game_running = True
            is_white = not players_colors[game_id, 1 - player_id]
            players_colors[game_id, player_id] = is_white

        start_new_thread(threaded_client, (connection, player_id, game_id, is_white))


run_server()
