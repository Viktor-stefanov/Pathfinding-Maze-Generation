import pygame
import math
import sys
import random
from queue import PriorityQueue

#### COLORS & IMAGES####


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
START_COLOR = (240, 20, 20)
END_COLOR = (20, 240, 20)
EXPAND_COLOR = (130, 232, 130)
VISITED_COLOR = (179, 249, 255)
PATH_COLOR = (252, 247, 113)
HOVERED = (55, 89, 46)

obstacle_img = pygame.image.load('img\\obstacle_color.png')
start_img = pygame.image.load('img\\start_color.png')
end_img = pygame.image.load('img\\end_color.png')
visited_img = pygame.image.load('img\\visited_color.png')
path_img = pygame.image.load('img\\path_color.png')
number_img = pygame.image.load('img\\number_img.png')


#### END OF COLORS ####

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


def reset_nodes():
    for row in board:
        for node in row:
            node.reset()


def set_random_weights():
    for node in random.sample([col for row in board for col in row], int(cells ** 2 * 0.33)):
        node.weight = random.randint(1, 9)

#### DISPLAY SETUP ####


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

big_font = pygame.font.SysFont('comicsansms', 80)
med_font = pygame.font.SysFont('comicsansms', 55)
small_font = pygame.font.SysFont('comicsansms', 35)
ratio = (1680 / s_width + 1050 / s_height) / 2
num_font = pygame.font.SysFont('comicsansms', int(15 / ratio))


#### END OF DISPLAY SETUP ####


#### MAZE GENERATING ALGORITHMS BELOW ####


def recursive_backtracking(start, end, mg):
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
                redraw_window(start, end, wg=False, alg_running=True)
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
            redraw_window(start, end, wg=False, alg_running=True)


def eller_algorithm(start, end, mg):
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
                redraw_window(start, end, wg=False, alg_running=True)

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
                            redraw_window(start, end, wg=False, alg_running=True)

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
                            redraw_window(start, end, wg=False, alg_running=True)

        current_set = next_set


def kruskal_algorithm(start, end, mg):
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
                    redraw_window(start, end, wg=False, alg_running=True)

                node_a.color = PATH_COLOR
                node_b.color = PATH_COLOR
                break


def prim_algorithm(start, end, mg):
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
            redraw_window(start, end, wg=False, alg_running=True)

        frontier_cell.color = PATH_COLOR
        current_cell.color = PATH_COLOR


#### END OF MAZE GENERATING ALGORITHMS ####


#### PATHFINDING ALGORITHMS BELOW ###


def reconstruct_path(path, start, end, wg):
    for node in path[::-1]:
        node.color = PATH_COLOR
        redraw_window(start, end, wg)


def find_path(end):
    # find the path from the end point to the start
    curr = end
    path = [curr]
    while curr.parent is not None:
        curr = curr.parent
        path.append(curr)

    return path


def find_bi_path(a, b):
    path = find_path(b)[::-1]
    path.extend(find_path(a))

    return path


def distance(a, b):
    # return math.sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)) # pythagorean theorem - use for weighted graphs?
    return abs(a.x - b.x) + abs(a.y - b.y)


def can_go_to(current, neighbor):
    # function to check if there is a path from current to neighbor
    if current.x - neighbor.x == 1 and current.walls[1] is True:
        return False
    elif current.x - neighbor.x == -1 and current.walls[3] is True:
        return False
    if current.y - neighbor.y == -1 and current.walls[2] is True:
        return False
    elif current.y - neighbor.y == 1 and current.walls[0] is True:
        return False

    return True


def bidirectional_dijkstra(start, end, wg, maze):
    start.distance_from_start = 0
    end.distance_from_start = 0

    visited_set = set()

    q = PriorityQueue()
    entry = 0

    q.put((0, entry, start, 'a'))
    entry += 1
    q.put((0, entry, end, 'b'))

    i = 0
    while not q.empty():
        *_, current, came = q.get()
        visited_set.add(current)
        current.color = VISITED_COLOR
        current.came_from = came

        for neighbor in current.neighbors:
            # check if we are solving a maze and if we are check if there is a wall between current node and the neighbor node
            if maze is not None and can_go_to(current, neighbor) is False:
                continue
            # intersection found between current and neighbor
            if current.came_from != neighbor.came_from and None not in (current.came_from, neighbor.came_from):
                a, b = (current, neighbor) if current.came_from == 'a' else (neighbor, current)
                path = find_bi_path(a, b)
                reconstruct_path(path, start, end, wg)
                return

            temp_distance = current.distance_from_start + current.weight
            if temp_distance < neighbor.distance_from_start and neighbor.obstacle is False:
                neighbor.parent = current
                neighbor.distance_from_start = temp_distance
                entry += 1

                q.put((temp_distance, entry, neighbor, came))

        # speed up the visualization otherwise it looks choppy
        i += 1
        if i == 2:
            redraw_window(start, end, wg)
            i = 0


