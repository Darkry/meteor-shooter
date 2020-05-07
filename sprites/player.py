import pygame
from os import path
from .projectile import Projectile

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        img_dir = path.join(path.dirname(__file__), '../images')
        player_img = pygame.image.load(path.join(img_dir, 'ship.png')).convert_alpha()
        self.groups = game.all_sprites
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.screen.get_width()/2
        self.rect.bottom = self.game.screen.get_height() - 10
        self.speedx = 0
        self.lives = 5

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.game.screen.get_width():
            self.rect.right = self.game.screen.get_width()

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.top)
        self.game.all_sprites.add(projectile)
        self.game.projectiles.add(projectile)