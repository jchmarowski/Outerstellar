import pygame
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed, enemy_image, img_size, hp, weapon, cooldown):
        super().__init__()
        img_size_tuple = (img_size, img_size)
        self.sprites = []
        #enemy_image = pygame.image.load("assets/{}.png".format(enemy_image)).convert_alpha()
        self.sprites.append(pygame.transform.scale(enemy_image, img_size_tuple))
        self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.hp = hp
        self.collision_damage = 5
        self.weapon_type = weapon
        self.weapon_cooldown = cooldown
        self.weapon_ready = False
        self.timer = self.weapon_cooldown

    def update(self):
        self.rect.x -= self.speed
        self.pos = self.rect.center
        self.destroy()
        self.timer -= 1
        if self.timer == 0:
            self.weapon_ready = True
            self.timer = self.weapon_cooldown

    def destroy(self):
        if self.rect.x <= -200:
            self.kill()

class Bomber(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        enemy_image = reference_dict["bomber1"]
        enemy_image2 = reference_dict["bomber2"]
        self.sprites = []
        self.sprites.append(enemy_image)
        self.sprites.append(enemy_image2)
        self.sprites.append(enemy_image)
        self.sprites.append(enemy_image2)
        self.current_sprite = 0
        self.sprite_first_frame = 0
        self.sprite_max_frame = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos
        self.rect = self.image.get_rect(center = pos)
        self.speed = 3
        self.hp = 35
        self.collision_damage = 5
        self.hit = False
        self.weapon_type = "plasmacannon"
        self.weapon_cooldown = 250
        self.weapon_ready = False
        self.timer = self.weapon_cooldown
        self.image.set_alpha(255)

    def update(self):
        self.rect.x -= self.speed
        self.destroy()
        self.timer -= 1
        self.current_sprite += 0.3
        self.image = self.sprites[int(self.current_sprite)]
        if self.hit:
            self.sprite_max_frame = 3
            self.hit = False
        if self.current_sprite >= self.sprite_max_frame:
            self.current_sprite = self.sprite_first_frame
            self.sprite_max_frame = self.sprite_first_frame
        if self.timer == 0:
            self.weapon_ready = True
            self.timer = self.weapon_cooldown

    def destroy(self):
        if self.rect.x <= -200 or self.rect.x > 2200:
            self.kill()
        if self.rect.y <= 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()



class Enemy_projectile(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.image = pygame.Surface((16,4))
        self.image.fill("red")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = pos)
        self.rect.x -= 1
        self.speed = speed
        self.damage = 1
        self.piercing = False

    def update(self):
        self.rect.x += self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= 0:
            self.kill()

from main import reference_dict