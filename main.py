from algorithms.pathfinding_algorithms import *
from globals import *
import pygame
import random
import math
import sys
from queue import PriorityQueue

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.walls = [True, True, True, True]
        self.weight = 1
        self.reset()

    def reset(self):
        self.distance_from_start = float('inf')
        self.distance_to_end = float('inf')
        self.color = None
        self.parent = None
        self.obstacle = False
        self.expanding = False
        # this instance variable is for the bidirectional dijkstra algorithm, so connection between start and end can be detected
        self.came_from = None

    def get_random_neighbor(self):
        # method to return random unvisited neighbor for maze generating algorithm
        choices = [neighbor for neighbor in self.neighbors if neighbor.visited is False]
        if choices == []:
            return None

        return random.choice(choices)


def reset_nodes(board):
    for row in board:
        for node in row:
            node.reset()


def set_random_weights(board):
    for node in random.sample([col for row in board for col in row], int(cells ** 2 * 0.33)):
        node.weight = random.randint(1, 9)


# DISPLAY SETUP BELOW
pygame.init()
clock = pygame.time.Clock()
fps = 0

# menu surface is a surface on which everything is aligned properly and it's used to get transformed to the current dimensions without breaking responsiveness
menu_surface = pygame.Surface((1680, 1050))
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
s_width, s_height = pygame.display.get_surface().get_size()
# change cells variable to increase the number of tiles on the screen
cells = 40
c_width, c_height = s_width / cells, s_height / cells

ratio = (1680 / s_width + 1050 / s_height) / 2
num_font = pygame.font.SysFont('comicsansms', int(15 / ratio))


# MAZE GENERATION ALGORITHMS BELOW

def recursive_backtracking(start, end, mg, board):
    visited_set = set()
    deadend_stack = []
    current = start
    while len(deadend_stack) != len(board) * len(board[0]):
        visited_set.add(current)
        current.color = VISITED_COLOR

        unvisited_neighbors = [neighbor for neighbor in current.neighbors if neighbor not in visited_set]
        if unvisited_neighbors != []:
            neighbor = random.choice(unvisited_neighbors)
        else:
        # else if unvisited neighbor is None then no neighbors are unvisited and we set current to current.parent
            current.color = PATH_COLOR
            current = current.parent
            deadend_stack.append(current)
            if mg is False:
                redraw_window(start, end, board, wg=False, alg_running=True)
            continue
        # delete (carve) wall from current to neighbor that has not been visited
        if current.x - neighbor.x == -1:
            current.walls[3] = False
            neighbor.walls[1] = False
        elif current.x - neighbor.x == 1:
            current.walls[1] = False
            neighbor.walls[3] = False
        elif current.y - neighbor.y == -1:
            current.walls[2] = False
            neighbor.walls[0] = False
        elif current.y - neighbor.y == 1:
            current.walls[0] = False
            neighbor.walls[2] = False

        neighbor.parent = current
        current = neighbor

        if mg is False:
            redraw_window(start, end, board, wg=False, alg_running=True)


def eller_algorithm(start, end, mg, board):
    current_set = [n for n in range(0, len(board))]

    for row in board:
        for idx, node in enumerate(row[:-1]):
            # if it is the last row or we are lucky and adjacent cell isn't belonging to the same set merge the 2 cells
            if (random.randint(0, 1) or row == board[-1]) and current_set[idx] != current_set[idx + 1]:
                if row != board[-1]:
                    current_set[idx+1] = current_set[idx]
                # remove (carve) walls vertically
                node.walls[2] = False
                row[idx+1].walls[0] = False

                node.color = VISITED_COLOR
                row[idx+1].color = VISITED_COLOR
            if mg is False:
                redraw_window(start, end, board, wg=False, alg_running=True)

        # make vertical connections if we are not on the last row
        if row != board[-1]:

            next_set = [n for n in range((board.index(row)+1) * len(row), (board.index(row)+2) * len(row))]
            have_moved = set()
            # while all the current row's sets have not made a vertical line
            while set(current_set) != have_moved:
                for idx, node in enumerate(row):
                    if random.randint(0, 1) and current_set[idx] not in have_moved:
                        have_moved.add(current_set[idx])
                        next_set[idx] = current_set[idx]
                        # remove (carve) walls horizontally
                        node.walls[3] = False
                        board[board.index(row)+1][idx].walls[1] = False

                        node.color = PATH_COLOR
                        board[board.index(row)+1][idx].color = PATH_COLOR
                        if mg is False:
                            redraw_window(start, end, board, wg=False, alg_running=True)

            # make some more vertical lines on the penultimate row, so that the last row will have a set with more than 1 cell thus make a wall and not look empty
            if row == board[-2]:
                for idx, node in enumerate(row):
                    if random.randint(0, 1) and node.walls[3] is True:
                        next_set[idx] = current_set[idx]
                        # remove (carve) walls horizontally
                        node.walls[3] = False
                        board[board.index(row)+1][idx].walls[1] = False

                        node.color = PATH_COLOR
                        board[board.index(row)+1][idx].color = PATH_COLOR
                        if mg is False:
                            redraw_window(start, end, board, wg=False, alg_running=True)

        current_set = next_set


