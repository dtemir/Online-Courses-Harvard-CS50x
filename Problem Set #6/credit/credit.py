from cs50 import get_int

n = get_int("Number: ")

while n < 1: 
    n = get_int("Number: ")

# print(n)

length = 0
first = 0
second = 0
firstDigit = 0
secondDigit = 0

while n > 1:
    curr = int(n % 10) 
    # print(curr)
    n = n / 10
    length += 1
    
    if length % 2 == 0:
        temp = curr * 2
        if temp > 9:
            first += int(temp - 10)
            first += int((temp / 10) % 10)
        else:
            first += int(temp)
    else:
        second += curr
    
    if firstDigit != secondDigit:
        secondDigit = firstDigit
    
    firstDigit = curr
    
# print(firstDigit, end = " ")
# print(secondDigit)
# print(length)
# print(f"{first} {second}")

    
if ((first + second) % 10 == 0):
    if (length == 15 and (firstDigit == 3 and (secondDigit == 4 or secondDigit == 7))):
        print("AMEX")
    elif (length == 16 and (firstDigit == 5 and (secondDigit == 1 or secondDigit == 2 or secondDigit == 3 or secondDigit == 4 or secondDigit == 5))):
        print("MASTERCARD")
    elif ((length == 13 or length == 16) and firstDigit == 4):
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")