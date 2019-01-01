import pyxel
from utils import *
from player import *
from enemy import *
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT,
                       CAPTION, FPS,
                       HIGH_SCORE, SCORE,
                       DEBUG)

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
        # TODO: make game title
        self.player.beGameover() # not good way ...

        pyxel.load(r"C:\Users\HOME\Documents\GitHub\pynasour\asset\asset.pyxel") # change here when use
        pyxel.run(self.update, self.draw)

    def update(self):
        global HIGH_SCORE, SCORE, FPS
        self.backgnd.update()  # execution order: back layer to front layer
        self.enemy.update()
        self.player.update()

        # score update
        if (Player.getState()!="IDLE"
        and pyxel.frame_count%(FPS//10)==0): # 1 sec -> score +10
            SCORE += 1

        # === Restart ===
        if Player.getState()=="IDLE":
            if pyxel.btn(pyxel.KEY_SPACE):
                # save high-score
                HIGH_SCORE = max(HIGH_SCORE, SCORE)
                with open(r"asset\score.txt", "w") as f:
                    f.write("High score: \n{}".format(HIGH_SCORE))
                # initialize state
                SCORE = 0
                self.backgnd.initialize()
                self.enemy.initialize()
                self.player.initialize()


    def draw(self):
        global SCORE, HIGH_SCORE, WINDOW_HEIGHT, WINDOW_WIDTH, DEBUG
        pyxel.cls(ColPal.gray_dark)
        self.backgnd.blt()
        self.enemy.blt()
        self.player.blt()

        # show score
        pyxel.text(WINDOW_WIDTH-50, 5, "HI {}  {}".format(HIGH_SCORE, SCORE), ColPal.white)
        # if gameover, show restart button
        if Player.getState()=="IDLE":
            pyxel.text(WINDOW_WIDTH//2-5, WINDOW_HEIGHT//2-5,
                        "GAME OVER\n[SPACE] TO CONTINUE", ColPal.white)
            pyxel.blt(WINDOW_WIDTH//2-48, WINDOW_HEIGHT//2-16,
                        App.IMG_ID, *App.BTN_RESTART.getRect())

        if DEBUG:
            pyxel.text(0, 20, "Frame: {}".format(pyxel.frame_count), ColPal.orange)
App()
