import pygame
import time

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
gray = (100, 100, 100)


def boardCreate(file):
    with open(file) as blueprint:
        board = []
        for line in blueprint:
            row = []
            for item in line.split(','):
                row.append(item == '1')
            board.append(row)
        return board


def onBoard(coordinate, board_w, board_h):
    # determines whether or not (True or False) a coordinate is on the board
    x, y = coordinate
    is_on_board = (
        0 <= x < board_w
        and 0 <= y < board_h
    )
    return is_on_board


def getCoords(board, x, y):
    # determines which positions are valid
    coords = [
        (x+dx, y+dy)
        for dx in range(-1, 2)
        for dy in range(-1, 2)
        if not (dx == 0 and dy == 0)
    ]

    newCoords = [
        coord
        for coord in coords
        if onBoard(coord, len(board[0]), len(board))
    ]

    return newCoords


def countNeighbors(board, coordinates):
    neighbor_count = sum([board[y][x] for x, y in coordinates])
    return neighbor_count


def tick(cell_is_currently_alive, neighbors):
    # ticks a coordinate, but needs to be done at the same time as other coordinates on the board
    cell_will_be_alive = cell_is_currently_alive and not (neighbors < 2 or neighbors > 3) or neighbors == 3
    return cell_will_be_alive


def tickAll(board):
    new_board = []
    for _ in board:
        new_board.append([])

    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            neighbor_count = countNeighbors(board, getCoords(board, x, y))
            coord = tick(cell, neighbor_count)
            new_board[y].append(coord)
    return new_board


def printBoard(board, board_w):
    disp_val_map = {
        True: 'O',
        False: ' ',
    }
    print('┌' + ('─' * board_w) + '┐')
    for row in board:
        print('│' + ''.join(map(disp_val_map.__getitem__, row)) + '│')

    print('└' + ('─' * board_w) + '┘')


def drawBoard(board, gameDisplay):
    for row_num, row in enumerate(board):
        for item_num, item in enumerate(row):
            if item:
                pygame.draw.rect(gameDisplay, (0, 0, 0), (item_num * 50, row_num * 50, 50, 50))


def main():

    board = boardCreate('map.txt')

    clock = pygame.time.Clock()

    board_h = len(board)
    board_w = len(board[0])

    display_width = board_w * 50
    display_height = board_h * 50

    gameDisplay = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption('Conway\'s Pygame of Life')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        drawBoard(board, gameDisplay)
        board = tickAll(board)
        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    main()
