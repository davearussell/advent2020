#! /usr/bin/python3
import os

MYDIR = os.path.realpath(os.path.dirname(__file__))


class Grid:
    def __init__(self, data, dims):
        self.dims = dims
        self.active = set()
        for y, row in enumerate(data.split('\n')):
            for x, cell in enumerate(row):
                if cell == '#':
                    self.active.add( (x, y) + (0,) * (dims - 2) )

    def adjacent(self, cell1, cell2):
        cells = {()}
        for lo, hi in zip(cell1, cell2):
            cells = {cell + (i,) for cell in cells for i in range(lo - 1, hi + 2)}
        return cells

    def tick(self):
        ranges = [{cell[d] for cell in self.active} for d in range(self.dims)]
        relevant_cells = self.adjacent((min(r) for r in ranges), (max(r) for r in ranges))
        active = self.active.copy()
        inactive = relevant_cells - active
        self.active = set()

        for cell in relevant_cells:
            neighbours = self.adjacent(cell, cell) - {cell}
            active_neighbours = neighbours & active
            if cell in active and len(active_neighbours) in [2, 3]:
                self.active.add(cell)
            if cell not in active and len(active_neighbours) == 3:
                self.active.add(cell)

    def run_for(self, n):
        for i in range(n):
            self.tick()
        return len(self.active)


def main():
    data = open(os.path.join(MYDIR, 'input.txt')).read().strip()
    print("Part 1:", Grid(data, 3).run_for(6))
    print("Part 2:", Grid(data, 4).run_for(6))


if __name__ == '__main__':
    main()
