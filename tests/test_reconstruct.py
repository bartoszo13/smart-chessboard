import chess

from core.reconstruct import score_moves, choose_move
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

def test_choose_move_after_e2e4():
    board = chess.Board()
    real = chess.Board()
    real.push_uci("e2e4")
    score = score_moves(board, observe(real))
    assert choose_move(score) == chess.Move.from_uci("e2e4")

def test_choose_move_after_e2e4_with_false_move():
    board = chess.Board()
    real = chess.Board()
    real.push_uci("e2e4")
    obs = list(observe(real))
    obs[chess.A1] = 0
    obs = tuple(obs)
    score = score_moves(board, obs)
    assert choose_move(score) == chess.Move.from_uci("e2e4")
    assert choose_move(score, max_distance=0) is None

def test_choose_move_returns_none_when_best_is_too_far():
    board = chess.Board()
    real = chess.Board()
    real.push_uci("e2e4")
    obs = list(observe(real))
    obs[chess.A3] = 1
    obs[chess.H3] = 1
    obs = tuple(obs)
    scores = score_moves(board, obs)
    assert choose_move(scores) is None
    assert choose_move(scores, max_distance=2) == chess.Move.from_uci("e2e4")

def test_choose_move_returns_none_on_tie():
    score = [(1, chess.Move.from_uci("e2e4")), (1, chess.Move.from_uci("d2d4"))]
    assert choose_move(score) is None
