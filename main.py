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
JUMPTIME = 8

# keeps track of game time
tick = 0

# display and character
grid = [[" " for j in range(WIDTH)] for i in range(HEIGHT)]
r = HEIGHT-1
c = 12
currentJump = JUMPTIME
slow = 3      # the higher slow is, the slower the game goes
lastSlowDecrease = 0  # last time the game was sped up (in ticks)
lives = 10
message = ""
# player score is defined as floor(tick/5)

def render(grid, message):
    for i in grid: print("".join(i[:-10]))
    print(message)

def setCharacter(nr, nc): # globals because I can't pass by reference
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
    setCharacter(r, c+1)

def isInput():
    return select.select([sys.stdin], [], [], 0)[0] # returns stdin if input, empty list otherwise

def generateObstacle(grid):
    w = random.randint(1, 12)
    h = random.randint(1, 4)
    for i in range(-1, -h-1, -1):
        for j in range(-1, -w-1, -1):
            grid[i][j] = "X"

def crash(speed):
    global r, c, grid, currentJump
    if r == HEIGHT-1 or grid[r+1][c] == "X": return
    for i in range(r+1, r+speed+1):
            if i >= HEIGHT-1:
                setCharacter(HEIGHT-1, c)
                break
            if grid[i+1][c] == "X":
                setCharacter(i, c)
                break
    else:
        setCharacter(r+speed, c)
    currentJump = JUMPTIME

def jump():
    global r, c, grid, currentJump
    if currentJump < JUMPTIME:
        if physics.deltaheight(currentJump) > 0:
            setCharacter(r-physics.deltaheight(currentJump), c)
            currentJump += 1
        else:
            for i in range(-1, physics.deltaheight(currentJump)-1, -1):
                if grid[r-i][c] == "X":
                    setCharacter(r-i-1, c)
                    currentJump = JUMPTIME
                    break
            else:
                setCharacter(r-physics.deltaheight(currentJump), c)
                currentJump += 1
    elif r < HEIGHT-1 and grid[r+1][c] == " ":
        crash(1)

def process(): # time is based on the number of iterations, or "ticks"
    global tick, r, c, grid, currentJump, slow, message
    
    if tick % 2 == 0:
        jump()
    
    if tick % 15*(slow+1) == 0:
        generateObstacle(grid)

    if grid[r][c+1] == "X": return False
    
    if tick % slow == 0:
        shift(grid)
    
    message = "Lives: " + str(lives) + "\nScore: " + str(int(tick/5))
    render(grid, message)
    return True

if __name__ == "__main__":
    tty.setcbreak(sys.stdin.fileno())
    setCharacter(r, c)
    print(
        "\n********************",
        "This is a platforming game. Jump on top or over the obstacles.",
        "If you hit an obstacle, you will lose a life. Lose all 10 and the game is over!",
        "You score and lives are shown at the bottom of the screen.",
        "Press space to jump, enter to dash back to the ground, or any other key to quit.",
        "Press any key to begin!",
        "********************\n",
        sep="\n"
    )

    while not isInput():
        pass

    while True:
        tick += 1     
        os.system('clear')

        if tick - lastSlowDecrease >= 1200 and slow > 1:
            slow -= 1
            lastSlowDecrease = tick

        if not process():
            lives -= 1
            if lives == 0:
                os.system('clear')
                print("Game over! Your score: " + str(int(tick/5)))
                break
            i = r
            while grid[i][c+1] != " ": i -= 1
            setCharacter(i-2, c)

        if isInput():
            ch = sys.stdin.read(1)
            if ch == " ": 
                if currentJump == JUMPTIME: currentJump = 0
            elif ch == "\n":
                crash(5)
            else: break

        time.sleep(0.02)
