#! /usr/bin/python3
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def main():
    data = [int(v) for v in open(os.path.join(MYDIR, 'input.txt')).read().split()]

    for i in range(25, len(data)):
        sums = {data[j] + data[k] for j in range(i - 25, i) for k in range(j + 1, i)}
        if data[i] not in sums:
            target = data[i]
            break
    print("Part 1:", target)

    lo = hi = 0
    while True:
        n = sum(data[lo:hi])
        if n == target:
            break
        elif n > target:
            lo += 1
        else:
            hi += 1
    values = data[lo:hi]
    print("Part 2:", min(values) + max(values))


if __name__ == '__main__':
    main()
