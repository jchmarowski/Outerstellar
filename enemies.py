import pygame
from settings import *


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
        self.timer += 0.7
        if self.timer > 2 * self.weapon_cooldown - self.weapon_cooldown * bullet_time:
            self.timer = 0
            self.weapon_ready = True

    def destroy(self):
        if self.rect.x <= -100 or self.rect.x > 2200:
            self.kill()
        if self.rect.y <= 0 or self.rect.y > SCREEN_HEIGHT:
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
        # Stats
        self.pos = pos
        self.speed = 3
        self.hp = 35
        self.heat = 0
        self.collision_damage = 5
        self.weapon_type = "plasma"
        self.weapon_cooldown = 100
        self.weapon_damage = 10
        self.weapon_ready = False
        self.timer = self.weapon_cooldown




class Enemy_projectile(pygame.sprite.Sprite):
    def __init__(self, pos, speed, weapon_damage):
        super().__init__()
        self.image = pygame.Surface((16,5))
        self.image.fill("red")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = pos)
        self.rect.x -= 1
        self.speed = speed
        self.damage = weapon_damage
        self.heat = 0
        self.piercing = False

    def update(self, bullet_time):
        self.rect.x += self.speed * bullet_time
        self.destroy()

    def destroy(self):
        if self.rect.x <= 0:
            self.kill()