def astar_dijkstra(start, end, maze, wg, dijkstra=False):
    start.distance_from_start = 0
    visited_set = set()

    entry = 0
    queue = PriorityQueue()
    queue.put((distance(start, end), entry, start))

    while not queue.empty():
        current = queue.get()[2]

        current.color = VISITED_COLOR
        visited_set.add(current)

        if current == end:
            path = find_path(end)
            reconstruct_path(path, start, end, wg)
            break

        for neighbor in current.neighbors:
            # check if we are solving a maze and if we are check if there is a wall between current node and the neighbor node
            if maze is not None and can_go_to(current, neighbor) is False:
                continue

            temp_distance = current.distance_from_start + current.weight
            if temp_distance < neighbor.distance_from_start and neighbor.obstacle is False and neighbor not in visited_set:
                neighbor.parent = current
                neighbor.distance_from_start = temp_distance

                if dijkstra is False:
                    # A* alg uses a heuristic function - distance() to calculate the distance from the current position until the end and adds it to the f score
                    neighbor.distance_to_end = distance(neighbor, end)
                    f_score = neighbor.distance_to_end + neighbor.distance_from_start
                else:
                    # dijkstra alg uses just the g_score or the distance from the current position to the start point
                    f_score = neighbor.distance_from_start

                entry += 1
                queue.put((f_score, entry, neighbor))

        redraw_window(start, end, wg)


#### END OF PATHFINDING ALGORITHMS ###


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


def start_alg(alg, start, end, maze, wg):
    if alg == 'd':
        astar_dijkstra(start, end, maze, wg, dijkstra=True)
    elif alg == 'a*':
        astar_dijkstra(start, end, maze, wg, dijkstra=False)
    elif alg == 'bi_d':
        bidirectional_dijkstra(start, end, wg, maze)


def start_maze(alg, start, end, mg):
    if alg == 'r_bt':
        recursive_backtracking(start, end, mg)
    elif alg == 'el':
        eller_algorithm(start, end, mg)
    elif alg == 'kr':
        kruskal_algorithm(start, end, mg)
    elif alg == 'prim':
        prim_algorithm(start, end, mg)


def update_weights(start, end):
    for row in board:
        for node in row:
            if node.weight > 1 and node not in (start, end):
                number = num_font.render(str(node.weight), True, BLACK)
                WIN.blit(number, (node.x * c_width + c_width // 2.5, node.y * c_height + 2))


def update_tiles(start, end):
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


def redraw_window(s, e, wg, alg_running=True):
    global fps

    WIN.fill(WHITE)
    update_tiles(s, e)
    if wg is True:
        update_weights(s, e)
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
    global board

    board = board_setup()
    start = board[0][0]
    end = board[cells - 1][cells - 1]

    if maze is not None:
        start_maze(maze, start, end, mg)
        reset_nodes()

    if wg is not False:
        set_random_weights()

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
        redraw_window(start, end, wg, alg_running=False)

        if solve is True:
            start_alg(alg, start, end, maze, wg)
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
                    reset_nodes()
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


#### MAIN MENU CODE ####


def blit_text(hovered, maze, pf, e_maze, e_pf, mg=False, wg=False):
    # blit the main text in the menu
    main_text = big_font.render('Pathfinding Algorithms Visualization', True, BLACK)
    main_text_shadow = big_font.render('Pathfinding Algorithms Visualization', True, GRAY)
    author = small_font.render('by Viktor Stefanov', True, BLACK)

    menu_surface.blit(main_text_shadow, (168, 53))
    menu_surface.blit(main_text, (165, 50))
    menu_surface.blit(author, (1050, 140))

    # legend box
    pygame.draw.rect(menu_surface, BLACK, (1270, 310, 350, 475), 4)
    # legend
    obstacle = small_font.render(' - obstacle cell', True, BLACK)
    start = small_font.render(' - start cell', True, BLACK)
    end = small_font.render(' - end cell', True, BLACK)
    visited = small_font.render(' - visited cell', True, BLACK)
    path = small_font.render(' - path cell', True, BLACK)
    num = small_font.render(' - cell\'s weight', True, BLACK)

    for idx, img in enumerate((start_img, end_img, obstacle_img, visited_img, path_img, number_img)):
        menu_surface.blit(img, (1290, 330 + idx * 75))

    for idx, text in enumerate((start, end, obstacle, visited, path, num)):
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

    return (d, bi_d, a, r_bt, el, kr, prim, mb, wgr)


def main_menu():
    pf_algs = ['d', 'bi_d', 'a*']
    maze_algs = ['r_bt', 'el', 'kr', 'prim']
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
                    pf_alg = pf_algs[pf]
                    maze_alg = maze_algs[maze] if maze is not None else None
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


#### MAIN MENU CODE ENDS ####


def main():
    alg, maze, mg, wg = main_menu()
    run_algorithm(alg, maze, mg, wg)


if __name__ == '__main__':
    main()