#! /usr/bin/python3
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


def parse_input(data):
    #    / \ / \
    #   |NW |NE |
    #  / \ / \ / \
    # | W |   | E |
    #  \ / \ / \ /
    #   |SW |SE |
    #    \ / \ /
    directions = {
        'ne': ( 1, -1),
        'e' : ( 2,  0),
        'se': ( 1,  1),
        'sw': (-1,  1),
        'w' : (-2,  0),
        'nw': (-1, -1),
    }
    tiles = []
    for line in data.split():
        tile = (0, 0)
        direction = ''
        for char in line:
            direction += char
            if direction in directions:
                x, y = directions[direction]
                tile = (tile[0] + x, tile[1] + y)
                direction = ''
        tiles.append(tile)
    return tiles


class Grid:
    def __init__(self):
        self.black_tiles = set()

    def flip(self, tile):
        self.black_tiles ^= {tile}

    def tick(self):
        xs = [tile[0] for tile in self.black_tiles]
        ys = [tile[1] for tile in self.black_tiles]
        x0, x1 = min(xs) - 2, max(xs) + 2
        y0, y1 = min(ys) - 1, max(ys) + 1
        new_blacks = set()
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if x & 1 != y & 1:
                    continue
                tile = (x, y)
                black = tile in self.black_tiles
                neighbours = {(x + 1, y - 1), (x + 2, y), (x + 1, y + 1),
                              (x - 1, y + 1), (x - 2, y), (x - 1, y - 1)}
                black_neighbours = len(neighbours & self.black_tiles)
                if ((black and 1 <= black_neighbours <= 2) or
                    (not black and black_neighbours == 2)):
                    new_blacks.add(tile)
        self.black_tiles = new_blacks


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    grid = Grid()
    for tile in parse_input(data):
        grid.flip(tile)

    print("Part 1:", len(grid.black_tiles))
    for i in range(100):
        grid.tick()
    print("Part 2:", len(grid.black_tiles))


if __name__ == '__main__':
    main()
