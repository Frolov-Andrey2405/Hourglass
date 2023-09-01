import random
import sys
import time
import bext

# Set up the constants:
PAUSE_LENGTH = 0.2  # (!) Try changing this to 0.0 or 1.0.
WIDE_FALL_CHANCE = 50  # (!) Try changing this to any number between 0 and 100:

SCREEN_WIDTH = 79
SCREEN_HEIGHT = 25
X = 0
Y = 1
SAND = chr(9617)
WALL = chr(9608)

# Set up the walls of the hourglass:
HOURGLASS = {
    (i, 1) for i in range(18, 37)
} | {
    (i, 23) for i in range(18, 37)
} | {
    (18, i) for i in range(1, 5)
} | {
    (36, i) for i in range(1, 5)
} | {
    (18, i + 19) for i in range(1, 5)
} | {
    (36, i + 19) for i in range(1, 5)
} | {
    (19 + i, 5 + i) for i in range(8)
} | {
    (35 - i, 5 + i) for i in range(8)
} | {
    (25 - i, 13 + i) for i in range(8)
} | {
    (29 + i, 13 + i) for i in range(8)
}

# Set up the initial sand at the top of the hourglass:
INITIAL_SAND = {(x, y) for y in range(8) for x in range(19 + y, 36 - y)}


def main():
    bext.fg('yellow')
    bext.clear()
    print('Ctrl-C to quit.', end='')

    # Display the walls of the hourglass:
    for wall in HOURGLASS:
        bext.goto(wall[X], wall[Y])
        print(WALL, end='')

    while True:
        allSand = list(INITIAL_SAND)
        for sand in allSand:
            bext.goto(sand[X], sand[Y])
            print(SAND, end='')

        runHourglassSimulation(allSand)


def runHourglassSimulation(allSand):
    while True:
        random.shuffle(allSand)
        sandMovedOnThisStep = False

        for i, sand in enumerate(allSand):
            if sand[Y] == SCREEN_HEIGHT - 1:
                continue

            below = (sand[X], sand[Y] + 1)
            noSandBelow = below not in allSand
            noWallBelow = below not in HOURGLASS
            canFallDown = noSandBelow and noWallBelow

            if canFallDown:
                bext.goto(sand[X], sand[Y])
                print(' ', end='')
                bext.goto(sand[X], sand[Y] + 1)
                print(SAND, end='')

                allSand[i] = (sand[X], sand[Y] + 1)
                sandMovedOnThisStep = True
            else:
                belowLeft = (sand[X] - 1, sand[Y] + 1)
                noSandBelowLeft = belowLeft not in allSand
                noWallBelowLeft = belowLeft not in HOURGLASS
                left = (sand[X] - 1, sand[Y])
                noWallLeft = left not in HOURGLASS
                notOnLeftEdge = sand[X] > 0
                canFallLeft = (
                    noSandBelowLeft and noWallBelowLeft
                    and noWallLeft and notOnLeftEdge)

                belowRight = (sand[X] + 1, sand[Y] + 1)
                noSandBelowRight = belowRight not in allSand
                noWallBelowRight = belowRight not in HOURGLASS
                right = (sand[X] + 1, sand[Y])
                noWallRight = right not in HOURGLASS
                notOnRightEdge = sand[X] < SCREEN_WIDTH - 1
                canFallRight = (noSandBelowRight and noWallBelowRight
                                and noWallRight and notOnRightEdge)

                fallingDirection = None

                if canFallLeft and not canFallRight:
                    fallingDirection = -1
                elif not canFallLeft and canFallRight:
                    fallingDirection = 1
                elif canFallLeft and canFallRight:
                    fallingDirection = random.choice((-1, 1))

                if fallingDirection is None:
                    continue

                if random.random() * 100 <= WIDE_FALL_CHANCE:
                    belowTwoLeft = (sand[X] - 2, sand[Y] + 1)
                    noSandBelowTwoLeft = belowTwoLeft not in allSand
                    noWallBelowTwoLeft = belowTwoLeft not in HOURGLASS
                    notOnSecondToLeftEdge = sand[X] > 1
                    canFallTwoLeft = (
                        canFallLeft and noSandBelowTwoLeft
                        and noWallBelowTwoLeft and notOnSecondToLeftEdge)

                    belowTwoRight = (sand[X] + 2, sand[Y] + 1)
                    noSandBelowTwoRight = belowTwoRight not in allSand
                    noWallBelowTwoRight = belowTwoRight not in HOURGLASS
                    notOnSecondToRightEdge = sand[X] < SCREEN_WIDTH - 2
                    canFallTwoRight = (
                        canFallRight and noSandBelowTwoRight
                        and noWallBelowTwoRight
                        and notOnSecondToRightEdge)

                    if canFallTwoLeft and not canFallTwoRight:
                        fallingDirection = -2
                    elif not canFallTwoLeft and canFallTwoRight:
                        fallingDirection = 2
                    elif canFallTwoLeft and canFallTwoRight:
                        fallingDirection = random.choice((-2, 2))

                bext.goto(sand[X], sand[Y])
                print(' ', end='')
                bext.goto(sand[X] + fallingDirection, sand[Y] + 1)
                print(SAND, end='')

                allSand[i] = (sand[X] + fallingDirection, sand[Y] + 1)
                sandMovedOnThisStep = True

        sys.stdout.flush()
        time.sleep(PAUSE_LENGTH)

        if not sandMovedOnThisStep:
            time.sleep(2)
            for sand in allSand:
                bext.goto(sand[X], sand[Y])
                print(' ', end='')
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
