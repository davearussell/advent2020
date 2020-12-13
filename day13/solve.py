#! /usr/bin/python3
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def bezout(a, b):
    r = [a, b]
    s = [1, 0]
    t = [0, 1]
    q = [None, None]
    i = 2
    while r[-1]:
        q.append(r[i-2] // r[i-1])
        r.append(r[i-2] - q[i] * r[i-1])
        s.append(s[i-2] - q[i] * s[i-1])
        t.append(t[i-2] - q[i] * t[i-1])
        i += 1
    return s[-2], t[-2]


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    line1, line2 = data.split()
    now = int(line1)
    intervals = line2.split(',')

    part1_intervals = [int(x) for x in intervals if x.isdigit()]
    def next_bus(now, interval):
        n, m = divmod(now, interval)
        ts = n * interval
        return ts if m == 0 else ts + interval
    times = {next_bus(now, interval): interval for interval in part1_intervals}
    first_time = min(times)
    print("Part 1:", (first_time - now) * times[first_time])

    part2_delays = {int(x): i for i, x in enumerate(intervals) if x.isdigit()}
    remainders = []
    for bus, delay in sorted(part2_delays.items()):
        a = -delay % bus
        remainders.append((bus, a))

    while len(remainders) > 1:
        (n1, a1), (n2, a2) = remainders[:2]
        b1, b2 = bezout(n1, n2)
        n3 = n1 * n2
        a3 = (n1 * b1 * a2 + n2 * b2 * a1) % n3
        remainders = [(n3, a3)] + remainders[2:]
    print("Part 2:", remainders[0][1])


if __name__ == '__main__':
    main()
