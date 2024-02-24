import pygame
from settings import *
from enemies import Enemy
from random import randint


class Level:
    def __init__(self):
        pass

    def run(self, dt):
        pass




class SmallStars(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        random_num = randint(0,5)
        self.image = pygame.Surface((2, 2))
        self.image.fill("white")
        self.image.set_alpha(40 * random_num)
        self.pos = (randint(SCREEN_WIDTH - 400, SCREEN_WIDTH + 400), randint(0, SCREEN_HEIGHT))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 0 - random_num

    def update(self, bullet_time):
        self.rect.x += self.speed * bullet_time -1
        self.destroy()


    def destroy(self):
        if self.rect.x <= 0:
            self.kill()

class BigStars(pygame.sprite.Sprite):
    def __init__(self, star1, star2, star3):
        super().__init__()
        random = randint(1,15)
        if random <= 7:
            self.type = 1
            self.image = star1
        elif random <= 14:
            self.type = 2
            self.image = star2
        else:
            self.type = 3
            self.image = star3
            self.shield = 20
            self.energy = 100
        self.pos = (SCREEN_WIDTH + 50, randint(0, SCREEN_HEIGHT))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 0 - randint(1,3)


    def update(self, bullet_time):
        self.rect.x += self.speed * bullet_time -1
        self.destroy()
        self.image.set_alpha(randint(120,240))


    def destroy(self):
        if self.rect.x <= -50:
            self.kill()
