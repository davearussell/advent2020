#! /usr/bin/python3
import functools
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


SEA_MONSTER = [
    "..................#.",
    "#....##....##....###",
    ".#..#..#..#..#..#...",
]


class Grid:
    def __init__(self, data):
        self.cells = data.split('\n')

    def rotate_right(self):
        self.cells = [
            ''.join(reversed([row[i] for row in self.cells]))
            for i in range(len(self.cells))
        ]

    def flip_vertical(self):
        self.cells = self.cells[::-1]

    def flip_horizontal(self):
        self.cells = [row[::-1] for row in self.cells]

    def __str__(self):
        return '\n'.join(self.cells)

    def array(self):
        return [list(row) for row in self.cells]


class Tile(Grid):
    def __init__(self, text):
        header, data = text.split('\n', 1)
        super().__init__(data)
        self.i = int(header.split()[-1].rstrip(':'))
        self.neighbours = {} # populated later

    @property
    def top(self):
        return self.cells[0]

    @property
    def bottom(self):
        return self.cells[-1]

    @property
    def left(self):
        return ''.join([row[0] for row in self.cells])

    @property
    def right(self):
        return ''.join([row[-1] for row in self.cells])

    def neighbour(self, side):
        edge = getattr(self, side)
        for _edge in (edge, edge[::-1]):
            if _edge in self.neighbours:
                return self.neighbours[_edge]
        raise Exception("No neighbour on that side")

    def find_edge(self, edge):
        candidates = (edge, edge[::-1])
        for side in ('top', 'bottom', 'left', 'right'):
            if getattr(self, side) in candidates:
                return side
        raise Exception("Tile does not have that edge")

    def orient(self, edge, side):
        while self.find_edge(edge) != side:
            self.rotate_right()
        if getattr(self, side) != edge:
            if side in ['top', 'bottom']:
                self.flip_horizontal()
            else:
                self.flip_vertical()
        assert getattr(self, side) == edge


def arrange_tiles(tiles):
    # 1. For each possible edge, find the 1 or 2 tiles that have that edge
    edges = {}
    for tile in tiles:
        for edge in [tile.top, tile.bottom, tile.left, tile.right]:
            assert edge != edge[::-1] # fortunately the puzzle input guarantees this
            edge = min(edge, edge[::-1]) # normalize to account for flips
            edges.setdefault(edge, []).append(tile)

    # 2. Find the neighbours of each tile
    for edge, matches in edges.items():
        assert len(matches) <= 2
        if len(matches) == 2:
            matches[0].neighbours[edge] = matches[1]
            matches[1].neighbours[edge] = matches[0]

    # 3. The four corner tiles are the ones with two neighbours
    corner_tiles = [tile for tile in tiles if len(tile.neighbours) == 2]
    assert len(corner_tiles) == 4

    # We don't know the orientation of the image yet, so we'll
    # assume the first corner we find is the top left
    grid_size = int(len(tiles) ** .5)
    assert grid_size ** 2 == len(tiles)
    grid = [[None for y in range(grid_size)] for x in range(grid_size)]
    grid[0][0] = topleft = corner_tiles[0]

    # 4. Rotate the tile so it has neighbours at the bottom and right
    corners = [topleft.find_edge(edge) for edge in topleft.neighbours]
    rotations = {
        ('left', 'top'): 2,
        ('right', 'top'): 1,
        ('bottom', 'right'): 0,
        ('bottom', 'left'): 3,
    }[tuple(sorted(corners))]
    for i in range(rotations):
        topleft.rotate_right()

    # 5. Fill in the grid
    for y in range(grid_size):
        if y > 0:
            neighbour_above = grid[y - 1][0]
            grid[y][0] = neighbour_above.neighbour('bottom')
            grid[y][0].orient(neighbour_above.bottom, 'top')
        for x in range(1, grid_size):
            neighbour_left = grid[y][x - 1]
            grid[y][x] = neighbour_left.neighbour('right')
            grid[y][x].orient(neighbour_left.right, 'left')

    return grid


def extract_image(grid):
    grid_size = len(grid)
    tile_size = len(grid[0][0].cells)
    image = ''
    for gy in range(grid_size):
        for ty in range(1, tile_size - 1):
            for tile in grid[gy]:
                image += tile.cells[ty][1:-1]
            image += '\n'
    return Grid(image.strip())


def mark_monsters(image):
    sm_height = len(SEA_MONSTER)
    sm_width = len(SEA_MONSTER[0])
    sm = [
        int(row.replace('#', '1').replace('.', '0'), base=2)
        for row in SEA_MONSTER
    ]

    image_size = len(image)
    bits = [int(''.join(row).replace('#', '1').replace('.', '0'), base=2) for row in image]

    for y in range(image_size - sm_height + 1):
        for x in range(image_size - sm_width + 1):
            shift = image_size - sm_width - x
            if ((bits[y + 1] >> shift) & sm[1] == sm[1] and
                (bits[y    ] >> shift) & sm[0] == sm[0] and
                (bits[y + 2] >> shift) & sm[2] == sm[2]):
                for yi in range(sm_height):
                    for xi in range(sm_width):
                        if (sm[yi] >> (sm_width - xi - 1)) & 1:
                            image[y + yi][x + xi] = 'O'

    return '\n'.join(''.join(row) for row in image)


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    tiles = [Tile(text) for text in data.split('\n\n')]
    grid = arrange_tiles(tiles)
    corner_tiles = [grid[0][0], grid[-1][0], grid[0][-1], grid[-1][-1]]
    print("Part 1:", functools.reduce(int.__mul__, [tile.i for tile in corner_tiles]))

    image = extract_image(grid)
    for flip in [0, 1]:
        if flip:
            image.flip_vertical()
        for rotate in [0, 1, 2, 3]:
            if rotate:
                image.rotate_right()
            marked = mark_monsters(image.array())
            if 'O' in marked:
                print("Part 2:", marked.count('#'))


if __name__ == '__main__':
    main()
