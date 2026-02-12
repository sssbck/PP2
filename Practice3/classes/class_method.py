class Counter:
    def __init__(self):
        self.value = 0

    def inc(self, step: int = 1):
        self.value += step

    def dec(self, step: int = 1):
        self.value -= step

    def reset(self):
        self.value = 0

    def show(self):
        print("Counter =", self.value)

if __name__ == "__main__":
    c = Counter()

    c.inc()
    c.show()

    c.inc(5)
    c.show()

    c.dec(2)
    c.show()

    c.reset()
    c.show()
