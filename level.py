import pygame
from settings import *
from enemies import Enemy
from random import randint

stars_list = []


class Level:
    def run(self, dt):
        pass


    def level_1_1(self):
        pass


class SmallStars(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill("white")
        self.image.set_alpha(randint(20,60 * (randint(1,4))))
        self.pos = (randint(1000, SCREEN_WIDTH * 2), randint(0, SCREEN_HEIGHT))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 0 - randint(1,3)

    def update(self):
        self.rect.x += self.speed
        self.destroy()
    def destroy(self):
        if self.rect.x <= 0:
            self.kill()

class BigStars(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = randint(25,60)
        star_image = pygame.image.load("assets/star{}.png".format(randint(1, 2))).convert_alpha()
        star_image = pygame.transform.scale(star_image, (self.size, self.size))
        self.image = star_image
        self.image.set_alpha(randint(120, 240))
        self.pos = (randint(1000, SCREEN_WIDTH * 2), randint(0, SCREEN_HEIGHT - 100))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 0 - randint(1,2)

    def update(self):
        self.rect.x += self.speed
        self.destroy()
        self.image.set_alpha(randint(100,250))
    def destroy(self):
        if self.rect.x <= 0:
            self.kill()