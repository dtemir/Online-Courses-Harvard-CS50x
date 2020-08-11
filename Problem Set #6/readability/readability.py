from cs50 import get_string

text = get_string("Text: ")

letters = 0
words = 0
sentences = 0

for i in range(len(text)):
    c = text[i]
    if ((c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z')):
        letters += 1
    elif (c == ' '):
        words += 1
    elif (c == '.' or c == '!' or c == '?'):
        sentences += 1
words += 1

L = (float(letters) * 100) / float(words)
S = (float(sentences) * 100) / float(words)

index = 0.0588 * L - 0.296 * S - 15.8
index = round(index)

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {int(index)}")