import pygame as pg
import random
from sprites import *
from os import path

TITLE = "PLATTY"
FPS = 60
FONT_NAME = 'arial'
numcoins = 10
COIN_SPAWN_PCT = 7
MOB_LAYER = 2
MOB_FREQ = 5000

PLATFORM_LIST = [(0, HEIGHT - 20, WIDTH, 20),
                 (WIDTH / 2 - 50, 500, 150, 20),
                 (125, HEIGHT - 250, 150, 20),
                 (650, 100, 150, 20),
                 (380, 250, 150, 20),
                 (155, 70, 80, 20)]


