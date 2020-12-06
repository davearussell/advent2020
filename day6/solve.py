#! /usr/bin/python3
import functools
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def main():
    text = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    groups = [
        [set(x) for x in group.split('\n')]
        for group in text.split('\n\n')
    ]
    ors = [functools.reduce(set.__or__, group) for group in groups]
    ands = [functools.reduce(set.__and__, group) for group in groups]
    print("Part 1: %d" % sum(map(len, ors)))
    print("Part 2: %d" % sum(map(len, ands)))


if __name__ == '__main__':
    main()
