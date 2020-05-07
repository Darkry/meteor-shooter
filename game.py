import pygame as pg
import random
from settings import *
from sprites.enemy import Enemy
from sprites.player import Player
from sprites.ally import Ally

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()
        self.allies = pg.sprite.Group()
        self.player = Player(self)
        self.alliesCreated = 0

        self.backgroundImg = pygame.image.load(path.join(IMG_DIR, 'background.png')).convert()
        self.gameoverImg = pygame.image.load(path.join(IMG_DIR, 'gameover.png')).convert()
        self.backgroundRect = self.backgroundImg.get_rect()

        #Create the enemies
        for i in range(ENEMIES):
            m = Enemy(self)
            self.all_sprites.add(m)
            self.enemies.add(m)

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

        #Detects hits between enemies and lasers
        hits = pygame.sprite.groupcollide(self.enemies, self.projectiles, False, True)
        for enemy, projectile in hits.items():

            #Remove one life of the enemy and delete if lives=0
            enemy.lives -= 1
            if(enemy.lives == 0):
                enemy.kill()
                self.score += 1

                #Add a new enemy instead
                m = Enemy(self)

        #Asteroid and Ally collision
        hits = pygame.sprite.groupcollide(self.allies, self.enemies, True, True)
        for enemy in hits:
            m = Enemy(self)

        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for enemy in hits:
            if enemy.type == "meteor":
                damage = 1
            elif enemy.type == "bomb":
                damage = 2

            self.player.lives = self.player.lives - damage
            m = Enemy(self)

            if(self.player.lives <= 0):
                self.playing = False

        if (self.score % 20) == 0 and self.score != 0 and self.alliesCreated < self.score/20:
            a = Ally(self)
            self.alliesCreated += 1

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.speedx = -5
                if event.key == pygame.K_RIGHT:
                    self.player.speedx = 5
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    self.player.speedx = 0

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)

        self.screen.blit(self.backgroundImg, self.backgroundRect)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 24, WIDTH/2, 20)
        self.draw_text(str(self.player.lives) + " LIVES", 20, 40, HEIGHT-30)

        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_gameover(self):
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.screen.blit(self.gameoverImg, self.backgroundRect)
        self.draw_text("SCORE: "+str(self.score), 40, WIDTH/2, HEIGHT/2+50)
        self.draw_text("Press g to try again.", 40, WIDTH/2, HEIGHT/2+80)

        pg.display.flip()
        self.wait_for_key(pygame.K_g)


    def draw_text(self, message, fontSize, x, y):
        font = pygame.font.Font(FONT_NAME, fontSize)
        text_surface = font.render(message, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self, key = pygame.K_SPACE):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key == key:
                        waiting = False

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_gameover()

pg.quit()