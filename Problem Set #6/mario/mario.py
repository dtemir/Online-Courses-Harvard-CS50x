from cs50 import get_int

height = get_int("Height: ")
while height < 1 or height > 8:
    height = get_int("Height: ")

for i in range(height):
    for j in range(height - i - 1):
        print(" ", end="")
    for b in range(i + 1):
        print("#", end="")
    print("  ", end="")
    for b in range(i + 1):
        print("#", end="")
    print("")
        