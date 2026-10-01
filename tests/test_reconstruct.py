import chess

from core.reconstruct import score_moves
from core.state import observe


def test_score_moves_finds_e2e4():
    board = chess.Board()
    real = chess.Board()
    real.push_uci("e2e4")
    scores = score_moves(board, observe(real))
    assert (0, chess.Move.from_uci("e2e4")) in scores
    assert len(scores) == 20


def test_score_moves_does_not_change_board():
    board = chess.Board()
    real = chess.Board()
    real.push_uci("e2e4")
    score_moves(board, observe(real))
    assert board.fen() == chess.Board().fen()