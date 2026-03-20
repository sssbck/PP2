from pathlib import Path

file_path = Path("example.txt")

with open(file_path, "w") as f:
    f.write("Hello\n")
    f.write("This is Practice 6\n")

with open(file_path, "a") as f:
    f.write("Appended line\n")

print("File created and updated")