def kruskal_algorithm(start, end, mg, board):
    nodes = [node for row in board for node in row]
    set_node = {set: [node] for set, node in enumerate(nodes)}

    edges = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            edges.append((board[row][col], board[row + 1][col], 'RIGHT')) if row < len(board) - 1 else None
            edges.append((board[row][col], board[row][col + 1], 'UP')) if col < len(board[0]) - 1 else None

    random.shuffle(edges)

    for (node_a, node_b, direction) in edges:
        if len(set_node) == 1:
            break
        set_a, set_b = None, None
        for set in list(set_node.keys()):
            if node_a in set_node[set]:
                set_a = set
            if node_b in set_node[set]:
                set_b = set
            if None not in (set_a, set_b) and set_a != set_b:
                set_node[set_a].extend(set_node[set_b])
                del set_node[set_b]
                if direction == 'UP':
                    node_a.walls[2] = False
                    node_b.walls[0] = False
                elif direction == 'RIGHT':
                    node_a.walls[3] = False
                    node_b.walls[1] = False

                node_a.color = VISITED_COLOR
                node_b.color = VISITED_COLOR

                if mg is False:
                    redraw_window(start, end, board, wg=False, alg_running=True)

                node_a.color = PATH_COLOR
                node_b.color = PATH_COLOR
                break


def prim_algorithm(start, end, mg, board):
    visited_cells = set()
    current_cell = board[random.randint(0, len(board)-1)][random.randint(0, len(board[0])-1)]
    d = {frontier_cell: current_cell for frontier_cell in current_cell.neighbors}

    while d != {}:
        frontier_cell, current_cell = random.choice(list(d.items()))
        del d[frontier_cell]
        visited_cells.add(frontier_cell)

        for f_cell in frontier_cell.neighbors:
            if f_cell not in visited_cells:
                d[f_cell] = frontier_cell

        # delete (carve) wall from current to neighbor that has not been visited
        if current_cell.x - frontier_cell.x == -1:
            current_cell.walls[3] = False
            frontier_cell.walls[1] = False
        elif current_cell.x - frontier_cell.x == 1:
            current_cell.walls[1] = False
            frontier_cell.walls[3] = False
        elif current_cell.y - frontier_cell.y == -1:
            current_cell.walls[2] = False
            frontier_cell.walls[0] = False
        elif current_cell.y - frontier_cell.y == 1:
            current_cell.walls[0] = False
            frontier_cell.walls[2] = False

        frontier_cell.color = VISITED_COLOR
        current_cell.color = VISITED_COLOR

        if mg is False:
            redraw_window(start, end, board, wg=False, alg_running=True)

        frontier_cell.color = PATH_COLOR
        current_cell.color = PATH_COLOR


def board_setup():
    board = [[Node(x, y) for y in range(cells)] for x in range(cells)]

    # set the neighbors of the node. Only up, left, right and down nodes are allowed
    for row in board:
        for node in row:
            if node.x - 1 >= 0:
                node.neighbors.append(board[node.x - 1][node.y])
            if node.x + 1 < cells:
                node.neighbors.append(board[node.x + 1][node.y])
            if node.y - 1 >= 0:
                node.neighbors.append(board[node.x][node.y - 1])
            if node.y + 1 < cells:
                node.neighbors.append(board[node.x][node.y + 1])

    return board


def start_alg(alg, start, end, maze, wg, board):
    if alg == 'd':
        astar_dijkstra(start, end, maze, wg, board, dijkstra=True)
    elif alg == 'a*':
        astar_dijkstra(start, end, maze, wg, board, dijkstra=False)
    elif alg == 'bi_d':
        bidirectional_dijkstra(start, end, wg, maze, board)


def start_maze(alg, start, end, mg, board):
    if alg == 'r_bt':
        recursive_backtracking(start, end, mg, board)
    elif alg == 'el':
        eller_algorithm(start, end, mg, board)
    elif alg == 'kr':
        kruskal_algorithm(start, end, mg, board)
    elif alg == 'prim':
        prim_algorithm(start, end, mg, board)


def update_weights(start, end):
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
        update_weights(start, end)
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


