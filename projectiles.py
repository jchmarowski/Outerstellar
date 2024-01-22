import pygame
from random import randint

global flash_alpha
flash_alpha = 250



class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.image = pygame.Surface((20,4))
        self.image.fill("cyan")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = pos)
        self.rect.x += 30
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x >= 2000:
            self.kill()

class Flash(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.size = 60
        flash_image = pygame.image.load("assets/cyan_flash{}.png".format(randint(1,4))).convert_alpha()
        flash_image = pygame.transform.scale(flash_image, (self.size,self.size))
        self.image = flash_image
        self.rect = self.image.get_rect(center = pos)
        self.rect.x += 35
        self.speed = 3



    def update(self):
        global flash_alpha
        flash_alpha -= 35
        self.image.set_alpha(flash_alpha)
        self.rect.x += self.speed
        #self.image.scroll(-1,0)
        if flash_alpha <= 40:
            self.kill()
            flash_alpha = 255
            self.size = 40


class Enemy_projectile(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.image = pygame.Surface((20,4))
        self.image.fill("red")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= 1:
            self.kill()