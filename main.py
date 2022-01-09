from algorithms.pathfinding_algorithms import *
from algorithms.mazegen_algorithms import *
from run_algorithm import *
from main_menu import *
from display import *
from globals import *
from node import *

if __name__ == "__main__":
    pathfinding_alg, maze_generation_alg, maze_generation, weighted_graph = main_menu()
    run_algorithm(pathfinding_alg, maze_generation_alg, maze_generation, weighted_graph)

