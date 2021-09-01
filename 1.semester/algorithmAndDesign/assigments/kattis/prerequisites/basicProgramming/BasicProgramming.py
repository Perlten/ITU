import fileinput


def main():
    input = fileinput.input()
    f_line = input.readline().replace("\n", "").split(" ")
    n = int(f_line[0])
    t = f_line[1]
    arr = [int(x) for x in input.readline().split(" ")]

    if t == "1":
        print(7)
    elif t == "2":
        if arr[0] > arr[1]:
            print("Bigger")
        elif arr[0] == arr[1]:
            print("Equal")
        else:
            print("Smaller")
    elif t == "3":
        sortedArr = [arr[0], arr[1], arr[2]]
        sortedArr.sort()
        print(sortedArr[1])
    elif t == "4":
        print(sum(arr))
    elif t == "5":
        print(sum([x for x in arr if x % 2 == 0]))
    elif t == "6":
        print("".join([chr((x % 26) + 97)  for x in arr]))
    elif t == "7":
        i = 0
        count = 0

        while(True):
            count = count + 1
            i = arr[i]
            if i > n - 1 or i < 0:
                print("Out")
                break
            elif i == n - 1:
                print("Done")
                break
            elif count == n:
                print("Cyclic")
                break


if __name__ == "__main__":
    main()
