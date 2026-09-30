import chess
import pytest

from core.state import observe, hamming

# observe
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


# hamming
def test_hamming_identical_is_zero():
    a = observe(chess.Board())
    assert hamming(a, a) == 0

def test_hamming_after_e2e4():
    board = chess.Board()
    board.push_uci("e2e4")
    assert hamming(observe(board), observe(chess.Board())) == 2

def test_hamming_after_e2e4_e7e5():
    board = chess.Board()
    board.push_uci("e2e4")
    board.push_uci("e7e5")
    assert hamming(observe(board), observe(chess.Board())) == 4

def test_hamming_different_lengths_raises():
    with pytest.raises(ValueError):
        hamming((1, 0), (1, 0, 0))