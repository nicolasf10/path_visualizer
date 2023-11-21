import pygame
import math
from queue import PriorityQueue

WIDTH = 800
ROWS = 30
WIN = pygame.display.set_mode((WIDTH // ROWS * ROWS, WIDTH // ROWS * ROWS))
pygame.display.set_caption("Path Finding Algorithms")

RED = (255, 36, 36)
GREEN = (51, 225, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (71, 71, 71)
PURPLE = (170, 0, 225)
ORANGE = (255, 135, 0)
GREY = (128, 128, 128)
TURQUOISE = (0, 225, 218)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    # 'get' methods
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    # 'make' methods
    def make_closed(self):
        self.color = RED

    def make_start(self):
        self.color = ORANGE

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbours = []
        if (
            self.row < self.total_rows - 1
            and not grid[self.row + 1][self.col].is_barrier()
        ):  # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if (
            self.col < self.total_rows - 1
            and not grid[self.row][self.col + 1].is_barrier()
        ):  # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def a_star_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(
                    neighbour.get_pos(), end.get_pos()
                )
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def depth_first_algorithm(draw, grid, start, end):
    frontier = [start]
    explored = {start}
    came_from = {}

    while len(frontier) > 0:
        spot = frontier.pop()
        explored.add(spot)
        if spot != start and spot != end:
            spot.make_open()

        if spot == end:
            reconstruct_path(came_from, end, draw)
            return True

        for neighbour in spot.neighbours:
            if neighbour not in explored:
                came_from[neighbour] = spot
                frontier.append(neighbour)

        draw()

    return False


def breadth_first_algorithm(draw, grid, start, end):
    frontier = [start]
    explored = {start}
    came_from = {}

    while len(frontier) > 0:
        spot = frontier.pop()

        for s in explored:
            s.make_closed()

        if spot != start and spot != end:
            spot.make_open()

        if spot == end:
            reconstruct_path(came_from, end, draw)
            return True

        for neighbour in spot.neighbours:
            if neighbour not in explored:
                explored.add(neighbour)
                came_from[neighbour] = spot
                frontier.insert(0, neighbour)

        draw()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    algorithm = "a*"

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            if not (spot.is_start() or spot.is_start()):
                                spot.reset()
                            spot.update_neighbors(grid)

                    if algorithm == "a*":
                        a_star_algorithm(
                            lambda: draw(win, grid, ROWS, width), grid, start, end
                        )
                    elif algorithm == "dpf":
                        depth_first_algorithm(
                            lambda: draw(win, grid, ROWS, width), grid, start, end
                        )
                    elif algorithm == "bdf":
                        breadth_first_algorithm(
                            lambda: draw(win, grid, ROWS, width), grid, start, end
                        )

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_a:
                    algorithm = "a*"

                if event.key == pygame.K_d:
                    algorithm = "dpf"

                if event.key == pygame.K_b:
                    algorithm = "bdf"

    pygame.quit()


main(WIN, WIDTH)