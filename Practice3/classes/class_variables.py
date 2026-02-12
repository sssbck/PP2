class Laptop:
    warranty_years = 2

    def __init__(self, brand: str):
        self.brand = brand

if __name__ == "__main__":
    l1 = Laptop("Dell")
    l2 = Laptop("HP")

    print(l1.brand, "warranty:", l1.warranty_years)
    print(l2.brand, "warranty:", l2.warranty_years)

    Laptop.warranty_years = 3
    print("After changing class variable:")
    print(l1.brand, "warranty:", l1.warranty_years)
    print(l2.brand, "warranty:", l2.warranty_years)

    l1.warranty_years = 10 
    print("After overriding for l1 only:")
    print(l1.brand, "warranty:", l1.warranty_years)
    print(l2.brand, "warranty:", l2.warranty_years)

    del l1.warranty_years
    print("After deleting override:")
    print(l1.brand, "warranty:", l1.warranty_years)
