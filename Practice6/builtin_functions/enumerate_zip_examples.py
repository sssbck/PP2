names = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 95]

for i, name in enumerate(names):# enumerate
    print(i, name)

for name, score in zip(names, scores):# zip
    print(name, score)

nums = [5, 2, 9, 1] # sorted
print("Sorted:", sorted(nums))

x = "123"
print(int(x), float(x)) # type conversion