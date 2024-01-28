import pygame
from settings import *
from enemies import Enemy
from random import randint

list_all = [[(2000, 80), 8, "scout1", 100, 10, "CannonLaserRocket", 200]]
light_fighter_fast_top = [[(2000, 80), 8, "scout1", 100, 10, "CannonLaserRocket", 200], [(2000, 160), 7, "scout1", 120, 10, "CannonLaserRocket", 200], [(2000, 240), 6, "scout1", 120, 10, "CannonLaserRocket", 200], [(2000, 320), 5, "scout1", 120, 10, "CannonLaserRocket", 200]]

very_random = list_all
enemy_formations_list = light_fighter_fast_top
class Level:
    def __init__(self):
        small_stars_sprite = SmallStars()
        self.small_stars = pygame.sprite.Group(small_stars_sprite)
        big_stars_sprite = BigStars()
        self.big_stars = pygame.sprite.Group(big_stars_sprite)
        #self.timer = pygame.time.get_ticks()
        #self.queue1 = []




    def run(self, dt):
        if len(self.small_stars.sprites()) < 100:
            self.small_stars.add(SmallStars())
        self.small_stars.update()

        if len(self.big_stars.sprites()) < 2:
            self.big_stars.add(BigStars())
        self.big_stars.update()
        #self.queue1 = light_fighter_fast_top




class SmallStars(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        random_num = randint(0,3)
        self.image = pygame.Surface((2, 2))
        self.image.fill("white")
        self.image.set_alpha(randint(40, 70) * random_num)
        self.pos = (randint(SCREEN_WIDTH - 400, SCREEN_WIDTH + 400), randint(0, SCREEN_HEIGHT - 200))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 0 - random_num

    def update(self):
        self.rect.x += self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= 0:
            self.kill()

class BigStars(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        random = randint(1,15)
        if random <= 7: self.type = 1
        elif random <= 14: self.type = 2
        else: self.type = 3
        self.size = (40 + random * 2)
        star_image = pygame.image.load("assets/star{}.png".format(self.type)).convert_alpha()
        star_image = pygame.transform.scale(star_image, (self.size, self.size))
        self.image = star_image
        self.image.set_alpha(80)
        self.pos = (randint(SCREEN_WIDTH - 400, SCREEN_WIDTH + 300), randint(0, SCREEN_HEIGHT - 200))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 0 - randint(1,3)
        self.shield = 20
        self.energy = 100

    def update(self):
        self.rect.x += self.speed
        self.destroy()
        self.image.set_alpha(randint(80,200))
    def destroy(self):
        if self.rect.x <= 0:
            self.kill()