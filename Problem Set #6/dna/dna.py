from sys import argv
import csv
import itertools

if len(argv) != 3: # check if command argument has exactly 3 arguments
    print("dna.py + database + sequence")

a = [] # list for storing max number of repeated STRs

with open(argv[1]) as database, open(argv[2]) as sequence:  # open files
    reader_data = csv.reader(database)  # create csv reader objects
    reader_seq = csv.reader(sequence)
    
    rows_data = list(reader_data)  # list with file data
    rows_seq = list(reader_seq)
    word = rows_seq[0][0]  # assign DNA string
    
    i = 1  # iterator to pick STRs (starting with 1 because rows_data[0][0] is 'name')
    while i < len(rows_data[0]):
        STR = rows_data[0][i] # assign current STR for checking
        # print(f"{i}: {STR}") # debugging
        max = 0  # variable for storing max number of repeated STRs
        curr = 0 # variable for storing current number of repeated STRs
        
        j = 0 # iterator to go through DNA string
        while j < len(word):
            if STR[0] == word[j]: # check characters of STR and DNA to know if we need to check the rest
                if word[j: (j + len(STR))] == STR: # check if the rest of DNA part is equal to STR
                    curr += 1 # increment current count of repeated STRs
                    # print(f"{j} {j + len(STR)} curr: {curr}")
                    j += len(STR) - 1 # increment iterator to skip checking characters 
                    # print(j)
                    if curr > max: # assign current count to maximum
                        max = curr
                else:
                    curr = 0 # drop count 
            else:
                curr = 0 # drop count
                    
            j += 1
        a.append(max) # add max number to the list
        i += 1
    # print(a)
        
    i = 1
    not_found = True # boolean to check if DNA was found or not
    while i < len(rows_data):
        candidate = rows_data[i]
        j = 1
        # print(f"i: {i} candidate: {candidate} a: {a}")
        while j < len(candidate):
            if int(candidate[j]) != a[j - 1]: # check if any of the characters are different 
                break
            if int(candidate[j]) == a[j - 1] and j == len(candidate) - 1: # if last characters are the same, print candidate's name
                print(candidate[0])
                not_found = False # assign false value to boolean
                break
            
            j += 1
        i += 1
    if not_found: # if boolean was not modified, print that there is no match
        print("No match")