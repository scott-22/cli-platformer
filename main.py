import time
import sys
import os
import select

# tty and termios only work on Unix systems
import tty
import termios

HEIGHT = 12
WIDTH = 50

display = [[" " for j in range(WIDTH)] for i in range(HEIGHT)]
r = HEIGHT-1
c = 5
display[r][c] = ")"
display[r][c-1] = "("

def render():
    for i in display: print("".join(i))

def shift():
    for i in display:
        i.pop(0)
        i.append("a")
    display[r][c-2] = " "
    display[r][c] = ")"
    display[r][c-1] = "("

def isinput():
    return select.select([sys.stdin], [], [], 0)[0] # returns stdin if input, empty list otherwise

if __name__ == "__main__":
    tty.setcbreak(sys.stdin.fileno())
    while True:
        time.sleep(0.02)
        os.system('clear')
        render()
        shift()
        if isinput():
            ch = sys.stdin.read(1)
            print(ch)
            break
