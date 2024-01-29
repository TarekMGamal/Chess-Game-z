import socket
from _thread import *

server = "192.168.1.51"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("server started, waiting for connections...")


def make_client(connection):
    while True:
        try:
            data = connection.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("disconnected")
                break
            else:
                print("received: ", reply)
                print("sending: ", reply)

            encoded_reply = str.encode(reply)
            connection.sendall(encoded_reply)
        except error:
            print("an error occurred: ", error)
            break


def make_server():
    while True:
        connection, ip_address = s.accept()

        print("connected to: ", ip_address)

        start_new_thread(make_client, (connection, ))


make_server()
