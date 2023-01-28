f = open("words.txt", 'r')
f2 = open("custom_insults.txt", 'w')
insults = []
first = []
second = []
third = []

for line in f:
    words = line.split()
    first.append(words[0])
    second.append(words[1])
    third.append(words[2])

length = len(first)

for i in range(length):
    for j in range(length):
        for k in range(length):
            f2.write(first[i] + " " + second[j] + " " + third[k] + "\n")

f.close()
f2.close()