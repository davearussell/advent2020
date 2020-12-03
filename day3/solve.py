#! /usr/bin/python3
import functools
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


class Grid:
    def __init__(self, text):
        self.lines = text.strip().split('\n')
        self.xsize = len(self.lines[0])
        self.ysize = len(self.lines)

    def lookup(self, x, y):
        return self.lines[y][x % self.xsize]

    def count_trees(self, xstride, ystride):
        x = y = n = 0
        while y < self.ysize - ystride:
            x += xstride
            y += ystride
            n += (self.lookup(x, y) == '#')
        return n


def main():
    grid = Grid(open(os.path.join(MYDIR, 'input.txt')).read())

    # Part 1
    print("Part 1: %d" % (grid.count_trees(3, 1),))

    # Part 2
    strides = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    counts = [grid.count_trees(*stride) for stride in strides]
    n = functools.reduce(lambda a, b: a * b, counts)
    print("Part 2: %d" % (n,))

if __name__ == '__main__':
    main()
