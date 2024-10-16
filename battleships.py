import keyboard as keyb
from random import randint
import time

def print_board(table, hit, new, pl, colour, use_new):
    if new and use_new:
        print('\033[7F')
    num_tup = ('1', '2', '3', '4', '5')
    print('  ', end='')
    print(*num_tup, end='   ')
    print(*num_tup)
    for i in range(5):
        for k in range(2):
            print(num_tup[i], end=' ')
            for j in range(5):
                if [i, j] == pl:
                    if colour:
                        print('\033[33;5mx', end='\033[0m ')
                    else:
                        print('O', end=' ')
                elif k == 0:
                    print(table[i][j], end=' ')
                else:
                    print(hit[i][j], end=' ')
        print()

def number(message, border):
    num = input(message)
    while not num.isdigit():
        num = input(f'Invalid input\nNot an integer\nTry again\n{message}')
    while int(num) < 8 or int(num) > border:
        num = input(f'Invalid input\nNot in range\nTry again\n{message}')
        while not num.isdigit():
            num = input(f'Invalid input\nNot an integer\nTry again\n{message}')
    return(int(num))

def guess():
    num_set = {'1', '2', '3', '4', '5'}
    guessed = input('xy\n')
    while not len(guessed) == 2:
        guessed = input('Invalid input\nxy\n')
    while not(guessed[0] in num_set or guessed[1] in num_set):
        guessed = input('Invalid input\nxy\n')
        while not len(guessed) == 2:
            guessed = input('Invalid input\nxy\n')
    guessed = [int(guessed[0]) - 1, int(guessed[1]) - 1]
    return(guessed)

def ship_left(table):
    flag = False
    for line in table:
        for simbol in line:
            if simbol == '■':
                flag = True
    return(flag)

def gen_board():
    table = [['□', '□', '□', '□', '□'],
             ['□', '□', '□', '□', '□'],
             ['□', '□', '□', '□', '□'],
             ['□', '□', '□', '□', '□'],
             ['□', '□', '□', '□', '□']]
    for _ in range(8):
        rand_p = [randint(0, 4), randint(0, 4)]
        while table[rand_p[0]][rand_p[1]] == '■':
            rand_p = [randint(0, 4), randint(0, 4)]
        table[rand_p[0]][rand_p[1]] = '■'
    return(table)

def change(table, hit, pvp, guessed):
    temp = str(guessed[1] + 1) + str(guessed[0] + 1)
    if table[guessed[0]][guessed[1]] == '■':
        table[guessed[0]][guessed[1]] = 'x'
        hit[guessed[0]][guessed[1]] = 'x'
        if pvp:
            print(f'Enemy ship destroyed at {temp}!')
        else:
            print(f'Our ship destroyed at {temp}!')
    else:
        table[guessed[0]][guessed[1]] = '*'
        hit[guessed[0]][guessed[1]] = '*'
        print(f'{temp} was a miss')
    return(table, hit)

def cp_input(hit):
    rand_p = [randint(0, 4), randint(0, 4)]
    while hit[rand_p[0]][rand_p[1]] != '_':
        rand_p = [randint(0, 4), randint(0, 4)]
    return(rand_p)

def move(table, pl_hit_arr, start, pl, colour, use_new):
    count = 0
    print_board(table, pl_hit_arr, False, pl, colour, use_new)
    while True:
        temp_key = keyb.read_key(suppress=True)
        if temp_key == 'w':
            pl = [pl[0] - 1, pl [1]]
            if pl[0] < 0:
                pl[0] = 4
            print_board(table, pl_hit_arr, True, pl, colour, use_new)
        elif temp_key == 's':
            pl = [pl[0] + 1, pl [1]]
            if pl[0] > 4:
                pl[0] = 0
            print_board(table, pl_hit_arr, True, pl, colour, use_new)
        elif temp_key == 'a':
            pl = [pl[0], pl [1] - 1]
            if pl[1] < 0:
                pl[1] = 4
            print_board(table, pl_hit_arr, True, pl, colour, use_new)
        elif temp_key == 'd':
            pl = [pl[0], pl [1] + 1]
            if pl[1] > 4:
                pl[1] = 0
            print_board(table, pl_hit_arr, True, pl, colour, use_new)
        elif temp_key == 'space':
            print('\r', end='')
            if start:
                if table[pl[0]][pl[1]] == '□':
                    table[pl[0]][pl[1]] = '■'
                    count += 1
                elif table[pl[0]][pl[1]] == '■':
                    table[pl[0]][pl[1]] = '□'
                    count -= 1
            else:
                time.sleep(0.2)
                return(pl)
        elif count == 8 and temp_key == 'q':
            print('\r\033[2DPress enter to proceed')
            input()
            time.sleep(0.2)
            return(table, pl)
        print('\033[2K', end='')
        time.sleep(0.2)

def main():
    colour = True
    use_new = True
    pl_table_arr = [['□', '□', '□', '□', '□'],
                    ['□', '□', '□', '□', '□'],
                    ['□', '□', '□', '□', '□'],
                    ['□', '□', '□', '□', '□'],
                    ['□', '□', '□', '□', '□']]
    pl_hit_arr = [['_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_']]
    cp_hit_arr = [['_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_']]
    pl_table_arr, pl = move(pl_table_arr, pl_hit_arr, True, [2, 2], colour, use_new)
    cp_table_arr = gen_board()
    tries = number('Number of tries 8 - 50:\n', 50)
    alive_pl = ship_left(pl_table_arr)
    alive_cp = ship_left(cp_table_arr)
    turn = 0
    while alive_pl and alive_cp and tries > 0:
        if turn % 2 == 0:
            print('Your turn')
            print(f'You have {tries} tries left')
            tries -= 1
            pl = move(pl_table_arr, pl_hit_arr, False, pl, colour, use_new)
            cp_table_arr, pl_hit_arr = change(cp_table_arr, pl_hit_arr, True, pl)
            alive_cp = ship_left(cp_table_arr)
        else:
            print('Enemy turn:')
            pl_table_arr, cp_hit_arr = change(pl_table_arr, cp_hit_arr, False, cp_input(cp_hit_arr))
            alive_pl = ship_left(pl_table_arr)
        turn += 1
    if alive_pl and not alive_cp:
        print('You won!')
    else:
        print('You lost')
        print('computer perspective:')
        print_board(cp_table_arr, cp_hit_arr, False, [5, 5], False, False)
    print('\r\033[2DPress enter to end the game')
    input()

if __name__ == '__main__':
    main()
