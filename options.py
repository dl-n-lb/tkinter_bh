import tkinter as tk
import tkinter.font as tkfont
from typing import Callable

from gamestate import *
from menu import MenuButton
from utils import *
from keybinds import KeyBinds

class OptionButton:
    dims: Rect
    act: str
    key: str
    font: tkfont.Font
    label: int
    btn: int
    btn_text: int
    active: bool
        
    def __init__(self, cv, dims, act, key, font):
        self.act = act
        self.key = key
        self.dims = Rect(dims.x+dims.w/2, dims.y, dims.w/2, dims.h)

        self.label = cv.create_text(dims.x+dims.w/2, dims.y+dims.h/2, font=font, text=act,
                                    anchor="e", fill="white")

        d = self.dims
        self.btn = cv.create_rectangle(d.x, d.y, d.x+d.w, d.y+d.h, fill="white")
        self.btn_txt = cv.create_text(d.x+d.w/2, d.y+d.h/2, font=font, text=key, fill="black")
        
        self.active = False

    def check_hovered(self, cv, x, y):
        if self.active:
            cv.itemconfig(self.btn, fill="white")
            self.active = False
        if x - self.dims.x < self.dims.w and abs(y - self.dims.y) < self.dims.h and self.dims.x < x and self.dims.y < y:
            cv.itemconfig(self.btn, fill="grey")
            self.active = True

    def update(self, cv, newKey):
        self.key = newKey
        cv.itemconfig(self.btn_txt, text=newKey)


class Options:
    win: tk.Tk
    cv:  tk.Canvas
    keybinds: KeyBinds
    ns: GameState
    btns: [OptionButton]
    menu_btns: [MenuButton]

    def __init__(self, keybinds):
        self.keybinds = keybinds
        self.btns = []
        self.menu_btns = []
        self.ns = GameState.OPTIONS

    
    def start(self, win, cv):
        self.win = win
        self.cv = cv
        win.unbind("<Escape>")
        win.unbind("<Button-1>")
        win.unbind("<KeyPress>")
        win.unbind("<KeyRelease>")
        cv.delete("all")

        BTN_WIDTH = WIDTH/5
        BTN_HEIGHT = HEIGHT/20
        btn_pad = BTN_WIDTH/10
        
        btn_fnt = tkfont.Font(family='Helvetica', size=18)
        
        quit_btn = MenuButton(cv, Rect(0, HEIGHT-BTN_HEIGHT, BTN_WIDTH, BTN_HEIGHT),
                              btn_pad, "quit", self.quit_act, btn_fnt)
        save_btn = MenuButton(cv, Rect(WIDTH-BTN_WIDTH, HEIGHT-BTN_HEIGHT, BTN_WIDTH, BTN_HEIGHT), btn_pad, "save", self.save_act, btn_fnt)
        self.menu_btns = [quit_btn, save_btn]


        BTN_WIDTH = WIDTH/3
        dims = Rect(WIDTH/2 - BTN_WIDTH/2, 100, BTN_WIDTH, BTN_HEIGHT)
        for kb in self.keybinds.keys:

            self.btns.append(OptionButton(cv, dims, self.keybinds.get(kb), kb,
                                          btn_fnt))
            dims.y += BTN_HEIGHT
    

        win.bind("<Button-1>", self.mouse_bind)
        return self.ns

    def mouse_bind(self, ev):
        for b in self.menu_btns:
            if b.active:
                b.call()
        for b in self.btns:
            if b.active:
                self.active_btn = b
                self.active_btn_act = self.active_btn.act
                self.active_btn_key = self.active_btn.key
                self.active_btn.update(self.cv, "")
                self.win.bind("<KeyPress>", self.record_bind)

    def record_bind(self, e):
        act = self.active_btn_act
        key = self.active_btn_key
        self.keybinds.edit(act, key, e.keysym.lower())
        self.active_btn.update(self.cv, e.keysym.lower())
        self.win.unbind("<KeyPress>")
                
    def quit_act(self):
        self.ns = GameState.START_MENU

    def save_act(self):
        self.keybinds.save()
    
    def loop(self, win, cv):
        mx = win.winfo_pointerx() - win.winfo_rootx()
        my = win.winfo_pointery() - win.winfo_rooty()

        for btn in self.btns:
            btn.check_hovered(cv, mx, my)

        for btn in self.menu_btns:
            btn.check_hovered(cv, mx, my)
            
        return self.ns
