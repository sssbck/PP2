
students = [
    {"name": "Alice", "gpa": 3.2},
    {"name": "Bob", "gpa": 3.9},
    {"name": "Charlie", "gpa": 2.8},
]

by_gpa = sorted(students, key=lambda s: s["gpa"])
print("by_gpa:", by_gpa)

by_gpa_desc = sorted(students, key=lambda s: s["gpa"], reverse=True)
print("by_gpa_desc:", by_gpa_desc)

by_name = sorted(students, key=lambda s: s["name"])
print("by_name:", by_name)

words = ["python", "a", "lambda", "hi", "function"]
sorted_words = sorted(words, key=lambda w: (len(w), w))
print("sorted_words:", sorted_words)
