#! /usr/bin/python3
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def part1(steps):
    x = y = 0
    bearing = 90
    vectors = {0: (0, 1), 90: (1, 0), 180: (0, -1), 270: (-1, 0)}
    for op, val in steps:
        if op == 'L':
            bearing = (bearing - val) % 360
        elif op == 'R':
            bearing = (bearing + val) % 360
        elif op == 'F':
            xd, yd = vectors[bearing]
            x += xd * val
            y += yd * val
        elif op == 'N':
            y += val
        elif op == 'E':
            x += val
        elif op == 'S':
            y -= val
        elif op == 'W':
            x -= val
        else:
            assert 0, (op, val)
    return abs(x) + abs(y)


def part2(steps):
    wx, wy = (10, 1)
    x, y = (0, 0)

    for op, val in steps:
        if op == 'N':
            wy += val
        elif op == 'E':
            wx += val
        elif op == 'S':
            wy -= val
        elif op == 'W':
            wx -= val
        elif op == 'F':
            x += wx * val
            y += wy * val
        elif op in ('L', 'R'):
            if (op, val) in [('L', 90), ('R', 270)]:
                wx, wy = -wy, wx
            elif (op, val) in [('R', 90), ('L', 270)]:
                wx, wy = wy, -wx
            elif val == 180:
                wx, wy = -wx, -wy
            else:
                assert 0, (op, val)
        else:
            assert 0, (op, val)
    return abs(x) + abs(y)


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    steps = [(s[0], int(s[1:])) for s in data.split()]

    print("Part 1:", part1(steps))
    print("Part 2:", part2(steps))


if __name__ == '__main__':
    main()
