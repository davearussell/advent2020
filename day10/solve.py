#! /usr/bin/python3
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read()
    adapters = sorted(map(int, data.split()))
    values = [0] + adapters + [adapters[-1] + 3]

    diff_counts = {}
    diffs = [hi - lo for (lo, hi) in zip(values, values[1:])]
    for diff in diffs:
        diff_counts[diff] = diff_counts.get(diff, 0) + 1
    print("Part 1:", diff_counts[1] * diff_counts[3])

    run_len_permutations = {
        2: 2,
        3: 4,
        4: 7,
        5: 13,
    }

    permutations = 1
    run_len = 0
    for diff in diffs:
        if diff == 1:
            run_len += 1
        else:
            if run_len > 1:
                permutations *= run_len_permutations[run_len]
            run_len = 0

    print("Part 2:", permutations)


if __name__ == '__main__':
    main()
