import tkinter as tk
import tkinter.font as tkfont
import dataclasses as dc
from typing import Callable

from utils import *
from gamestate import GameState
from leaderboard import LeaderBoard

class MenuButton:
    dims: Rect
    active: bool
    cv_id: int
    cev: Callable
    
    def __init__(self, cv: tk.Canvas, dims: Rect, txt_pad: float, text: str,
                 click_ev: Callable, font: tkfont.Font):
        self.dims = dims
        self.active = False
        self.cv_id = cv.create_text(dims.x+txt_pad, dims.y+dims.h/2,
                                    font=font, text=text, anchor="w",
                                    fill="white")
        self.cev = click_ev

    def check_hovered(self, cv: tk.Canvas, x: int, y: int):
        # NOTE: If active set the text to black
        if self.active:
            cv.itemconfig(self.cv_id, fill="white")
            self.active = False
        if x - self.dims.x < self.dims.w and abs(y - self.dims.y) < self.dims.h and self.dims.x < x and self.dims.y < y:
            cv.itemconfig(self.cv_id, fill="black")
            self.active = True

    def call(self):
        self.cev()

class Menu:
    next_state: GameState
    lb: LeaderBoard

    def __init__(self, lb, game):
        self.game = game
        self.lb = lb
        pass

    def start(self, win, cv):
        win.unbind("<Escape>")
        win.unbind("<Button-1>")
        win.unbind("<KeyPress>")
        win.unbind("<KeyRelease>")
        cv.delete("all")

        win.bind("<Escape>", lambda x: win.destroy())
        win.bind("<Button-1>", self.mouse_bind)

        # TODO: hardcoded
        self.lb.draw(cv, Rect(1080, 200, 200, 1000))
            
        self.next_state = GameState.MENU
        
        fnt_title  = tkfont.Font(family='Helvetica', size=36, weight='bold')
        fnt_button = tkfont.Font(family='Helvetica', size=18)

        cv.create_text(WIDTH/2, HEIGHT/2, text=GAME_TITLE, fill="white",
                            font=fnt_title)

        # button dimensions
        btn_w = WIDTH / 5
        btn_h = HEIGHT / 20
        btn_pad = btn_w / 10

        btn_y = HEIGHT/2 + 50

        # create buttons
        play_btn = MenuButton(cv, Rect(0, btn_y + 0 * btn_h, btn_w, btn_h),
                              btn_pad, "play", self.play_btn_act, fnt_button)
        load_btn = MenuButton(cv, Rect(0, btn_y + 1 * btn_h, btn_w, btn_h),
                              btn_pad, "load", self.load_btn_act, fnt_button)
        opts_btn = MenuButton(cv, Rect(0, btn_y + 2 * btn_h, btn_w, btn_h),
                              btn_pad, "options", self.opts_btn_act, fnt_button)
        quit_btn = MenuButton(cv, Rect(0, btn_y + 3 * btn_h, btn_w, btn_h),
                              btn_pad, "quit", self.quit_btn_act, fnt_button)
        
        self.menu_buttons = [play_btn, load_btn, opts_btn, quit_btn]
        return self.next_state

    # a bind for clicking buttons
    def mouse_bind(self, ev):
        for b in self.menu_buttons:
            if b.active:
                b.call()
    
    def play_btn_act(self):
        self.next_state = GameState.START_GAMEPLAY

    def load_btn_act(self):
        # read in save data
        with open("save", "r") as f:
            data = f.readlines()[0].strip().split(" ")
            score = int(data[0])
            lv = int(data[1])
            lives = int(data[2])
            self.game.level.diff = lv
            self.game.gameplay.score = score
            self.game.gameplay.p_hp = lives
        self.next_state = GameState.START_GAMEPLAY

    def opts_btn_act(self):
        self.next_state = GameState.START_OPTIONS

    def quit_btn_act(self):
        self.next_state = GameState.QUIT

    def loop(self, win, cv):
        mx = win.winfo_pointerx() - win.winfo_rootx()
        my = win.winfo_pointery() - win.winfo_rooty()
        for btn in self.menu_buttons:
            btn.check_hovered(cv, mx, my)

        return self.next_state
        

