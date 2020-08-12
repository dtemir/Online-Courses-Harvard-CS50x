from sys import argv
import csv
from cs50 import SQL

if len(argv) != 2: 
    print("python import.py characters.csv")
    exit()
    
db = SQL("sqlite:///students.db")

with open(argv[1], "r") as database:
    reader = csv.reader(database)
    
    line_number = 0
    
    for row in reader:
     
        if line_number != 0:
            name = row[0].split()
            school = row[1]
            year = row[2]
            if len(name) == 2:
                name.insert(1, None)

            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(%s, %s, %s, %s, %s)", 
                       name[0], name[1], name[2], school, year)
            
        line_number += 1