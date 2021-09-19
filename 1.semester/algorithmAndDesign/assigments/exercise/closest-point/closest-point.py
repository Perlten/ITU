import fileinput
import sys
import re
import math

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

    px = sorted(point_list, key=lambda p: p.x)
    py = sorted(point_list, key=lambda p: p.y)
    
    sp = smallest_point(px, py)

    print(sp)
    # print(brute_force(point_list))


def brute_force(p: list):
    min_distance = sys.maxsize
    for p1 in p:
        for p2 in p:
            distance = p1.distance(p2)
            if not p1 == p2 and min_distance > distance:
                min_distance = distance
    return min_distance


def examine_overlap(py: list, delta: int, split_x: int) -> int:
    py = [point for point in py if point.x >= split_x -
          delta and point.x <= split_x + delta]

    for i in range(len(py)):
        for j in range(min(7, len(py) - i)):
            if py[i] != py[j + i]:
                delta = min(delta, py[i].distance(py[j + i]))

    return delta


def smallest_point(px: list, py: list) -> int:
    if len(px) <= 3:
        return brute_force(px)

    split_point = len(px) // 2

    x_l_p = px[:split_point]
    x_r_p = px[split_point:]

    y_l_p = py[:split_point]
    y_r_p = py[split_point:]

    l_delta = smallest_point(x_l_p, y_l_p)
    r_delta = smallest_point(x_r_p, y_r_p)

    delta = l_delta if l_delta <= r_delta else r_delta

    return examine_overlap(py, delta, px[split_point].x)


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
