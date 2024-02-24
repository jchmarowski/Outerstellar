import random

import pygame
from pygame.math import Vector2
import math
from settings import *
from random import randint


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, img, img_hit, img_hot, img_shield):
        super().__init__()
        normal_image = img
        hit_image = img_hit
        heat_image = img_hot
        shielded_img = img_shield
        self.sprites = []
        self.sprites.append(normal_image)
        self.sprites.append(hit_image)
        self.sprites.append(heat_image)
        self.sprites.append(hit_image)
        self.sprites.append(shielded_img)
        self.sprites.append(hit_image)
        self.current_sprite = 0
        self.sprite_first_frame = 0
        self.sprite_last_frame = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.hit = False
        # Stats
        self.pos = pos
        self.speed = 1
        self.hp = 1
        self.scrap = 1
        self.heat = 0
        self.collision_damage = 5
        self.weapon_type = "default"
        self.weapon_cooldown = 100
        self.weapon_damage = 0
        self.weapon_ready = False
        self.timer = 0


    def update(self, bullet_time):
        self.rect.x -= self.speed * bullet_time
        self.destroy()
        self.current_sprite += 0.2
        self.image = self.sprites[int(self.current_sprite)]
        if self.hit:
            self.sprite_last_frame += 0.9
            self.hit = False
        if self.current_sprite >= self.sprite_last_frame:
            self.current_sprite = self.sprite_first_frame
            self.sprite_last_frame = self.sprite_first_frame
        self.timer += 0.99
        if self.timer > 2 * self.weapon_cooldown - self.weapon_cooldown * bullet_time:
            self.timer = 0
            self.weapon_ready = True

    def destroy(self):
        if self.rect.x <= -100 or self.rect.x > 2200:
            self.kill()
        if self.rect.y <= 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()
        if self.hp <= 0:
            self.kill()


class Bomber(Enemy):
    def __init__(self, pos, img, img_hit, img_hot, img_shielded):
        super().__init__(pos, img, img_hit, img_hot, img_shielded)
        normal_image = img
        hit_image = img_hit
        heat_image = img_hot
        shielded_img = img_shielded
        self.sprites = []
        self.sprites.append(normal_image)
        self.sprites.append(hit_image)
        self.sprites.append(heat_image)
        self.sprites.append(hit_image)
        self.sprites.append(shielded_img)
        self.sprites.append(hit_image)
        self.current_sprite = 0
        self.sprite_first_frame = 0
        self.sprite_last_frame = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.hit = False
        self.pos = pos
        # Stats
        self.speed = 3
        self.hp = 35
        self.heat = 0
        self.collision_damage = 5
        self.weapon_type = "standard"
        self.weapon_cooldown = 100
        self.weapon_damage = 10
        self.weapon_ready = False
        self.timer = self.weapon_cooldown
        self.scrap = randint(0,5)

class Scout(Enemy):
    def __init__(self, pos, img, img_hit, img_hot, img_shielded):
        super().__init__(pos, img, img_hit, img_hot, img_shielded)
        normal_image = img
        hit_image = img_hit
        heat_image = img_hot
        shielded_img = img_shielded
        self.sprites = []
        self.sprites.append(normal_image)
        self.sprites.append(hit_image)
        self.sprites.append(heat_image)
        self.sprites.append(hit_image)
        self.sprites.append(shielded_img)
        self.sprites.append(hit_image)
        self.current_sprite = 0
        self.sprite_first_frame = 0
        self.sprite_last_frame = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.hit = False
        self.pos = pos
        # Stats
        self.speed = 5
        self.hp = 15
        self.heat = 0
        self.collision_damage = 2
        self.weapon_type = "radar"
        self.weapon_cooldown = 150
        self.weapon_damage = 0
        self.weapon_ready = False
        self.timer = self.weapon_cooldown
        self.scrap = randint(0,2)




class Enemy_projectile(pygame.sprite.Sprite):
    def __init__(self, pos, weapon_damage, scrap, image = None, target = None):
        super().__init__()
        self.image = pygame.Surface((16,5))
        self.image.fill("red")
        self.mask = pygame.mask.from_surface(self.image)
        self.org_pos = Vector2(pos)
        self.pos = self.org_pos
        self.rect = self.image.get_rect(center = pos)
        self.damage = weapon_damage
        self.speed = 8
        self.heat = 0
        self.scrap = scrap
        self.piercing = False
        self.target = Vector2((-50,self.rect.y))
        self.movement = self.target - self.org_pos

    def update(self, bullet_time):
        self.pos += self.movement.normalize() * self.speed * bullet_time
        self.rect.center = self.pos
        self.destroy()

    def destroy(self):
        if self.rect.x <= -300 or self.rect.x > SCREEN_WIDTH + 300:
            self.kill()
        if self.rect.y < -300 or self.rect.y > SCREEN_HEIGHT +300:
            self.kill()

class Radar_ping(Enemy_projectile):
    def __init__(self, pos, weapon_damage, scrap, image, target):
        super().__init__(pos, weapon_damage, scrap, image, target)
        self.target = Vector2(target)
        self.org_pos = Vector2(pos)
        self.pos = self.org_pos
        self.movement = self.target - self.org_pos
        self.angle = math.degrees(math.atan2(-self.movement[1], self.movement[0]))
        self.image = pygame.transform.rotate(image, self.angle)
        self.image.set_alpha(110)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.damage = weapon_damage
        self.speed = 10
        self.heat = 0
        self.scrap = 0
        self.piercing = True

class Scrap(Enemy_projectile):
    def __init__(self, pos, weapon_damage, scrap):
        super().__init__(pos, weapon_damage, scrap)
        self.image = pygame.Surface((20, 20))
        self.image.fill("gray")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.speed = random.choice([-2, -1, 1, 2])
        self.damage = 0
        self.heat = 0
        self.scrap = scrap