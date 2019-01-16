"""A module to provide

###########################
# Music and sound effects #
###########################

"""

import pyxel


def sfx_jump():
    """Play jump sound."""
    pyxel.play(ch=3, snd=32)

def sfx_ground():
    """Play sound for when hits the ground."""
    pyxel.play(ch=3, snd=33)

def sfx_death():
    """Play sound for when ball hits paddle."""
    pyxel.play(ch=3, snd=34)

def start_music():
    """Start the music track."""
    pyxel.playm(msc=0, loop=True)

def stop_music():
    """Stop the music track by starting an unused track."""
    pyxel.stop()
    #pyxel.playm(msc=7, loop=True)

