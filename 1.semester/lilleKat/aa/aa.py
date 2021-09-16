import fileinput
import sys

def main():
    n, word_list = get_formatted_data()

    word_list_sorted = word_list.copy()
    word_list_sorted.sort()

    if(word_list == word_list_sorted):
        print("yes")
    else:
        print("no")



def get_formatted_data():
    data_input = create_data_input()
    n = int(data_input.readline())
    res = []
    for i in range(n):
        line = data_input.readline().replace("\n", "")
        res.append(line)
    return n, res


def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data

if __name__ == "__main__":
    main()

