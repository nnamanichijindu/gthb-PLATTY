import pygame as pg
import random
from settings import *
from sprites import *
from os import path
speed = 4
class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.win = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        # load spritesheet image


    def new(self):
        # start a new game
        self.score = 0
        self.ball = Ball()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat,)
            self.all_sprites.add(p)
            self.platforms.add(p)
        for i in range(numcoins):
            c = coin()
            c.rect.x = random.randint(0, WIDTH - 30)
            c.rect.y = random.randint(0, HEIGHT - 50)
            self.all_sprites.add(c)
            self.coins.add(c)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()


        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right  and \
                   self.player.pos.x > lowest.rect.left:
                    if self.player.pos.y < hits[0].rect.bottom:
                        self.player.pos.y = hits[0].rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        coinhit = pg.sprite.spritecollide(self.player, self.coins, True)
        for coin in coinhit:
            self.score += 1
        self.win.fill(BGCOLOR)
    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop - draw

        self.win.fill(BGCOLOR)
        self.all_sprites.draw(self.win)
        self.win.blit(self.player.image,self.player.rect)
        self.win.blit(self.ball.image,self.ball.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)

        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_win(self):
        # game splash/start screen
        self.win.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, up to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_win(self):
        # game over/continue
        if not self.running:
            return
        self.win.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.win.blit(text_surface, text_rect)



g = Game()
g.show_start_win()
while g.running:
    g.new()
    g.show_go_win()

pg.quit()