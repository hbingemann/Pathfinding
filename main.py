import pygame

from aStar import Grid

pygame.init()

# global constants
SIZE = WIDTH, HEIGHT = 1000, 860
SQUARE_SIZE = 20
FPS = 60

# colors
BACKGROUND_COLOR = (210, 210, 210)  # almost white
GRID_COLOR = (60, 60, 60)  # almost black
OBSTACLE_COLOR = (20, 20, 20)  # black
START_COLOR = (209, 204, 44)  # yellowish
END_COLOR = (191, 105, 23)  # orange
PATH_COLOR = (38, 96, 166)  # blue
GREEN = (47, 168, 83)
RED = (220, 0, 0)


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


def visualize_algorithm(screen, grid):
    # this is the loop that will show the algorithm in action

    # set some useful variables
    time_since_action = 0
    time_between_actions = 10  # in milliseconds

    # start the process
    grid.start_tick_process()

    # reset the screen
    draw_background(screen)
    draw_squares_at(screen, grid.obstacles, OBSTACLE_COLOR)

    # starting main loop
    run = True
    clock = pygame.time.Clock()
    while run:

        # regulate game speed
        clock.tick(FPS)
        time_since_action += clock.get_time()

        # check events
        for event in pygame.event.get():

            # close window
            if event.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                run = False

            # end the process
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.key.key_code("return"):
                    return []

        # check if process can be continued
        if time_since_action > time_between_actions:
            time_since_action = 0
            path = grid.tick_process()
            if path is not None:
                # we found a solution
                # it will return [] if there was no solution
                # and a list of coords if there was a solution
                return path

        # create positions from objects
        green_positions = [(node.x, node.y) for node in grid.green_nodes]
        red_positions = [(node.x, node.y) for node in grid.red_nodes]

        # now draw what has happened
        draw_squares_at(screen, green_positions, GREEN)
        draw_squares_at(screen, red_positions, RED)
        draw_square_at(screen, grid.start_pos, START_COLOR)
        draw_square_at(screen, grid.end_pos, END_COLOR)
        pygame.display.update()


def main():
    # setting some values that will be useful
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('PATHFINDING')

    mouse_deleting_obstacles = False
    mouse_drawing_obstacles = False
    mouse_on_start = False
    mouse_on_end = False
    keep_finding_path = False
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
                # left click
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    mouse_grid_pos = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                    if mouse_grid_pos == grid.start_pos:
                        mouse_on_start = True
                    elif mouse_grid_pos == grid.end_pos:
                        mouse_on_end = True
                    else:
                        mouse_drawing_obstacles = True

                # right click
                elif event.button == 3:
                    mouse_deleting_obstacles = True

            # mouse up
            if event.type == pygame.MOUSEBUTTONUP:

                # left click
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    mouse_grid_pos = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                    if mouse_on_end:
                        end = mouse_grid_pos
                        grid.end_pos = end
                    elif mouse_on_start:
                        start = mouse_grid_pos
                        grid.start_pos = start
                    # set them all to false
                    mouse_drawing_obstacles = False
                    mouse_on_end = False
                    mouse_on_start = False

                # right click
                elif event.button == 3:
                    mouse_deleting_obstacles = False

            # button down
            if event.type == pygame.KEYDOWN:

                # clear button
                if event.key == pygame.key.key_code("c"):
                    obstacles = []
                    path = []

                # start calculating button
                elif event.key == pygame.key.key_code("return"):
                    path = visualize_algorithm(screen, grid)

                # always draw the path button
                elif event.key == pygame.key.key_code("space"):
                    keep_finding_path = not keep_finding_path
                    if not keep_finding_path:
                        path = []

                # remove most recently created obstacle
                elif event.key == pygame.key.key_code("backspace"):
                    obstacles.pop()

        pos = pygame.mouse.get_pos()
        mouse_grid_pos = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE

        if mouse_drawing_obstacles:
            obstacle = mouse_grid_pos
            if obstacle not in obstacles:
                obstacles.append(obstacle)
                grid.obstacles = obstacles
        elif mouse_deleting_obstacles:
            if mouse_grid_pos in obstacles:
                obstacles.remove(mouse_grid_pos)
        elif mouse_on_end:
            end = mouse_grid_pos
            grid.end_pos = mouse_grid_pos
        elif mouse_on_start:
            start = mouse_grid_pos
            grid.start_pos = mouse_grid_pos
        if keep_finding_path:
            path = grid.find_path()

        draw_background(screen)
        draw_squares_at(screen, obstacles, OBSTACLE_COLOR)
        draw_squares_at(screen, path, PATH_COLOR)
        draw_square_at(screen, start, START_COLOR)
        draw_square_at(screen, end, END_COLOR)
        pygame.display.update()


if __name__ == '__main__':
    main()
