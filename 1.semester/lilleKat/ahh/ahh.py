import fileinput
import sys


def main():
    n1, n2 = get_formatted_data()

    if len(n1) >= len(n2):
        print("go") 
    else: 
        print("no")


def get_formatted_data():
    data_input = create_data_input()
    n1 = data_input.readline().replace("\n", "")
    n2 = data_input.readline().replace("\n", "")
    return n1, n2


def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data


if __name__ == "__main__":
    main()
