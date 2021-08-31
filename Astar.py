import algorithm as algorithm
import pygame
import math
from queue import PriorityQueue

# pygame display setting
WIDTH = 800  # width of the window, if it is 50*50, then each grid width will be 800/50
WIN = pygame.display.set_mode((WIDTH, WIDTH))  # how big the display is going to be
pygame.display.set_caption("A* Path Finding Algorithm")

# constant setting of color in RGB number, pygame can recognize it into color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# spot location(row, col), size(width), state(color), neighbours, total rows
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width  # coordinate is the right bottom corner
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):  # to tell if this spot is closed, if red, then closed
        return self.color == RED

    def is_open(self):  # to tell if this spot is open
        return self.color == GREEN

    def is_barrier(self):  # to tell if this spot is a barrier
        return self.color == BLACK

    def is_start(self):  # to tell if this spot is the start
        return self.color == ORANGE

    def is_end(self):  # to tell if this spot is the end
        return self.color == PURPLE

    def reset(self):  # to reset the state
        self.color = WHITE

    def make_start(self):  # to set the start spot
        self.color = ORANGE

    def make_closed(self):  # to close
        self.color = RED

    def make_open(self):  # to open
        self.color = GREEN

    def make_barrier(self):  # to make it the barrier
        self.color = BLACK

    def make_end(self):  # to make it the end
        self.color = TURQUOISE

    def make_path(self):  # to make it the path
        self.color = PURPLE

    def draw(self, win):  # draw the rectangle here  (only the cube)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        # rect means the way to draw a rectangle (location and size)

    def update_neighbours(self, grid):
        self.neighbours = []

        # movement check
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # down
            self.neighbours.append(grid[self.row + 1][self.col]) # move down

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # up
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # right
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # left
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):  # lt means less than, we compare two spots here
        return False


# In A* pathway finding algorithm, f(n)=g(n)+h(n)

# heuristic function h(n)
def h(p1, p2):  # manhattan distance
    x1, y1 = p1  # coordinate of p1  eg.p1=(1,9)
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
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
            end.make_end()
            return True

        for neighbor in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put(f_score[neighbor], count, neighbor)
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()
    return False


# make a grid
def make_grid(rows, width):
    grid = []
    gap = width // rows  # // here means integer division, eg, 10//3=3
    for i in range(rows):  # from row 1 to the final row
        grid.append([])  # add nothing                     what if i don't add this line??????
        for j in range(rows):
            spot = Spot(i, j, gap, rows)  # the class of Spot here including location, size and total rows
            grid[i].append(spot)  # add one spot each time to the grid
    return grid


# draw grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))  # horizontal lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))  # vertical lines


# draw everything including grid lines
def draw(win, grid, rows, width):
    win.fill(WHITE)  # fills the screen with white color

    for row in grid:
        for spot in row:
            spot.draw(win)  # draw all the white win

    draw_grid(win, rows, width)
    pygame.display.update()


# mouse click
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos

    row = x // gap
    col = y // gap

    return row, col


# main function
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():  # to monitor the user event
            if event.type == pygame.QUIT:  # if we press the X button at the top right hand corner, then stop running the game and quit
                run = False

            if pygame.mouse.get_pressed()[0]:  # if the user click the left mouse; 0 1 2: left middle right
                pos = pygame.mouse.get_pos()  # get the mouse click position
                row, col = get_clicked_pos(pos, ROWS, width)  # get mouse row and col
                spot = grid[row][col]
                if not start and spot != end:  # start spot and end spot are not the same spot
                    start = spot  # make the mouse spot as the start
                    start.make_start()  # make the color as orange
                elif not end and spot != start:  # end spot and end spot are not the same spot
                    end = spot  # make the mouse spot as the end
                    end.make_end()  # make the color as turquoise
                elif spot != end and spot != start:  # barrier spot
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:  # if the user click the right mouse
                pos = pygame.mouse.get_pos()  # get the mouse click position
                row, col = get_clicked_pos(pos, ROWS, width)  # get mouse row and col
                spot = grid[row][col]
                spot.reset()  # make it white
                if spot == start:
                    start = None  # reset the start

                elif spot == end:
                    end = None  # reset the end

            if event.type == pygame.KEYDOWN:  # if the keyboard is pressed
                if event.key == pygame.K_SPACE and start and end:  # if the key is the space bar and we haven't started the algorithm
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()  # exit the game window


main(WIN, WIDTH)
