
from collections import deque

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze

    def solve(self, start, end):
        q = deque([start])
        visited = {start: None}
        while q:
            node = q.popleft()
            if node == end:
                break
            x, y = node
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = x+dx, y+dy
                if 0<=nx<self.maze.shape[0] and 0<=ny<self.maze.shape[1] and self.maze[nx,ny]==0 and (nx,ny) not in visited:
                    visited[(nx,ny)] = node
                    q.append((nx,ny))
        path, cur = [], end
        while cur:
            path.append(cur)
            cur = visited.get(cur)
        if not path or path[-1] != start:
            return []
        return list(reversed(path))
