import fileinput
import sys

def main():
    data = get_formatted_data()

def get_formatted_data():
    data_input = create_data_input()

    run = True
    while (run):
        meta_line = data_input.readline().replace("\n", "").split(" ")
        n = int(meta_line[0])
        l = int(meta_line[1])
        w = int(meta_line[2])
        sprinkler_list = []
        for i in range(n): 




def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data

if __name__ == "_main_":
    main()