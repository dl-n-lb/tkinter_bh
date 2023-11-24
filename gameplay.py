import dataclasses as dc
import tkinter as tk
import tkinter.font as tkfont
import math
import random

from utils import *
from gamestate import *
from leaderboard import LeaderBoard
import keybinds as kb
from entities import *
import level as lv

class ScoreInfo:
    def __init__(self, cv, rect, score, hp, lvl, tr):
        self.lives = []
        l_s = 35
        l_g = 5
        self.image = tk.PhotoImage(file="heart.gif")
        for i in range(hp):
            l = cv.create_image(rect.x + i * l_s + l_s/2 + (i+1) * l_g, rect.y + l_s/2, image=self.image)
            self.lives.append(l)

        fnt_s = tkfont.Font(family='Helvetica', size=18)

        self.score = cv.create_text(rect.x + l_g, rect.y + l_s * 2,
                                    text="Score: " + str(score), anchor="nw",
                                    font=fnt_s, fill="white")

        self.lvl = cv.create_text(rect.x + l_g, rect.y + l_s * 4,
                                  text="Level " + str(lvl), anchor="nw",
                                  font=fnt_s, fill="white")

        self.tr = cv.create_text(rect.x + l_g, rect.y + l_s * 6,
                                  text="Time: " + str(tr), anchor="nw",
                                  font=fnt_s, fill="white")

    def update(self, cv, score, hp, tr):
        while hp < len(self.lives):
            l = self.lives.pop()
            cv.delete(l)
        cv.itemconfig(self.score, text="Score: "+str(score))
        cv.itemconfig(self.tr, text="Time: "+str(tr))
    

class GamePlay:
    p: Player
    s: [Spawner]
    dims: Rect
    t: int
    score: int
    keybinds: kb.KeyBinds
    lb: LeaderBoard
    level: lv.Level

    def __init__(self, keybinds, lb, level):
        self.keybinds = keybinds
        self.lb = lb
        self.level = level
        self.p_hp = None
        self.score = None

    def start(self, win, cv):
        win.unbind("<Escape>")
        win.unbind("<Button-1>")
        win.unbind("<KeyPress>")
        win.unbind("<KeyRelease>")
        cv.delete("all")

        win.bind("<KeyPress>",   self.key_press)
        win.bind("<KeyRelease>", self.key_release)
        win.bind("<Escape>", self.pause)

        sx = (WIDTH  -  GAME_WIDTH) / 2
        sy = (HEIGHT - GAME_HEIGHT) / 2
        self.dims = Rect(sx, sy, GAME_WIDTH, GAME_HEIGHT)


        # background
        cv.create_rectangle(sx, sy , sx + GAME_WIDTH, sy + GAME_HEIGHT,
                            fill="#000000")
        self.bg_img = tk.PhotoImage(file="bg.gif")
        self.bg =  cv.create_image(sx + GAME_WIDTH/2, 0, image=self.bg_img)
        self.bg_y = 0
        
        px = self.dims.x + self.dims.w/2
        py = self.dims.y + self.dims.h/4 * 3
        a = 15/2
        self.p_img = tk.PhotoImage(file="player.gif")
        p_tag = cv.create_image(px, py, image=self.p_img)
        #p_tag = cv.create_oval(px-a, py-a, px+a, py+a, fill="white",
        #                       outline="white")
        php = self.p_hp if self.p_hp else 5
        self.p = Player(px, py, 0, 0, p_tag, 15, 5, php, False)
        
        # draw the leaderboard on the left
        self.lb.draw(cv, Rect(0, 100, self.dims.x, HEIGHT - 100))

        # draw the score + hp on the right
        if not self.score:
            self.score = 0

        srect = Rect(self.dims.x + self.dims.w, 100,
                     WIDTH - self.dims.x - self.dims.w, HEIGHT-100)
        self.score_info = ScoreInfo(cv, srect, self.score, self.p.hp, self.level.diff, LEVEL_TIME/1000)
        
        self.s = []

        sx = self.dims.x + self.dims.w / 2
        sy = self.dims.y + 200

        self.t = 0
        self.paused = False
        self.paused_txt = None

        self.boss_img_img = tk.PhotoImage(file="boss.gif")
        self.boss_img = None
        self.should_boss = False

        return GameState.GAMEPLAY

    def move_bg(self, cv):
        self.bg_y += HEIGHT/720/2
        self.bg_y %= HEIGHT
        cv.coords(self.bg, self.dims.x + self.dims.w / 2, self.bg_y)
    
    def pause(self, e):
        self.paused = not self.paused            
    
    def key_press(self, e):
        act = self.keybinds.get(e.keysym)
        if act == "cheat":
            for s in self.s:
                s.hp = 0
        elif act == "boss":
            self.paused = True
            self.should_boss = True
        self.p.handle_key_press(act)

    def key_release(self, e):
        act = self.keybinds.get(e.keysym)
        self.p.handle_key_release(act)
        
    def loop(self, win, cv):
        if self.paused:
            if not self.paused_txt:
                self.paused_txt = cv.create_text(WIDTH/2, HEIGHT/2,
                                                 text="PAUSED", fill="white")
            if not self.boss_img and self.should_boss:
                self.boss_img = cv.create_image(WIDTH/2, HEIGHT/2, image=self.boss_img_img)

        else:
            self.move_bg(cv)
            self.should_boss = False
            if self.paused_txt:
                cv.delete(self.paused_txt)
                self.paused_txt = None
            if self.boss_img:
                cv.delete(self.boss_img)
                self.boss_img = None
            self.score_info.update(cv, self.score, self.p.hp, (LEVEL_TIME - self.t)/1000)
            self.p.update(self.dims)
            if self.p.hp <= 0:
                print("DEAD at: ", self.score)
                return GameState.START_GAMEOVER
            
            self.p.draw(cv)
            
            if self.level.update():
                spx = random.randint(self.dims.x + 100, self.dims.x + self.dims.w - 100)
                spy = random.randint(0, 200) # TODO: hardcoded
                t_ang = math.atan2(self.p.y - spy, self.p.x - spx)
                
                tag = cv.create_oval(spx-10, spy-10,
                                 spx+10, spy+10, fill="red", outline="red")
                sp = self.level.get_spawner(tag, t_ang)
                sp.x = spx
                sp.y = spy
                #sp.ang += t_ang
                self.s.append(sp)
            
            for s in self.s:
                res = s.update(self.t, cv, self.dims)
                if res == None:
                    self.s.remove(s)
                    continue
                if not res:                
                    s.amt = 0
                collide(self.p, s, cv)

            self.t += int(1000 * FIXED_DT)
            if self.t > LEVEL_TIME:
                return GameState.START_LEVEL_END
            self.score += int(1000 * FIXED_DT)
        
        return GameState.GAMEPLAY
