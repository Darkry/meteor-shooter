import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'images')

pygame.init()

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen settings
WIDTH = 400
HEIGHT = 600
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Meteor Shooter")

done = False
clock = pygame.time.Clock()

#DRAW TEXT ON SCREEN
font_name = pygame.font.match_font('arial')
def draw_text(message, fontSize, x, y):
    font = pygame.font.Font(font_name, fontSize)
    text_surface = font.render(message, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.lives = 5

    def update(self):
        self.rect.x += self.speedx
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.top)
        all_sprites.add(projectile)
        projectiles.add(projectile)

# Enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

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
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(2, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 6)

# Projectile
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Load all game graphics
background = pygame.image.load(path.join(img_dir, 'background.png')).convert()
background_rect = background.get_rect()
gameover = pygame.image.load(path.join(img_dir, 'gameover.png')).convert()

player_img = pygame.image.load(path.join(img_dir, 'ship.png')).convert_alpha()
meteor_img = pygame.image.load(path.join(img_dir, 'meteor.png')).convert_alpha()
bomb_img = pygame.image.load(path.join(img_dir, 'bomb.png')).convert_alpha()
laser_img = pygame.image.load(path.join(img_dir, 'laser.png')).convert_alpha()

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()

#Create the enemies
for i in range(5):
    m = Enemy()
    all_sprites.add(m)
    enemies.add(m)

#Set score to 0
score = 0

# Game loop
while not done:

    clock.tick(FPS)

    # Process inputs/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speedx = -5
            if event.key == pygame.K_RIGHT:
                player.speedx = 5
            if event.key == pygame.K_SPACE:
                player.shoot()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.speedx = 0
            if event.key == pygame.K_RIGHT:
                player.speedx = 0

    # Update
    all_sprites.update()

    #Detects hits between enemies and lasers
    hits = pygame.sprite.groupcollide(enemies, projectiles, False, True)
    for enemy, projectile in hits.items():
        #Increase Score
        score += 1

        #Remove one life of the enemy and delete if lives=0
        enemy.lives -= 1
        if(enemy.lives == 0):
            enemy.kill()

            #Add a new enemy instead
            m = Enemy()
            all_sprites.add(m)
            enemies.add(m)

    hits = pygame.sprite.spritecollide(player, enemies, True)
    for enemy in hits:
        if enemy.type == "meteor":
            damage = 1
        elif enemy.type == "bomb":
            damage = 2

        player.lives = player.lives - damage
        m = Enemy()
        enemies.add(m)
        all_sprites.add(m)

        if(player.lives <= 0):
            done = True

    # Draw
    screen.fill(BLACK)

    if(done == False):
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(str(score), 24, WIDTH/2, 20)
        draw_text(str(player.lives) + " LIVES", 20, 40, HEIGHT-30)
    else:
        screen.blit(gameover, background_rect)
        draw_text("SCORE: "+str(score), 40, WIDTH/2, HEIGHT/2+50)



    # Flip the display
    pygame.display.flip()

pygame.quit()