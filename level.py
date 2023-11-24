import random
from entities import *

# difficulty from 0-10
class Level:
    diff: int

    def __init__(self, diff):
        self.diff = diff

    # return False or True whether a spawner should be spawned
    def update(self):
        return random.randint(0, (10-min(self.diff, 10))*100) < 10

    def get_spawner(self, tag, tang):
        diff = self.diff
        amt = random.randint(1, diff)
        ang_r = 0 if amt == 1 else random.random() * 2 * math.pi
        return Spawner(20, 0, 0, random.randint(50, 100 + diff * 20),
                       (random.random()-0.5) * diff/10,
                       tang + (random.random() - 0.5) / diff,
                       (random.random() - 0.5) * 0.1,
                       (random.random() - 0.5) * 0.01,
                       random.randint(100//diff, 500 + 1000//diff),
                       0,
                       amt,
                       ang_r,
                       3000 + diff * 500,
                       tag)
