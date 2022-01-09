from globals import cells
import random

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.walls = [True, True, True, True]
        self.weight = 1
        self.distance_from_start = float('inf')
        self.distance_to_end = float('inf')
        self.color = None
        self.parent = None
        self.obstacle = False
        self.expanding = False
        self.came_from = None  # for the bidirectional dijkstra algorithm, for the connection between start and end to be detected

    def reset(self):
        self.distance_from_start = float('inf')
        self.distance_to_end = float('inf')
        self.color = None
        self.parent = None
        self.obstacle = False
        self.expanding = False
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


