from random import randint

numbers = [0,0,0,0,0,0]

for i in range(0,6000):
    num = randint(0,6)
    numbers[num] = numbers[num]+1

print(numbers[4])
