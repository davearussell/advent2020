#! /usr/bin/python3
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def execute(insns):
    acc = ptr = 0
    seen = set()
    while ptr not in seen and ptr < len(insns):
        seen.add(ptr)
        op, arg = insns[ptr]
        if op == 'acc':
            acc += int(arg)
        elif op == 'jmp':
            ptr += (int(arg) - 1)
        ptr += 1
    return (ptr >= len(insns), acc)


def main():
    text = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    insns = [line.split() for line in text.split('\n')]

    print("Part 1:", execute(insns)[1])

    for i in range(len(insns)):
        op, arg = insns[i]
        if op != 'acc':
            fixed_insns = insns.copy()
            fixed_insns[i] = ('jmp' if op == 'nop' else 'nop', arg)
            term, acc = execute(fixed_insns)
            if term:
                print("Part 2:", acc)


if __name__ == '__main__':
    main()
