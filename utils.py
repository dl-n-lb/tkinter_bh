import dataclasses as dc

# the title of the window to be displayed
GAME_TITLE: str = "DODGE THE BULLETS" # original name

# width and height of the window
WIDTH    : int = 1280
HEIGHT   : int = 720

# describes the aspect ratio of the playfield
# which the game will render in the middle of the screen
GAME_ASPECT_RATIO : float = 1

GAME_WIDTH = HEIGHT * GAME_ASPECT_RATIO
GAME_HEIGHT = HEIGHT

BG_COLOR : str = "#0b0c0f"

# movement stuff
PLAYER_SZ: float = 10
PLAYER_SPD: float = 141
FOCUS_SPD: float = PLAYER_SPD / 2
FRAMERATE: int = 60
FIXED_DT : float = 1 / FRAMERATE

LEVEL_TIME: int = 30000

PROJ_RAD: float = 5

# where to fetch keybinds from disc
KEYBINDS_PATH="./keybinds"

@dc.dataclass
class Rect:
    __slots__ = ["x", "y", "w", "h"]
    x: float
    y: float
    w: float
    h: float
