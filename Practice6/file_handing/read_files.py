with open("example.txt", "r") as f:
    print("Full content:")
    print(f.read())

with open("example.txt", "r") as f:
    print("First line:")
    print(f.readline())

with open("example.txt", "r") as f:
    print("All lines:")
    print(f.readlines())