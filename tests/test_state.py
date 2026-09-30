import chess

from core.state import observe


def test_start_position():
    expected = (1,) * 16 + (0,) * 32 + (2,) * 16
    assert observe(chess.Board()) == expected


def test_after_e2e4():
    board = chess.Board()
    board.push_uci("e2e4")
    obs = observe(board)
    assert obs[chess.E2] == 0   # pole startowe puste
    assert obs[chess.E4] == 1   # biały pionek na e4


def test_black_piece_is_2():
    board = chess.Board()
    board.push_uci("e2e4")
    board.push_uci("e7e5")
    assert observe(board)[chess.E5] == 2