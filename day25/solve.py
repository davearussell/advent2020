#! /usr/bin/python3
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))

MAGIC_NUMBER = 20201227


def loop_size(subject_number, public_key):
    n = 0
    k = 1
    while k != public_key:
        k = (k * subject_number) % MAGIC_NUMBER
        n += 1
    return n


def transform(subject_number, loop_size):
    n = 1
    for i in range(loop_size):
        n = (n * subject_number) % MAGIC_NUMBER
    return n


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    public_keys = [int(s) for s in data.split()]
    loop_sizes = [loop_size(7, public_key) for public_key in public_keys]
    k1 = transform(public_keys[0], loop_sizes[1])
    k2 = transform(public_keys[1], loop_sizes[0])
    assert k1 == k2
    print(k1)


    


if __name__ == '__main__':
    main()
