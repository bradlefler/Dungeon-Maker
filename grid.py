"""
 Pygame code adapted from: https://www.pygame.org/wiki/GettingStarted

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
from copy import deepcopy
import random
import math
import pygame
import monster_hunter
import sys

recurse = 0
grid_size_y = 55
grid_size_x = 55
room_amount = 12
min_room_size_x = 5
min_room_size_y = 5
max_room_size_x = 9
max_room_size_y = 9
buffer_size = 2
grid = []
rooms = []
room_id = 0
boss_room = 0
entrance_room = 0
hall_id_no = 0
hall_ids = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
halls = {}
neighbors = []

#for Pygame
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WIDTH = 10
HEIGHT = WIDTH
MARGIN = 3

def init_grid():
    for i in range(grid_size_y):
        temp = []
        for j in range(grid_size_x):
            temp.append("_")
        grid.append(temp)

def add_room():
    global room_id
    add_hall_neighbor(hall_ids[room_id], str(room_id))
    length = random.randint(min_room_size_y, max_room_size_y)
    width = random.randint(min_room_size_x, max_room_size_x)
    if length%2 == 0:
        length = length + 1
    if width%2 == 0:
        width = width + 1
    x = random.randint(2, grid_size_x - length - 1)
    y = random.randint(2, grid_size_y - width - 1)
    while grid[y][x] != "_" or grid[y + width][x + length] != "_" or grid[y + width][x] != "_" or grid[y][x + length] != "_" or grid[y + int(width/2)][x + int(length/2)] != "_":
        x = random.randint(2, grid_size_x - length - 1)
        y = random.randint(2, grid_size_y - width - 1)
    temp = [y + math.floor(width/2), x + math.floor(length/2), length, width]
    rooms.append(temp)
    for i in range(length):
        for j in range(width):
            grid[y + j][x + i] = str(room_id)
    buff_x = x - buffer_size
    buff_y = y - buffer_size
    buff_length = length + buffer_size*2
    buff_width = width + buffer_size*2
    for i in range(buff_length):
        for j in range(buff_width):
            if buff_y + j < grid_size_y and buff_x + i < grid_size_x and buff_y + j > -1 and buff_x + i > -1:
                if(grid[buff_y + j][buff_x + i] == "_"):
                    grid[buff_y + j][buff_x + i] = "/"
    grid[y + math.floor(width/2)][x + math.floor(length/2)] = hall_ids[room_id]
    room_id = room_id + 1



def print_grid():
    for i in range(grid_size_y):
        temp = ""
        for j in range(grid_size_x):
            if grid[i][j] == "_" or grid[i][j] == "/":
                temp = temp + " "
            else:
                temp = temp + "O"
        print(temp)

def print_grid_alt():
    for i in range(grid_size_y):
        temp = ""
        for j in range(grid_size_x):
            temp = temp + grid[i][j]
        print(temp)

def add_hall_neighbor(hall_id, room_id):
    if hall_id in halls.keys():
        if not_exist_in_vector(halls[hall_id], room_id):
            halls[hall_id].append(room_id)
    else:
        temp = []
        temp.append(room_id)
        halls[hall_id] = temp

def not_exist_in_vector(list, value):
    found = True
    for i in range(len(list)):
        if list[i] == value:
            found = False
            break
    return found

def exchange_neighbors(hall_id, hall_id2):
    temp1 = halls[hall_id]
    temp2 = halls[hall_id2]
    for i in range(len(temp1)):
        if not_exist_in_vector(halls[hall_id2], temp1[i]):
            halls[hall_id2].append(temp1[i])
    for i in range(len(temp2)):
        if not_exist_in_vector(halls[hall_id], temp2[i]):
            halls[hall_id].append(temp2[i])

def add_hall(room1, room2, start_room):
    y1 = room1[0]
    y2 = room2[0]
    x1 = room1[1]
    x2 = room2[1]
    done = False
    if x1 != x2:
        incx = 1
        distance = x2 - x1
        if x1 > x2:
            incx = -1
            distance = x1 - x2
        for i in range(distance):
            x1 = x1 + incx
            if grid[y1][x1].isdigit():
                add_hall_neighbor(hall_ids[int(start_room)], grid[y1][x1])
            if grid[y1][x1].isalpha():
                exchange_neighbors(hall_ids[int(start_room)], grid[y1][x1])
                done = True
                break
            elif grid[y1+1][x1].isalpha():
                done = True
                grid[y1][x1] = hall_ids[int(start_room)]
                exchange_neighbors(hall_ids[int(start_room)], grid[y1+1][x1])
                break
            elif grid[y1-1][x1].isalpha():
                done = True
                grid[y1][x1] = hall_ids[int(start_room)]
                exchange_neighbors(hall_ids[int(start_room)], grid[y1-1][x1])
                break
            elif grid[y1+2][x1].isalpha():
                grid[y1][x1] = hall_ids[int(start_room)]
                grid[y1+1][x1] = hall_ids[int(start_room)]
                exchange_neighbors(hall_ids[int(start_room)], grid[y1+2][x1])
                done = True
                break
            elif grid[y1-2][x1].isalpha():
                grid[y1][x1] = hall_ids[int(start_room)]
                grid[y1-1][x1] = hall_ids[int(start_room)]
                exchange_neighbors(hall_ids[int(start_room)], grid[y1-2][x1])
                done = True
                break
            elif grid[y1+3][x1].isalpha():
                grid[y1][x1] = hall_ids[int(start_room)]
                grid[y1+1][x1] = hall_ids[int(start_room)]
                grid[y1+2][x1] = hall_ids[int(start_room)]
                exchange_neighbors(hall_ids[int(start_room)], grid[y1+3][x1])
                done = True
                break
            elif grid[y1-3][x1].isalpha():
                grid[y1][x1] = hall_ids[int(start_room)]
                grid[y1-1][x1] = hall_ids[int(start_room)]
                grid[y1-2][x1] = hall_ids[int(start_room)]
                exchange_neighbors(hall_ids[int(start_room)], grid[y1-3][x1])
                done = True
                break
            else:
                grid[y1][x1] = hall_ids[int(start_room)]
    if y1 != y2 and done == False:
        incy = 1
        distance = y2 - y1
        if y1 > y2:
            incy = -1
            distance = y1 - y2
        for i in range(distance):
            y1 = y1 + incy
            if grid[y1][x1].isdigit():
                add_hall_neighbor(hall_ids[int(start_room)], grid[y1][x1])
            if grid[y1][x1].isalpha():
                exchange_neighbors(hall_ids[int(start_room)], grid[y1][x1])
                done = True
                break
            elif grid[y1][x1 + 1].isalpha():
                done = True
                grid[y1][x1] = hall_ids[int(start_room)]
                exchange_neighbors(hall_ids[int(start_room)], grid[y1][x1 + 1])
                break
            elif grid[y1][x1 - 1].isalpha():
                done = True
                grid[y1][x1] = hall_ids[int(start_room)]
                exchange_neighbors(hall_ids[int(start_room)], grid[y1][x1 - 1])
                break
            elif grid[y1][x1 + 2].isalpha():
                grid[y1][x1] = hall_ids[int(start_room)]
                grid[y1][x1 + 1] = hall_ids[int(start_room)]
                exchange_neighbors(hall_ids[int(start_room)], grid[y1][x1 + 2])
                done = True
                break
            elif grid[y1][x1 - 2].isalpha():
                grid[y1][x1] = hall_ids[int(start_room)]
                grid[y1][x1 - 1] = hall_ids[int(start_room)]
                exchange_neighbors(hall_ids[int(start_room)], grid[y1][x1 - 2])
                done = True
                break
            elif grid[y1][x1 + 3].isalpha():
                grid[y1][x1] = hall_ids[int(start_room)]
                grid[y1][x1 + 1] = hall_ids[int(start_room)]
                grid[y1][x1 + 2] = hall_ids[int(start_room)]
                exchange_neighbors(hall_ids[int(start_room)], grid[y1][x1 + 3])
                done = True
                break
            elif grid[y1][x1 - 3].isalpha():
                grid[y1][x1] = hall_ids[int(start_room)]
                grid[y1][x1 - 1] = hall_ids[int(start_room)]
                grid[y1][x1 - 2] = hall_ids[int(start_room)]
                exchange_neighbors(hall_ids[int(start_room)], grid[y1][x1 - 3])
                done = True
                break
            else:
                grid[y1][x1] = hall_ids[int(start_room)]

def add_hall_no_interrupts(room1, room2, start_room):
    y1 = room1[0]
    y2 = room2[0]
    x1 = room1[1]
    x2 = room2[1]
    if x1 != x2:
        incx = 1
        distance = x2 - x1
        if x1 > x2:
            incx = -1
            distance = x1 - x2
        for i in range(distance):
            x1 = x1 + incx
            grid[y1][x1] = hall_ids[int(start_room)]
    if y1 != y2:
        incy = 1
        distance = y2 - y1
        if y1 > y2:
            incy = -1
            distance = y1 - y2
        for i in range(distance):
            y1 = y1 + incy
            grid[y1][x1] = hall_ids[int(start_room)]

def build_neighbor_list():
    for i in range(room_amount):
        temp = []
        for j in range(room_amount):
            temp.append(0) #0 means not a neighbor
        neighbors.append(temp)
    for key in halls:
        temp = halls[key]
        for i in range(len(temp)):
            for j in range(len(temp)):
                neighbors[int(temp[i])][int(temp[j])] = 1
    for i in range(len(neighbors)):
        for j in range(len(neighbors[i])):
            cur = neighbors[i][j]
            if cur == 1:
                temp = neighbors[j]
                for k in range(len(temp)):
                    if temp[k] == 1:
                        neighbors[i][k] = 1

def check_distance(room1, room2):
    y1 = room1[0]
    y2 = room2[0]
    x1 = room1[1]
    x2 = room2[1]
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def check_connectivity():
    groups = []
    equal = True
    for i in range(len(neighbors) - 1):
        a = neighbors[i]
        b = neighbors[i + 1]
        if a != b:
            temp_a = []
            temp_b = []
            for j in range(len(a)):
                if a[j] == 1:
                    temp_a.append(j)
                if b[j] == 1:
                    temp_b.append(j)
            found_a = False
            found_b = False
            for k in range(len(groups)):
                if groups[k] == temp_a:
                    found_a = True
                if groups[k] == temp_b:
                    found_b = True
            if found_a == False:
                groups.append(temp_a)
            if found_b == False:
                groups.append(temp_b)
            equal = False
    if equal == True or len(groups) < 2:
        return
    for i in range(len(groups)-1):
        vec_a = groups[i]
        vec_b = groups[i+1]
        shortest = 1000
        a = -1
        b = -1
        for j in range(len(vec_a)):
            for k in range(len(vec_b)):
                room1 = rooms[vec_a[j]]
                room2 = rooms[vec_b[k]]
                d = check_distance(room1, room2)
                if d < shortest:
                    shortest = d
                    a = vec_a[j]
                    b = vec_b[k]
        add_hall_no_interrupts(rooms[a], rooms[b], a)

def py_game(screen, thresh_list, enc_list):
    global boss_room
    global entrance_room
    done = False
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
        # Set the screen background
        screen.fill(BLACK)
        # Draw the grid
        for row in range(grid_size_y):
            for column in range(grid_size_x):
                color = BLACK
                if grid[row][column] != "/" and grid[row][column] != "_":
                    color = WHITE
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        # Limit to 60 frames per second
        #clock.tick(60)
        for i in range(len(rooms)):
            y = rooms[i][0]
            x = rooms[i][1]
            pos_y = (y * HEIGHT) + ((y + 1) * MARGIN)
            pos_x = (x * WIDTH) + ((x + 1) * MARGIN)
            font = pygame.font.SysFont(None, 24)
            img = font.render(str(i), True, RED)
            screen.blit(img, (pos_x, pos_y))
        w, h = pygame.display.get_surface().get_size()

        text_space = 40
        exp_text_y = h-25
        text = "Easy: " + str(thresh_list[0])
        text_easy = font.render(text, True, WHITE)
        ez_x = 10
        screen.blit(text_easy, (10, exp_text_y))

        text = "Medium: " + str(thresh_list[1])
        text_med = font.render(text, True, WHITE)
        med_x = ez_x + text_easy.get_width() + text_space
        screen.blit(text_med, (med_x, exp_text_y))

        text = "Hard: " + str(thresh_list[2])
        text_hard = font.render(text, True, WHITE)
        hard_x = med_x + text_med.get_width() + text_space
        screen.blit(text_hard, (hard_x, exp_text_y))

        text = "Deadly: " + str(thresh_list[3])
        text_ded = font.render(text, True, WHITE)
        ded_x = hard_x + text_hard.get_width() + text_space
        screen.blit(text_ded, (ded_x, exp_text_y))

        text = "Daily Budget: " + str(thresh_list[4])
        text_bud = font.render(text, True, WHITE)
        bud_x = ded_x + text_ded.get_width() + text_space
        screen.blit(text_bud, (bud_x, exp_text_y))

        #enc_list_text = []
        enc_x = w-340
        enc_space = 8
        enc_y = 25
        for i in range(len(enc_list)):
            name = enc_list[i][0]
            text = ""
            if name != "Puzzle" and name != "Trap":
                text = str(i) + ": " + enc_list[i][3] + " " + name
                if int(enc_list[i][3]) > 1:
                    text = text + "s"
            elif name == "Puzzle":
                text = str(i) + ": " + "Puzzle " + enc_list[i][2]
            elif name == "Trap":
                text = str(i) + ": " + enc_list[i][1] + " " + enc_list[i][2] + " " + enc_list[i][3]
            if i == entrance_room:
                text = text + " (Entrance)"
            if i == boss_room:
                text = text + " (Boss)"
            temp_text_box = font.render(text, True, WHITE)
            screen.blit(temp_text_box, (enc_x, enc_y))
            enc_y = enc_y + enc_space + temp_text_box.get_height()


        pygame.display.flip() #display to screen

def save(name, screen):
    pygame.image.save(screen, "saves/"+name)

def find_important_rooms():
    global entrance_room
    global boss_room
    min = -1
    min_total = 1000
    max = -1
    max_total = -1000
    for i in range(len(rooms)):
        y = rooms[i][0]
        x = rooms[i][1]
        total = y + x
        if total < min_total:
            min_total = total
            min = i
        if total > max_total:
            max_total = total
            max = i
    entrance_room = min
    boss_room = max

def create_entrance():
    y = rooms[entrance_room][0]
    x = rooms[entrance_room][1]
    if y < x:
        while y >= 0:
            grid[y][x] = hall_ids[entrance_room]
            y = y - 1
    else:
        while x >= 0:
            grid[y][x] = hall_ids[entrance_room]
            x = x - 1

def create_grid(thresh_list, monster_type):
    init_grid()
    for i in range(room_amount):
        add_room()
    for i in range(1, room_amount):
        temp = rooms[i]
        add_hall(temp, rooms[i - 1], str(i))
    for i in range(room_amount):
        temp = rooms[i]
        room_connect = random.randint(0, room_amount - 1)
        while room_connect == i:
            room_connect = random.randint(0, room_amount - 1)
        add_hall(temp, rooms[room_connect], str(i))
    build_neighbor_list()
    check_connectivity()
    pygame.init()
    find_important_rooms()
    room_encounters = monster_hunter.start(monster_type, thresh_list, room_amount, boss_room)
    create_entrance()
    window_x = (grid_size_x * WIDTH) + ((grid_size_x + 1) * MARGIN) + 340
    window_y = (grid_size_y * HEIGHT) + ((grid_size_y + 1) * MARGIN) + 50
    WINDOW_SIZE = [window_x, window_y]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Array Backed Grid")
    py_game(screen, thresh_list, room_encounters)
    save("screenshot.jpg", screen)
    pygame.quit()
