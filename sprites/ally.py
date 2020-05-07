import pygame
import random
from os import path
from .projectile import Projectile

class Ally(pygame.sprite.Sprite):
    def __init__(self, game):
        img_dir = path.join(path.dirname(__file__), '../images')
        ally_img = pygame.image.load(path.join(img_dir, 'ally.png')).convert_alpha()
        self.groups = game.all_sprites, game.allies
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = ally_img
        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.screen.get_width()/2
        self.rect.bottom = self.game.screen.get_height() - 60
        self.speedx = 0
        self.lives = 1
        self.goingRight = True

    def update(self):
        self.AI()
        self.rect.x += self.speedx


    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.top)
        self.game.projectiles.add(projectile)
        self.game.all_sprites.add(projectile)

    def AI(self):
        if(self.goingRight == False and self.rect.left < 0):
            self.goingRight = True
        elif(self.goingRight == True and self.rect.right > self.game.screen.get_width()):
            self.goingRight = False

        if(self.goingRight == True):
            self.speedx = 2
        else:
            self.speedx = -2

        #Shoot?
        if(random.randrange(1,15) == 1):
            self.shoot()
