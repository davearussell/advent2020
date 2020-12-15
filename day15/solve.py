#! /usr/bin/python3
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def main():
    data = [2, 20, 0, 4, 1, 17]
    target = 30000000

    numbers = list(data)
    times = {n: [i] for i, n in enumerate(data)}
    ts = len(data)
    while ts < target:
        prev = times[numbers[-1]][-2:]
        n = 0 if len(prev) == 1 else prev[1] - prev[0]
        times.setdefault(n, []).append(ts)
        numbers.append(n)
        ts += 1

    print("Part 1:", numbers[2019])
    print("Part 2:", numbers[target - 1])


if __name__ == '__main__':
    main()
