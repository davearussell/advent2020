#! /usr/bin/python3
import os
import re

MYDIR = os.path.realpath(os.path.dirname(__file__))


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    groups = []
    pat = re.compile(r'(.+) \(contains (.+)\)')
    for line in data.split('\n'):
        foods, allergens = pat.match(line).groups()
        groups.append( (set(foods.split(' ')), set(allergens.split(', '))) )

    all_foods = {food for (foods, allergens) in groups for food in foods}
    all_allergens = {allergen for (foods, allergens) in groups for allergen in allergens}

    candidates = {allergen: all_foods.copy() for allergen in all_allergens}
    for foods, allergens in groups:
        for allergen in allergens:
            candidates[allergen] &= foods

    allergen_map = {} # allergen -> food
    while candidates:
        for allergen, foods in candidates.items():
            if len(foods) == 1:
                del candidates[allergen]
                food = foods.pop()
                allergen_map[allergen] = food
                for other_allergen, other_foods in candidates.items():
                    other_foods -= {food}
                break

    safe_foods = all_foods - set(allergen_map.values())
    safe_count = sum(len(foods & safe_foods) for foods, _ in groups)
    print("Part 1:", safe_count)

    ordered_bad_foods = [food for (allergen, food) in sorted(allergen_map.items())]
    print("Part 2:", ','.join(ordered_bad_foods))


if __name__ == '__main__':
    main()
