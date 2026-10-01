import chess

from core.reconstruct import score_moves, choose_move, detect_move, Status
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
    scores = score_moves(board, observe(real))
    assert choose_move(scores) == chess.Move.from_uci("e2e4")


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


def test_detect_move_on_unchanged_board():
    board = chess.Board()
    real = chess.Board()
    assert detect_move(board, observe(real)) == (Status.NO_CHANGE, None)


def test_detect_move_on_unchanged_board_with_false_move():
    board = chess.Board()
    obs = list(observe(board))
    obs[chess.A1] = 0
    obs = tuple(obs)
    assert detect_move(board, obs) == (Status.NO_CHANGE, None)


def test_detect_move_after_e2e4():
    board = chess.Board()
    real = chess.Board()
    real.push_uci("e2e4")
    assert detect_move(board, observe(real)) == (Status.MOVE, chess.Move.from_uci("e2e4"))


def test_detect_move_unknown_when_two_cells_wrong():
    # Two wrong cells: too far from any legal move, and several moves tie.
    board = chess.Board()
    obs = list(observe(board))
    obs[chess.A3] = 1
    obs[chess.H3] = 1
    obs = tuple(obs)
    assert detect_move(board, obs) == (Status.UNKNOWN, None)


def test_detect_move_lifted_piece_looks_like_no_change():
    # Snapshot cannot tell a lifted piece from a one-cell sensor error.
    # Telling them apart needs readings over time (next stage).
    board = chess.Board()
    obs = list(observe(board))
    obs[chess.E2] = 0
    obs = tuple(obs)
    assert detect_move(board, obs) == (Status.NO_CHANGE, None)


def test_detect_move_passes_max_distance_to_choose_move():
    board = chess.Board()
    real = chess.Board()
    real.push_uci("e2e4")
    obs = list(observe(real))
    obs[chess.A3] = 1
    obs[chess.H3] = 1
    obs = tuple(obs)
    assert detect_move(board, obs) == (Status.UNKNOWN, None)
    assert detect_move(board, obs, max_distance=2) == (Status.MOVE, chess.Move.from_uci("e2e4"))


def test_detect_move_plain_move_works_with_higher_max_distance():
    board = chess.Board()
    real = chess.Board()
    real.push_uci("e2e4")
    result = detect_move(board, observe(real), max_distance=2)
    assert result == (Status.MOVE, chess.Move.from_uci("e2e4"))


def test_detect_move_unknown_when_game_is_over():
    # Fool's mate: White is checkmated and has no legal moves.
    board = chess.Board("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3")
    obs = list(observe(board))
    obs[chess.A3] = 1
    obs[chess.H3] = 1
    obs = tuple(obs)
    assert detect_move(board, obs) == (Status.UNKNOWN, None)