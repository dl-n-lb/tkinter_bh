import tkinter as tk
import tkinter.font as tkfont
from gamestate import GameState
from leaderboard import LeaderBoard
from menu import MenuButton
from utils import *

class LevelEnd:
    score: int
    lb: LeaderBoard
    fnt: tkfont.Font
    fnt_s: tkfont.Font
    ttl: int
    score: int
    score_widget: int

    def __init__(self, lb):
        self.lb = lb
    
    def start(self, win, cv, gameplay):
        win.unbind("<Escape>")
        win.unbind("<Button-1>")
        win.unbind("<KeyPress>")
        win.unbind("<KeyRelease>")
        cv.delete("all")

        self.gp = gameplay

        self.score = gameplay.score
        print(self.score)
        
        self.fnt = tkfont.Font(family='Helvetica', size=24, weight='bold')
        self.fnt_s = tkfont.Font(family='Helvetica', size=18)

        w = cv.winfo_width()
        h = cv.winfo_height()
        
        self.ttl = cv.create_text(w/2, h/2, text="LEVEL CLEAR", font=self.fnt, fill="white")
        self.score_widget = cv.create_text(w/2, h/2+50, text="Current Score: " + str(self.score),
                                    font=self.fnt_s, fill="white")

        BTN_WIDTH = WIDTH/5
        BTN_HEIGHT = HEIGHT/20
        btn_pad = BTN_WIDTH/10

        
        cont_btn = MenuButton(cv, Rect(btn_pad, HEIGHT-3*BTN_HEIGHT, BTN_WIDTH, BTN_HEIGHT),
                              btn_pad, "continue", self.cont_act, self.fnt_s)
        save_btn = MenuButton(cv, Rect(btn_pad, HEIGHT-2*BTN_HEIGHT, BTN_WIDTH, BTN_HEIGHT), btn_pad, "save", self.save_act, self.fnt_s)

        self.btns = [cont_btn, save_btn]
        self.submitted = False
        self.ns = GameState.LEVEL_END
        
        win.bind("<Button-1>", self.mouse_bind)
        return self.ns

    def mouse_bind(self, ev):
        for b in self.btns:
            if b.active:
                b.call()
    
    def cont_act(self):
        self.gp.level.diff += 1
        self.gp.p_hp = self.gp.p.hp
        self.ns = GameState.START_GAMEPLAY

    def save_act(self):
        with open("save", "w") as f:
            # got to load the next level after the one which was cleared
            f.write(str(self.score) + " " + str(self.gp.level.diff + 1) + " " + str(self.gp.p.hp))
        self.ns = GameState.START_MENU

    def loop(self, win, cv):
        mx = win.winfo_pointerx() - win.winfo_rootx()
        my = win.winfo_pointery() - win.winfo_rooty()

        for btn in self.btns:
            btn.check_hovered(cv, mx, my)

        return self.ns
