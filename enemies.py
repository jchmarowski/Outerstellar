import pygame

import projectiles
from projectiles import Enemy_projectile
from player import Player

start_time = pygame.time.get_ticks()
global enemy_power
enemy_power = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        #file_path =
        img_size = (120, 120)
        enemy_image = pygame.image.load("assets/heavy-fighter.png").convert_alpha()
        enemy_image = pygame.transform.scale(enemy_image, img_size)
        self.image = enemy_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.hp = 5

        self.cooldown = 100




    def update(self):
        self.rect.x -= self.speed
        self.destroy()



    def destroy(self):
        if self.rect.x <= -200:
            self.kill()




