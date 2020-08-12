from sys import argv
from cs50 import SQL

if len(argv) != 2:
    print("python roster.py Gryffindor")
    exit()

db = SQL("sqlite:///students.db")

school = argv[1]

dict = db.execute("SELECT first, middle, last, birth FROM students WHERE house = %s ORDER BY last, first", school)

for i in range(len(dict)):
    first = dict[i].get("first")
    middle = dict[i].get("middle")
    last = dict[i].get("last")
    year = dict[i].get("birth")
    
    if middle == None:
        print(f"{first} {last}, born {year}")
    else:
        print(f"{first} {middle} {last}, born {year}")
    