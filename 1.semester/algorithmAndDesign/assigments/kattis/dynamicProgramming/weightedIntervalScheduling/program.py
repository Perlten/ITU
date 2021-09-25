import fileinput
import sys


def main():
    data = get_formatted_data()
    print(solve(data))


def solve(intervals: list) -> int:
    n = len(intervals)

    intervals.sort(key=lambda arr: arr[1])

    M = {}

    for i in range(n):
        s, _, w = intervals[i]
        if i <= 0:
            M[i] = 0
        elif i == 1:
            M[i] = w
        else:
            x = 2

            for j in range(2, i + 1):
                _, f, _ = intervals[i - j]
                if s >= f:
                    x = j
                    break

            take: int = w + M[i - x]
            drop: int = 0 + M[i - 1]

            M[i] = max(take, drop)

    return M[n - 1]


def get_formatted_data() -> list:
    data_input = create_data_input()

    n: int = int(data_input.readline())

    interval_list = []

    for _ in range(n):
        interval_list.append([int(x) for x in data_input.readline().strip().split(" ")])

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
