from utils import *

# if True, show every object's position
DEBUG = False

VERSION = "0.2"
WINDOW_WIDTH, WINDOW_HEIGHT = (240, 120)
CAPTION = "Pynasour"
FPS = 60                 # FPS need devided by 10
ANIM_FPS = FPS//5


SCORE = 0
with open(r"asset\score.txt", "r") as f:
    l = f.readlines()
    HIGH_SCORE = int(l[1])

# BackGround color of img bank 
COLKEY = ColPal.pink
