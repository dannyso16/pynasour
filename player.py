import pyxel
from utils import *
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT,
                       CAPTION, FPS, ANIM_FPS,
                       HIGH_SCORE, SCORE,
                       COLKEY)

class Player:
    """playable character"""
    global COLKEY
    # === CLASS VARIABLES ===
    IMG_ID = 0                        # img_bankのID
    _W, _H = 24, 26
    # dinosour
    NORMAL = Rect(_W*0, 0, _W, _H, COLKEY)
    BLINK  = Rect(_W*1, 0, _W, _H, COLKEY)
    RUN1   = Rect(_W*2, 0, _W, _H, COLKEY)
    RUN2   = Rect(_W*3, 0, _W, _H, COLKEY)
    CRASH  = Rect(_W*4, 0, _W, _H, COLKEY)

    RUN_ANIM = [RUN1, RUN2]

    INITIAL_POS = Vec(30, 70)         # 初期状態
    JUMP_VELOCITY = 11                # jump時の速度(大きくすると高く飛ぶ)
    JUMP_DURING_TIME = 2              # jumpの持続時間を決める(大きくすると長く滞空)
    state = "RUN"                     # state: "RUN" or "JUMP" or"IDLE"
    pos = INITIAL_POS                 # position of Player

    def __init__(self):
        """velocity: 猫の進行の向き"""
        self.initialize()
        self.showInfo()

    def initialize(self):
        Player.pos = Player.INITIAL_POS
        self.velocity = Vec(0, 0)
        Player.state = "RUN"            # "RUN" or "JUMP" or "IDLE
        # TODO: Add state

    def showInfo(self):
        print("getSize: ", self.getSize())

    def update(self):
        # btnでjump
        # print(Player.state, self.velocity.x, self.velocity.y, Player.pos.y)
        if (Player.state=="RUN" and
            (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_SPACE))):
            self.velocity = Vec(0,-Player.JUMP_VELOCITY)
            Player.state = "JUMP"

        if (Player.state=="JUMP"):
            if pyxel.frame_count%Player.JUMP_DURING_TIME==0:
                self.velocity = Vec(0, self.velocity.y + 1)
                Player.pos = Vec(Player.pos.x, Player.pos.y + self.velocity.y)
                if Player.pos.y >= Player.INITIAL_POS.y: # 地面に着地したら
                    Player.pos = Player.INITIAL_POS
                    Player.state = "RUN"

        if Player.state=="IDLE":
            pass

    def blt(self):
        if self.state == "IDLE":
            pyxel.blt(self.pos.x, self.pos.y,
                      self.IMG_ID, *Player.CRASH.getRect())
        else:
            f = (pyxel.frame_count//ANIM_FPS)%len(Player.RUN_ANIM)
            pyxel.blt(self.pos.x, self.pos.y,
                        Player.IMG_ID, *Player.RUN_ANIM[f].getRect())
        pyxel.text(0,0,"Player_pos: ({}, {})".format(
                    Player.pos.x, Player.pos.y), ColPal.orange)


    @classmethod
    def beGameover(cls):
        cls.state = "IDLE"

    @classmethod
    def getPos(cls):
        """return: pos(Vec)"""
        return Player.pos

    # TODO: なくす
    @classmethod
    def getSize(cls):
        return cls._W, cls._H

    @classmethod
    def getState(cls):
        return cls.state


# === example=====
# c = Player()
# c.update(pos=Vec(0,0), velocity=Vec(1,1))
