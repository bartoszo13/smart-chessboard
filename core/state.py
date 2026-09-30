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

def hamming(a, b):
    if len(a) != len(b):
        raise ValueError("err: the readings must be the same length")
    
    distance = 0
    
    for x, y in zip(a, b):
        if x != y: 
            distance += 1

    return distance

if __name__ == "__main__":
    a = observe(chess.Board())
    print(a)
    print(hamming(a, a))