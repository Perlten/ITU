
import fileinput
import sys
from typing import List
import itertools


def main():
    test_cases, coins = get_formatted_data()
    coins.sort()
    for index, test_case in enumerate(test_cases):
        solve(coins, test_case)

def solve(coins: list, amount: int):
    n = len(coins)
    




def get_formatted_data():
    data_input = create_data_input()
    
    test_cases_n = int(data_input.readline())
    test_cases = []

    for _ in range(test_cases_n):
        test_cases.append(int(data_input.readline()))
    
    coins_n = int(data_input.readline())
    coins = []
    for _ in range(coins_n):
        coins.append(int(data_input.readline()))
    
    return test_cases, coins




def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data

if __name__ == "__main__":
    main()

