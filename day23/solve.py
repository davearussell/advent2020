#! /usr/bin/python3
import os
import numpy
import numba

MYDIR = os.path.realpath(os.path.dirname(__file__))


def flatten_circle(circle, label):
    flat = []
    for i in range(len(circle) - 1):
        flat.append(label)
        label = circle[label]
    return flat


def make_circle(base_cups, n_cups):
    circle = numpy.zeros(n_cups + 1, numpy.uint32)
    for a, b in zip(base_cups, base_cups[1:]):
        circle[a] = b
    count_from = len(base_cups) + 1
    if count_from <= n_cups:
        circle[base_cups[-1]] = count_from
        for i in range(count_from, n_cups):
            circle[i] = i + 1
        circle[n_cups] = base_cups[0]
    else:
        circle[base_cups[-1]] = base_cups[0]
    return circle


@numba.njit("uint32[:](uint32[:], uint32, uint32)", cache=True)
def iterate(circle, current, iters):
    n_cups = len(circle) - 1

    for i in range(iters):
        move1 = circle[current]
        move2 = circle[move1]
        move3 = circle[move2]
        next_current = circle[move3]

        target = current - 1
        while True:
            if target < 1:
                target = n_cups
            elif target == move1 or target == move2 or target == move3:
                target -= 1
            else:
                break

        circle[current] = next_current
        circle[move3] = circle[target]
        circle[target] = move1
        current = next_current
    return circle


def play(base_cups, n_cups, iters):
    circle = make_circle(base_cups, n_cups)
    final_circle = iterate(circle, base_cups[0], iters)
    return flatten_circle(final_circle, 1)


def main():
    data = "562893147"
    cups = [int(s) for s in data]

    part1 = play(cups, len(data), 100)
    print("Part 1:", ''.join(map(str, part1[1:])))

    a, b = play(cups, 1000000, 10000000)[1:3]
    print("Part 2:", int(a) * int(b))


if __name__ == '__main__':
    main()
