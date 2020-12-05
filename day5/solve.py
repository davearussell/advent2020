#! /usr/bin/python3
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def main():
    text = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    numbers = text.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
    seats = {int(n, base=2) for n in numbers.split()}
    min_taken, max_taken = min(seats), max(seats)
    all_seats = set(range(min_taken, max_taken + 1))
    empty = all_seats - seats
    assert len(empty) == 1, empty
    my_seat = empty.pop()

    print("Part 1: %d" % (max_taken,))
    print("Part 2: %d" % (my_seat,))


if __name__ == '__main__':
    main()
