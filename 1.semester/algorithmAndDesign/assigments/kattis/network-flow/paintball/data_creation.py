import random

with open("hello.txt", "w") as f:
    f.write("1000 5000\n")
    for i in range(0, 5000):
        n1 = (i % 1000) + 1
        n2 = random.randint(1, 1000)
        f.write(f"{n1}  {n2}")
        f.write("\n")