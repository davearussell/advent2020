#! /usr/bin/python3
import functools
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def parse_input(text):
    rules = {}
    tickets = []

    for line in text.split('\n'):
        if ': ' in line:
            k, v = line.split(':')
            rules[k] = []
            for r in v.split(' or '):
                lo, hi = r.split('-')
                rules[k].append((int(lo), int(hi)))
        elif ',' in line:
            tickets.append([int(v) for v in line.split(',')])
    return rules, tickets


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    rules, tickets = parse_input(data)
    n_fields = len(tickets[0])

    valid_values = set()
    for ranges in rules.values():
        for lo, hi in ranges:
            valid_values |= set(range(lo, hi + 1))
    invalid_values = []
    valid_tickets = [tickets[0]]

    for ticket in tickets[1:]:
        bad = (set(ticket) - valid_values)
        if not bad:
            valid_tickets.append(ticket)
        invalid_values += bad

    print("Part 1:", sum(invalid_values))

    def valid_for(v, ranges):
        return any(lo <= v <= hi for (lo, hi) in ranges)

    possible_indices = {name: set() for name in rules}
    for name, ranges in rules.items():
        for i in range(len(valid_tickets[0])):
            values = {ticket[i] for ticket in valid_tickets}
            if all([valid_for(v, ranges) for v in values]):
                possible_indices[name].add(i)

    name_map = {}
    while possible_indices:
        for name, indices in possible_indices.items():
            if len(indices) == 1:
                i = indices.pop()
                name_map[name] = i
                del possible_indices[name]
                for other_indices in possible_indices.values():
                    other_indices -= {i}
                break
        else:
            assert 0, "no trivial solution"

    values = [tickets[0][i] for (name, i) in name_map.items() if 'departure' in name]
    print("Part 2:", functools.reduce(int.__mul__, values))


if __name__ == '__main__':
    main()
