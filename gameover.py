import tkinter as tk
import tkinter.font as tkfont
from gamestate import GameState
from leaderboard import LeaderBoard
from gameplay import GamePlay

class GameOver:
    score: int
    lb: LeaderBoard
    gp: GamePlay
    fnt: tkfont.Font
    fnt_s: tkfont.Font
    ttl: int
    score: int
    score_widget: int
    name_enter: tk.Entry
    enter_win: int

    def __init__(self, lb):
        self.lb = lb
    
    def start(self, win, cv, gp):
        win.unbind("<Escape>")
        win.unbind("<Button-1>")
        win.unbind("<KeyPress>")
        win.unbind("<KeyRelease>")
        cv.delete("all")

        self.score = gp.score
        print(self.score)

        gp.score = 0
        
        self.fnt = tkfont.Font(family='Helvetica', size=24, weight='bold')
        self.fnt_s = tkfont.Font(family='Helvetica', size=18)

        w = cv.winfo_width()
        h = cv.winfo_height()
        
        self.ttl = cv.create_text(w/2, h/2, text="GAME OVER", font=self.fnt, fill="white")
        self.score_widget = cv.create_text(w/2, h/2+50, text="Your Score: " + str(self.score),
                                    font=self.fnt_s, fill="white")
        self.name_enter = tk.Entry(cv, font=self.fnt)
        self.enter_win = cv.create_window(w/2, h/2+100, window=self.name_enter)

        win.bind("<KeyPress>", self.check_return)
        self.submitted = False
        return GameState.GAMEOVER

    def check_return(self, e):
        if e.keysym == "Return":
            txt = self.name_enter.get()
            if txt.isalnum():
                # valid name
                self.lb.append(txt, self.score)
                self.submitted = True
                

    def loop(self, win, cv):
        if self.submitted:
            return GameState.START_MENU
        return GameState.GAMEOVER
