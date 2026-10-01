import chess

from core.state import observe, hamming

def score_moves(board, observed):
    scores = []
    for move in list(board.legal_moves):
        board.push(move)

        distance = hamming(observed, observe(board))
        board.pop()

        scores.append((distance, move))

    return scores