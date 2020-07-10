import pygame as pg
from settings import *
from random import randint
vec = pg.math.Vector2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
WIDTH = 800
HEIGHT = 600
coinslist = pg.sprite.Group()

PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.18
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20
win = pg.display.set_mode((WIDTH, HEIGHT))
win_rect = win.get_rect()

UPLEFT = 0
DOWNLEFT = 1
UPRIGHT = 2
DOWNRIGHT = 3


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping =False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standingf[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.mask = pg.mask.from_surface(self.image)


    def load_images(self):
        self.standingf = [pg.image.load("standing.png").convert()]
        for frame in self.standingf:
            frame.set_colorkey(BLACK)
        self.coins = [pg.image.load("coin.png").convert()]
        for frame in self.standingf:
            frame.set_colorkey(BLACK)
        self.walkf_r = [pg.image.load("R1.png").convert(),
                       pg.image.load("R2.png").convert(),
                       pg.image.load("R3.png").convert(),
                       pg.image.load("R4.png").convert(),
                       pg.image.load("R5.png").convert(),
                       pg.image.load("R6.png").convert(),
                       pg.image.load("R7.png").convert(),
                       pg.image.load("R8.png").convert(),
                       pg.image.load("R9.png").convert()]
        for frame in self.walkf_r:
            frame.set_colorkey(BLACK)
        self.walkf_l = [pg.image.load("L1.png").convert(),
                       pg.image.load("L2.png").convert(),
                        pg.image.load("L3.png").convert(),
                       pg.image.load("L4.png").convert(),
                       pg.image.load("L5.png").convert(),
                       pg.image.load("L6.png").convert(),
                       pg.image.load("L7.png").convert(),
                       pg.image.load("L8.png").convert(),
                       pg.image.load("L9.png").convert()]
        for frame in self.walkf_l:
            frame.set_colorkey(BLACK)
        self.jumpf = [pg.image.load("standing.png").convert()]
        for frame in self.jumpf:
            frame.set_colorkey(BLACK)
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP


    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if abs(self.vel.x) < 0.7:
            self.vel.x = 0
        # wrap around the sides of the screen
        if self.pos.x > WIDTH-15:
            self.pos.x = WIDTH-15
        if self.pos.x < 15:
            self.pos.x = 15

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walkf_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walkf_r[self.current_frame]
                else:
                    self.image = self.walkf_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standingf)
                bottom = self.rect.bottom
                self.image = self.standingf[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom



class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class coin(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 30))
        self.image.fill(BGCOLOR)
        self.image.set_colorkey(BLACK)
        pg.draw.ellipse(self.image, YELLOW, [0, 0, 30, 30])
        self.rect = self.image.get_rect()



class Ball(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.bl = pg.image.load("standing.png").convert()
        self.image = self.bl
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = 50
        self.y = 60
        self.width = 64
        self.height = 64
        self.vel = 3
        self.rect.x = 0
        self.rect.y = 0




    def update(self):
        self.rect.x += self.vel
        self.y += self.vel
        pg.display.update()



