import pygame
import random
from random import randint
from pygame.math import Vector2

class Neutrals(pygame.sprite.Sprite):
    def __init__(self, position, image, image2, image3, image4):
        super().__init__()
        self.image = image
        self.image_hit = image2
        self.org_image = image
        self.org_image_heat = image3
        self.org_image_heat2 = image4
        self.rect = self.image.get_rect(center = position)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = position
        self.speed = 0
        self.hp = 0
        self.heat = 0
        self.change_image = True
        self.change_image2 = True
        self.damage = 0
        self.timer = 0
        self.hit = False

    def update(self, bullet_time):
        self.rect.x -= self.speed * bullet_time
        self.timer += 1
        self.heated()
        if self.hit == True:
            self.image = pygame.transform.rotate(self.image_hit, self.rotation)
            self.hit = False
        if self.rotation > 0:
            if self.timer % 5 == 0:
                self.rotation += 1
                self.image = pygame.transform.rotate(self.org_image, self.rotation)
                self.mask = pygame.mask.from_surface(self.image)
        elif self.rotation < 0:
            if self.timer % 5 == 0:
                self.rotation -= 1
                self.image = pygame.transform.rotate(self.org_image, self.rotation)
                self.mask = pygame.mask.from_surface(self.image)

        if self.rect.x < -100:
            self.kill()
    def heated(self):
        if self.type == "asteroid":
            if self.heat > 50 and self.change_image2:
                self.org_image = self.org_image_heat2
                self.change_image2 = False
            elif self.heat > 25 and self.change_image:
                self.org_image = self.org_image_heat
                self.change_image = False

class Asteroid(Neutrals):
    def __init__(self, position, image, image2, image3, image4):
        super().__init__(position, image, image2, image3, image4)
        self.image = image
        self.image_hit = image2
        self.org_image = image
        self.org_image_heat = image3
        self.org_image_heat2 = image4
        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = position
        self.speed = randint(1,1) # Must be higher than 1 because bullet time.
        self.damage = 2 * self.speed
        self.hp = 100
        self.rotation = random.randrange(-3, 3, 2)
        self.heat = 0
        self.timer = 0
        self.type = "asteroid"

class Rock(Neutrals):
    def __init__(self, position, image, image2, image3, image4=None):
        super().__init__(position, image, image2, image3, image4)
        self.mask = pygame.mask.from_surface(image)
        self.pos = position
        self.speed = randint(1,1)
        self.damage = self.speed
        self.hp = 10
        self.rotation = random.randrange(-2, 2)
        self.heat = 0
        self.timer = 0
        self.type = "rock"

class Ice(Neutrals):
    def __init__(self, position, image, image2, image3):
        super().__init__(position, image, image2, image3)
        self.mask = pygame.mask.from_surface(image)
        self.pos = position
        self.speed = randint(1,1)
        self.damage = 1
        self.hp = 20
        self.rotation = random.randrange(-2, 2)
        self.heat = 0
        self.timer = 0
        self.type = "ice"



class Scrap(pygame.sprite.Sprite):
    def __init__(self, pos, value, img, img2):
        super().__init__()
        self.pos = Vector2(pos)
        self.vel = Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        self.image = img
        if value > 5:
            self.image = img2
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.value = value

        self.damage = -1
        self.hp = 15
        self.heat = 0

    def update(self, bullet_time, camera_shift_x=0, camera_shift_y=0):
        self.pos += self.vel * bullet_time
        self.pos.x += camera_shift_x
        self.pos.y += camera_shift_y
        self.rect.center = self.pos
