import fileinput
import sys
from typing import Counter


def main():
    n, intervals = get_formatted_data()
    non_overlapping_intervals = run_interval_scheduling(n, intervals)
    print(non_overlapping_intervals)


def run_interval_scheduling(n: int, intervals: list) -> int:
    intervals = sorted(intervals, key=lambda i: i[1])
    base_end_time = -1
    non_overlapping_intervals = 0
    for interval in intervals:
        if(base_end_time == -1 or base_end_time <= interval[0]):
            base_end_time = interval[1]
            non_overlapping_intervals += 1

    return non_overlapping_intervals

def get_formatted_data() -> list:
    data_input = create_data_input()
    n = int(data_input.readline())
    intervals = []
    for i in range(n):
        intervals.append([int(x) for x in data_input.readline().replace("\n", "").split(" ")])
    return n, intervals


def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data


if __name__ == "__main__":
    main()
