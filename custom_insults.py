f = open("custom_insults.txt", 'r')

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
            insults.append(first[i] + " " + second[j] + " " + third[k])
print(length)
print(insults)