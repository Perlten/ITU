import sys
import fileinput


def main():
    input = create_input()

    line: str = input.readline()
    while line.startswith("#"):
        line = input.readline()

    n = int(line[2:])

    proposer = {}
    rejecter = {}

    create_map(proposer, rejecter, n, input)

    res = run_gs_algo(proposer, rejecter, n)

    res = correct_order(res, proposer)

    print("\n".join(res))


def run_gs_algo(proposers: dict, rejecters: dict, n: int) -> list:
    available_proposers: list = [proposer for proposer in proposers]
    matches: dict[str, list[str]] = {}

    while(len(available_proposers) != 0):
        current_proposer = available_proposers[0]
        potential_rejecter = proposers[current_proposer]["priorityList"][0]
        if potential_rejecter not in matches:
            matches[potential_rejecter] = [current_proposer, potential_rejecter]
            proposers[current_proposer]["priorityList"].pop(0)
            available_proposers.pop(0)
        else:
            old_proposer = matches[potential_rejecter][0]

            current_proposer_score = rejecters[potential_rejecter]["priorityList"].index(current_proposer)
            old_proposer_score = rejecters[potential_rejecter]["priorityList"].index(old_proposer)

            if(current_proposer_score < old_proposer_score):
                proposers[current_proposer]["priorityList"].pop(0)
                matches[potential_rejecter] = [current_proposer, potential_rejecter]

                available_proposers.pop(0)
                available_proposers.append(old_proposer)
            else:
                proposers[current_proposer]["priorityList"].pop(0)

    return [proposers[match[0]]["name"] + " -- " + rejecters[match[1]]["name"] for match in matches.values()]


def create_map(proposer: map, rejecter: map, n: int, input: fileinput.FileInput) -> None:
    def create_entity(map: map):
        data = input.readline().split(" ")
        index = int(data[0])
        name = data[1].replace("\n", "")

        map[index] = {"name": name, "index": index}

    def add_priorities() -> None:
        input.readline()
        for i in range(n * 2):
            line: str = input.readline()
            index: int = int(line.split(":")[0])

            entity = None
            if index in proposer:
                entity = proposer[index]
            else:
                entity = rejecter[index]

            priorityList = [int(x) for x in line.split(":")[1].removesuffix("\n").strip().split(" ")]
            entity["priorityList"] = priorityList

    for i in range(n):
        create_entity(proposer)
        create_entity(rejecter)

    add_priorities()


def create_input() -> fileinput.FileInput:
    input = None
    if len(sys.argv) > 1:
        input = fileinput.input(sys.argv[1])
    else:
        input = fileinput.input()

    return input


def correct_order(res: dict[str], proposer: dict):
    ordered_res: list = []
    for p in proposer.values():
        for r in res:
            if r.split(" ")[0] == p["name"]:
                ordered_res.append(r)

    return ordered_res


if __name__ == "__main__":
    main()
