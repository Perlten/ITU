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
        M[i] = intervals[i][2]

    for i in range(1, n):
        s, _, w = intervals[i]

        x = binary_search(intervals, i)

        take: int = w if x == -1 else w + M[x]
        drop: int = 0 + M[i - 1]

        M[i] = max(take, drop)

    return M[n - 1]


def binary_search(intervals: list,  n) -> int:
    low = 0
    high = n
 
    while low <= high:
        mid = (low + high) // 2
        if intervals[mid][1] <= intervals[n][0]:
            if intervals[mid + 1][1] <= intervals[n][0]:
                low = mid + 1
            else:
                return mid
        else:
            high = mid - 1
 
    return -1


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
