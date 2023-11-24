from enum import Enum

class GameState(Enum):
    START_MENU      = 0
    MENU            = 1
    START_GAMEPLAY  = 2
    GAMEPLAY        = 3
    PAUSE           = 4
    START_OPTIONS   = 5
    OPTIONS         = 6
    START_GAMEOVER  = 7
    GAMEOVER        = 8
    QUIT            = 9
    START_LEVEL_END = 10
    LEVEL_END       = 11
