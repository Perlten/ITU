import sys
import fileinput


def main():
    for line in fileinput.input():
        nums = [int(x) for x in line.split(" ")]
        print(abs(nums[0] - nums[1]))

if __name__ == "__main__":
    main()


