import chess
from enum import Enum

from core.state import observe, hamming

class Status(Enum):
    NO_CHANGE = "no_change"
    MOVE = "move"
    UNKNOWN = "unknown"
    UNRELIABLE_SIGNAL = "unreliable_signal"

def score_moves(board, observed):
    scores = []
    for move in list(board.legal_moves):
        board.push(move)

        distance = hamming(observe(board), observed)
        board.pop()

        scores.append((distance, move))

    return scores

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

# Largest distance from the current position still treated as "no change".
# A real move changes at least 2 cells, so this must stay below 2.
NO_CHANGE_MAX = 1

def detect_move(board, observed, max_distance=1):
    distance = hamming(observe(board), observed)

    if distance <= NO_CHANGE_MAX:
        return (Status.NO_CHANGE, None)
    else:
        score = score_moves(board, observed)
        move = choose_move(score, max_distance)
        
        if move is not None:
            return (Status.MOVE, move)
        else:
            return (Status.UNKNOWN, move)
        