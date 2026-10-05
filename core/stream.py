from collections import deque
from core.reconstruct import detect_move, Status

class Debouncer:
    def __init__(self, n=3):
        if n < 1:
            raise ValueError("err: n must be at leat 1")
        
        self.n = n
        self.stack = deque(maxlen=n)

    def update(self, reading):
        self.stack.append(reading)

        if len(self.stack) < self.n:
            return None

        for i in range(len(self.stack) - 1):
            if self.stack[i] != self.stack[i + 1]:
                return None

        return reading

class Tracker:
    def __init__(self, board, n=3, max_distance=1):
        self.debouncer = Debouncer(n)
        self.board = board
        self.max_distance = max_distance

    def update(self, reading):
        stable = self.debouncer.update(reading)
        if stable is None:
            return (Status.UNRELIABLE_SIGNAL, None)

        status, move = detect_move(self.board, stable, self.max_distance)
        if status == Status.MOVE:
            self.board.push(move)

        return (status, move)
    