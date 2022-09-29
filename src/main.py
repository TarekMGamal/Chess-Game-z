from board.board import Board
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook


if __name__ == '__main__':
    print("Hello Chess!")

    b = Board()

    # black pieces
    b.add_piece(Rook(0,0,'black'),0,0)
    b.add_piece(Rook(0,7,'black'),0,7)
    b.add_piece(Knight(0,1,'black'),0,1)
    b.add_piece(Knight(0,6,'black'),0,6)
    b.add_piece(Bishop(0,2,'black'),0,2)
    b.add_piece(Bishop(0,5,'black'),0,5)
    b.add_piece(Queen(0,3,'black'),0,3)
    b.add_piece(King(0,4,'black'),0,4)

    # black pawns
    for j in range(8):
        b.add_piece(Pawn(1,j,'black'),1,j)

    # white pieces
    b.add_piece(Rook(7,0,'white'),7,0)
    b.add_piece(Rook(7,7,'white'),7,7)
    b.add_piece(Knight(7,1,'white'),7,1)
    b.add_piece(Knight(7,6,'white'),7,6)
    b.add_piece(Bishop(7,2,'white'),7,2)
    b.add_piece(Bishop(7,5,'white'),7,5)
    b.add_piece(Queen(7,3,'white'),7,3)
    b.add_piece(King(7,4,'white'),7,4)

    # white pawns
    for j in range(8):
        b.add_piece(Pawn(6,j,'white'),6,j)

    squares = b.get_squares()
    for i in range(8):
        for j in range(8):
            square = squares[i][j]
            print(square.get_color() , end=' ')

        print()
    
    print()

    for i in range(8):
        for j in range(8):
            square = squares[i][j]
            piece = square.get_piece()
            if piece != None:
                print(piece.name , end=' ')

        print()

    print('done')