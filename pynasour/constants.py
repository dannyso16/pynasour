import pkg_resources
import pyxel  # type: ignore

from .utils import ColPal

# if True, show every object's position
DEBUG = False

VERSION = "0.2"
WINDOW_WIDTH, WINDOW_HEIGHT = (240, 120)
CAPTION = "Pynasour"
FPS = 60  # FPS need devided by 10
ANIM_FPS = FPS // 5

# BackGround color of img bank
COLKEY = ColPal.pink


class Score:
    # === class variables ===
    _score = 0
    _high_score = 0

    def __init__(self):
        self.initialize()

    @classmethod
    def update(cls):
        global FPS
        if pyxel.frame_count % (FPS // 10) == 0:  # 1 sec -> score +10
            cls._score += 1

    @classmethod
    def initialize(cls):
        cls._score = 0
        score_loc = pkg_resources.resource_filename(__name__, "asset/score.txt")
        with open(score_loc, "r") as f:
            lines = f.readlines()
            cls._high_score = int(lines[1])

    @classmethod
    def saveHighScore(cls):
        cls._high_score = max(cls._high_score, cls._score)
        score_loc = pkg_resources.resource_filename(__name__, "asset/score.txt")
        with open(score_loc, "w") as f:
            f.write("High score: \n{}".format(cls._high_score))

    @classmethod
    def getScore(cls):
        return cls._score

    @classmethod
    def getHighScore(cls):
        return cls._high_score
