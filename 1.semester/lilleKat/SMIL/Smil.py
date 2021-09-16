

smile_types = [":)", ";)", ":-)", ";-)"]



import fileinput
import sys

def main():
    smil_line: str = get_formatted_data()

    results = []

    index = -1

    t = False

    for i in range(len(smil_line)):
        char = smil_line[i]
        if(char == ":" or char == ";"):
            index = i
            t = True
        elif t and char == ")":
            results.append(index)
            index = -1
            t = False
        elif t and char == "-":
            pass
        else:
            t = False
            index = -1

    for x in results:
        print(x) 
            
        
        





def get_formatted_data():
    data_input = create_data_input()
    return data_input.readline()



def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data

if __name__ == "__main__":
    main()

