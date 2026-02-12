

def greet(name: str) -> None:
    print(f"Hello, {name}!")

def add(a: int, b: int) -> int:
    return a + b

def is_even(n: int) -> bool:
    return n % 2 == 0

def print_line() -> None:
    print("-" * 40)

if __name__ == "__main__":
    greet("Aman")

    print_line()
    result = add(10, 5)
    print("10 + 5 =", result)

    print_line()
    for x in [1, 2, 3, 4]:
        print(x, "is even?", is_even(x))

    print_line()
    print_line()
    print_line()
