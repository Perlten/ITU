import fileinput
import sys
import re
import math
import time


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance(self, other: 'Point'):
        distance = abs(
            math.sqrt(((self.x - other.x)**2)+((self.y - other.y)**2)))
        return distance

    def __str__(self):
        return f"x: {self.x} y: {self.y}"

    def __eq__(self, other: "Point"):
        return id(self) == id(other)


def main():
    point_list = get_formatted_data()

    old_time = time.time()

    px = sorted(point_list, key=lambda p: p.x)

    sp = smallest_point(px)

    print(sp)
    print(time.time() - old_time)
    # print(brute_force(point_list))


def brute_force(p: list):
    min_distance = sys.maxsize
    for p1 in p:
        for p2 in p:
            distance = p1.distance(p2)
            if not p1 == p2 and min_distance > distance:
                min_distance = distance
    return min_distance


def examine_overlap(p: list, delta: int, split_x: int) -> int:
    py = sorted([x for x in p if x.x >= split_x -
                delta and x.x <= split_x + delta], key=lambda p: p.y)

    for i in range(len(py)):
        for j in range(min(8, len(py) - i)):
            if p[i] != p[j + i]:
                delta = min(delta, py[i].distance(py[j + i]))

    return delta


def smallest_point(p: list) -> int:
    if len(p) <= 25:
        return brute_force(p)

    split_point = len(p) // 2

    l_delta = smallest_point(p[:split_point])
    r_delta = smallest_point(p[split_point:])

    delta = min(l_delta, r_delta)

    return examine_overlap(p, delta, p[split_point].x)


def get_formatted_data() -> list:
    data_input = create_data_input()
    line = data_input.readline()
    while "NODE_COORD_SECTION" not in line:
        line = data_input.readline()

    points = []

    line = data_input.readline()
    while "EOF" not in line:
        line_split = re.sub("\s+", " ", line.strip()).split(" ")

        x = float(line_split[1])
        y = float(line_split[2])
        point = Point(x, y)
        points.append(point)
        line = data_input.readline()

    return points


def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data


if __name__ == "__main__":
    main()
