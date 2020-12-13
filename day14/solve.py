#! /usr/bin/python3
import os
import re

MYDIR = os.path.realpath(os.path.dirname(__file__))


def parse_input(data):
    code = []
    pat = re.compile(r'([a-z]+)(?:\[(\d+)\])? = ([0-9X]+)')
    for line in data.split('\n'):
        groups = pat.match(line).groups()
        if groups[0] == 'mask':
            code.append(('mask', groups[2]))
        else:
            code.append(('mem', (int(groups[1]), int(groups[2]))))
    return code


def part1(code):
    zeros = ones = 0
    mem = {}
    for op, arg in code:
        if op == 'mask':
            zeros = int(arg.replace('X', '1'), base=2)
            ones = int(arg.replace('X', '0'), base=2)
        else:
            addr, val = arg
            mem[addr] = (val | ones) & zeros
    return sum(mem.values())


def generate_masks(mask):
    masks = [((1 << 36) - 1, int(mask.replace('X', '0'), base=2))]
    for i, bit in enumerate(mask):
        pos = 35 - i
        if bit == 'X':
            new_masks = []
            for zeros, ones in masks:
                new_masks += [(zeros,               ones | (1 << pos)),
                              (zeros & ~(1 << pos), ones             )]
            masks = new_masks
    return masks


def part2(code):
    mem = {}
    masks = []
    for op, arg in code:
        if op == 'mask':
            masks = generate_masks(arg)
        else:
            addr, value = arg
            for zeros, ones in masks:
                mem[(addr | ones) & zeros] = value
    return sum(mem.values())


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    code = parse_input(data)
    print("Part 1:", part1(code))
    print("Part 2:", part2(code))


if __name__ == '__main__':
    main()
