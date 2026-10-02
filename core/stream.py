from collections import deque

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
