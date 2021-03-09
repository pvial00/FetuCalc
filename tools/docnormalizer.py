import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

f = open(input_file, "r")
text = f.read()
f.close()

def filter_letters(text):
    newtext = []
    lines = text.split('\n')
    for line in lines:
        for word in line.split():
            for char in word:
                print(char)
                if ord(char) >= 65 and ord(char) <= 90:
                   newtext.append(char)
                elif ord(char) >= 97 and ord(char) <= 122:
                   sub = chr(ord(char) - 32)
                   print(sub)
                   newtext.append(sub)
            newtext.append(" ")
        newtext.append("\n")
    return "".join(newtext)
           
output_text = filter_letters(text)
f = open(output_file, "w")
f.write(output_text)
f.close() 
