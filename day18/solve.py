#! /usr/bin/python3
import os
import lark

MYDIR = os.path.realpath(os.path.dirname(__file__))

PART1_GRAMMAR = """
?start: expr
?expr: atom
     | expr "+" atom -> add
     | expr "*" atom -> mul
?atom: NUMBER -> number
     | "(" expr ")"
%import common.NUMBER
%import common.WS
%ignore WS
"""

PART2_GRAMMAR = """
?start: expr
?expr: sum
     | expr "*" sum -> mul
?sum: atom
    | sum "+" atom -> add
?atom: NUMBER -> number
     | "(" expr ")"
%import common.NUMBER
%import common.WS
%ignore WS
"""


@lark.v_args(inline=True)
class Tree(lark.Transformer):
    from operator import add, mul
    number = int


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    lines = data.split('\n')
    part1_parser = lark.Lark(PART1_GRAMMAR, parser='lalr', transformer=Tree())
    part2_parser = lark.Lark(PART2_GRAMMAR, parser='lalr', transformer=Tree())
    print("Part 1:", sum(map(part1_parser.parse, lines)))
    print("Part 2:", sum(map(part2_parser.parse, lines)))


if __name__ == '__main__':
    main()
