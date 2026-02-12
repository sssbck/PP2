

def sum_all(*args: int) -> int:
    """Sums any number of integer arguments."""
    total = 0
    for x in args:
        total += x
    return total

def print_profile(**kwargs):
    """Prints key-value data of a profile."""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

def build_sentence(*words: str, sep: str = " ") -> str:
    """Builds a sentence from any number of words."""
    return sep.join(words)

def apply_discount(price: float, **kwargs) -> float:
    """
    Applies discounts:
    - percent: percent discount (e.g., 10 means 10%)
    - fixed: fixed discount amount
    """
    percent = kwargs.get("percent", 0)
    fixed = kwargs.get("fixed", 0)

    new_price = price - (price * percent / 100) - fixed
    return max(new_price, 0)

if __name__ == "__main__":
    print("sum_all(1,2,3,4) =", sum_all(1, 2, 3, 4))

    print_profile(name="Alice", age=20, city="Almaty")

    print(build_sentence("I", "love", "Python"))
    print(build_sentence("a", "b", "c", sep="-"))

    print("Discounted:", apply_discount(1000, percent=10))
    print("Discounted:", apply_discount(1000, fixed=250))
    print("Discounted:", apply_discount(1000, percent=10, fixed=50))
