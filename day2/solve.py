#! /usr/bin/python3
import os
import re

MYDIR = os.path.realpath(os.path.dirname(__file__))


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read()
    passwords = []
    pat = re.compile(r"(\d+)[-](\d+) (.): (.+)")
    for line in data.strip().split('\n'):
        i, j, char, pwd = pat.match(line).groups()
        passwords.append(( int(i), int(j), char, pwd ))

    p1_valid = [pwd for (i, j, char, pwd) in passwords
                if i <= pwd.count(char) <= j]
    print("Part 1: %d valid passwords" % (len(p1_valid),))

    p2_valid = [pwd for (i, j, char, pwd) in passwords
                if (pwd[i - 1] == char) != (pwd[j - 1] == char)]
    print("Part 2: %d valid passwords" % (len(p2_valid),))


if __name__ == '__main__':
    main()
