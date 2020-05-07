import pygame
from os import path

# Projectile
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img_dir = path.join(path.dirname(__file__), '../images')
        laser_img = pygame.image.load(path.join(img_dir, 'laser.png')).convert_alpha()
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()