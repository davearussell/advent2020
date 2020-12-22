#! /usr/bin/python3
import copy
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def score(winner, decks):
    return sum((i + 1) * card for (i, card) in enumerate(reversed(decks[winner])))


def part1(decks):
    while all(decks):
        cards = [deck.pop(0) for deck in decks]
        winner = 0 if cards[0] > cards[1] else 1
        decks[winner] += [cards[winner], cards[1 - winner]]
    return winner, decks


def part2(decks, indent=""):
    seen = set()

    while all(decks):
        k = tuple(map(tuple, decks))
        if k in seen:
            return 0, decks
        seen.add(k)

        cards = [deck.pop(0) for deck in decks]
        if all(len(decks[i]) >= cards[i] for i in range(len(decks))):
            subdecks = [deck[:card] for card, deck in zip(cards, decks)]
            winner, _ = part2(subdecks, indent + "  ")
        else:
            winner = 0 if cards[0] > cards[1] else 1
        decks[winner] += [cards[winner], cards[1 - winner]]
    return winner, decks


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    decks = [[int(x) for x in player.split('\n') if 'Player' not in x]
             for player in data.split('\n\n')]

    print("Part 1:", score(*part1(copy.deepcopy(decks))))
    print("Part 2:", score(*part2(copy.deepcopy(decks))))

if __name__ == '__main__':
    main()
