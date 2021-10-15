# Maze generation & pathfinding algorithms visualization #

## General Information ##
This is a python implementation of 3 pathfinding algorithms - A*, Dijkstra's and Bidirectional Dijkstra's
and 4 maze generation algorithms - Recursive backtracking, Kruskal's, Prim's, Eller's. The code is written in python
with the pygame library used for visualization. 
* More information about the algorithms - [pathfinding](https://en.wikipedia.org/wiki/Pathfinding), [maze generation](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
* Extensive information about specific maze generation algorithms [here](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)

## Requirements ##
-python3
-pygame

## Setup ##
To run the project locally you'll need to clone or download the repository and run the .exe file.
For people with python3 installed, simply run python3 main.py in the downloaded folder.
* You can download the repo and extract the directiory like that:
  ![](screenshots/help_download.png?raw=true)
  ![](screenshots/help_extract.png?raw=true)
Then simply run the pathfinder.exe file.


## Controls ##
* Choose options from the main menu and press ENTER to start
* S - set the start tile to the mouse position
* E - set the end tile to the mouse position
* Left click - create an obstacle at the mouse position
* Right click - delete the obstacle at the mouse position
* W + left click - mark the cell at the mouse position as selected
* W + left click + number - add a weight to the selected cell
* R - erase the board from all obstacles and paths - restart
* M - main menu
* Esc, q - quit
