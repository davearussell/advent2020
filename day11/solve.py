#! /usr/bin/python3
import copy
import os
import sys

MYDIR = os.path.realpath(os.path.dirname(__file__))


class Grid:
    max_neighbours = 3

    def __init__(self, data):
        self.cells = [list(row) for row in data.split('\n')]
        self.xsize = len(self.cells[0])
        self.ysize = len(self.cells)
        self.compute_neighbouring_cells()

    def compute_neighbouring_cells(self):
        self.neighbours = {} # (x, y) -> [(nx, ny), ...]
        for x in range(self.xsize):
            for y in range(self.ysize):
                l = self.neighbours[(x, y)] = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 1] if dx == 0 else [-1, 0, 1]:
                        nx, ny = (x + dx, y + dy)
                        if 0 <= nx < self.xsize and 0 <= ny < self.ysize:
                            l.append((nx, ny))

    def iterate(self):
        changes = 0
        new_cells = copy.deepcopy(self.cells)
        for x in range(self.xsize):
            for y in range(self.ysize):
                cell = self.cells[y][x]
                neighbours = [self.cells[y][x] for (x, y) in self.neighbours[(x, y)]].count('#')
                if cell == 'L' and neighbours == 0:
                    new_cells[y][x] = '#'
                    changes += 1
                elif cell == '#' and neighbours > self.max_neighbours:
                    new_cells[y][x] = 'L'
                    changes += 1
        if changes:
            self.cells = new_cells
        return changes

    def stabilize(self):
        while self.iterate():
            pass
        return sum(row.count('#') for row in self.cells)


class VisibleGrid(Grid):
    max_neighbours = 4

    def compute_neighbouring_cells(self):
        self.neighbours = {} # (x, y) -> [(nx, ny), ...]
        for x in range(self.xsize):
            for y in range(self.ysize):
                l = self.neighbours[(x, y)] = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 1] if dx == 0 else [-1, 0, 1]:
                        distance = 0
                        while True:
                            distance += 1
                            nx, ny = (x + distance * dx, y + distance * dy)
                            if not (0 <= nx < self.xsize and 0 <= ny < self.ysize):
                                break
                            if self.cells[ny][nx] != '.':
                                l.append((nx, ny))
                                break


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    print("Part 1:", Grid(data).stabilize())
    print("Part 2:", VisibleGrid(data).stabilize())


if __name__ == '__main__':
    main()
