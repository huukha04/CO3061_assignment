from pipe import Pipe 

import heapq

class Game:
    def __init__(self, grid: list[list[Pipe]]):
        self.grid = grid
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.source = self._get_source()
        self.rotations = 0
        self.flow()

    def flow(self):
        # bfs
        for y in range(self.rows):
            for x in range(self.cols):
                pipe = self.grid[y][x]
                if not pipe.is_source():
                    self.grid[y][x] = pipe.unset_water()

        q: list[tuple[int, int]] = [self.source]
        while len(q) > 0:
            r, c = q.pop(0)
            pipe = self.grid[r][c]
            if pipe.contains_water() and not pipe.is_source():
                continue
            self.grid[r][c] = pipe.set_water()
            if pipe.up():
                if r > 0 and self.grid[r - 1][c].down():
                    q.append((r - 1, c))
            if pipe.right():
                if c < self.cols - 1 and self.grid[r][c + 1].left():
                    q.append((r, c + 1))
            if pipe.down():
                if r < self.rows - 1 and self.grid[r + 1][c].up():
                    q.append((r + 1, c))
            if pipe.left():
                if c > 0 and self.grid[r][c - 1].right():
                    q.append((r, c - 1))

    def clone(self):
        grid_clone = [[pipe for pipe in row] for row in self.grid]
        new_game = Game(grid_clone)
        return new_game

    def ended(self):
        for row in self.grid:
            for pipe in row:
                if pipe.is_sink() and not pipe.contains_water():
                    return False
        return True

    def rotate(self, y, x):
        self.grid[y][x] = self.grid[y][x].rotate_clockwise()
        self.rotations += 1
        self.flow()

    def rotate_to_next_valid_state(self, y, x):
        for _ in range(4):
            self.grid[y][x] = self.grid[y][x].rotate_clockwise()
            self.rotations += 1

            if self._valid_pipe(y, x):
                break

        self.flow()
        return self

    def solve_dfs(self):
        fixed = self._set_guaranteed_pipes()
        stack: list[Game] = [self]
        visited = set()
        visited.add(self)

        from gui import GameGUI
        self.gui = GameGUI(self) 

        while len(stack) > 0:
            game = stack.pop()
            if game.ended():
                self.gui.update(game)
                return game

            for y in range(game.rows):
                for x in range(game.cols):
                    if fixed[y][x]:
                        continue

                    new_game = game.clone().rotate_to_next_valid_state(y, x)
                    if not (new_game in visited):
                        stack.append(new_game)
                        visited.add(new_game)
            self.gui.update(game)
        return None
    
    def _set_guaranteed_pipes(self):
        # we presolve the pipe with only one possible state
        # that is the straight pipe at the border (only one possible rotation)
        # the T pipe at the border (only one possible rotation)
        # the corner pipe at the corner (only one possible rotation)
        
        # this array used to store if pipe is fixed

        fixed = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for y in range(self.rows):
            for x in range(self.cols):
                pipe = self.grid[y][x]
                cnt = 0
                rot = pipe
                new_pipe = pipe
                for _ in range(4):
                    if self._valid_pipe(y, x, new_pipe):
                        cnt += 1
                        rot = new_pipe
                    new_pipe = new_pipe.rotate_clockwise()
                if cnt == 1:
                    self.grid[y][x] = rot
                    fixed[y][x] = 1

        return fixed

    def _valid_pipe(self, y, x, pipe = None):
        # greedy rotation
        # invalid pipes are considered as pipes that flow out of the grid
        # and sinks that flow into other sinks
        # prevent rotation from valid to invalid pipe
        if not pipe:
            pipe = self.grid[y][x]

        for dy, dx in pipe.get_offset():
            new_y, new_x = y + dy, x + dx
            if new_y < 0 or new_y >= self.rows or new_x < 0 or new_x >= self.cols:
                return False
            adjacent_pipe = self.grid[new_y][new_x]
            if pipe.is_sink() and adjacent_pipe.is_sink():
                return False
        return True

    def _count_unconnected_direction(self, y, x):
        cnt = 0
        pipe: Pipe = self.grid[y][x]
        if pipe.up() and (y == 0 or not self.grid[y - 1][x].down()):
            cnt += 1
        if pipe.right() and (x == self.cols - 1 or not self.grid[y][x + 1].left()):
            cnt += 1
        if pipe.down() and (y == self.rows - 1 or not self.grid[y + 1][x].up()):
            cnt += 1
        if pipe.left() and (x == 0 or not self.grid[y][x - 1].right()):
            cnt += 1
        return cnt

    def _count_no_water_sinks(self):
        cnt = 0
        for row in self.grid:
            for pipe in row:
                if pipe.is_sink() and not pipe.contains_water():
                    cnt += 1
        return cnt

    def _get_source(self):
        for y in range(self.rows):
            for x in range(self.cols):
                pipe = self.grid[y][x]
                if pipe.is_source():
                    return (y, x)
        raise ValueError("No source found")

    def __lt__(self, other):
        return self._count_no_water_sinks() < other._count_no_water_sinks()

    def __eq__(self, other):
        # if two objects have same hash, use eq
        return self.grid == other.grid

    def __repr__(self):
        return "\n".join("".join(str(pipe) for pipe in row) for row in self.grid)

    def __hash__(self):
        # hash 2d array of int
        flat = [pipe for row in self.grid for pipe in row]
        return hash(tuple(flat))
