import pygame.image
import pygame.font
import os.path
""" in this file are defined all global variables that are going to be used in
    the main application (main.py) """

cells = 40  # change cells variable to increase the number of tiles on the screen

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
START_COLOR = (240, 20, 20)
END_COLOR = (20, 240, 20)
EXPAND_COLOR = (130, 232, 130)
VISITED_COLOR = (179, 249, 255)
PATH_COLOR = (252, 247, 113)
HOVERED = (55, 89, 46)

# load images
obstacle_img = pygame.image.load(os.path.join('img', 'obstacle_color.png'))
start_img = pygame.image.load(os.path.join('img', 'start_color.png'))
end_img = pygame.image.load(os.path.join('img', 'end_color.png'))
visited_img = pygame.image.load(os.path.join('img', 'visited_color.png'))
path_img = pygame.image.load(os.path.join('img', 'path_color.png'))
number_img = pygame.image.load(os.path.join('img', 'number_img.png'))
main_menu_imgs = (obstacle_img, start_img, end_img, visited_img, path_img, number_img)

# load fonts
pygame.font.init()
big_font = pygame.font.SysFont('comicsansms', 80)
med_font = pygame.font.SysFont('comicsansms', 55)
small_font = pygame.font.SysFont('comicsansms', 35)

# create rendered text here to avoid rendering the text every time the text is blit on the screen
main_menu_header = big_font.render('Pathfinding Algorithms Visualization', True, BLACK)
main_menu_header_shadow = big_font.render('Pathfinding Algorithms Visualization', True, GRAY)
main_menu_author = small_font.render('by Viktor Stefanov', True, BLACK)
# rendered text for the legend in the main menu
main_menu_obstacle = small_font.render(' - obstacle cell', True, BLACK)
main_menu_start = small_font.render(' - start cell', True, BLACK)
main_menu_end = small_font.render(' - end cell', True, BLACK)
main_menu_visited = small_font.render(' - visited cell', True, BLACK)
main_menu_path = small_font.render(' - path cell', True, BLACK)
main_menu_num = small_font.render(' - cell\'s weight', True, BLACK)
main_menu_legend_text = (main_menu_obstacle, main_menu_start, main_menu_end, main_menu_visited, main_menu_path, main_menu_num)
