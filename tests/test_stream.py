import pytest
import chess

from core.reconstruct import Status
from core.stream import Debouncer, Tracker
from core.state import observe

A = (0,)
B = (1,)

def test_returns_reading_after_identical_n():
    d = Debouncer(3)
    results = []
    for reading in [A, A, A]:
        results.append(d.update(reading))
    assert results == [None, None, A]


def test_none_when_readings_differ():
    d = Debouncer(3)
    results = []
    for reading in [A, A, B]:
        results.append(d.update(reading))
    assert results == [None, None, None]


def test_n_equal_one_passes_immediately():
    d = Debouncer(1)
    results = []
    for reading in [A]:
        results.append(d.update(reading))
    assert results == [A]


def test_flicker_blocks_stability():
    d = Debouncer(3)
    results = []
    for reading in [A, A, A, B, A, A, A]:
        results.append(d.update(reading))
    assert results == [None, None, A, None, None, None, A]


def test_readings_differ():
    d = Debouncer(3)
    results = []
    for reading in [A, A, A, B, B, B]:
        results.append(d.update(reading))
    assert results == [None, None, A, None, None, B]
    

def test_debouncer_rejects_n_below_one():
    with pytest.raises(ValueError):
        Debouncer(0)

def test_unstable_when_reading_changes():
    board = chess.Board()
    t = Tracker(board, 3, 1)
    before = observe(chess.Board())
    after_board = chess.Board()
    after_board.push_uci("e2e4")
    after = observe(after_board)

    assert t.update(before) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(before) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(after) == (Status.UNRELIABLE_SIGNAL, None)

def test_no_change_after_three_identical_readings():
    board = chess.Board()
    t = Tracker(board, 3, 1)
    start = observe(chess.Board())

    assert t.update(start) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(start) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(start) == (Status.NO_CHANGE, None)

def test_move_recognized_after_stable_readings():
    board = chess.Board()
    t = Tracker(board, 3, 1)
    start_board = chess.Board()
    start = observe(start_board)

    assert t.update(start) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(start) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(start) == (Status.NO_CHANGE, None)

    start_board.push_uci("e2e4")
    moved = observe(start_board)
    assert t.update(moved) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(moved) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(moved) == (Status.MOVE, chess.Move.from_uci("e2e4"))
    assert board.fen() == start_board.fen()

def test_no_change_after_another_reading_after_move():
    board = chess.Board()
    t = Tracker(board, 3, 1)
    start_board = chess.Board()
    start = observe(start_board)

    assert t.update(start) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(start) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(start) == (Status.NO_CHANGE, None)

    start_board.push_uci("e2e4")
    moved = observe(start_board)
    assert t.update(moved) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(moved) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(moved) == (Status.MOVE, chess.Move.from_uci("e2e4"))
    assert t.update(moved) == (Status.NO_CHANGE, None)

def test_unknown_when_two_wrong_squares():
    board = chess.Board()
    t = Tracker(board, 3, 1)
    start_board = chess.Board()
    start = list(observe(start_board))
    start[chess.A3] = 1
    start[chess.H3] = 1
    start = tuple(start)

    assert t.update(start) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(start) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(start) == (Status.UNKNOWN, None)
    assert board.fen() == chess.Board().fen()


def test_two_moves_recognized_after_stable_readings():
    board = chess.Board()
    t = Tracker(board, 3, 1)
    start_board = chess.Board()
    start = observe(start_board)

    assert t.update(start) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(start) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(start) == (Status.NO_CHANGE, None)

    start_board.push_uci("e2e4")
    after_e4 = observe(start_board)
    assert t.update(after_e4) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(after_e4) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(after_e4) == (Status.MOVE, chess.Move.from_uci("e2e4"))
    assert board.fen() == start_board.fen()

    start_board.push_uci("e7e5")
    after_e5 = observe(start_board)
    assert t.update(after_e5) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(after_e5) == (Status.UNRELIABLE_SIGNAL, None)
    assert t.update(after_e5) == (Status.MOVE, chess.Move.from_uci("e7e5"))
    assert board.fen() == start_board.fen()
