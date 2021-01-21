import pygame


class Node(object):
    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0


def visualize_grid(screen, grid, size, rows):
    gray = (200, 200, 200)
    black = (0, 0, 0)
    green = (0, 255, 0)
    red = (255, 0, 0)
    space = size // rows
    screen.fill(gray)

    for y, row in enumerate(grid):  # Colors squares in grid
        for x, value in enumerate(row):
            if value == 1:  # barrier
                pygame.draw.rect(screen, black, ((x * space), (y * space), space, space))
            elif value == 2:  # start
                pygame.draw.rect(screen, green, ((x * space), (y * space), space, space))
            elif value == 3:  # end
                pygame.draw.rect(screen, red, ((x * space), (y * space), space, space))
            elif value == 4:
                pygame.draw.rect(screen, (30, 50, 255), ((x * space), (y * space), space, space))
            elif value == 5:
                pygame.draw.rect(screen, (255, 0, 255), ((x * space), (y * space), space, space))

    for x in range(rows):  # Draws Lines on grid
        pygame.draw.line(screen, black, (0, x * space), (size, x * space))
        for y in range(rows):
            pygame.draw.line(screen, black, (y * space, 0), (y * space, size))

    pygame.display.flip()


def get_neighbors(grid, current):  # Check if adjacent/diagonal nodes are available
    column, row = current.pos
    successors = []
    if row != 39 and grid[row + 1][column] in (0, 3):  # Check Down
        successors.append(Node(current.parent, (column, row + 1)))
    if row != 0 and grid[row - 1][column] in (0, 3):  # Check Up
        successors.append(Node(current.parent, (column, row - 1)))
    if column != 39 and grid[row][column + 1] in (0, 3):  # Check Right
        successors.append(Node(current.parent, (column + 1, row)))
    if column != 0 and grid[row][column - 1] in (0, 3):  # Check Left
        successors.append(Node(current.parent, (column - 1, row)))
    if row != 39 and column != 39 and grid[row + 1][column + 1] in (0, 3):
        successors.append(Node(current.parent, (column + 1, row + 1)))  # Check Bottom Right
    if row != 39 and column != 0 and grid[row + 1][column - 1] in (0, 3):
        successors.append(Node(current.parent, (column - 1, row + 1)))  # Check Bottom Left
    if row != 0 and column != 39 and grid[row - 1][column + 1] in (0, 3):
        successors.append(Node(current.parent, (column + 1, row - 1)))  # Check Top Right
    if row != 0 and column != 0 and grid[row - 1][column - 1] in (0, 3):
        successors.append(Node(current.parent, (column - 1, row - 1)))  # Check Top Left
    return successors


def heuristic(pos1, end):
    x1, y1 = pos1
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(grid, start, end, visualize):
    start_node = Node(None, start)
    end_node = Node(None, end)
    start_node.g = start_node.h = start_node.f = 0
    end_node.g = end_node.h = end_node.f = 0
    open_list = []
    closed_list = []
    open_list.append(start_node)

    while open_list:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_list[0]
        current_i = 0
        for i, node in enumerate(open_list):  # Find node with lowest f score
            if node.f < current.f:
                current = node
                current_i = i
        open_list.pop(current_i)
        closed_list.append(current)

        if current.pos == end_node.pos:  # Stops loop when path to end is found
            path = []
            while current:  # Back tracks parent of node
                path.append(current.pos)
                current = current.parent
            for pos in path[::-1]:
                x, y = pos
                if grid[y][x] not in (2, 3):
                    grid[y][x] = 5
            visualize()  # Update grid
            return

        successors = get_neighbors(grid, current)  # Check neighbors surrounding nodes

        for successor in successors:
            grid[successor.pos[1]][successor.pos[0]] = 4 if grid[successor.pos[1]][successor.pos[0]] != 3 else 3
            visualize()  # Update grid
            if successor in closed_list:  # Check if successor already in closed list
                continue
            if successor in open_list:  # Check if successor already in open list
                if successor.g > (current.g + 1):  # Check if g score higher than parent
                    continue
            else:
                successor.g = current.g + 1  # Set values for successor and append to open list
                successor.h = heuristic(successor.pos, end_node.pos)
                successor.f = successor.g + successor.h
                successor.parent = current
                open_list.append(successor)
    print('Path Not Found')


def main():
    pygame.init()
    size = 800
    screen = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Pathfinding Visualizer")

    rows = 40

    grid = [[0 for x in range(rows)] for y in range(rows)]
    visualize_grid(screen, grid, size, rows)

    run = True
    square_start = False
    square_end = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Mouse1 to place
                pos_x, pos_y = pygame.mouse.get_pos()  # Get mouse position on screen
                space = size // rows  # Convert mouse position to grid
                x = pos_x // space
                y = pos_y // space
                if not square_start and grid[y][x] != 3:
                    grid[y][x] = 2
                    start_pos = (x, y)
                    square_start = True
                elif not square_end and grid[y][x] != 2:
                    grid[y][x] = 3
                    end_pos = (x, y)
                    square_end = True
                elif grid[y][x] in (0, 4, 5):
                    grid[y][x] = 1
                visualize_grid(screen, grid, size, rows)

            if pygame.mouse.get_pressed()[2]:  # Mouse2 to delete
                pos_x, pos_y = pygame.mouse.get_pos()  # Get mouse position on screen
                space = size // rows  # Convert mouse position to grid
                x = pos_x // space
                y = pos_y // space
                if grid[y][x] == 2:
                    square_start = False
                elif grid[y][x] == 3:
                    square_end = False
                grid[y][x] = 0
                visualize_grid(screen, grid, size, rows)

            if event.type == pygame.KEYDOWN and square_start and square_end:
                for y, row in enumerate(grid):
                    for x, node in enumerate(row):
                        if node in (4, 5):
                            grid[y][x] = 0
                a_star_search(grid, start_pos, end_pos, lambda: visualize_grid(screen, grid, size, rows))

    pygame.quit()


if __name__ == "__main__":
    main()
