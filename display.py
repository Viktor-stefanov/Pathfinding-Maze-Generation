from globals import *
import pygame
import sys

pygame.init()
clock = pygame.time.Clock()
fps = 0

# menu surface is a surface on which everything is aligned properly and is used as a pattern based upon which
# to transform the current screen dimensions without breaking responsiveness
menu_surface = pygame.Surface((1680, 1050))
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
s_width, s_height = WIN.get_width(), WIN.get_height() 
c_width, c_height = s_width / cells, s_height / cells

ratio = (1680 / s_width + 1050 / s_height) / 2
num_font = pygame.font.SysFont('comicsansms', int(15 / ratio))

def update_weights(board, start, end):
    for row in board:
        for node in row:
            if node.weight > 1 and node not in (start, end):
                number = num_font.render(str(node.weight), True, BLACK)
                WIN.blit(number, (node.x * c_width + c_width // 2.5, node.y * c_height + 2))

def update_tiles(start, end, board):
    for row in board:
        for node in row:
            # draw the walls of the nodes
            if node.walls[0] is True:
                pygame.draw.line(WIN, BLACK, (node.x * c_width, node.y * c_height), (node.x * c_width + c_width, node.y * c_height))
            if node.walls[1] is True:
                pygame.draw.line(WIN, BLACK, (node.x * c_width, node.y * c_height), (node.x * c_width, node.y * c_height + c_height))
            if node.walls[2] is True:
                pygame.draw.line(WIN, BLACK, (node.x * c_width, node.y * c_height + c_height), (node.x * c_width + c_width, node.y * c_height + c_height))
            if node.walls[3] is True:
                pygame.draw.line(WIN, BLACK, (node.x * c_width + c_width, node.y * c_height), (node.x * c_width + c_width, node.y * c_height + c_height))

            # give the nodes a color
            rect = (node.x * c_width + 1, node.y * c_height + 1, c_width, c_height)
            if node.color is not None:
                pygame.draw.rect(WIN, node.color, rect)
            if node.obstacle is True:
                pygame.draw.rect(WIN, BLACK, rect)
            if node is start:
                pygame.draw.rect(WIN, START_COLOR, rect)
            if node is end:
                pygame.draw.rect(WIN, END_COLOR, rect)

def redraw_window(start, end, board, wg=False, alg_running=True):
    global fps

    WIN.fill(WHITE)
    update_tiles(start, end, board)
    if wg is True:
        update_weights(board, start, end)
    # if alg is running this is used to not repeat the code below for each individual algorithm
    if alg_running is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    fps *= 2
                    if fps >= 500:
                        fps = 500
                elif event.button == 5:
                    fps /= 2
                    if fps < 1:
                        fps = 1
        clock.tick(fps)

    pygame.display.update()

