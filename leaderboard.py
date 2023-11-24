import tkinter as tk
from functools import cmp_to_key
import tkinter.font as tkfont

class LeaderBoard:
    scores: {str:int}
    fnt: tkfont.Font
    fnt_s: tkfont.Font
    score_rects: [int]
    title: int
    drawn: bool
    
    def __init__(self):
        self.scores = []
        # assumes sorted
        with open("leaderboard", "r") as lbf:
            for line in lbf.readlines():
                kv = line.strip().split(" ")
                self.scores.append((kv[0], int(kv[1])))

        self.fnt = tkfont.Font(family='Helvetica', size=24, weight='bold')
        self.fnt_s = tkfont.Font(family='Helvetica', size=18)
        self.score_rects = []
        self.title = None
        self.drawn = False

    def append(self, name, score):
        self.scores.append((name, score))
        self.scores.sort(key=cmp_to_key(lambda x, y: y[1] - x[1]))
        txt = ""
        for s in self.scores:
            txt += s[0] + " " + str(s[1]) + "\n"
        with open("leaderboard", "w") as f:
            f.write(txt)

    def draw(self, cv, rect):
        if self.drawn:
            for s in self.score_rects:
                cv.destroy(s)
            cv.destroy(self.title)
            self.drawn = False

        txt_pad = 25
        self.title = cv.create_text(rect.x + rect.w - txt_pad, rect.y,
                                         text="SCORES", fill="white",
                                         font=self.fnt, anchor="ne")
        max_scores = 5 # at most 5 scores will be displayed
        dh = 50
        for i in range(min(len(self.scores), max_scores)):
            text = self.scores[i][0] + ": " + str(self.scores[i][1])
            self.score_rects.append(cv.create_text(rect.x + rect.w - txt_pad,
                                                   rect.y + dh,
                                                   text=text, fill="white",
                                                   font=self.fnt_s, anchor="ne"))
            dh += 50
