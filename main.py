''' REQUIRED FEATURES LIST (TODO)
1. The use of images                                                     [x]
2. The use of shapes                                                     [x]
3. The use of text                                                       [x]
4. A scoring mechanism                                                   [x]
5. A leaderboard presented at appropriate places in the game             [x]
  - With player initials                                                 [x]
  - Persistent between closing + opening                                 [x]
6. Movement of objects                                                   [x]
7. User can move an object                                               [x]
8. Collision detection                                                   [x]
9. Pause and unpause the game                                            [x]
10. Customizeable controls                                               [x]
11. Special cheat codes (like konami code??)                             [x]
12. save/load features                                                   [x]
13. a 'boss key' (hide the game so it looks like the user is doing work) [x]
'''

import dataclasses as dc
import tkinter as tk
import tkinter.font as tkfont
from typing import Callable

import time
import math

import menu
import gameplay as gp
import keybinds as kb
import leaderboard as lb
import options as opt
import gameover as go
import level as lv
import level_end as le
from gamestate import GameState
from utils import *


# i love oop!
class Game:
    win: tk.Tk
    cv: tk.Canvas

    t: float
    state: GameState
    state_fns: {GameState: Callable}

    menu: menu.Menu
    gameplay: gp.GamePlay
    leaderboard: lb.LeaderBoard
    options: opt.Options
    gameover: go.GameOver
    level: lv.Level

    def __init__(self):
        self.win = tk.Tk()
        self.win.title(GAME_TITLE)
        self.win.geometry(str(WIDTH) + "x" + str(HEIGHT))

        self.cv = tk.Canvas(width=WIDTH, height=HEIGHT, background=BG_COLOR)
        self.cv.pack()

        self.keybinds = kb.KeyBinds()

        self.level = lv.Level(1)
        
        self.leaderboard = lb.LeaderBoard()
        self.menu = menu.Menu(self.leaderboard, self)
        self.gameplay = gp.GamePlay(self.keybinds, self.leaderboard, self.level)
        self.options = opt.Options(self.keybinds)
        self.gameover = go.GameOver(self.leaderboard)
        self.level_end = le.LevelEnd(self.leaderboard)

        self.state_fns = {
            GameState.START_MENU: self.menu.start,
            GameState.MENU: self.menu.loop,
            GameState.QUIT: lambda x, y: self.win.destroy(),
            GameState.START_GAMEPLAY: self.gameplay.start,
            GameState.GAMEPLAY: self.gameplay.loop,
            GameState.START_OPTIONS: self.options.start,
            GameState.OPTIONS: self.options.loop,
            GameState.START_GAMEOVER: lambda win, cv: self.gameover.start(win, cv, self.gameplay),
            GameState.GAMEOVER: self.gameover.loop,
            GameState.START_LEVEL_END: lambda w, c: self.level_end.start(w, c, self.gameplay),
            GameState.LEVEL_END: self.level_end.loop
        }
        
        self.t = 0
        
    def start(self):
        self.state = GameState.START_MENU
        self.main_loop()
        self.win.mainloop()

    def main_loop(self):        
        self.t += FIXED_DT
        # this is a good line of code!
        self.state = self.state_fns[self.state](self.win, self.cv)
        self.win.after(int(FIXED_DT * 1000), self.main_loop)
        
        

if __name__ == "__main__":
    game = Game()
    game.start()