def run_algorithm(alg, maze, mg, wg):
    board = board_setup()
    start = board[0][0]
    end = board[cells - 1][cells - 1]

    if maze is not None:
        start_maze(maze, start, end, mg, board)
        reset_nodes(board)

    if wg is not False:
        set_random_weights(board)

    picked_number = {
        pygame.K_1: 1,
        pygame.K_2: 2,
        pygame.K_3: 3,
        pygame.K_4: 4,
        pygame.K_5: 5,
        pygame.K_6: 6,
        pygame.K_7: 7,
        pygame.K_8: 8,
        pygame.K_9: 9,
    }
    solve, finished, draw, erase, pick_start, pick_end, choose_cell, selected_cell, add_weight = False, False, False, False, False, False, False, None, False
    while True:
        redraw_window(start, end, board, wg=wg, alg_running=False)

        if solve is True:
            start_alg(alg, start, end, maze, wg, board)
            draw, solve = False, False
            finished = True

        for event in pygame.event.get():
            # check for user input
            if event.type == pygame.QUIT:
                sys.exit()
                # start algorithm
            if event.type == pygame.KEYDOWN:
                if add_weight is True:
                    num = picked_number.get(event.key, None)
                    if num is not None:
                        selected_cell.weight = num
                        selected_cell.color = None
                        add_weight = False

                if event.key == pygame.K_SPACE:
                    solve = True
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    sys.exit()
                elif event.key == pygame.K_r:
                    finished = False
                    reset_nodes(board)
                elif event.key == pygame.K_w:
                    choose_cell = 1
                # return to the menu
                elif event.key == pygame.K_m:
                    main()
                elif event.key == pygame.K_s:
                    pick_start = True
                elif event.key == pygame.K_e:
                    pick_end = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    pick_start = False
                elif event.key == pygame.K_e:
                    pick_end = False
                elif event.key == pygame.K_w:
                    choose_cell = False
                    add_weight = True
            # set draw/erase to True/False if the left/right click is being held down/up
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if choose_cell is not False:
                        choose_cell = True
                    else:
                        draw = True
                elif event.button == 3:
                    erase = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if choose_cell is True:
                        choose_cell = 'stop'
                    draw = False
                if event.button == 3:
                    erase = False

        if finished is False:
            if pick_start is True:
                x, y = pygame.mouse.get_pos()
                x = int(x / c_width)
                y = int(y / c_height)
                if 0 <= x < cells and 0 <= y < cells and board[x][y] != end:
                    start = board[x][y]

            if pick_end is True:
                x, y = pygame.mouse.get_pos()
                x = int(x / c_width)
                y = int(y / c_height)

                if 0 <= x < cells and 0 <= y < cells and board[x][y] != start:
                    end = board[x][y]

            if maze is None:
                if choose_cell is True:
                    x, y = pygame.mouse.get_pos()
                    x = int(x / c_width)
                    y = int(y / c_height)

                    if 0 <= x < cells and 0 <= y < cells:
                        if selected_cell is not None:
                            selected_cell.color = WHITE
                        selected_cell = board[x][y]
                        selected_cell.color = VISITED_COLOR

                if draw is True:
                    x, y = pygame.mouse.get_pos()
                    x = int(x / c_width)
                    y = int(y / c_height)
                    if y < cells and x < cells:
                        board[x][y].obstacle = True

                if erase is True:
                    x, y = pygame.mouse.get_pos()
                    x = int(x / c_width)
                    y = int(y / c_height)
                    if y < cells and x < cells:
                        board[x][y].obstacle = False

# MAIN MENU CODE BELOW

