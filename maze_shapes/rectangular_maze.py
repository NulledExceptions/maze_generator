
import numpy as np, random
from maze_shapes.solver import MazeSolver

class RectangularMaze:
    def __init__(self, size, logger=None):
        # enforce odd size to align corridors on odd indices
        if size % 2 == 0:
            size += 1
        self.size = size
        self.logger = logger
        self.grid = np.ones((size, size), dtype=int)
        self.start = None
        self.end = None

    def _choose_opposite_edges(self):
        return random.choice([('top', 'bottom'), ('left', 'right')])

    def _rand_odd(self, lo, hi):
        # returns a random odd integer between lo and hi inclusive
        r = random.randrange(lo | 1, hi+1, 2)
        return r

    def _random_edge_cell(self, side):
        # ensure corridor alignment: interior coordinate (odd) adjacent to edge
        if side == 'top': 
            return (0, self._rand_odd(1, self.size - 2))
        if side == 'bottom': 
            return (self.size - 1, self._rand_odd(1, self.size - 2))
        if side == 'left': 
            return (self._rand_odd(1, self.size - 2), 0)
        # right
        return (self._rand_odd(1, self.size - 2), self.size - 1)

    def _carve_maze(self):
        # randomized DFS (backtracker) on odd cells
        stack = [(1, 1)]
        self.grid[1, 1] = 0
        while stack:
            x, y = stack[-1]
            dirs = [(2,0),(-2,0),(0,2),(0,-2)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.size-1 and 0 < ny < self.size-1 and self.grid[nx, ny] == 1:
                    self.grid[x + dx//2, y + dy//2] = 0  # knock down wall
                    self.grid[nx, ny] = 0               # carve cell
                    stack.append((nx, ny))
                    break
            else:
                stack.pop()

    def _connect_to_interior(self, pos):
        # Open the cell adjacent to the boundary opening so it joins the carved tree
        x, y = pos
        if x == 0: self.grid[1, y] = 0
        elif x == self.size - 1: self.grid[self.size - 2, y] = 0
        if y == 0: self.grid[x, 1] = 0
        elif y == self.size - 1: self.grid[x, self.size - 2] = 0

    def generate(self, max_attempts=50):
        for attempt in range(max_attempts):
            # reset and carve a perfect maze
            self.grid[:] = 1
            self._carve_maze()

            # choose opposite-edge start/end and open them
            a, b = self._choose_opposite_edges()
            self.start = self._random_edge_cell(a)
            self.end = self._random_edge_cell(b)
            self.grid[self.start] = 0
            self.grid[self.end] = 0
            self._connect_to_interior(self.start)
            self._connect_to_interior(self.end)

            # validate solvability (unique path guaranteed by perfect maze)
            solver = MazeSolver(self.grid)
            path = solver.solve(self.start, self.end)
            if path:
                if self.logger:
                    self.logger.info(f"Solvable maze on attempt {attempt+1}: {self.start}->{self.end}")
                return self.grid, self.start, self.end, path
            if self.logger:
                self.logger.warning(f"Retrying generation attempt {attempt+1}/{max_attempts}")
        raise ValueError("Failed to generate solvable maze after attempts")
