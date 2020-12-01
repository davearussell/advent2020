#! /usr/bin/python3
import functools
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def main():
    vals = set(map(int, open(os.path.join(MYDIR, 'input.txt')).read().split()))
    sums = {a + b for a in vals for b in vals if a != b}
    def mul(a, b): return a * b
    product_part1 = functools.reduce(mul, [n for n in vals if 2020 - n in vals])
    product_part2 = functools.reduce(mul, [n for n in vals if 2020 - n in sums])
    print("Part 1: %d" % (product_part1,))
    print("Part 2: %d" % (product_part2,))


if __name__ == '__main__':
    main()
