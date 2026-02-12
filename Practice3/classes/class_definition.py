

class Dog:
    def bark(self):
        print("Woof!")

    def info(self, name: str, age: int):
        print(f"Dog name: {name}, age: {age}")

if __name__ == "__main__":
    # Example 1: create object
    d = Dog()
    d.bark()

    # Example 2: call method with parameters
    d.info("Rex", 3)

    # Example 3: multiple objects
    d2 = Dog()
    d2.info("Buddy", 5)

    # Example 4: objects are independent
    d.bark()
    d2.bark()
