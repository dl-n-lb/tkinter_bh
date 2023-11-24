from utils import *

'''
key bindings are stored like
action1 keysym1
action2 keysym2

actions are:
moveUp
moveDown
moveLeft
moveRight
focus
cheat
boss
'''
class KeyBinds:    
    def __init__(self):
        self.keys = dict()
        with open(KEYBINDS_PATH, "r") as f:
            for line in f.readlines():
                data = line.strip().split(" ")
                self.keys[data[1].lower()] = data[0]
        print(self.keys)

    def save(self):
        s = ""
        for key in self.keys:
            s += self.keys[key] + " " + key + "\n"
        with open(KEYBINDS_PATH, "w") as f:
            f.write(s)

    def get(self, key):
        try:
            return self.keys[key.lower()]
        except:
            print(key)
            return ""

    def edit(self, act, oldKey, newKey):
        self.keys.pop(oldKey)
        self.keys[newKey] = act
