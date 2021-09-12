import fileinput
import sys

def main():
    data = get_formatted_data()

    results = []
    for vector_pair in data:
        vector1: list = vector_pair["vector1"]
        vector2: list = vector_pair["vector2"]
        n: int = vector_pair["n"]
        
        vector1.sort()
        vector2.sort()

        result = 0
        for i in range(n):
            result += vector1[i] * vector2[-i - 1]

        results.append(result)

    for index, res in enumerate(results):
        print(f"Case #{index + 1}: {res}")


def get_formatted_data():
    data_input = create_data_input()

    t = int(data_input.readline())

    data = []

    for i in range(t):
        data.append(get_scalar_vectors(data_input))

    return data


def get_scalar_vectors(data_input: fileinput.FileInput): 
    vector1 = []
    vector2 = []

    n = int(data_input.readline())

    vector1 = [int(x) for x in data_input.readline().replace("\n", "").split(" ")]
    vector2 = [int(x) for x in data_input.readline().replace("\n", "").split(" ")]

    return {"vector1" : vector1, "vector2": vector2, "n": n}




def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data

if __name__ == "__main__":
    main()