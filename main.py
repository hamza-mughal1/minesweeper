import pygame
import random
import time

pygame.init()

def create_bombs(grid,grid_dimension,ignore_cell = []):
    i = 0
    while i < no_bomb:
        box = random.randint(0,(grid_dimension**2)-1)
        if (grid[box] == "-") and (box not in ignore_cell):
            grid[box] = "*"
            i += 1
            
def print_grid(grid_dimension, grid):
    for i in range(0,grid_dimension*grid_dimension,grid_dimension):
        for j in range(i,i+grid_dimension):
            print(grid[j],end= " ")
        print()

def count_neigbors(cell_no,dimension):
    l = []
    if cell_no%dimension != 0: 
        l.append((cell_no-1,"LEFT"))
    if cell_no%dimension != dimension-1:
        l.append((cell_no+1,"RIGHT"))
    if int(cell_no/dimension) != 0:
        l.append((cell_no-dimension,"UP"))
    if int(cell_no/dimension) < dimension-1:
        l.append((cell_no+dimension,"DOWN"))
    
    if (cell_no%dimension != dimension-1) and (int(cell_no/dimension) != 0): 
        l.append(((cell_no-dimension)+1,"UP-RIGHT"))
    if (cell_no%dimension != 0) and (int(cell_no/dimension) != 0):
        l.append(((cell_no-dimension)-1,"UP-LEFT"))
    if (cell_no%dimension != dimension-1) and (int(cell_no/dimension) < dimension-1):
        l.append(((cell_no+dimension)+1,"DOWN-RIGHT"))
    if (cell_no%dimension != 0) and (int(cell_no/dimension) < dimension-1):
        l.append(((cell_no+dimension)-1,"DOWN-LEFT"))
    
    return l

def number_of_neighbor_bombs(grid,grid_dimension):
    
    for k in grid:  
        neighbor_bombs = 0
        for z in count_neigbors(k,grid_dimension):
            if grid[z[0]] == "*":
                neighbor_bombs += 1
        
        if neighbor_bombs > 0 and grid[k] != "*":
            grid[k] = neighbor_bombs

def opening_hint(tiles,grid,tile_no:list):
    main_lis = []
    for t in tile_no:
        l = count_neigbors(t,grid_dimension)
        for i in l:
            if grid[i[0]] != "*" and tiles[i[0]] != "-":
                tiles[i[0]] = "-"
                if grid[i[0]] == "-":
                    main_lis.append(i[0])
    if main_lis:
        main_lis = list(set(main_lis))
        opening_hint(tiles,grid,tile_no=main_lis)

def count_for_win(tiles : dict, no_bombs):
    no_red_tiles = 0
    no_white_tiles = 0
    for _, value in tiles.items():
        if value == "_":
            no_red_tiles += 1
        elif value == "|":
            no_white_tiles += 1
    
    if (no_red_tiles == no_bombs) and (no_white_tiles == 0):
        return 1
    return 0

win_dimension = 900
grid_dimension = 9
no_bomb = 10
text_padding = 20
no_bomb_left = no_bomb
run = True
allowed = True
end_screen = False
wining = False
font = pygame.font.SysFont('Arial', 32)
win = pygame.display.set_mode((win_dimension,win_dimension))
pygame.display.set_caption("MineSweeper")
grid = {key:"-" for key in range(grid_dimension*grid_dimension)}
tiles = {key:"|" for key in range(grid_dimension*grid_dimension)}

create_bombs(grid,grid_dimension)
number_of_neighbor_bombs(grid,grid_dimension)

start = time.time()
while run:
    if count_for_win(tiles, no_bomb):
        end_screen = True
        wining = True

    list_of_tiles = []

    win.fill((0,0,0))

    k = 0
    for j in range(0,win_dimension-1,win_dimension//grid_dimension):
        for i in range(0,win_dimension-1,win_dimension//grid_dimension):
                rect = pygame.Rect(i,j,win_dimension//grid_dimension,win_dimension//grid_dimension)
                tile = pygame.Rect(i,j,win_dimension//grid_dimension,win_dimension//grid_dimension)
                list_of_tiles.append(tile)
                
                if grid[k] != "-" and grid[k] != "*":
                    text = font.render(str(grid[k]),1,(0,255,0))
                    win.blit(text,(i+text_padding,j+text_padding))
                

                color = (255,255,255)
                fill_border = 2

                if grid[k] == "*":
                    font2 = pygame.font.SysFont('Impact', 60)
                    text = font2.render(str(grid[k]),1,(255,0,0))
                    win.blit(text,(i+40,j+30))
                    color = (255,0,0)
                    fill_border = 5
                    
                    
                
            
                pygame.draw.rect(win, color, rect, fill_border)
                if tiles[k] == "|":
                    pygame.draw.rect(win, (255,255,255), tile)
                if tiles[k] == "_":
                     pygame.draw.rect(win, (255,0,0), tile)
                
                k += 1

    if end_screen:
        pygame.display.flip()
        time.sleep(2)
        win.fill((0,0,0))
        font = pygame.font.SysFont('Impact', 70)
        if wining:
            text = font.render("you won!",1,(0,225,0))
            print("total time took : ",time.time()-start)
        else:
            text = font.render("you loss!",1,(255,0,0))
        win.blit(text,((win_dimension//2)-150,(win_dimension//2)-35))
        pygame.display.flip()
        time.sleep(2)
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False   

        if event.type == pygame.MOUSEBUTTONDOWN:
            mos = pygame.mouse.get_pos()
            for pos,i in enumerate(list_of_tiles):
                if i.collidepoint(mos):
                    if allowed:
                        if grid[pos] != "-":
                            grid = {key:"-" for key in range(grid_dimension*grid_dimension)}
                            create_bombs(grid,grid_dimension,ignore_cell=[pos,pos+1,
                                                                          pos-1,
                                                                          pos-grid_dimension,
                                                                          pos+grid_dimension,
                                                                          (pos-grid_dimension)-1,
                                                                          (pos-grid_dimension)+1,
                                                                          (pos+grid_dimension)-1,
                                                                          (pos+grid_dimension)+1])
                            number_of_neighbor_bombs(grid,grid_dimension)
                        opening_hint(tiles,grid,[pos])
                        allowed = False
                    if grid[pos] == "*":
                        print("you failed!")
                        tiles = {key:"-" for key in range(grid_dimension*grid_dimension)}
                        end_screen = True
                    tiles[pos] = "-"
                    print(no_bomb_left)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                mos = pygame.mouse.get_pos()
                for pos,i in enumerate(list_of_tiles):
                    if i.collidepoint(mos):
                        if no_bomb_left > 0 and tiles[pos] == "|":
                            tiles[pos] = "_"
                            no_bomb_left -= 1
            elif event.key == pygame.K_LEFT:
                mos = pygame.mouse.get_pos()
                for pos,i in enumerate(list_of_tiles):
                    if i.collidepoint(mos):
                        if no_bomb_left < 10 and tiles[pos] == "_":
                            tiles[pos] = "|"
                            no_bomb_left += 1


      
    
        

    pygame.display.flip()
        


pygame.quit()