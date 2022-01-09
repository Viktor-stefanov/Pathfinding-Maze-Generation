from display import *
from globals import *
import random

def recursive_backtracking(start, end, mg, board):
    visited_set = set()
    deadend_stack = []
    current = start
    while len(deadend_stack) != (len(board) * len(board[0])):
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


