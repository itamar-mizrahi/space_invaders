import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY   = (150, 150, 150)
PURPLE = (255, 0, 255)
RED    = (255, 0, 0)
BLUE   = (0, 100, 255)
CYAN   = (0, 255, 255)

FPS = 60
HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except:
            pass
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))
