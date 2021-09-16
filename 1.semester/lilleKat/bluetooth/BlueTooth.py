
import fileinput
import sys


def main():
    data = get_formatted_data()


def get_formatted_data():
    data_input = create_data_input()
    left_side_top = {"+1", "+2", "+3", "+4", "+5", "+6", "+7", "+8"}
    left_side_bot = {"-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8"}
    
    right_side_top = {"1+", "2+", "3+", "4+", "5+", "6+", "7+", "8+"}
    right_side_bot = {"1-", "2-", "3-", "4-", "5-", "6-", "7-", "8-"}

    n = int(data_input.readline())
   
    blue_tooth_left = False
    
    for i in range(1, n + 1):
        line: str = data_input.readline().replace("\n", "")
        if line.startswith("-") or line.startswith("+"):
            if "+" in line:
                left_side_top.remove(line[:2])
            else:   
                left_side_bot.remove(line[:2])
            if line.split(" ")[1] == "b":
                blue_tooth_left = True
        else:
            if "+" in line:
                right_side_top.remove(line[:2])
            else:
                right_side_bot.remove(line[:2])

    for i in range(1, 9):
        if len(right_side_bot) >= 1 and len(right_side_top) >= 1 and blue_tooth_left:
            print(1)
            break

        elif len(left_side_bot) >= 1 and len(left_side_top) >= 1 and not blue_tooth_left:
            print(0)
            break
        else:
            print(2)
            break


def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data


if __name__ == "__main__":
    main()
