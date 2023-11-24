import dataclasses as dc
import tkinter as tk
import math

from utils import *

@dc.dataclass
class Proj:
    x: float
    y: float
    v: float
    ang: float
    tag: int

    def draw(self, cv):
        cv.coords(self.tag, self.x-PROJ_RAD, self.y-PROJ_RAD,
                  self.x+PROJ_RAD, self.y+PROJ_RAD)

    def update(self):
        self.x += self.v * FIXED_DT * math.cos(self.ang)
        self.y += self.v * FIXED_DT * math.sin(self.ang)


class Spawner:
    sz: float # size of the spawner    
    x : float # spawner x
    y : float # spawner y
    
    v: float # spawn velocity
    a: float # spawn acceleration
    
    ang  : float # spawn angle (if multiple are spawned this will be the center of the range)
    dang : float # change in ang per spawn
    ddang: float # change in dang per spawn
    
    spawn_interval: float # interval between spawns (ms)
    spawn_offset  : float # offset for spawns
    prev_tick: int # tick of previous 

    amt: int # amount per spawn
    ang_range: float # range of spawn angles (only used if amt > 1)
    
    projectiles: [Proj] # list of projectiles

    hp: int
    tag: int

    def __init__(self, sz: float, x: float, y: float, v: float, a: float,
                 ang: float, dang: float, ddang: float, spi: float, spo: float,
                 amt: int, ang_r: float, hp: int, tag: int):
        self.sz = sz
        self.x = x
        self.y = y
        self.v = v
        self.a = a
        self.ang = ang
        self.dang = dang
        self.ddang = ddang
        self.spawn_interval = spi
        self.spawn_offset = spo
        self.amt = amt
        self.ang_range = ang_r
        self.prev_tick = 0
        self.projectiles = []

        self.hp = hp
        self.tag = tag

    def remove(self, p: Proj, cv: tk.Canvas):
        cv.delete(p.tag)
        self.projectiles.remove(p)

    def update(self, t: float, cv: tk.Canvas, alive_rect: Rect):
        max_x: int = alive_rect.x + alive_rect.w
        max_y: int = alive_rect.y + alive_rect.h
        
        for p in self.projectiles:
            p.update()
            if p.x > max_x or p.x < alive_rect.x or p.y > max_y or p.y < alive_rect.y:
                cv.delete(p.tag)
                self.projectiles.remove(p)
            p.draw(cv)
            p.v += self.a

        # spawn new ones if necessary
        if (t - self.spawn_offset) // self.spawn_interval > self.prev_tick:
            self.prev_tick = (t - self.spawn_offset) // self.spawn_interval
            for i in range(self.amt):
                a = i / self.amt - 0.5 # coeff
                ang = self.ang + self.ang_range * a
                px = self.x + self.sz * math.cos(ang)
                py = self.y + self.sz * math.sin(ang)
                tag = cv.create_oval(px-PROJ_RAD, py-PROJ_RAD,
                                     px+PROJ_RAD, py+PROJ_RAD, fill="blue", outline="blue")

                self.projectiles.append(Proj(px, py, self.v, ang, tag))

        if self.hp <= 0:
            cv.delete(self.tag)
            if len(self.projectiles) == 0:
                return None
            return False
        self.hp -= math.floor(1000/FRAMERATE)
        self.ang += self.dang * FIXED_DT
        self.dang += self.ddang * FIXED_DT
        return True

@dc.dataclass
class Player:
    __slots__ = ["x", "y", "vx", "vy", "tag", "sz", "hitbox_sz", "hp", "is_focused"]
    x: float
    y: float
    vx: float
    vy: float
    tag: int
    sz: float
    hitbox_sz: float

    hp: int

    is_focused: bool

    def update(self, dims):
        if self.is_focused:
            vx = self.vx * FOCUS_SPD
            vy = self.vy * FOCUS_SPD
        else:
            vx = self.vx * PLAYER_SPD
            vy = self.vy * PLAYER_SPD

        vlen = self.vx**2 + self.vy**2
        if vlen > 1:
            vx /= math.sqrt(vlen)
            vy /= math.sqrt(vlen)

        self.x += vx * FIXED_DT
        self.y += vy * FIXED_DT
        if self.x < dims.x + self.sz / 2:
            self.x = dims.x + self.sz / 2
        if self.y < dims.y + self.sz / 2:
            self.y = dims.y + self.sz / 2
        if self.x > dims.x + dims.w - self.sz / 2:
            self.x = dims.x + dims.w - self.sz / 2
        if self.y > dims.y + dims.h - self.sz / 2:
            self.y = dims.y + dims.h - self.sz / 2

        

    def handle_key_press(self, act):
        if act == "moveUp":
            self.vy = max(self.vy - 1, -1)
        elif act == "moveDown":
            self.vy = min(self.vy + 1, 1)
        elif act == "moveLeft":
            self.vx = max(self.vx - 1, -1)
        elif act == "moveRight":
            self.vx = min(self.vx + 1, 1)
        elif act == "focus":
            self.is_focused = True

    def handle_key_release(self, act):
        if act == "moveUp":
            self.vy = min(self.vy + 1, 1)
        elif act == "moveDown":
            self.vy = max(self.vy - 1, -1)
        elif act == "moveLeft":
            self.vx = min(self.vx + 1, 1)
        elif act == "moveRight":
            self.vx = max(self.vx - 1, -1)
        elif act == "focus":
            self.is_focused = False

    def draw(self, c: tk.Canvas):
        a = self.sz/2
        c.coords(self.tag, self.x, self.y)
        #c.coords(self.tag, self.x-a, self.y-a, self.x+a, self.y+a)


def collide(p: Player, s: Spawner, cv: tk.Canvas):
    for pr in s.projectiles:
        if math.dist((p.x, p.y), (pr.x, pr.y)) - p.hitbox_sz - PROJ_RAD < 0:
            p.hp -= 1
            s.remove(pr, cv)
