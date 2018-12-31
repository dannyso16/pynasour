import pyxel
import random
from utils import *
from player import *
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT,
                       CAPTION, FPS, ANIM_FPS,
                       HIGH_SCORE, SCORE,
                       COLKEY)

# TODO: 敵の出現の乱数をどうするのか
# TODO: 鳥の出現のスコアはいつから
# TODO: 速度の変化は
# TODO: 当たり判定 調整

class Enemy:
    """Enemy: サボテン，プテラノドン"""
    # === CLASS VARIABLES ===
    IMG_ID = 0
    # cactus
    CACTUS_W, CACTUS_H = 16, 24
    Cactus_big1 = Rect(CACTUS_W*0, 32, CACTUS_W, CACTUS_H, COLKEY)
    Cactus_big2 = Rect(CACTUS_W*1, 32, CACTUS_W, CACTUS_H, COLKEY)
    Cactus_big3 = Rect(CACTUS_W*2, 32, CACTUS_W, CACTUS_H, COLKEY)
    Cactus_sml1 = Rect(CACTUS_W*3, 32, CACTUS_W, CACTUS_H, COLKEY)
    Cactus_sml2 = Rect(CACTUS_W*4, 32, CACTUS_W, CACTUS_H, COLKEY)
    Cactus_sml3 = Rect(CACTUS_W*5, 32, CACTUS_W, CACTUS_H, COLKEY)
    CACTUS_ANIMs = [[Cactus_big1, Cactus_big2, Cactus_big3],
                    [Cactus_sml1, Cactus_sml2, Cactus_sml3]]

    # Ptera
    PTERA_W, PTERA_H = 24, 24
    dwn   = Rect(PTERA_W*0, 56, PTERA_W, PTERA_H, COLKEY)
    up    = Rect(PTERA_W*1, 56, PTERA_W, PTERA_H, COLKEY)
    PTERA_ANIMs = [[dwn, up]]

    INIT_POS = Vec(280, 73)
    cur_anim = CACTUS_ANIMs[0]
    velocity = 4               # this is common with the speed of Ground
    # TODO: 速度を変更できるように
    COLLIDE_OFFSET = 4         # between [0 - Player_img_size]
                               # 小さいほど厳しい判定

    def __init__(self):
        """pos: (x, y)
        velocity: 猫の進行の向き"""
        self.initialize()
        self.showInfo()

    def update(self):
        # print( self.velocity.x, self.velocity.y, self.pos.y)
        if Player.getState()=="IDLE":
            return
        if pyxel.frame_count%2:
            self.pos = Vec(self.pos.x + self.velocity.x, self.pos.y)

        if self.pos.x < -20:
            self.initialize()

        if self.collideWithPlayer():
            Player.beGameover()


    def collideWithPlayer(self):
        """return: (bool) collide with Player or not """
        p_pos = Player.getPos()
        px, py = p_pos.x, p_pos.y
        pw, ph = Player.getSize()
        cx, cy = self.pos.x, self.pos.y
        if ( abs(cx-px) < pw-Enemy.COLLIDE_OFFSET
        and abs(cy-py) < ph-Enemy.COLLIDE_OFFSET ):
            return True
        else:
            return False

    def blt(self):
        global ANIM_FPS
        f = (pyxel.frame_count//ANIM_FPS)%len(self.cur_anim)
        pyxel.blt(self.pos.x, self.pos.y,
                    Enemy.IMG_ID, *self.cur_anim[f].getRect())
        pyxel.text(0, 20,
                    "Enemy_pos: ({},{})".format(self.pos.x, self.pos.y), ColPal.orange)


    def initialize(self):
        self.velocity = Vec(-4, 0)
        if random.random()<0.2:       # ptera
            self.cur_anim = Enemy.PTERA_ANIMs[0]
            gnd_y = self.INIT_POS.y   # height of Ground
            self.pos = Vec(self.INIT_POS.x,
                            gnd_y -40*random.randrange(0,2))
        else:                         # cactus
            self.cur_anim = Enemy.CACTUS_ANIMs[random.randrange(0,2)] # big or small cactus
            self.pos = self.INIT_POS

    def showInfo(self):
        print("hello")

    def getVelocity(self):
        # TODO: change velocity along the score increase
        return self.velocity


class BackGround:
    # === CLASS VARIABLES ===
    IMG_ID = 0
    # cloud
    CLOUD_W, CLOUD_H = 48, 16
    CLOUD_normal     = Rect(0, 80, CLOUD_W, CLOUD_H, COLKEY)
    CLOUD_INIT_POS = [Vec(280, 26), Vec(400, 16), Vec(550, 30)]

    # Ground
    GND_W, GND_H = 128, 16
    GND_normal = Rect(0, 128, GND_W, GND_H)
    GND_INIT_POS = [Vec(0, 88), Vec(GND_W, 88), Vec(2*GND_W, 88)]


    def __init__(self):
        self.initialize()
        self.showInfo()

    def update(self):
        if Player.getState()=="IDLE":
            return
        if pyxel.frame_count%2:
            for i in range(len(self.cloud_pos)):
                self.cloud_pos[i] = Vec(self.cloud_pos[i].x + self.cloud_velocity.x,
                                        self.cloud_pos[i].y)
            for i in range(len(self.gnd_pos)):
                self.gnd_pos[i] = Vec(self.gnd_pos[i].x + self.gnd_velocity.x,
                                        self.gnd_pos[i].y)

        # 左端についたら右端に戻す
        # lastに合わせて距離を保つ
        for i in range(len(self.cloud_pos)):
            if self.cloud_pos[i].x < -50:
                self.cloud_pos[i] = Vec(self.CLOUD_INIT_POS[-1].x,
                                        self.cloud_pos[i].y)
        for i in range(len(self.gnd_pos)):
            if self.gnd_pos[i].x < -120:
                self.gnd_pos[i]   = Vec(self.GND_INIT_POS[-1].x,
                                        self.gnd_pos[i].y)

    def blt(self):
        for i,pos in enumerate(self.cloud_pos):
            pyxel.blt(pos.x, pos.y,
                      BackGround.IMG_ID, *BackGround.CLOUD_normal.getRect())
        for i,pos in enumerate(self.gnd_pos):
            pyxel.blt(pos.x, pos.y,
                      BackGround.IMG_ID, *BackGround.GND_normal.getRect())
            # pyxel.text(0, 30+i*10,
            #             "Gnd_pos: ({},{})".format(
            #             pos.x, pos.y), 3)


    def initialize(self):
        self.cloud_velocity = Vec(-1, 0)
        self.gnd_velocity   = Vec(-4, 0) # change with enemy's velocity
        # cloud pos(list)
        self.cloud_pos = [self.CLOUD_INIT_POS[i]
                            for i in range(len(self.CLOUD_INIT_POS))]
        # ground pos
        self.gnd_pos = [self.GND_INIT_POS[i]
                            for i in range(len(self.GND_INIT_POS))]

    def showInfo(self):
        print("hello")




# === example=====
# c = Enemy()
# c.update(pos=Vec(0,0), velocity=Vec(1,1))
