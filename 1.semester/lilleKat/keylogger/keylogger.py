import fileinput
import sys


sound_converter = {
"clank": "a",
"bong":  "b",
"click": "c",
"tap": "d",
"poing": "e",
"clonk": "f",
"clack": "g",
"ping": "h",
"tip": "i",
"cloing": "j",
"tic": "k",
"cling": "l",
"bing": "m",
"pong": "n",
"clang": "o",
"pang": "p",
"clong": "q",
"tac": "r",
"boing": "s",
"boink": "t",
"cloink": "u",
"rattle": "v",
"clock": "w",
"toc": "x",
"clink": "y",
"tuc": "z",

"whack": " ",
"bump": "capslock",
"pop": "delete",
"thumb": "shift_release",
"dink": "shift_hold",

}

def main():
    n, key_pres_list = get_formatted_data()

    uppercase = False
    shift_held = False
    res = []
    for i in range(n):
        sound = key_pres_list[i]
        key = sound_converter[sound]


        if (key == "delete"):
            if(len(res) > 0):
                res.pop()
            continue
        if(key == "capslock"):
            uppercase = not uppercase
            continue

        if(key == "shift_hold"):
            shift_held = True
            continue

        elif(key == "shift_release"):
            shift_held = False
            continue
        
        if(uppercase and not shift_held):
            key = key.capitalize()
        
        if(shift_held and not uppercase):
            key = key.capitalize()
            

        res.append(key) 
    print("".join(res))
    
def get_formatted_data():
    data_input = create_data_input()
    n = int(data_input.readline())
    key_pres_list = []
    for i in range(n):
        key = data_input.readline().replace("\n", "")
        key_pres_list.append(key)

    return n, key_pres_list


def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data

if __name__ == "__main__":
    main()


