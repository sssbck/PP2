
square = lambda x: x * x
print("square(5) =", square(5))

add = lambda a, b: a + b
print("add(3,4) =", add(3, 4))

def make_multiplier(k: int):
    return lambda x: x * k

times3 = make_multiplier(3)
print("times3(10) =", times3(10))

def abs_def(x: int) -> int:
    return x if x >= 0 else -x

abs_lambda = lambda x: x if x >= 0 else -x
print("abs_def(-7) =", abs_def(-7))
print("abs_lambda(-7) =", abs_lambda(-7))
