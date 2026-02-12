
def power(base: int, exponent: int = 2) -> int:
    return base ** exponent

def format_name(first: str, last: str, middle: str = "") -> str:
    if middle:
        return f"{first} {middle} {last}"
    return f"{first} {last}"

def repeat_text(text: str, times: int = 3) -> str:
    return " ".join([text] * times)

def clamp(value: int, low: int, high: int) -> int:
    if value < low:
        return low
    if value > high:
        return high
    return value

if __name__ == "__main__":
    print("power(3, 4) =", power(3, 4))

    print("power(5) =", power(5))  
    print(format_name("John", "Smith"))
    print(format_name("John", "Smith", "Michael"))
    print("clamp(15, 0, 10) =", clamp(15, 0, 10))
    print("clamp(-2, 0, 10) =", clamp(-2, 0, 10))
    print("clamp(7, 0, 10) =", clamp(7, 0, 10))
