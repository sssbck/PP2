
nums = list(range(-5, 11))

positives = list(filter(lambda x: x > 0, nums))
print("positives:", positives)

evens = list(filter(lambda x: x % 2 == 0, nums))
print("evens:", evens)

div_by_3 = list(filter(lambda x: x % 3 == 0, nums))
print("div_by_3:", div_by_3)

scores = [45, 60, 75, 82, 90, 33]
passed = list(filter(lambda s: s >= 60, scores))
print("passed:", passed)
