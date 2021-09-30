import fileinput
import sys


def main():
    d, coins = get_formatted_data()

    upper_bound = coins[-1] + coins[-2]
    lower_bound = coins[-3]

    dynamic_res = dynamic_approach(coins, upper_bound)

    for i in reversed(range(lower_bound, upper_bound)):
        if(greedy_approach(coins, i) != dynamic_res[i]):
            print("non-canonical") 
            exit()
    
    print("canonical")
  


def get_formatted_data():
    data_input = create_data_input()

    d = int(data_input.readline())
    coins = [int(coin) for coin in data_input.readline().strip().split(" ")]

    return d, coins


def greedy_approach(coins: list, amount: int) -> int:
    counter = 0
    while(amount > 0):
        for coin in reversed(coins):
            if coin <= amount:

                divided = amount / coin
                
                amount = amount -  (coin * divided);
                counter = counter + divided;

                break
    return counter


def dynamic_approach(coins: list,  amount: int) -> list:
    M = [0] * (amount + 1)

    for coin in coins:
        for current_amount in range(amount + 1):
            if coin <= current_amount:
                leftover = current_amount - coin
                coins_used_for_leftover = M[leftover]
                if M[current_amount] == 0:
                    M[current_amount] = coins_used_for_leftover + 1
                else:
                    M[current_amount] = min(coins_used_for_leftover + 1, M[current_amount])
                

    return M


def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data


if __name__ == "__main__":
    main()
