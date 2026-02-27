"""
generators.py
Practice 4 — Iterators & Generators
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator, Iterable


def demo_iter_and_next() -> None:
    numbers = [10, 20, 30]
    it = iter(numbers)
    print("iter/next demo:")
    print(next(it))  
    print(next(it))  
    print(next(it))  
    print()


def demo_loop_iterator() -> None:
    text = "abc"
    it = iter(text)
    print("Loop through iterator:")
    for ch in it:
        print(ch)
    print()


@dataclass
class CountDown:
    """
    Custom Iterator:
    CountDown(5) -> 5,4,3,2,1
    """
    start: int

    def __post_init__(self) -> None:
        if self.start < 0:
            raise ValueError("start must be >= 0")
        self._current = self.start

    def __iter__(self) -> "CountDown":
        return self

    def __next__(self) -> int:
        if self._current <= 0:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value


def squares_generator(n: int) -> Iterator[int]:
    """Generator function that yields squares from 1..n."""
    if n < 0:
        raise ValueError("n must be >= 0")
    for i in range(1, n + 1):
        yield i * i


def even_numbers(limit: int) -> Iterator[int]:
    """Yields even numbers from 0..limit inclusive."""
    if limit < 0:
        raise ValueError("limit must be >= 0")
    for x in range(0, limit + 1):
        if x % 2 == 0:
            yield x


def demo_generators() -> None:
    print("Generator function (squares):", list(squares_generator(7)))
    print("Generator function (evens):", list(even_numbers(12)))

    gen_expr = (x * 2 for x in range(5))
    print("Generator expression:", list(gen_expr))
    print()


def main() -> None:
    demo_iter_and_next()
    demo_loop_iterator()

    print("Custom iterator (CountDown):")
    for v in CountDown(5):
        print(v, end=" ")
    print("\n")

    demo_generators()


if __name__ == "__main__":
    main()