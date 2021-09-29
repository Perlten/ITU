
import fileinput
import sys
import itertools


def main():
    test_cases = get_formatted_data()
    for test_case in test_cases:
        coins = test_case["coins"]
        amount = test_case["amount"]
        
        coins.sort()

        amount_used, coins_used = solve(coins, amount)
        
        print(f"{amount_used} {coins_used}")


def solve(coins: list, amount: int):
    M = [0] * (amount + 1)

    for coin in coins:
        for current_amount in range(amount):
            if coin <= current_amount:
                leftover = current_amount - coin
                coins_used_for_leftover =  M[leftover]
                
                M[current_amount] = coins_used_for_leftover + 1
                break


    return - 1
        


def get_formatted_data():
    data_input = create_data_input()

    test_cases_n = int(data_input.readline())
    test_cases = []

    for _ in range(test_cases_n):
        amount = int(data_input.readline()) 

        coins_n = int(data_input.readline())
        coins = []
        for _ in range(coins_n):
            coins.append(int(data_input.readline()))
        test_cases.append({"amount": amount, "coins": coins})

    return test_cases


def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data


if __name__ == "__main__":
    main()
