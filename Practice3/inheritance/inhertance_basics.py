class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return "Meow"

class Dog(Animal):
    def speak(self):
        return "Woof"

if __name__ == "__main__":
    cat = Cat("Murka")
    dog = Dog("Rex")

    print(cat.name, "says", cat.speak())
    print(dog.name, "says", dog.speak())

    animals = [cat, dog]
    for a in animals:
        print(a.name, "->", a.speak())

    base = Animal("Unknown")
    print(base.name, "says", base.speak())
