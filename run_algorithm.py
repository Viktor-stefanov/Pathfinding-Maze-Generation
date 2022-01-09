from algorithms.pathfinding_algorithms import *
from algorithms.mazegen_algorithms import *
from main_menu import main_menu 
from display import *
from node import *

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

def start_mazegen(alg, start, end, mg, board):
    if alg == 'r_bt':
        recursive_backtracking(start, end, mg, board)
    elif alg == 'el':
        eller_algorithm(start, end, mg, board)
    elif alg == 'kr':
        kruskal_algorithm(start, end, mg, board)
    elif alg == 'prim':
        prim_algorithm(start, end, mg, board)

def run_algorithm(alg, maze, mg, wg):
    board = board_setup()
    start = board[0][0]
    end = board[cells - 1][cells - 1]

    if maze is not None:
        start_mazegen(maze, start, end, mg, board)
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
            if event.type == pygame.QUIT:
                sys.exit()
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
                elif event.key == pygame.K_m:        
                    main_menu()
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


