import pyxel
from utils import *
from player import *
from enemy import *
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT,
                       CAPTION, FPS,
                       HIGH_SCORE, SCORE)

# TODO: スコアの実装 ok
# TODO: 背景の実装

# === MAIN ===
class App:
    # restart BUTTOn
    IMG_ID = 0
    BTN_W, BTN_H = 32, 32
    BTN_RESTART = Rect(0, 96, BTN_W, BTN_H, COLKEY)

    def __init__(self):
        global WINDOW_HEIGHT, WINDOW_WIDTH, CAPTION, FPS, COLKEY
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption=CAPTION, fps=FPS)

        # === Generate Instances ===
        self.player = Player()
        self.enemy  = Enemy()
        self.backgnd  =  BackGround()
        # TODO: タイトル画面
        self.player.beGameover()

        # pyxel.image(Player.IMG_ID).load(0, 0,
        #     "C:/code/python_script/Library/pyxel/asset/cat_16x16.png")
        pyxel.load(r"C:\Users\HOME\pyxel\dinasour\asset\asset_akune.pyxel")
        pyxel.run(self.update, self.draw)

    def update(self):
        global HIGH_SCORE, SCORE, FPS
        self.backgnd.update()
        self.enemy.update()
        self.player.update()

        # score
        if (Player.getState()!="IDLE"
        and pyxel.frame_count%(FPS//10)==0): # 1 sec -> score +10
            SCORE += 1

        # === Restart ===
        if Player.getState()=="IDLE":
            if pyxel.btn(pyxel.KEY_SPACE):
                HIGH_SCORE = max(HIGH_SCORE, SCORE)
                SCORE = 0
                self.backgnd.initialize()
                self.enemy.initialize()
                self.player.initialize()


    def draw(self):
        global SCORE, HIGH_SCORE, WINDOW_HEIGHT, WINDOW_WIDTH
        pyxel.cls(ColPal.gray_dark)
        self.backgnd.blt()
        self.enemy.blt()
        self.player.blt()

        # show score
        pyxel.text(WINDOW_WIDTH-50, 5, "HI {}  {}".format(HIGH_SCORE, SCORE), ColPal.white)
        pyxel.text(0, 10, "Frame: {}".format(pyxel.frame_count), ColPal.orange)
        if Player.getState()=="IDLE":
            pyxel.text(WINDOW_WIDTH//2-5, WINDOW_HEIGHT//2-5,
                        "GAME OVER\n[SPACE] TO CONTINUE", ColPal.white)
            pyxel.blt(WINDOW_WIDTH//2-48, WINDOW_HEIGHT//2-16,
                        App.IMG_ID, *App.BTN_RESTART.getRect())

App()
