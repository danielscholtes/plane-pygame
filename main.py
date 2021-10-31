import pygame
import sys
import random
from Plane import Plane

# A pygame game which uses an algorithm to determine whether or not
# a plane can move randomly or needs to be corrected
# For every turn add +1 point and for every correction remove -1 points


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500
PLANE_IMAGE = 'plane.png'
TOTAL_TURNS = 1000

planes = []


def main():
    # Initializes the pygame screen
    global SCREEN, CLOCK
    img = pygame.image.load(PLANE_IMAGE)
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)
    amount = 4
    init_planes(amount)

    turns = 0
    corrections = 0
    collision = False

    while True:
        SCREEN.fill(WHITE)
        draw_grid()
        # Places all the planes on the screen and moves them accordingly
        for plane in planes:
            if turns < amount * TOTAL_TURNS and not collision:
                corrected = move(plane)
                if corrected:
                    corrections += 1
                turns += 1

            SCREEN.blit(img, (plane.get_x() * 50 + 4, plane.get_y() * 50 + 10))

        for plane in planes:
            for plane2 in planes:
                if plane == plane2:
                    continue
                # If planes collide (which they shouldn't) then stop the program
                if plane.get_x() == plane2.get_x() and plane.get_y() == plane2.get_y():
                    collision = True
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

        print("Turns:", turns, "Corrections:", corrections, "Points:", (turns - corrections))


def init_planes(amount):
    """
    Initializes all the planes
    :param amount: The amount of planes to add
    """
    # Keeps track of previous plane locations to prevent
    # placing places on each other
    cant = []
    for i in range(amount):

        # Randomly generates an x, y on the grid
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        # Prevents placing a plane on top of another
        while (x, y) in cant:
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        cant.append((x, y))
        planes.append(Plane(x, y))


def move(plane):
    """
    :return: True if plane movement was corrected, False if not, and the (x, y) coordinate the plane moved to
    """

    # Loads in all possible locations the plane can move to (horizontally, vertically and diagonally)
    init_loc_count = 0
    possible_locations = []
    # Possible location backup which will keep track of where the other planes are
    possible_locations_backup = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            x = plane.get_x() + i
            y = plane.get_y() + j

            # Prevent the plane from going out of the grid
            if x == -1 or x == 10 or y == -1 or y == 10:
                continue

            possible_locations.append((x, y))
            possible_locations_backup.append((x, y))
            init_loc_count += 1

    # Loops through all other planes
    for plane2 in planes:
        if plane2 == plane:
            continue

        # If plane is 1 block away remove it from the possible location
        dist_x = abs(plane.get_x() - plane2.get_x())
        dist_y = abs(plane.get_y() - plane2.get_y())
        if (dist_x == 0 or dist_x == 1) and (dist_y == 0 or dist_y == 1):
            if (plane2.get_x(), plane2.get_y()) in possible_locations:
                possible_locations.remove((plane2.get_x(), plane2.get_y()))
            if (plane2.get_x(), plane2.get_y()) in possible_locations_backup:
                possible_locations_backup.remove((plane2.get_x(), plane2.get_y()))

            # We go through all blocks surrounding the second plane and see if they intersect
            # the blocks surrounding the initial plane
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue

                    x = plane2.get_x() + i
                    y = plane2.get_y() + j

                    if x == plane.get_x() and y == plane.get_y():
                        continue

                    dist_x = abs(plane.get_x() - x)
                    dist_y = abs(plane.get_y() - y)

                    # If the blocks intersect we remove them from the possible locations
                    # The reason for this is to create distance between the planes so we wont need to
                    # correct them twice in a row (by moving them closer to eachother)
                    if (dist_x == 0 or dist_x == 1) and (dist_y == 0 or dist_y == 1) and (x, y) in possible_locations:
                        possible_locations.remove((x, y))

    # If there are no possible locations we take from the backup which only the plane
    # locations were removed
    if len(possible_locations) == 0:
        x, y = random.choice(possible_locations_backup)
    else:
        x, y = random.choice(possible_locations)

    plane.set_x(x)
    plane.set_y(y)

    # If the initial location count is not equal to the current count
    # then we corrected the course of the plane by adjusting the
    # possible locations
    return len(possible_locations) != init_loc_count


def draw_grid():
    """
    Draws a grid on the screen
    """
    block_size = 50  # Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)


if __name__ == '__main__':
    main()
