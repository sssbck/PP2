class Student:
    def __init__(self, name: str, gpa: float):
        self.name = name
        self.gpa = gpa

    def display(self):
        print(f"Student: {self.name}, GPA: {self.gpa}")

if __name__ == "__main__":
    s1 = Student("Aman", 3.5)
    s1.display()

    s2 = Student("Dana", 3.9)
    s2.display()

    s1.gpa = 3.7
    s1.display()

    group = [s1, s2]
    for st in group:
        st.display()
