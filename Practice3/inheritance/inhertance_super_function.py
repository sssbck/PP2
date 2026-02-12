class Person:
    def __init__(self, name: str):
        self.name = name

    def intro(self):
        return f"My name is {self.name}"

class Student(Person):
    def __init__(self, name: str, gpa: float):
        super().__init__(name)  # call parent constructor
        self.gpa = gpa

    def intro(self):
        return f"{super().intro()} and my GPA is {self.gpa}"

if __name__ == "__main__":
    s = Student("Aman", 3.5)

    print("name:", s.name)

    print("gpa:", s.gpa)

    print(s.intro())

    p = Person("Bob")
    print(p.intro())