def blit_text(hovered, maze, pf, e_maze, e_pf, mg=False, wg=False):
    # blit the header text in the main menu
    menu_surface.blit(main_menu_header_shadow, (168, 53))
    menu_surface.blit(main_menu_header, (165, 50))
    menu_surface.blit(main_menu_author, (1050, 140))

    # draw the legend box and blit the legend images
    pygame.draw.rect(menu_surface, BLACK, (1270, 310, 350, 475), 4)
    # idx * 75 is here simply to make use of the for loop, instead of manually setting each img/text's position
    for idx, img in enumerate(main_menu_imgs):
        menu_surface.blit(img, (1290, 330 + idx * 75))
    for idx, text in enumerate(main_menu_legend_text):
        menu_surface.blit(text, (1340, 325 + idx * 75))

    # blit the maze generating algorithm options
    choose_maze_alg = med_font.render('Pick maze generation algorithm(optional):', True, BLACK)
    menu_surface.blit(choose_maze_alg, (85, 590))

    maze_colors = [BLACK] * 6
    colors = [BLACK] * 3
    if e_pf is not None:
        colors[e_pf] = BLACK
    if e_maze is not None:
        maze_colors[e_maze] = BLACK

    if hovered is not None:
        if hovered <= 2:
            colors[hovered] = HOVERED
        elif hovered != 7:
            maze_colors[hovered-3] = HOVERED
        else:
            maze_colors[4] = HOVERED

    if pf is not None:
        colors[pf] = END_COLOR
    if maze is not None:
        maze_colors[maze] = END_COLOR
    if mg is not False:
        maze_colors[4] = END_COLOR
    if wg is not False:
        maze_colors[5] = END_COLOR


    rec_bt = small_font.render('- RECURSIVE BACKTRACKING', True, maze_colors[0])
    eller_alg = small_font.render('- ELLER\'S ALGORITHM', True, maze_colors[1])
    kruskal_alg = small_font.render('- KRUSKAL\'S ALGORITHM', True, maze_colors[2])
    prim_alg = small_font.render('- PRIM\'S ALGORITHM', True, maze_colors[3])

    if mg is False:
        maze_build = small_font.render('Generate maze instantly?', True, maze_colors[4])
    else:
        maze_build = small_font.render('Generate maze instantly!', True, maze_colors[4])
    if wg is False:
        weight_graph = small_font.render('Add random cell weights?', True, maze_colors[5])
    else:
        weight_graph = small_font.render('Add random cell weights!', True, maze_colors[5])

    r_bt = menu_surface.blit(rec_bt, (85, 670))
    el = menu_surface.blit(eller_alg, (85, 725))
    kr = menu_surface.blit(kruskal_alg, (630, 670))
    prim = menu_surface.blit(prim_alg, (630, 725))
    mb = menu_surface.blit(maze_build, (85, 780))
    wgr = menu_surface.blit(weight_graph, (85, 825))

    # blit the pathfinding algorithm options
    choose_alg = med_font.render('Pick pathfinding algorithm:', True, BLACK)
    menu_surface.blit(choose_alg, (85, 310))

    dijkstra = small_font.render('- DIJKSTRA/BFS ALGORITHM', True, colors[0])
    bi_dijkstra = small_font.render('- BIDIRECTIONAL DIJKSTRA', True, colors[1])
    a_star = small_font.render('- A* ALGORITHM', True, colors[2])

    d = menu_surface.blit(dijkstra, (85, 390))
    bi_d = menu_surface.blit(bi_dijkstra, (85, 450))
    a = menu_surface.blit(a_star, (630, 390))

    return d, bi_d, a, r_bt, el, kr, prim, mb, wgr

def main_menu():
    pathfinding_algs = ['d', 'bi_d', 'a*']
    maze_generation_algs = ['r_bt', 'el', 'kr', 'prim']
    hover, maze, pf, mg, wg, e_maze, e_pf = None, None, None, False, False, None, None
    while True:
        menu_surface.fill(WHITE)
        rects = blit_text(hover, maze, pf, e_maze, e_pf, mg, wg)

        x, y = pygame.mouse.get_pos()
        x, y = x / (WIN.get_width() / menu_surface.get_width()), y / (WIN.get_height() / menu_surface.get_height())
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    sys.exit()
                if event.key == pygame.K_RETURN and pf is not None:
                    # return the chosen algorithm
                    pf_alg = pathfinding_algs[pf]
                    maze_alg = maze_generation_algs[maze] if maze is not None else None
                    return pf_alg, maze_alg, mg, wg
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = [rect.collidepoint((x, y)) for rect in rects]
                    if 1 in clicked:
                        chosen = clicked.index(1)
                        if chosen <= 2:
                            pf = chosen
                            e_pf = None
                        elif chosen < 7:
                            maze = chosen-3
                            e_maze = None
                            wg = False
                        elif chosen == 7:
                            if maze is not None:
                                mg = True
                        elif chosen == 8:
                            if maze is None:
                                wg = True
                elif event.button == 3:
                    clicked = [rect.collidepoint((x, y)) for rect in rects]
                    if 1 in clicked:
                        undone = clicked.index(1)
                        if undone <= 2:
                            e_pf = undone
                            if pf == e_pf:
                                pf = None
                        elif undone < 7:
                            e_maze = undone-3
                            if maze == e_maze:
                                maze = None
                                mg = False
                        elif undone == 7:
                            mg = False
                        else:
                            wg = False

        # check for hovering over the algorithm options
        hover = [rect.collidepoint((x, y)) for rect in rects]
        if 1 in hover:
            hover = hover.index(1)
        else:
            hover = None

        # transform the menu surface to the current screen dimensions
        WIN.blit(pygame.transform.scale(menu_surface, WIN.get_rect().size), (0, 0))

        pygame.display.update()

def main():
    pathfinding_alg, maze_generation_alg, maze_generation, weighted_graph = main_menu()
    run_algorithm(pathfinding_alg, maze_generation_alg, maze_generation, weighted_graph)


if __name__ == '__main__':
    main()
