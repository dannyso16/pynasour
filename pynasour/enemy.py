import random
from copy import deepcopy

import pyxel  # type: ignore

from .constants import ANIM_FPS, COLKEY, DEBUG, Score
from .player import Player
from .utils import ColPal, Rect, Vec


class Enemy(object):
    """Enemy: サボテン，プテラノドン"""

    # === CLASS VARIABLES ===
    IMG_ID = 0
    # cactus img
    CACTUS_W, CACTUS_H = 16, 24
    Cactus_big1 = Rect(CACTUS_W * 0, 32, CACTUS_W, CACTUS_H, COLKEY)
    Cactus_big2 = Rect(CACTUS_W * 1, 32, CACTUS_W, CACTUS_H, COLKEY)
    Cactus_big3 = Rect(CACTUS_W * 2, 32, CACTUS_W, CACTUS_H, COLKEY)
    Cactus_sml1 = Rect(CACTUS_W * 3, 32, CACTUS_W, CACTUS_H, COLKEY)
    Cactus_sml2 = Rect(CACTUS_W * 4, 32, CACTUS_W, CACTUS_H, COLKEY)
    Cactus_sml3 = Rect(CACTUS_W * 5, 32, CACTUS_W, CACTUS_H, COLKEY)
    CACTUS_ANIMs = [[Cactus_big1, Cactus_big2, Cactus_big3], [Cactus_sml1, Cactus_sml2]]

    # Ptera img
    PTERA_W, PTERA_H = 24, 24
    dwn = Rect(PTERA_W * 0, 56, PTERA_W, PTERA_H, COLKEY)
    up = Rect(PTERA_W * 1, 56, PTERA_W, PTERA_H, COLKEY)
    PTERA_ANIMs = [[dwn, up]]

    # enemy spawn interval is between [MIN_INTERVAL, MAX_INTERVAL]
    # enemy spawns in SPAWN_POS or further position from Dinasour
    ENEMY_NUM = 6
    MIN_INTERVAL = 85
    MAX_INTERVAL = 150
    SPAWN_POS = 280
    GND_HEIGHT = 73
    PTERA_SPAWN_RATIO = 0.4  # ptera spawn rate [0 - 1]
    INIT_VELOCITY_X = -4  # initail velocity of enemy

    COLLIDE_OFFSET = 4  # between [0 - Player_img_size]
    # 小さいほど厳しい判定

    def __init__(self):
        self.initialize()
        self.showInfo()

    def initialize(self):
        self.velocity = Vec(Enemy.INIT_VELOCITY_X, 0)
        interval = random.randrange(self.MIN_INTERVAL, self.MAX_INTERVAL)
        self.INIT_POS = [
            Vec(self.SPAWN_POS + i * self.MAX_INTERVAL + interval, self.GND_HEIGHT)
            for i in range(self.ENEMY_NUM)
        ]

        self.cur_anim = [None] * self.ENEMY_NUM
        self.pos = deepcopy(self.INIT_POS)
        # enemy is cactus or ptera
        for i in range(self.ENEMY_NUM):
            if random.random() < self.PTERA_SPAWN_RATIO:  # ptera
                self.cur_anim[i] = Enemy.PTERA_ANIMs[0]
                self.pos[i].y -= 40 * random.randrange(0, 2)
            else:  # big or small Cactus
                self.cur_anim[i] = Enemy.CACTUS_ANIMs[random.randrange(0, 2)]

    def showInfo(self):
        pass

    def update(self):
        if Player.getState() == "IDLE":
            return
        # update pos, velocity, interval
        self.updateVelAndIntrvl()
        if pyxel.frame_count % 2:
            for i in range(len(self.pos)):
                self.pos[i] = Vec(self.pos[i].x + self.velocity.x, self.pos[i].y)

        # 左端についたら右端に戻す
        for i in range(self.ENEMY_NUM):
            if self.pos[i].x < -50:
                # reset pos
                interval = random.randrange(self.MIN_INTERVAL, self.MAX_INTERVAL)
                spawn_x = max(self.pos[i - 1].x, self.SPAWN_POS)
                self.pos[i] = Vec(spawn_x + interval, self.GND_HEIGHT)

                # select cactus or ptera at random
                if random.random() < self.PTERA_SPAWN_RATIO:  # ptera
                    self.cur_anim[i] = Enemy.PTERA_ANIMs[0]
                    self.pos[i].y -= 40 * random.randrange(0, 2)
                else:  # cactus
                    self.cur_anim[i] = Enemy.CACTUS_ANIMs[random.randrange(0, 2)]

        if self.collideWithPlayer():
            Player.beGameover()

    def collideWithPlayer(self):
        """return: (bool) collide with Player or not"""
        p_pos = Player.getPos()
        playr_x, playr_y = p_pos.x, p_pos.y
        playr_w, playr_h = Player.getSize()
        for pos in self.pos:
            enemy_x, enemy_y = pos.x, pos.y
            if (
                abs(enemy_x - playr_x) < playr_w - Enemy.COLLIDE_OFFSET
                and abs(enemy_y - playr_y) < playr_h - Enemy.COLLIDE_OFFSET
            ):
                return True
        else:
            return False

    def blt(self):
        global ANIM_FPS, DEBUG
        for i, (pos, cur_anim) in enumerate(zip(self.pos, self.cur_anim)):
            f = (pyxel.frame_count // ANIM_FPS) % len(cur_anim)
            pyxel.blt(pos.x, pos.y, Enemy.IMG_ID, *cur_anim[f].getRect())
            if DEBUG:
                pyxel.text(
                    50,
                    i * 10,
                    "Enemy{}: ({},{})".format(i, pos.x, pos.y),
                    ColPal.orange,
                )

    def updateVelAndIntrvl(self):
        # TODO: adjast the coefs
        dif = Score.getScore() // 100
        vel_x = self.INIT_VELOCITY_X - dif
        self.velocity = Vec(vel_x, 0)
        self.MIN_INTERVAL = 85 + 15 * dif
        self.MAX_INTERVAL = 150 + 15 * dif


class BackGround:
    # === CLASS VARIABLES ===
    IMG_ID = 0
    # cloud
    CLOUD_W, CLOUD_H = 48, 16
    CLOUD_normal = Rect(0, 80, CLOUD_W, CLOUD_H, COLKEY)
    CLOUD_INIT_POS = [Vec(280, 26), Vec(400, 16), Vec(550, 30)]

    # Ground
    GND_W, GND_H = 128, 16
    GND_normal = Rect(0, 128, GND_W, GND_H)
    GND_INIT_POS = [Vec(0, 88), Vec(GND_W, 88), Vec(2 * GND_W, 88)]

    INIT_VELOCITY_X = -4

    def __init__(self):
        self.initialize()
        self.showInfo()

    def initialize(self):
        self.cloud_velocity = Vec(self.INIT_VELOCITY_X // 4, 0)
        self.gnd_velocity = Vec(self.INIT_VELOCITY_X, 0)  # same with enemy's velocity
        # cloud pos(list)
        self.cloud_pos = deepcopy(self.CLOUD_INIT_POS)

        # ground pos(list)
        self.gnd_pos = deepcopy(self.GND_INIT_POS)

    def showInfo(self):
        pass

    def update(self):
        if Player.getState() == "IDLE":
            return
        # update velocity, pos
        self.updateVel()
        if pyxel.frame_count % 2:
            for i in range(len(self.cloud_pos)):
                self.cloud_pos[i] = Vec(
                    self.cloud_pos[i].x + self.cloud_velocity.x, self.cloud_pos[i].y
                )
            for i in range(len(self.gnd_pos)):
                self.gnd_pos[i] = Vec(
                    self.gnd_pos[i].x + self.gnd_velocity.x, self.gnd_pos[i].y
                )

        # 左端についたら右端に戻す
        # lastに合わせて距離を保つ
        for i in range(len(self.cloud_pos)):
            if self.cloud_pos[i].x < -50:
                self.cloud_pos[i] = Vec(self.CLOUD_INIT_POS[-1].x, self.cloud_pos[i].y)
        for i in range(len(self.gnd_pos)):
            if self.gnd_pos[i].x < -120:
                self.gnd_pos[i] = Vec(self.GND_INIT_POS[-1].x, self.gnd_pos[i].y)

    def blt(self):
        for i, pos in enumerate(self.cloud_pos):
            pyxel.blt(
                pos.x, pos.y, BackGround.IMG_ID, *BackGround.CLOUD_normal.getRect()
            )
        for i, pos in enumerate(self.gnd_pos):
            pyxel.blt(pos.x, pos.y, BackGround.IMG_ID, *BackGround.GND_normal.getRect())

    def updateVel(self):
        # TODO: adjast the coefs
        dif = Score.getScore() // 100
        vel_x = self.INIT_VELOCITY_X - dif
        self.velocity = Vec(vel_x, 0)
