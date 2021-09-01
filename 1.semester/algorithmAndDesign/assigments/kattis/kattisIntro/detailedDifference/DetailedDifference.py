import fileinput

def main():
    finalRes = ""
    t = fileinput.input()
    num = int(t.readline())

    for i in range(num):
        line1 = t.readline()
        line2 = t.readline()

        res = ""
        for x in range(len(line1) - 1):
            if line1[x] != line2[x]:
                res += "*"
            else:
                res += "."
       
        finalRes += line1  + line2  + res +  "\n"
        if(i != num - 1):
            finalRes += "\n"

    print(finalRes, end = "")

if __name__ == "__main__":
    main()


