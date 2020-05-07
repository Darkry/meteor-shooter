import pygame
import random
from os import path

# Enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game

        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        img_dir = path.join(path.dirname(__file__), '../images')
        meteor_img = pygame.image.load(path.join(img_dir, 'meteor.png')).convert_alpha()
        bomb_img = pygame.image.load(path.join(img_dir, 'bomb.png')).convert_alpha()

        #Decide whether it's a bomb or a meteor
        if(random.randint(1,7) == 7):
            self.type = "bomb"
            self.lives = 3
            self.image = bomb_img
        else:
            self.type = "meteor"
            self.lives = 1
            self.image = meteor_img


        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.game.screen.get_width() - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(2, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > self.game.screen.get_height():
            self.rect.x = random.randrange(self.game.screen.get_width() - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 6)