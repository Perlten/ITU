import fileinput
import sys



def main():
    data = get_formatted_data()
    amount_saved = shopaholic_algoritme(data["n"], data["price_array"])
    print(amount_saved)

def shopaholic_algoritme(n, price_array):
    amount_saved = 0
    
    price_array.sort(reverse=True)
    for i in range(2, n, 3):
        amount_saved += price_array[i]
    return amount_saved
    
def get_formatted_data():
    data = create_data_input()
    n = int(data.readline())
    price_array = [int(x) for x in data.readline().replace("\n", "").split(" ")]
    return {"n": n, "price_array": price_array}


def create_data_input():
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data


if __name__ == "__main__":
    main()
