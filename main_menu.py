from display import *
from globals import *

def blit_text(hovered, maze, pf, e_maze, e_pf, mg=False, wg=False):
    # blit the header text in the main menu
    menu_surface.blit(main_menu_header_shadow, (168, 53))
    menu_surface.blit(main_menu_header, (165, 50))
    menu_surface.blit(main_menu_author, (1050, 140))

    # draw the legend box and blit the legend images
    pygame.draw.rect(menu_surface, BLACK, (1270, 310, 350, 475), 4)
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
                elif event.key == pygame.K_RETURN:
                    pf_alg = pathfinding_algs[pf] if pf is not None else None
                    maze_alg = maze_generation_algs[maze] if maze is not None else None
                    if pf_alg is not None:
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
