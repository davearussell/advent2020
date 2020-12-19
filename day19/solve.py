#! /usr/bin/python3
import os
import re
import lark

MYDIR = os.path.realpath(os.path.dirname(__file__))


def parse_input(data):
    grammar = ['A: "a"', 'B: "b"']
    messages = []
    for line in data.split('\n'):
        if ':' not in line:
            messages.append(line)
        else:
            i, rule = line.split(': ')
            if rule in ['"a"', '"b"']:
                gbody = rule[1].upper()
            else:
                gbody = re.sub(r'(\d+)', r'r\1', rule)
            grammar.append("r%s: %s" % (i, gbody))
    return '\n'.join(grammar), messages


def count_matches(parser, messages):
    matches = 0
    for message in messages:
        try:
            parser.parse(message)
            matches += 1
        except lark.exceptions.LarkError:
            pass
    return matches


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()

    part1_grammar, messages = parse_input(data)
    part1_parser = lark.Lark(part1_grammar, start='r0')
    print("Part 1:", count_matches(part1_parser, messages))

    part2_grammar = (part1_grammar
                     .replace('r8: r42', 'r8: r42 | r42 r8')
                     .replace('r11: r42 r31', 'r11: r42 r31 | r42 r11 r31'))
    part2_parser = lark.Lark(part2_grammar, start='r0')
    print("Part 2:", count_matches(part2_parser, messages))



if __name__ == '__main__':
    main()
