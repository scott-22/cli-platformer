import time
import sys
import os
import random
import select

# tty and termios only work on Unix systems
import tty
import termios

import physics

HEIGHT = 12
WIDTH = 75 # 25 pixels at end is for creating obstacles
JUMPTIME = 6

# keeps track of game time
tick = 0

# display and character
grid = [[" " for j in range(WIDTH)] for i in range(HEIGHT)]
r = HEIGHT-1
c = 12
currentjump = 6
message = "notfalling"

def render(grid):
    for i in grid: print("".join(i[:-10]))
    print(message)

def setcharacter(nr, nc): # globals because I can't pass by reference
    global r, c           # and this project is too small for OOP
    grid[r][c] = " "
    grid[r][c-1] = " "
    grid[nr][nc] = ")"
    grid[nr][nc-1] = "("
    r = nr
    c = nc

def shift(grid):
    global r, c
    for i in grid:
        i.pop(0)
        i.append(" ")
    c -= 1
    setcharacter(r, c+1)

def isinput():
    return select.select([sys.stdin], [], [], 0)[0] # returns stdin if input, empty list otherwise

def generateobstacle(grid):
    w = random.randint(1, 12)
    h = random.randint(1, 4)
    for i in range(-1, -h-1, -1):
        for j in range(-1, -w-1, -1):
            grid[i][j] = "X"

def crash(speed):
    global r, c, grid, currentjump
    if r == HEIGHT-1 or grid[r+1][c] != " ": return
    for i in range(r+1, r+speed+1):
            if i >= HEIGHT-1:
                setcharacter(HEIGHT-1, c)
                break
            if grid[i+1][c] != " ":
                setcharacter(i, c)
                break
    else:
        setcharacter(r+speed, c)
    currentjump = JUMPTIME

def jump():
    global r, c, grid, currentjump
    if currentjump < JUMPTIME:
        if physics.deltaheight(currentjump) > 0:
            setcharacter(r-physics.deltaheight(currentjump), c)
            currentjump += 1
        else:
            for i in range(-1, physics.deltaheight(currentjump)-1, -1):
                if grid[r-i][c] != " ":
                    setcharacter(r-i-1, c)
                    currentjump = JUMPTIME
                    break
            else:
                setcharacter(r-physics.deltaheight(currentjump), c)
                currentjump += 1
    elif r < HEIGHT-1 and grid[r+1][c] == " ":
        crash(1)

def process(): # time is based on the number of iterations, or "ticks"
    global tick, r, c, grid, currentjump, message
    
    jump()
    
    if tick % 15 == 0: #add obstacle every 15 ticks
        generateobstacle(grid)

    if grid[r][c+1] != " ": return False
    
    shift(grid)
    render(grid)
    return True

if __name__ == "__main__":
    tty.setcbreak(sys.stdin.fileno())
    setcharacter(r, c)

    while True:
        tick += 1        
        os.system('clear')

        process()

        if isinput():
            ch = sys.stdin.read(1)
            if ch == " ": 
                if currentjump == JUMPTIME: currentjump = 0
            elif ch == "\n":
                crash(3)
            else: break

        time.sleep(0.04)
