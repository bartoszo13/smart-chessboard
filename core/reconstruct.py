import chess

from core.state import observe, hamming

def score_moves(board, observed):
    scores = []
    for move in list(board.legal_moves):
        board.push(move)

        distance = hamming(observe(board), observed)
        board.pop()

        scores.append((distance, move))

    return scores

#TODO: ERR IF CHECKMATE OR STALEMATE 
def choose_move(scores, max_distance = 1):
    if not scores:
        return None
    
    candidates = []
    best = min(d for d, _ in scores)

    for d, move in scores:
        if d == best:
            candidates.append(move)

    if best > max_distance:
        return None
    
    if len(candidates) == 1:
        return candidates[0]
    
    return None