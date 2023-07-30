from boards.board import Board

if __name__ == '__main__':
    print("Hello Chess!")

    b = Board()

    squares = b.get_squares()
    for i in range(8):
        for j in range(8):
            square = squares[i][j]
            print(square.get_color(), end=' ')

        print()

    print()

    for i in range(8):
        for j in range(8):
            square = squares[i][j]
            piece = square.get_piece()
            if piece is not None:
                print(piece.name, end=' ')

        print()

    square = b.get_square(0, 3)
    lista = b.get_valid_moves(square)
    print(lista)
    print(len(lista))

    # move = lista[8]
    # b.move_piece(move)

    for i in range(8):
        for j in range(8):
            square = squares[i][j]
            piece = square.get_piece()
            if piece is not None:
                print(piece.name, end=' ')
            else:
                print('     ', end=' ')

        print()

    print('done')
