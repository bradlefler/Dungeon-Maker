import math
import random

cr = {
"0": 10,
"1/8": 25,
"1/4": 50,
"1/2": 100,
"1": 200,
"2": 450,
"3": 700,
"4": 1100,
"5": 1800,
"6": 2300,
"7": 2900,
"8": 3900,
"9": 5000,
"10": 5900,
"11": 7200,
"12": 8400,
"13": 10000,
"14": 11500,
"15": 13000,
"16": 15000,
"17": 18000,
"18": 20000,
"19": 22000,
"20": 25000,
"21": 33000,
"22": 41000,
"23": 50000,
"24": 62000,
"25": 75000,
"26": 90000,
"30": 155000
}

def get_trap(exp):
    dc = ""
    damage = ""
    trap_type = ""
    if exp > 6000:
        dc = "DC 15"
        damage = "3d6 damage"
    elif exp <= 6000 and exp >= 2500:
        dc = "DC 12"
        damage = "2d6 damage"
    elif exp < 2500:
        dc = "DC 10"
        damage = "1d8 damage"
    t_num = random.randint(1, 3)
    if t_num == 1:
        trap_type = "Spike trap"
    elif t_num == 2:
        trap_type = "Pit trap"
    elif t_num == 3:
        trap_type = "Swinging blade trap"
    result = ["Trap", trap_type, dc, damage]
    return result

def read_file(mv, file):
    f = open(file, "r")
    for x in f:
        temp = x.split(",")
        mv.append(temp)
    f.close()

def read_file_alt(mv, file):
    f = open(file, "r")
    for x in f:
        temp = x
        mv.append(temp)
    f.close()

def choose(mv, exp, results):
    multiplier = [1.0, 1.0, 1.5, 2.0, 2.0, 2.0, 2.0, 2.5, 2.5]
    for i in range(len(mv)):
        for j in range(8):
            num = 8 - j
            mult = multiplier[num]
            temp = []
            for k in range(len(mv[i])):
                temp.append(mv[i][k])
            total = cr[temp[1]]*num*mult
            if total <= float(exp) and total >= float(exp)*0.90:
                temp.append(str(num))
                temp.append(str(total))
                results.append(temp)
                break

def boss_pick(boss_room, exp, mv, room_contents):
    results_boss = []
    choose(mv, exp, results_boss)
    min = 99999
    mon_num = 0
    for i in range(len(results_boss)):
        num = int(results_boss[i][3])
        if num < min:
            min = num
            mon_num = i
    room_contents[boss_room] = results_boss[mon_num]

def start(monster_type, thresh, rooms, boss_room):
    file = "resources/monster_lists/type_lists/" + monster_type + ".txt"
    file2 = "resources/puzzles.txt"
    pv = [] #puzzle vector
    mv = [] #monster vector
    read_file(mv, file)
    read_file_alt(pv, file2)
    exp = thresh[1]
    monster_room_amount = math.floor(thresh[4]/thresh[1])
    results = []
    choose(mv, exp, results)
    if len(results) == 0:
        sys.exit("Error: No monsters in list. There may be no suitable monsters for the settings you selected. Try again with a different monster type.")
    room_contents = []
    for i in range(rooms):
        enc_num = random.randint(0, len(results) - 1)
        room_contents.append(results[enc_num])
    puzzle_num = rooms - monster_room_amount
    for i in range(puzzle_num - 1):
        room_num = random.randint(0, len(room_contents) - 1)
        puzzle_num = random.randint(0, len(pv) - 1)
        temp_list = []
        temp_list.append("Puzzle")
        temp_list.append(pv[puzzle_num])
        temp_list.append(str(puzzle_num + 1))
        room_contents[room_num] = temp_list
    boss_pick(boss_room, thresh[2], mv, room_contents)
    for i in range(len(room_contents)):
        if room_contents[i][0] == "Puzzle":
            room_contents[i] = get_trap(thresh[1])
            break
    for i in range(len(room_contents)):
        if room_contents[i][0] == "Puzzle":
            print(room_contents[i][1])
    return room_contents
