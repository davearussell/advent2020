#! /usr/bin/python3
import os
import re

MYDIR = os.path.realpath(os.path.dirname(__file__))


def parse_rules(text):
    outer_pat = re.compile(r'(.+?) bags contain (.+)[.]')
    inner_pat = re.compile(r'(\d+) (.+) bags?')
    rules = {}
    for line in text.split('\n'):
        container_type, contents = outer_pat.match(line).groups()
        rules[container_type] = {}
        if contents == 'no other bags':
            continue
        for content in contents.split(','):
            n, content_type = inner_pat.match(content.strip()).groups()
            rules[container_type][content_type] = int(n)
    return rules


def populate_flat(rules, flat, container):
    contents = flat[container] = {}
    for containee, n in rules[container].items():
        contents[containee] = contents.get(containee, 0) + n
        if containee not in flat:
            populate_flat(rules, flat, containee)
        for indirect_containee, indirect_n in flat[containee].items():
            contents[indirect_containee] = contents.get(indirect_containee, 0) + n * indirect_n


def main():
    text = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    rules = parse_rules(text)

    flat = {}
    for k in rules:
        if k not in flat:
            populate_flat(rules, flat, k)

    print("Part 1:", len([x for x in flat.values() if 'shiny gold' in x]))
    print("Part 2:", sum(flat['shiny gold'].values()))


if __name__ == '__main__':
    main()
