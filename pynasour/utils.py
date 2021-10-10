# TODO: colpal to enum
import gzip
import os
import pickle

import pyxel

"""(function) margeAndSave
(class) Vec
(class) ColPal
(class) Rect
"""


def margePyxelFiles(img_file_path, music_file_path, save_to):
    """img_file + music_file -> marged_file
    assume 'pixel-artist' and 'music-maker' work together
    this comine img_bank and music_bank (no check data exist or not)"""
    # FIXME: the game-window never ended Corretly
    # check all file extension is .pyxel
    try:
        assert os.path.basename(img_file_path).split(".")[-1] == "pyxel"
        assert os.path.basename(music_file_path).split(".")[-1] == "pyxel"
        assert os.path.basename(save_to).split(".")[-1] == "pyxel"
    except AssertionError:
        print("AssertionError: Check file paths (extension must be .pyxel)")

    # === Constants from constants.py===
    RENDERER_IMAGE_COUNT = 4
    AUDIO_SOUND_COUNT = 65
    AUDIO_MUSIC_COUNT = 8

    pyxel.init(1, 1)  # need to pyxel.load
    data = {"version": pyxel.VERSION}

    # load img data from 'img_file_path'
    pyxel.load(img_file_path)
    image_list = [pyxel.image(i).data.dumps() for i in range(RENDERER_IMAGE_COUNT - 1)]
    data["image"] = image_list

    # tilemap_list = [
    #     (pyxel.tilemap(i).data.dumps(), pyxel.tilemap(i).refimg)
    #     for i in range(RENDERER_TILEMAP_COUNT)
    # ]
    # data["tilemap"] = tilemap_list

    # load music data from 'music_file_path'
    pyxel.load(music_file_path)
    sound_list = [pyxel.sound(i) for i in range(AUDIO_SOUND_COUNT - 1)]
    data["sound"] = sound_list

    music_list = [pyxel.music(i) for i in range(AUDIO_MUSIC_COUNT - 1)]
    data["music"] = music_list

    pickled_data = pickle.dumps(data)

    with gzip.open(save_to, mode="wb") as fp:
        fp.write(pickled_data)
    print("Corretly Saved Data. : {}".format(save_to))
    pyxel.quit()


class Vec:
    """2d coordinate"""

    def __init__(self, x, y):
        self.x = x
        self.y = y


class ColPal:
    """color pallete for pyxel"""

    black = 0
    navy = 1
    purple = 2
    green = 3
    brown = 4
    gray_dark = 5
    gray_light = 6
    white = 7
    red = 8
    orange = 9
    yellow = 10
    lime = 11
    cyan = 12
    steel_blue = 13
    pink = 14
    peach = 15

    def __init__(self):
        """black, navy, purple, green,
        brown, gray_dark, gray_light
        white, red, orange, yellow, lime,
        cyan, steel_blue, pink, peach
        """
        pass


class Rect:
    def __init__(self, u, v, w, h, colkey=ColPal.pink):
        """the region of size (w, h) from (u, v)
        colkey: treated as transparent (default: pink)
        """
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.colkey = colkey

    def getRect(self):
        return [self.u, self.v, self.w, self.h, self.colkey]
