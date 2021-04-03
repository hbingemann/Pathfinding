
import pygame

from aStar import Grid

pygame.init()

# global constants
SIZE = WIDTH, HEIGHT = 1000, 860
SQUARE_SIZE = 20  # the path will be represented by these squares
FPS = 60

# colors
BACKGROUND_COLOR = (210, 210, 210)
GRID_COLOR = (60, 60, 60)
OBSTACLE_COLOR = (20, 20, 20)
START_COLOR = (209, 204, 44)
END_COLOR = (47, 168, 83)
PATH_COLOR = (38, 96, 166)


def draw_background(screen):
    # background
    screen.fill(BACKGROUND_COLOR)
    # add a grid
    for x in range(WIDTH // SQUARE_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x * SQUARE_SIZE, 0), (x * SQUARE_SIZE, HEIGHT))
    for y in range(HEIGHT // SQUARE_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y * SQUARE_SIZE), (WIDTH, y * SQUARE_SIZE))


def draw_squares_at(surface, square_locations, color):
    for pos in square_locations:
        x, y = pos
        rect = (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(surface, color, rect)


def draw_square_at(surface, square_pos, color):
    x, y = square_pos
    rect = (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(surface, color, rect)


def main():
    # setting some values that will be useful
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('PATHFINDING')

    mouse_drawing_obstacles = False
    mouse_on_start = False
    mouse_on_end = False
    path = []

    obstacles = []
    grid_size = WIDTH // SQUARE_SIZE, HEIGHT // SQUARE_SIZE
    start = (0, 0)
    end = (12, 12)

    grid = Grid(start, end, grid_size, obstacles)

    # starting main loop
    run = True
    clock = pygame.time.Clock()
    while run:
        # regulate game speed
        clock.tick(FPS)

        # check events
        for event in pygame.event.get():

            # close window
            if event.type == pygame.QUIT:
                run = False

            # mouse down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    grid_pos = (x // SQUARE_SIZE, y // SQUARE_SIZE)
                    if grid_pos == start:
                        mouse_on_start = True
                    elif grid_pos == end:
                        mouse_on_end = True
                    else:
                        mouse_drawing_obstacles = True

            # mouse up
            if event.type == pygame.MOUSEBUTTONUP:

                # left click
                if event.button == 1:
                    mouse_drawing_obstacles = False
                    x, y = pygame.mouse.get_pos()
                    if mouse_on_end:
                        end = (x // SQUARE_SIZE, y // SQUARE_SIZE)
                        grid.end_node.x, grid.end_node.y = end
                    elif mouse_on_start:
                        start = (x // SQUARE_SIZE, y // SQUARE_SIZE)
                        grid.start_node.x, grid.start_node.y = start
                    mouse_on_end = False
                    mouse_on_start = False

                # right click
                elif event.button == 3:
                    pass

            # button down
            if event.type == pygame.KEYDOWN:

                # clear button
                if event.key == pygame.key.key_code("c"):
                    obstacles = []
                    path = []

                # start calculating button
                elif event.key == pygame.key.key_code("return"):
                    path = grid.find_path(0)

        if mouse_drawing_obstacles:
            x, y = pygame.mouse.get_pos()
            obstacle = x // SQUARE_SIZE, y // SQUARE_SIZE
            obstacles.append(obstacle)
            grid.obstacles = obstacles

        draw_background(screen)
        draw_squares_at(screen, obstacles, OBSTACLE_COLOR)
        draw_squares_at(screen, path, PATH_COLOR)
        draw_square_at(screen, start, START_COLOR)
        draw_square_at(screen, end, END_COLOR)
        pygame.display.update()


if __name__ == '__main__':
    main()
