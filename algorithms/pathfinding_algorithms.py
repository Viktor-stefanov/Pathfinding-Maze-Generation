from display import *
from globals import *
from queue import PriorityQueue

def reconstruct_path(path, start, end, wg, board):
    for node in path[::-1]:
        node.color = PATH_COLOR
        redraw_window(start, end, board, wg=wg)

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

def a_start_distance(current, start, end):
    g_cost = abs(current.x - start.x) + abs(current.y - start.y)
    h_cost = abs(current.x - end.x) + abs(current.y - end.y)
    return g_cost + h_cost

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

def bidirectional_dijkstra(start, end, wg, maze, board):
    start.distance_from_start = 0
    end.distance_from_start = 0

    visited_set = set()

    q = priorityQueue()
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
                reconstruct_path(path, start, end, wg, board)
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
            redraw_window(start, end, board, wg=wg)
            i = 0

def astar_dijkstra(start, end, maze, wg, board, dijkstra=False):
    start.distance_from_start = 0
    visited_set = set()

    entry = 0
    queue = PriorityQueue()
    queue.put((distance(start, end), entry, start))

    iterations = 0
    while not queue.empty():
        iterations += 1
        current = queue.get()[2]

        current.color = VISITED_COLOR
        visited_set.add(current)

        if current == end:
            path = find_path(end)
            reconstruct_path(path, start, end, wg, board)
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

        redraw_window(start, end, board, wg=wg)
