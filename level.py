import pygame
from settings import *
from enemies import Enemy
from random import randint



light_fighter_wall = [[(2000, 150), 2, "light-fighter", 150, 20, "CannonLaserRocket", 200], [(2000, 250), 2, "light-fighter", 150, 20, "CannonLaserRocket", 200]]

#                      (Enemy((2000, 300), 2, "light-fighter", 150, 20, "CannonLaserRocket", 200)), (Enemy((2000, 400), 2, "light-fighter", 150, 20, "CannonLaserRocket", 200)), (Enemy((2000, 450), 2, "light-fighter", 150, 20, "CannonLaserRocket", 200))]

enemy_fodder_list = light_fighter_wall
class Level:
    def __init__(self):
        small_stars_sprite = SmallStars()
        self.small_stars = pygame.sprite.Group(small_stars_sprite)
        big_stars_sprite = BigStars()
        self.big_stars = pygame.sprite.Group(big_stars_sprite)
        self.stage = 0
        self.queue1 = []




    def run(self, dt):
        if len(self.small_stars.sprites()) < 100:
            self.small_stars.add(SmallStars())
        self.small_stars.update()

        if len(self.big_stars.sprites()) < 2:
            self.big_stars.add(BigStars())
        self.big_stars.update()
        self.stage += 1 # 1 = 1 second
        if self.stage % 300 == 0:
            self.queue1 = light_fighter_wall


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
        self.image.set_alpha(randint(120, 240))
        self.pos = (randint(SCREEN_WIDTH - 400, SCREEN_WIDTH + 300), randint(0, SCREEN_HEIGHT - 200))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 0 - randint(1,3)

    def update(self):
        self.rect.x += self.speed
        self.destroy()
        self.image.set_alpha(randint(100,220))
    def destroy(self):
        if self.rect.x <= 0:
            self.kill()