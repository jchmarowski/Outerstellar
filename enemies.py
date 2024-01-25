import pygame

import projectiles

from player import Player

start_time = pygame.time.get_ticks()
global enemy_power
enemy_power = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed, enemy_image, img_size, hp, weapon, cooldown):
        super().__init__()
        #file_path =
        img_size = (img_size, img_size)
        enemy_image = pygame.image.load("assets/{}.png".format(enemy_image)).convert_alpha()
        enemy_image = pygame.transform.scale(enemy_image, img_size)
        enemy_image_hit = pygame.image.load("assets/heavy-fighter-hit2.png").convert_alpha()
        enemy_image_hit = pygame.transform.scale(enemy_image_hit, (130, 130))
        self.image = enemy_image
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.hp = hp
        self.hit = enemy_image_hit
        self.weapon = weapon
        self.weapon_cooldown = cooldown

    def update(self):
        self.rect.x -= self.speed
        self.destroy()


    def destroy(self):
        if self.rect.x <= -200:
            self.kill()

class Enemy_projectile(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.image = pygame.Surface((20,4))
        self.image.fill("cyan")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = pos)
        self.rect.x += 30
        self.speed = speed
        self.damage = 1
        self.piercing = False

    def update(self):
        self.rect.x += self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x >= 2000:
            self.kill()
