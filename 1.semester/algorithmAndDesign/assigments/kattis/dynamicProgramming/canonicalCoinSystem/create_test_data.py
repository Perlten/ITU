from random import randint

AMOUNT = 100

value_list = []
value_used: set = set()
while (len(value_list) < AMOUNT - 1):
    value = randint(0, 1000000)
    if( value not in value_used):
        value_list.append(value)
        value_used.add(value)

value_list.sort()

with open ("test_data.in", 'w') as file:
    file.write(str(AMOUNT) + "\n")
    file.write("1 ")
    for value in value_list:
        file.write(str(value))
        file.write(" ")
    print("file created")