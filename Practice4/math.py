"""
math.py
Practice 4 — Math & Random
"""

from __future__ import annotations
import math
import random


def demo_builtin_math() -> None:
    nums = [3, -7, 10, 2, 2.6]

    print("Built-in math:")
    print("min:", min(nums))
    print("max:", max(nums))
    print("abs(-7):", abs(-7))
    print("round(2.6):", round(2.6))
    print("round(2.65, 1):", round(2.65, 1))
    print("pow(2, 10):", pow(2, 10))
    print()


def demo_math_module() -> None:
    x = 7.9
    angle = math.pi / 3  

    print("math module:")
    print("sqrt(81):", math.sqrt(81))
    print("ceil(7.9):", math.ceil(x))
    print("floor(7.9):", math.floor(x))
    print("sin(pi/3):", math.sin(angle))
    print("cos(pi/3):", math.cos(angle))
    print("pi:", math.pi)
    print("e:", math.e)
    print()


def demo_random() -> None:
    print("random module:")
    print("random():", random.random())  
    print("randint(1, 100):", random.randint(1, 100))

    items = ["A", "B", "C", "D", "E"]
    print("choice(items):", random.choice(items))

    random.shuffle(items)
    print("shuffle(items):", items)
    print()


def main() -> None:
    demo_builtin_math()
    demo_math_module()
    demo_random()


if __name__ == "__main__":
    main()