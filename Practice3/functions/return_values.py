
def divide(a: float, b: float):

    if b == 0:
        return None, "Division by zero is not allowed"
    return a / b, None

def find_max(numbers: list[int]) -> int:
    maximum = numbers[0]
    for x in numbers[1:]:
        if x > maximum:
            maximum = x
    return maximum

def grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"

def sign(n: int) -> int:
    if n < 0:
        return -1
    if n > 0:
        return 1
    return 0

if __name__ == "__main__":
    res, err = divide(10, 2)
    print("divide(10,2):", res, err)

    res, err = divide(10, 0)
    print("divide(10,0):", res, err)
    print("max:", find_max([5, 1, 9, 2]))
    for s in [95, 82, 74, 61, 50]:
        print(s, "->", grade(s))
    for x in [-7, 0, 3]:
        print("sign(", x, ") =", sign(x))
