import pytest

from core.stream import Debouncer

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
        