#! /usr/bin/python3
import functools
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def parse_input(text):
    passports = []
    text = text.replace('\n\n','\0').replace('\n', ' ')
    for line in text.split('\0'):
        passport = {}
        for entry in line.split():
            k, v = entry.split(':', 1)
            passport[k] = v
        passports.append(passport)
    return passports


def _intrange(s, lo, hi):
    return s.isdigit() and lo <= int(s) <= hi


def byr_valid(s):
    return _intrange(s, 1920, 2002)


def iyr_valid(s):
    return _intrange(s, 2010, 2020)


def eyr_valid(s):
    return _intrange(s, 2020, 2030)


def hgt_valid(s):
    v, unit = s[:-2], s[-2:]
    if unit == 'cm':
        return _intrange(v, 150, 193)
    elif unit == 'in':
        return _intrange(v, 59, 76)
    return False


def hcl_valid(s):
    return s[0] == '#' and all(c in '0123456789abcdef' for c in s[1:])


def ecl_valid(s):
    return s in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def pid_valid(s):
    return len(s) == 9 and s.isdigit()


def main():
    passports = parse_input(open(os.path.join(MYDIR, 'input.txt')).read())

    validators = {
        'byr': byr_valid,
        'iyr': iyr_valid,
        'eyr': eyr_valid,
        'hgt': hgt_valid,
        'hcl': hcl_valid,
        'ecl': ecl_valid,
        'pid': pid_valid,
    }

    # Part 1
    p1_valid = [
        passport for passport in passports
        if all(key in passport
               for key in validators)
    ]
    print("Part 1: %d valid passwords" % (len(p1_valid),))

    # Part 2
    p2_valid = [
        passport for passport in p1_valid
        if all(validator(passport[key])
               for (key, validator) in validators.items())
    ]
    print("Part 2: %d valid passwords" % (len(p2_valid),))
    


if __name__ == '__main__':
    main()
