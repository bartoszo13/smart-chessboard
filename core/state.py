import chess

def observe(board):
    board_list = []

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is None:
            board_list.append(0)
        elif piece.color == chess.WHITE:
            board_list.append(1)
        else:
            board_list.append(2)


    return tuple(board_list)

if __name__ == "__main__":
    print(observe(chess.Board()))