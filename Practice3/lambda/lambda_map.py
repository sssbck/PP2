
numbers = [-2, -1, 0, 1, 2]

squares = list(map(lambda x: x * x, numbers))
print("squares:", squares)

abs_values = list(map(lambda x: abs(x), numbers))
print("abs:", abs_values)

labeled = list(map(lambda x: f"num={x}", numbers))
print("labeled:", labeled)

step1 = list(map(lambda x: x + 5, numbers))
step2 = list(map(lambda x: x * 2, step1))
print("chain:", step2)
