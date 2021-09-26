import fileinput
import sys
import math

def main():
    data = get_formatted_data()
    print(solve(data))


def solve(intervals: list) -> int:
    n = len(intervals)

    intervals.sort(key=lambda arr: arr[1])

    M = {}

    for i in range(n):
        s, _, w = intervals[i]
        if i == 0:
            M[i] = 0
        elif i == 1:
            M[i] = w
        else:
            x = binary_search(i, intervals, s, i // 2, i)

            take = w if x == -1 else w + M[x]
            drop: int = 0 + M[i - 1]

            M[i] = max(take, drop)

    return M[n - 1]


def binary_search(start_index: int, intervals: list, start_time: int, lookup_index: int, previous_index: int = 0):
    lookup = intervals[lookup_index]
    _, finish_time, _ = lookup

    if (finish_time > start_time):
        if(lookup_index == 0):
            return -1

        return binary_search(start_index, intervals, start_time, lookup_index // 2, lookup_index)
    elif (finish_time < start_time):
        if (start_index != lookup_index + 1 and intervals[lookup_index + 1][1] > start_time):
            return lookup_index

        return binary_search(start_index, intervals, start_time, math.ceil((lookup_index + previous_index) / 2), lookup_index)
    else:
        return lookup_index


def get_formatted_data() -> list:
    data_input = create_data_input()

    n: int = int(data_input.readline())

    interval_list = []

    for _ in range(n):
        interval_list.append(
            [int(x) for x in data_input.readline().strip().split(" ")])

    return interval_list


def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data


if __name__ == "__main__":
    main()
